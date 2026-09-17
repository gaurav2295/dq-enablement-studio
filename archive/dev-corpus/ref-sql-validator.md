---
id: ref-sql-validator
type: reference
title: SQL Validator (static checks)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - prereq:ref-sql-generator
  - implements:std-optsel-select-structure
  - implements:std-view-naming-patterns
  - relates:ref-catalog-deriver
  - relates:ref-catalog-promotion
  - relates:ref-zconcatenatedkey-and-ziserrorflag-sql-emission
  - relates:ref-audit-engine
  - relates:ref-ai-static-validator-gate
  - relates:gls-auto-repair
sources:
  - vault:studio-architecture/Studio — SQL Validator (static checks).md
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [studio, engine, sql, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`core/sql_validator.py::validate_sql_pair` runs the production deep-audit catalog — the 13
core checks below, plus the later additions listed after them — against every generated
OptSel/RptSel pair BEFORE it lands in bulk results — built after package #21 shipped 12 high-severity bugs (4 unresolved aliases, 8
trailing commas), closing the regex-detectable gap.

It is the gate the [[ref-local-deriver]], [[ref-catalog-deriver]], and
[[ref-ai-derive-and-enhance-internals|AI Enhance loop]] all call after
[[ref-sql-generator|generation]]. It never blocks generation — findings ride on
`spec._validator_findings` + `spec._warnings` (the reconciliation banner reads them), and
the call site is fail-soft (`except: pass`). See [[ref-ai-static-validator-gate]] for the
retry behaviour.

## What it does

`validate_sql_pair(sql_optsel="", sql_rptsel="", *, rule_type="Error", main_view_name="")`
(`:79-127`):

- Runs `_run_all_checks` on the OptSel body; empty OptSel on a non-profiling rule → High
  `missing-optsel`.
- For **Error** rules only: runs `_run_all_checks` on RptSel + the cross-view
  `_check_rptsel_pattern`; missing RptSel → High `missing-rptsel`. (Info uses a single
  InfSel; profiling pairs have a different shape and skip the Error-shaped checks.)
- Returns a `ValidationResult` (findings list). `result.has_high_severity` is the flag that
  drives the AI Enhance retry-once loop.

Each `ValidationFinding` carries `severity` (High/Medium/Low), `category`
(Syntax/Structure/Standards/Logic/Pairing), `check_name`, `issue`, `view_type`, and an
optional executable `remediation_query` (SSMS-pasteable snippet; None when the fix is
purely a code edit).

## The checks (`_run_all_checks`, `:135-164`)

| # | check_name | sev | cat | what it catches |
|---|---|---|---|---|
| 1 | `trailing-comma-before-from` | High | Syntax | `,\s*\n\s*FROM` — the package-#21 bug class |
| 2 | `unbalanced-parens` / `-brackets` | High | Syntax | paren/bracket count after masking string literals |
| 3 | `null-compared-with-eq` | High | Syntax | `= NULL` / `<> NULL` → use `IS [NOT] NULL` |
| 4 | `case-missing-end` | High | Syntax | more `CASE` than `END` (masked) |
| 5 | `join-without-on` | High | Syntax | paren-aware; skips `CROSS JOIN` |
| 6 | `missing-semicolon-before-go` | Medium | Structure | batch terminator hygiene |
| 7 | `missing-tech-columns` | High | Standards | OptSel/InfSel must expose `zSourceSystemID`, `zConcatenatedKey`, `zIsErrorFlag` (last skipped when `rule_type != error` — Info uses `[Implication]`) |
| 8 | `unresolved-aliases` | High | Logic | `X.col` where `X` was never declared by FROM/JOIN/subquery; skips DBO/SYS + bracketed qualifiers |
| 9 | `null-unsafe-key-concat` | Low | Logic | `… + '\|' + … AS [zConcatenatedKey]` → use NULL-safe CONCAT |
| 10 | `literal-flag-fallback` | Medium | Logic | the `/* TODO: literal 1 */` marker the catalog promoter leaves when it can't extract a per-row predicate |
| 11 | `view-name-rule-id-mismatch` | High | Standards | `DQ_NNNN_` in the view name ≠ `-- Rule ID: NNNN` banner (leading zeros stripped) — sibling-replication bug |
| 12 | `catalog-methodology-bypass` | High | Standards | a `-- Source: Syniti Rule Catalog` view lacking ANY methodology banner shipped raw |
| 13 | `rptsel-not-wrapping-optsel` + `rptsel-missing-flag-filter` | Medium | Standards | cross-view: RptSel must reference its OptSel AND filter `[zIsErrorFlag] = 1` (regex `\[zIsErrorFlag\]\s*=\s*1`) |

### Checks added after this catalogue was written

The 13 above are the deep-audit catalog as the vault snapshot recorded it. `_run_all_checks`
has since grown; the additions matter most on the AI-Enhance path, where several of them are
the difference between a save and a `422`:

