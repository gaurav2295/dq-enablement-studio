---
id: ref-target-mdm-model-fit
type: reference
title: Target MDM Model Fit
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - prereq:ref-schema-profiler
  - relates:ref-profiling-metrics-and-divergence-signals
  - relates:ref-attribute-usage-analysis
  - relates:ref-three-database-architecture
  - relates:ref-dqrulespec-data-model
  - relates:ref-profiler-and-audit-pages
  - relates:gls-mdg
sources:
  - vault:studio-architecture/Studio — Target MDM Model Fit.md
tags: [studio, engine, methodology, sap, profiling]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`core/target_model.py` imports an Excel-authored "target model" (the future-state shape an
MDM project is moving TOWARDS) and emits an idempotent `Target_Fit_Report.sql` that
compares every target attribute against the latest profiling stats, scoring each as `fit` /
`partial` / `gap` / `unmapped`.

This is the gap-analysis companion to the [[ref-schema-profiler]]: the profiler measures
what the data IS today; the target model declares what it SHOULD be, and the fit report
joins the two. The report is an optional extra file in the profile bundle — included only
when a target model is loaded.

## What it does

1. Author authors a target model in Excel (5 sheets: Instructions, Project, Entities,
   Attributes, FitRules). `generate_template_xlsx` (`:160-312`) emits the template
   pre-seeded with real SAP sample rows — `MARA.MATNR/MTART/MEINS`, `KNA1.KUNNR/LAND1`,
   sample source_system `"ECCZ02100"`.
2. `parse_target_model_xlsx` (`:337-443`) reads it back. **Tolerant** — warnings collect
   onto `model.warnings`, it never raises. The FitRules sheet layers user overrides on top
   of the defaults; unknown rule keys produce a warning; `nullable` is parsed loosely from
   `false/f/no/n/0`.
3. `generate_target_fit_sql` (`:453-664`) emits the deployable `Target_Fit_Report.sql`.

## The FitRule kinds (`:42-55`)

A `FitRule` is `(key, kind, param, description)`. `kind` ∈:

| kind | meaning |
|---|---|
| `non_null_pct_min` | attribute's non-null % must be ≥ `param` |
| `distinct_count_min` | distinct value count must be ≥ `param` |
| `distinct_count_max` | distinct value count must be ≤ `param` |
| `profile_signal_in` | the column's `profile_signal` must be in a set |
| `profile_signal_not_in` | the column's `profile_signal` must NOT be in a set |

## The 5 default fit rules (`DEFAULT_FIT_RULES`, `:61-107`)

| key | kind | param | gist |
|---|---|---|---|
| `non_null_98` | `non_null_pct_min` | `0.98` | near-mandatory field |
| `non_null_95` | `non_null_pct_min` | `0.95` | strongly populated |
| `non_null_80` | `non_null_pct_min` | `0.80` | mostly populated |
| `has_values` | `distinct_count_min` | `1` | not entirely empty |
| `categorical_small` | `distinct_count_max` | `50` | code/category field, small domain |

These are built-ins; the FitRules sheet overrides/extends them per project.

## The four verdicts and the 10% partial band (`:295-299`, computed in SQL `:564-657`)

- **`fit`** — all of the attribute's rules pass.
- **`partial`** — at least one rule fails but is **within 10% of threshold**. This band
  applies ONLY to `non_null_pct_min`: it is `partial` when the measured non-null % is
  `>= param * 0.90`.
- **`gap`** — at least one rule fails by **more than 10%**.
- **`unmapped`** — no profiling row was found for the attribute's source mapping (NULL
  `run_id`) — i.e. the target column was never profiled.

The headline `fit_verdict` is the **worst-of** roll-up across all rules on the attribute:
`gap > partial > unmapped > fit`.

> [!note] One attribute, one verdict
> Target says `MARA.MTART` must satisfy `non_null_98` (≥ 0.98). Profiling measured 0.94
> non-null. 0.94 ≥ 0.98 × 0.90 = 0.882, so this rule is **partial**, not gap. If a second
> rule on the same attribute came back `gap`, the headline rolls up to **gap** (worst-of).

## The generated SQL (`generate_target_fit_sql`, `:453-664`)

- **Idempotent** — `CREATE OR ALTER` + `IF OBJECT_ID` guards, so it can be re-run safely.
- Creates two staging tables holding the parsed model: `dbo.DQ_TargetModel_Attributes` and
  `dbo.DQ_TargetModel_FitRules`.
- Then creates view `dbo.DQ_Profile_TargetFit`, which joins each target attribute to
  **latest-run** profile stats — `dbo.DQ_Profile_Columns` via `dbo.DQ_Profile_Run` (the
  profiler's `run_id`-cascaded star schema).
- Default `working_db = "WRKDQ"` (Syniti working-DB convention).
- **Run AFTER the main `DQ_Schema_Profile.sql`** — it consumes the `DQ_Profile_*` tables
  that script populates.

## Inputs & outputs

| | |
|---|---|
| **Input** | the authored target-model `.xlsx` (Project / Entities / Attributes / FitRules sheets) |
| **Data model** | `TargetModel` → `TargetEntity` → `TargetAttribute` (entity_id, attribute_name, target_type, target_nullable, source_system/schema/table/column, `rules`, notes) + `FitRule` list; `:110-154` |
| **Output** | `Target_Fit_Report.sql` (staging tables + `DQ_Profile_TargetFit` view); shipped as an optional file in the profile-bundle ZIP **only when a target model is loaded** (`routes.py:2818-2835`) |
| **Failure mode** | parse never raises; problems surface on `model.warnings` |

## Source

- `core/target_model.py:42-107` — `FitRule` kinds + `DEFAULT_FIT_RULES` (the
  0.98/0.95/0.80, has_values, categorical_small built-ins)
- `core/target_model.py:160-312` — `generate_template_xlsx` (5-sheet template, SAP sample
  rows)
- `core/target_model.py:337-443` — `parse_target_model_xlsx` (tolerant parser, override
  layering)
- `core/target_model.py:453-664` — `generate_target_fit_sql` (idempotent SQL, staging
  tables, `DQ_Profile_TargetFit`, verdict computation at `:564-657`)

> [!note] Why these numbers?
> The code fixes the default non-null thresholds at 0.98/0.95/0.80 and the partial band at
> 10%, but does not record the business rationale for those exact values. Treat them as the
> shipped defaults, overridable per project via the FitRules sheet.

## Related

[[ref-schema-profiler]] · [[ref-profiling-metrics-and-divergence-signals]] ·
[[ref-attribute-usage-analysis]] · [[ref-three-database-architecture]] ·
[[ref-dqrulespec-data-model]] · [[ref-profiler-and-audit-pages]] · [[ref-exporters]]
