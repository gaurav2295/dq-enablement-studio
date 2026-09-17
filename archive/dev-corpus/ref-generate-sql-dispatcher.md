---
id: ref-generate-sql-dispatcher
type: reference
title: generate_sql Dispatcher
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-sql-generator
  - relates:ref-deletion-flag-normalization-in-sql-gen
  - relates:ref-profiling-view-generation
  - relates:ref-zconcatenatedkey-and-ziserrorflag-sql-emission
  - relates:ref-rule-type-detection
  - relates:ref-dqrulespec-data-model
  - relates:con-rule-types
  - relates:con-view-types
  - relates:prn-optsel-is-the-universe
sources:
  - vault:studio-architecture/Studio — generate_sql Dispatcher.md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`generate_sql(spec)` is the single SQL-generation entrypoint: it runs
`_normalise_deletion_flags` defensively, then returns a `(primary, secondary)` tuple keyed on
`spec.rule_type` — Error → `(OptSel, RptSel)`, Info → `(InfSel, None)`, Profiling → `(PrfSel,
PrfSum)`.

Every caller (single-rule designer, bulk pipeline, AI-derive, catalog promotion) goes through this
one function — it is the seam where a [[ref-dqrulespec-data-model|DQRuleSpec]] becomes deployable
view SQL. The two returned strings are written into rule-type-agnostic slots: `spec.sql_optsel`
(primary) and `spec.sql_rptsel` (secondary), so the same fields carry PrfSel/PrfSum for profiling
rules.

## What it does

1. **Normalise first.** Calls `_normalise_deletion_flags(spec)` before any branch — see
   [[ref-deletion-flag-normalization-in-sql-gen]]. This moves any deletion-flag predicate (`LVORM`
   / `LOEKZ` / `LOEVM`, the `_DELETION_FLAG_FIELDS` set) out of `spec.logic` and into
   `spec.filters` as an `EXCLUSION`, so the flag lands in the WHERE and never in the
   `zIsErrorFlag` CASE. Defensive — both derivers already classify correctly; this catches
   AI-constructed or hand-edited specs.
2. **Branch on `spec.rule_type`** (the `RuleType` enum):
   - `RuleType.INFO` → `(generate_infsel(spec), None)` — one summary view, no error detection.
   - `RuleType.PROFILING` → `generate_prfsel_pair(spec)` → `(PrfSel, PrfSum)`.
   - **default (Error)** → resolve the OptSel view name, then `(generate_optsel(spec),
     generate_rptsel(spec, optsel_view_name))`. The OptSel name is resolved once and passed into
     RptSel so the wrapper's `FROM` points at the exact OptSel view.

## Key conventions (do / don't)

- **DO route everything through `generate_sql`.** It is the only place that guarantees the
  deletion-flag normalisation runs before generation — calling `generate_optsel` directly skips
  it.
- **Branch order is enum-explicit, not string-sniffing.** Info and Profiling are matched against
  `RuleType.INFO` / `RuleType.PROFILING`; Error is the fallthrough default.
- **The tuple slots are semantic, not literal.** `(primary, secondary)` → `sql_optsel` /
  `sql_rptsel` regardless of rule type. For profiling, "optsel" holds PrfSel and "rptsel" holds
  PrfSum.
- **Info's secondary is always `None`** — there is no defects-report wrapper for an information
  rule.
- **Error is the universe + filtered pair.** OptSel = all candidate rows with a per-row
  `zIsErrorFlag` CASE; RptSel = `SELECT * FROM <OptSel> WHERE [zIsErrorFlag] = 1`. The error
  predicate lives in the CASE, never the WHERE. See [[ref-sql-generator]],
  [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] and
  [[prn-optsel-is-the-universe]].
- **Profiling FROMs the working DB, not the prep layer** (unlike OptSel/InfSel) — see
  [[ref-profiling-view-generation]].

## Inputs & outputs

| | |
|---|---|
| **Input** | one `DQRuleSpec` (`spec.rule_type`, `spec.logic`, `spec.filters`, `spec.architecture`, …) |
| **Side effect** | mutates `spec` in place via `_normalise_deletion_flags` (logic→filters reclassification) |
| **Error** | `(optsel_sql, rptsel_sql)` |
| **Info** | `(infsel_sql, None)` |
| **Profiling** | `(prfsel_sql, prfsum_sql)` |
| **Return type** | `tuple[str, str \| None]` → `spec.sql_optsel` (primary), `spec.sql_rptsel` (secondary) |

## Source

- `core/sql_generator.py:124-158` — `generate_sql` dispatcher (the spec/finding cites `:132-166`)
- `core/sql_generator.py:81` — `_DELETION_FLAG_FIELDS = {"LVORM", "LOEKZ", "LOEVM"}`
- `core/sql_generator.py:84-121` — `_normalise_deletion_flags`
- `core/sql_generator.py:161-219` — `generate_optsel`; `:222-243` — `generate_rptsel`;
  `:246-…` — `generate_infsel`; `generate_prfsel_pair` for the profiling pair

## Related

- [[ref-sql-generator]]
- [[ref-deletion-flag-normalization-in-sql-gen]]
- [[ref-profiling-view-generation]]
- [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]]
- [[ref-logic-case-predicate-templates]]
- [[ref-view-name-token-resolution]]
- [[ref-rule-type-detection]]
- [[ref-local-deriver]]
- [[ref-catalog-promotion]]
- [[ref-dqrulespec-data-model]]
- [[con-rule-types]]
- [[con-view-types]]