| check_name | sev | what it catches |
|---|---|---|
| `forbidden-right-join` / `forbidden-outer-apply` | High | RIGHT JOIN and OUTER APPLY, prohibited outright — rewrite as LEFT/INNER JOIN, a CTE, or `EXISTS` |
| `hardcoded-mandt` | High | `MANDT` compared to a fixed client-number literal |
| `hardcoded-system-id-literal` | High | `'<code>' AS zSourceSystemID` instead of a column reference |
| `concat-key-pipe-delimiter` | High | `zConcatenatedKey` built with `'\|'` instead of `'_'` |
| `unresolved-tbd-placeholder` | High | a `TBD` token surviving into the view name or the `FROM`/JOIN body |
| `join-missing-system-id-pairing` | Medium | a symmetric-field JOIN (`a.FIELD = b.FIELD`, brackets included, CTE-internal included) with no `zSourceSystemID` equality alongside it — **on the AI-Enhance blocking allowlist despite its Medium severity** |
| `excessive-sql-comments` | Medium | performance-tuning, index-suggestion, uniqueness-narrative or edge-case prose inline in SQL; auto-repaired away by `_strip_verbose_comments` before the AI-Enhance gate runs |
| `concat-key-well-formed` | Medium | `zConcatenatedKey` not referencing `zSourceSystemID` or not built with `CONCAT(...)` (config-driven, `shell_guardrails.yaml`) |
| `section-header-order`, `view-naming-pattern`, `header-comment-incomplete` | Medium/Low | the config-driven structural standards |
| `unnecessary-select-distinct` | Low | `SELECT DISTINCT` on an Opportunity View — usually masks a join fan-out bug |
| `source-system-out-of-scope` | Medium | a fan-out rule's `system_filter` outside the project's configured scope (spec-level, not pure text) |

Severity and blocking are separate decisions — see [[std-ai-enhance-guardrails]] and
[[ref-ai-static-validator-gate]]. Note that the six newest codes are not yet registered in
`knowledge/harness/requirements.json`, so they have no `std-req-*` unit
(std-harness-requirements).

### Concrete values

- Required tech columns: `_REQUIRED_OPTSEL_TECH_COLS = ("zSourceSystemID",
  "zConcatenatedKey", "zIsErrorFlag")` (`:370-374`). These are the
  [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission|Syniti Technical Fields]].
- Methodology banners (`_METHODOLOGY_BANNERS`, `:580-585`) — a catalog-sourced view must
  carry one: `Promoted from Info catalog entry` · `Restructured native Error catalog entry`
  · `Best-effort methodology applied` · `Catalog entry not auto-restructurable`. Only a view
  with NONE of these (yet tagged `-- Source: Syniti Rule Catalog`) trips check #12 — it
  bypassed [[ref-catalog-promotion|promotion]].
- View-id routing (check #11): banner regex `^--\s*Rule\s+ID:\s*(\S+)$`; view regex captures
  `DQ_(\d+)_` from `CREATE VIEW`; both `lstrip("0")` before comparing.

## Inputs & outputs

| | |
|---|---|
| **Input** | `sql_optsel`, `sql_rptsel` strings; `rule_type` (Error/Info/Profiling) selecting which standards apply; `main_view_name` |
| **Output** | `ValidationResult` with `findings`, `has_high_severity`, `has_any`, `messages()` (e.g. `[High] (OptSel) missing-tech-columns: …`) |
| **Consumed by** | deriver gate (`local_deriver.py:2761-2786`, `catalog_deriver.py:444-466`) → stamps `_validator_findings`/`_warnings`; AI Enhance → retries once on any High; [[ref-audit-engine\|Audit engine]] static mode runs this catalog per view |

> [!success] Implementation status — resolved 2026-07-01 (KNOWN-ISSUES B2, B6)
> Check #11 (`view-name-rule-id-mismatch`) and check #12 both route on the `DQ_{id}_` view
> name and the `-- Rule ID:` banner agreeing. Canonical naming is
> `DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}` with `{system}` = the PRODUCTION
> system ID. There is now ONE canonical view-name pattern: the YAML resolver defaults were
> aligned to the dataclass so `{system}` is present on both OptSel and RptSel names
> regardless of build path, and the `{desc}` token is included in the canonical pattern. A
> rule no longer deploys under two names. See [[ref-view-name-token-resolution]].

> [!success] Implementation status — resolved 2026-07-01 (KNOWN-ISSUES B10)
> Wiring a paste-SQL validation page is FastAPI + Jinja (`app.py` + `ui/templates/*.html`),
> not Streamlit — CLAUDE.md has been corrected accordingly. The validator itself is
> framework-agnostic — pure regex over the SQL body.

## Source

- `core/sql_validator.py:79-127` — `validate_sql_pair` entry, pairing checks.
- `core/sql_validator.py:135-164` — `_run_all_checks` runner (check ordering).
- `core/sql_validator.py:377-431` — tech-column + RptSel cross-view checks.
- `core/sql_validator.py:434-650` — unresolved-aliases, catalog-banner, view-name/rule-id
  checks.
- Detail: `knowledge-mining/sql-generation.md` §11.

## Related

[[ref-sql-generator]] · [[ref-generate-sql-dispatcher]] · [[ref-sql-parser]] ·
[[ref-catalog-deriver]] · [[ref-catalog-promotion]] ·
[[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] · [[ref-view-name-token-resolution]] ·
[[ref-sql-comment-and-formatting-standard]] · [[ref-audit-engine]] ·
[[ref-ai-static-validator-gate]] · [[ref-ai-derive-and-enhance-internals]] ·
[[prn-catalog-promotion-wraps-instead-of-injecting]] ·
[[prn-sql-comments-must-match-local-derive-quality]]
