---
id: ref-logic-builder-templates
type: reference
title: Logic Builder Templates
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - prereq:ref-field-matching
  - prereq:ref-rule-type-detection
  - implements:prn-ziserrorflag-is-integer
  - relates:ref-logic-case-predicate-templates
  - relates:ref-deletion-flag-resolver
  - relates:ref-output-section-builders
sources:
  - vault:studio-architecture/Studio — Logic Builder Templates.md
tags: [studio, engine, methodology]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`_build_logic` emits exactly ONE `LogicEntry` per rule — the per-row error-detection condition —
choosing a template by rule-type category and always anchoring `table_field` to `matched[0]` (the
rule's OBJECT). The entry's `value` string encodes the `1`/`0` flag mapping in text, which the SQL
generator later parses into the `zIsErrorFlag` CASE.

This is the bridge between [[ref-local-deriver|Local Deriver]]'s field matching and
[[ref-logic-case-predicate-templates|Logic-CASE Predicate Templates]] /
[[ref-zconcatenatedkey-and-ziserrorflag-sql-emission|zConcatenatedKey & zIsErrorFlag SQL Emission]].
It runs only for **Error** rules — Info and Profiling specs get `logic = []` (no error detection).

## What it does

After [[ref-field-matching|Field Matching (longest-key-wins)]] orders matches by position so the
OBJECT lands at `matched[0]`, the deriver calls `_build_logic(matched, rule_type, rule_name)`. It
picks the OBJECT (`check = matched[0]`, `tf = check.table_field`) and returns a single `LogicEntry`
whose template is selected by the business-category `rule_type` from
[[ref-rule-type-detection|Rule-Type Detection]].

The result drives [[ref-dqrulespec-data-model|DQRuleSpec]]'s `LogicEntry` fields (`element`,
`operator`, `table_field`, `value`, `instruction`) and renders into the markdown "Logic / Check
Conditions" section.

## The templates (in branch order)

One `LogicEntry` per call. `matched[0]` always supplies `table_field`. The `value` field carries
the flag mapping as `"1 - If …\n0 - If …"` text.

| Branch | When | element | table_field | value (flag text) |
|---|---|---|---|---|
| Empty-match TBD | `matched` is empty | `TBD — review required` | `""` | (none — instruction explains flag couldn't be derived) |
| Comparison / Consistency (2 matches) | Consistency + ≥2 matches | `<X.desc> must align with <Y.desc>` | X (the OBJECT, `matched[0]`) | `1 - If X.tf <> Y.tf` / `0 - If X.tf = Y.tf` |
| Completeness | rule_type = Completeness | `<desc> is Missing` | matched[0] | `1 - If ( [Field Value] IS NULL or = '' or = '0' )` / `0 - If ( … IS NOT NULL and <> '' )` |
| Consistency (1 match) | Consistency, single match | `<desc> is Inconsistent` | matched[0] | values match across org levels |
| Else | Accuracy / Uniqueness / Timeliness / Relevancy | `<desc> Check` | matched[0] | `1 - If condition fails` / `0 - If condition passes` |

The comparison branch is what makes ordering matter: `matched[0]` = what's checked, `matched[1]` =
the reference, so the emitted predicate is `X <> Y`, not the reverse.

### Deletion-detection variant — `_build_deletion_logic`

A separate path: when `matched` is empty **and** [[ref-deletion-flag-resolver|Deletion Flag
Resolver (3-tier)]]'s intent regex fires (`marked/flagged for deletion`, `not be deleted`,
`deletion flag/indicator`), the deriver swaps in:

```
element     = "Marked For Deletion"
table_field = <table>.<field>          (the deletion flag itself)
value       = "1 - If (<tf> = 'X')\n0 - If (<tf> <> 'X')"
```

Here the flag **IS** the error condition, not a WHERE exclusion (the matching exclusion is
suppressed via `skip_flags`). See [[ref-deletion-flag-normalization-in-sql-gen|Deletion Flag
Normalization in SQL Gen]].

## Inputs & outputs

- **In:** `matched: list[_MatchedField]` (position-ordered), `rule_type` (business category),
  `rule_name`.
- **Out:** a 1-element `list[LogicEntry]` (or `[]` for empty-match-with-no-deletion-intent before
  the deletion check, and always `[]` for Info/Profiling).
- **Downstream:** `value`'s `1 - If(<cond>)` text is consumed by `sql_generator._parse_logic_case`,
  which produces `CASE WHEN <error> THEN 1 ELSE 0 END AS [zIsErrorFlag]`. When no logic exists, the
  generator emits `/* zIsErrorFlag: define logic condition */ NULL AS [zIsErrorFlag]`.

## Canonical rules (the truth)

- **`zIsErrorFlag` is INTEGER `1` (defect) / `0` (pass)** — `flag = 1` is ALWAYS the defect. Never
  strings, never CAST-to-decimal. The templates' `1 - If …` / `0 - If …` text encodes exactly this.
- **The error predicate lives in the CASE, never the WHERE.** `OptSel` returns the universe (all
  candidate rows + per-row flag); `RptSel = SELECT * FROM <OptSel> WHERE [zIsErrorFlag] = 1`.
- **A deletion flag is the error condition only when the rule INTENT is to detect deletion.**
  Otherwise it stays a WHERE exclusion — see the [[ref-sap-baseline-model|SAP Baseline Model
  (logical vs physical)]] deletion-flag registry.

> [!note] Review-required guardrail
> When a domain is detected but `matched` is empty (and it's not Info/Profiling/deletion-detection),
> the deriver sets `_review_required` and the SQL generator emits a `NULL` `zIsErrorFlag` with a
> `/* TBD */` marker — a stale or guessed rule can never silently reach production.

## Source

- `core/local_deriver.py:736-848` — `_build_logic`
- `core/local_deriver.py` — `_build_deletion_logic`, `_detect_deletion_intent` (deletion-detection variant)
- Consumed by `core/sql_generator.py::_parse_logic_case` → `[zIsErrorFlag]` CASE

## Related

[[ref-output-section-builders]] · [[ref-sql-generator]]
