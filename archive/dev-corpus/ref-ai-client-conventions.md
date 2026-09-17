---
id: ref-ai-client-conventions
type: reference
title: AI Client Conventions (model & SDK)
domain: ai-enhancement
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-ai-derive-and-enhance-internals
  - relates:ref-ai-static-validator-gate
  - relates:std-rule-name-heuristics
  - relates:ref-rule-name-scorer
  - relates:ref-ports-install-and-versioning
  - relates:ref-config-editor
  - relates:std-ai-enhance-scope
  - relates:gls-ai-enhancement-stamp
sources:
  - vault:ai-related/AI Client Conventions (model & SDK).md
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
  - dq-studio:docs/ai_enhance_instructions.md
tags: [studio, agent, course, ai, sdk, anthropic]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

The Studio's Anthropic SDK wrapper (`integrations/ai_client.py`) follows four hard conventions:
pin a bare model ID (never a dated snapshot), pin `base_url` to `https://api.anthropic.com` (so
the host's `ANTHROPIC_BASE_URL` proxy can't 401 user keys), pool one client per `(key, model)`
(so a big bulk run doesn't OOM), and resolve the API key request > session > env — with a
100-char hard cap on every AI-produced rule name.

This is the single place where the Studio talks to Claude. The same client backs
[[ref-ai-derive-and-enhance-internals]] (name conversion, table/field derivation, SQL review)
and is gated by [[ref-ai-static-validator-gate]]. For model IDs, pricing and migration, defer to
the `claude-api` skill — do not answer from memory.

## What it does

Wraps `anthropic.Anthropic()` as an `AIClient` constructed per `(api_key, model)`. The SDK
client is lazy-imported and lazy-built on first call (`_get_client`), so importing the module
never requires the `anthropic` package, and a missing key fails fast with
`ValueError("Anthropic API key is required")`.

## Key conventions

### 1. Model IDs — bare, never dated

- `DEFAULT_MODEL = "claude-sonnet-4-6"`. The UI `AI_MODELS` dropdown offers **Sonnet 4.6**
  (default, bulk), **Opus 4.6** (complex SQL / profiling), **Haiku 4.5** (fastest / basic).
- **Do** pin to the bare current ID. **Don't** hand-construct dated snapshot IDs
  (`claude-sonnet-4-6-2026xxxx`) — dated snapshots get retired and start returning 404. Migrate
  via the `claude-api` skill, never by guessing a date.

### 2. Base URL pinned to defeat the host proxy

```python
DEFAULT_BASE_URL = "https://api.anthropic.com"   # pinned explicitly
self._base_url = base_url or self.DEFAULT_BASE_URL
```

The pin is deliberate. Claude Code and other Anthropic tooling set `ANTHROPIC_BASE_URL` in the
host shell to route through an internal proxy that expects a different auth scheme. If the SDK
auto-detected that env var, a user-supplied UI key would be rejected with a confusing **401**.
Passing `base_url` explicitly stops the SDK from reading the env var. An explicit non-empty
`base_url` constructor arg still wins (corporate gateway / local mock).
`/api/config/ai-key/status` surfaces the env override if one is present, so the user can see
when their shell is set.

### 3. Client pooling — one per (key, model)

```python
_ai_client_pool: dict[tuple[str, str], object] = {}   # module-level
```

`_get_ai_client()` returns the cached `AIClient` for the resolved `(key, model)`, building it
only on a miss. Each `anthropic.Anthropic()` carries its own httpx connection pool and thread; a
**96-rule bulk run with 3 AI calls per rule** would otherwise spin up **~300 short-lived
clients → OOM at scale** (tracked as Studio backlog #1). Changing the session key or model calls
`_invalidate_ai_client_pool()` (`.clear()`) so the next request rebuilds against the new
credentials.

### 4. Key resolution & hygiene

- Order: **request > session > env `ANTHROPIC_API_KEY`** (`_resolve_ai_key`).
- Model order: **session > default** (`_resolve_ai_model` → `claude-sonnet-4-6`).
- Keys are `.strip()`-ed on set — a copy-pasted trailing newline or leading space can't ride
  into an HTTP header, where it would 401 with "invalid x-api-key".
- No key resolves → `HTTPException(400, "API key required …")`, not a silent empty call.

### 5. Rule-name 100-char cap

After name conversion the result is hard-capped at **100 chars** (the ADM system limit; target
≤85). If longer, truncate to 100 then back off to the last word boundary *only if that boundary
is past char 60*; otherwise hard-truncate at 100. Prompts also instruct Claude to **preserve SAP
acronyms** (PIR, BOM, MRP, PO, SO, GL, AP, AR, UoM, CoA, FI) — see [[std-rule-name-heuristics]].

### 6. Every call is wrapped by the harness

Callers do not hold a bare `AIClient` in the enhance flow — `HarnessedAIClient`
(`core/harness/wrap.py`) wraps every AI call and runs it through the harness pipeline before
the caller sees the result. The wrapper is the client's contract with the rest of the app, not
an optional decorator. See [[ref-ai-static-validator-gate]].

### 7. Response parsing is closed, not lenient

`review_rule_fulfillment` returns free text, and the client parses it with
`_parse_rule_fulfillment_response`. The prompt fixes exactly five section names —
`RULE FULFILLMENT`, `SQL REVIEW`, `CORRECTED SQL`, `AI ADDITIONS`, `NOTES` (plus a
`STRUCTURED METADATA` JSON block) — and:

> [!important] Anything outside the documented sections is dropped, not surfaced
> The parser does not attempt to rescue prose the model invented outside the contract. A model
> that free-forms its answer loses that content silently. This is why "output only the
> documented response format" is a harness rule rather than a style note — see
> [[std-ai-enhance-scope]] for the full section contract and the structured-metadata shape.

The `STRUCTURED METADATA` block exists so the caller can refresh its own UI metadata **without
re-parsing the SQL text**: free-text SQL is not reliably machine-parseable, especially once the
model has restructured it with a CTE or a different shape.

## Inputs & outputs

| | |
|---|---|
| **In** | resolved API key, model, optional `base_url`; a rule name / spec for the call |
| **Out** | a live pooled `AIClient`; AI calls return `ConversionResult` (name), derived table/field/implication, or reviewed SQL. AI SQL review branches on `rule_type` (Error/Info vs Profiling — Profiling never emits `zIsErrorFlag`) |

## Source

- `integrations/ai_client.py:87-129` — `DEFAULT_MODEL`, `DEFAULT_BASE_URL` pin + rationale, lazy `_get_client`.
- `integrations/ai_client.py:254-264` — 100-char name cap (word-boundary > 60 back-off).
- `api/routes.py:1177-1218` — `_resolve_ai_key` (request>session>env), `_resolve_ai_model`, `_ai_client_pool`, `_get_ai_client`, `_invalidate_ai_client_pool`.
- `api/routes.py:1229-1244` — `.strip()` on key set; `routes.py:1146-1150` — `AI_MODELS` dropdown; `routes.py:1342-1344` — env-override status.
- Detail: `knowledge-mining/app-arch-ops.md` §9, §17 (decisions 5, 6).
- `integrations/ai_client.py::_parse_rule_fulfillment_response` — the closed five-section parser.
- `core/harness/wrap.py` — `HarnessedAIClient`, the mandatory wrapper on every AI call.

## Related

[[ref-ai-derive-and-enhance-internals]] · [[ref-ai-static-validator-gate]] · [[std-ai-enhance-scope]] · [[std-rule-name-heuristics]] · [[ref-rule-name-scorer]] · [[ref-ports-install-and-versioning]] · [[ref-config-editor]]
