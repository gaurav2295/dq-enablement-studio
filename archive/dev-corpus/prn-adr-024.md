---
id: prn-adr-024
type: principle
kind: decision
title: ADR D-24 — The dead inline trust-verification block in api/routes.py is kept, not deleted
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-24
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The dead inline trust-verification block in api/routes.py is kept, not deleted.

## Rationale

A trust-verification block guarded by `if isinstance(result, dict) and "_harness" not in result:` (around api/routes.py line 1805-1812, inside _run_ai_enhance_core) never runs for any live traffic — every real production caller goes through HarnessedAIClient.enhance_spec, which always sets _harness on its result dict, making the guard always true (branch never taken). It is kept specifically because tests/test_ai_client.py's four TestTrustVerificationRouteWiring tests monkeypatch _get_ai_client with a bare stub that has no enhance_spec-side harness wiring at all, deliberately bypassing HarnessedAIClient to exercise this exact inline logic in isolation.

## Consequence

Engineers may delete the inline block, but only together with reworking those four tests to exercise the same trust-verification behavior through the real HarnessedAIClient/TableFieldTrustCheck path instead. Recorded here per harness-v2 design Amendment O-6 so this known-accepted gap is explicit and reviewable rather than only a code comment.

> [!note] Provenance
> Architecture decision **D-24** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
