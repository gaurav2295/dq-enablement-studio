---
id: ref-audit-engine
type: reference
title: Audit Engine (runtime + cross-rule)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - contrast:gls-coverage
  - relates:ref-sql-validator
  - relates:ref-catalog-promotion
  - relates:ref-multi-impl-fan-out-engine
  - relates:ref-bulk-processor-and-dqops-id-invariants
  - relates:prc-audit-rule-quality
  - relates:prn-optsel-is-the-universe
  - relates:ref-exporters
  - relates:gls-dq-score
sources:
  - vault:studio-architecture/Studio — Audit Engine (runtime + cross-rule).md
  - dq-studio:docs/Studio_Overview.md
tags: [studio, engine, methodology, sql, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`core/audit_engine.py::run_full_audit` is the post-deploy safety net: it runs three modes — a
per-view static validator, 7 runtime issue groups ported from the user's
`dbo.usp_DQ_Audit_Counts` stored proc, and cross-rule duplicate/aliasing checks — scoring each rule
by the canonical `DQ score = 100 − (rpt/opt × 100)`.

Where the [[ref-sql-validator|static validator]] catches regex-detectable defects at generation
time, the audit engine ingests **actual row counts** (the `dbo.DQ_View_Counts` file the user runs
in the prep DB) and catches defects only visible at runtime: impossible scores, outliers, missing
source systems, stale counts. It is the structural quality gate for bulk output (AI SQL review is
OFF by default in bulk — the Audit page is where quality is enforced).

## What it does — the three modes

1. **Static** — runs the [[ref-sql-validator|sql_validator]] catalog per view, plus audit-only
   cross-file checks.
2. **Runtime** — ports the **7 issue groups** of `dbo.usp_DQ_Audit_Counts` (the parity-scoring
   heart, below).
3. **Cross-rule** — duplicate view names, near-duplicate SQL, inconsistent table aliasing.

`run_full_audit(...)` defaults (`:87-95`): `min_population_for_outlier = 10` (skip 0%/100% outlier
checks below this opportunity count — avoids tiny-population false positives); `stale_count_days = 7`;
`expected_source_systems` defaults to the distinct `z_source_system_id` across counts rows. Findings
sort by severity (High>Medium>Low) → category → rule_id → check_name (`:202-206`).

Each `AuditFinding` (`:35-52`) carries `severity`, `category`, `check_name`, `issue`, `rule_id`,
`rule_family`, `view_name`, `view_type` (OptSel/RptSel/InfSel), `source_system`, `opt_count`,
`rpt_count`, `dq_score_pct`, `defect_rate_pct`, and an optional executable `remediation_query`.
Categories: Syntax, Structure, Standards, Logic, Pairing, Coverage, Outlier, Score Validity,
Cross-System, Empty View, Stale Counts, Cross-Rule.

## The DQ-score formula (canonical)

```text
defect_pct = rpt / opt * 100
dq_score_pct = 100 - defect_pct        # rpt = RptSel rows (defects), opt = OptSel rows (universe)
```

`rpt` is the defect count (`[zIsErrorFlag] = 1`); `opt` is the full opportunity universe. A clean
rule scores 100%. The Score-Validity group exists to catch values that fall **outside** `[0, 100]`
— they are structurally impossible and mean the SQL is wrong, not the data.

## The 7 runtime issue groups (`:368-613`)

| # | group / fn | findings (severity) | trigger |
|---|---|---|---|
| 1 | Score Validity `_check_score_validity` `:368-442` | `defects-exceed-opportunities` (High) | `rpt > opt` → negative score (impossible) |
| | | `defects-without-opportunities` (High) | `opt == 0 and rpt > 0` |
| | | `rptsel-missing` (High/Pairing) | opt present, rpt None, no InfSel |
| | | `optsel-missing` (High/Pairing) | opt None, rpt present → can't compute score |
| 2+3 | Outliers `_check_outliers` `:445-493` (skip when `opt < min_pop`) | `outlier-0pct` (Medium) | `rpt == 0` → score 100% (perfect data, or inverted CASE) |
| | | `outlier-100pct` (High) | `rpt == opt and opt > 0` → score 0% (inverted CASE or missing exclusion filter) |
| 4 | Coverage `_check_coverage` `:496-525` | `missing-source-system` (Medium) | family spans ≥2 systems but isn't full (`len(present) < len(expected) and len(present) >= 2`) |
| 5 | Cross-System Skew `_check_cross_system_skew` `:528-559` | `defects-concentrated` (Medium) | `len(systems) >= 2` and `(systems_with_defects / total) < 0.5` |
| 6 | Empty Views `_check_empty_views` `:562-589` | `empty-optsel` (Medium) | `opt == 0 and rpt == 0` → score not calculable |
| 7 | Stale Counts `_check_stale_counts` `:592-613` | `stale-count` (Low) | last refresh older than `stale_count_days` (default 7) |

View suffixes recognised: `OptSel, RptSel, InfSel, PrfSel, PrfSum`; rule_id parsed via `DQ_(\d+)_`
(`:215`). The counts pivot (`_pivot_counts` `:319-354`) is keyed by `(rule_id, z_source_system_id)`,
carrying opt/rpt/inf counts + view names side by side and the latest `last_refreshed` — mirroring
the proc's `#CountsPivot`.

## Cross-rule + tracker×SQL checks

**Cross-rule** (`_check_cross_rule` `:257-311`): `duplicate-view-name` (High — same name in >1 file
→ deploy silently overwrites); `inconsistent-table-aliasing` (Low — only when a table is aliased
**>3** different ways, after filtering SQL keyword tokens).

**Tracker × SQL alignment** (`:621-782`) — canonical wrappers, not orphans:

- `tracker-without-sql` (High): tracker view with no SQL file.
- `sql-without-tracker` (Medium) — **suppressed for canonical companion wrappers.**
  `_PARTNER_PAIRS = (("_RptSel","_OptSel"), ("_PrfSum","_PrfSel"))`: the tracker registers each rule
  once via its PRIMARY view (OptSel/InfSel/PrfSel); RptSel & PrfSum are wrappers, not separately
  tracked. A SQL-only companion is a false positive when its primary partner IS in the tracker
  (`:646-674`).
- `tracker-dqops-view-name-mismatch` (High, `:691-730`): the tracker DQOPSID must match the
  `DQ_<id>_` segment in the view name (both normalised by `lstrip("0")`). Catches the
  [[ref-multi-impl-fan-out-engine|bulk-pipeline sibling-replication bug]] — each fan-out impl gets
  its own DQOps id but the SQL body inherits the lead's rule_id (e.g. tracker DQOPSID=0122 but view
  `DQ_0121_P03_*`).
- `tracker-error-shipped-as-infsel` (High, `:747-782`): ReportType=Error but view ends `_InfSel` →
  pipeline silently downgraded the rule type; re-run required.
- `_tracker_get` (`:733-744`) tolerates inconsistent xlsx header normalisation (tries
  `view_name`/`reportid`/`report_id`/`ReportID`, `dqopsid`/`DQOPSID`, `report_type`/`reporttype`) —
  `ReportID` normalises to `reportid` with no separator, and without this the check silently saw
  zero tracker rows and emitted spurious findings.

## The Audit & Validate page — what a consultant reads

The engine's findings surface on the Audit & Validate page as one severity-ranked list. Read
top-down: **every HIGH maps to a known methodology violation**, and the issue text names the check.

| Severity | Check | Catches |
|---|---|---|
| HIGH | `missing-tech-columns` | An OptSel missing zSourceSystemID / zConcatenatedKey / zIsErrorFlag |
| HIGH | `rptsel-missing-flag-filter` | RptSel without `WHERE [zIsErrorFlag] = 1` |
| HIGH | `view-name-rule-id-mismatch` | View name's `DQ_X_` segment differs from the banner's `-- Rule ID: Y` |
| HIGH | `catalog-methodology-bypass` | Catalog-sourced view without any methodology promoter banner |
| HIGH | `tracker-dqops-view-name-mismatch` | Tracker `DQOPSID` disagrees with the view name's rule_id segment |
| HIGH | `tracker-error-shipped-as-infsel` | Tracker says Error but the view name uses `_InfSel` |
| HIGH | `unbalanced-parens`, `case-missing-end`, `join-without-on`, `null-compared-with-eq`, `unresolved-aliases` | Hard syntax / structural bugs |
| HIGH | `duplicate-view-name`, `missing-optsel`, `missing-rptsel` | Cross-rule pairing failures |
| MEDIUM | `literal-flag-fallback` | OptSel uses the `/* TODO: literal 1 */` fallback — a DBA must refine it |
| MEDIUM | `missing-semicolon-before-go`, `rptsel-not-wrapping-optsel` | Methodology-shape drift |
| LOW | `null-unsafe-key-concat` | zConcatenatedKey built with `+` instead of `CONCAT` |

The runtime-count groups above (score validity, 0%/100% outliers, system coverage, cross-system
skew, empty views, stale counts) are added to this list only when a counts file is uploaded.

> [!tip] Triage order when something looks wrong
> 1. Run Audit & Validate first — upload `DQ_Rule_Deploy.sql` and `DQ_Report_Tracker.xlsx`, and work
>    the HIGH findings.
> 2. Check `Batch_Summary.xlsx` — its reconciliation sheet lists every input row → output spec with
>    the promoter status (`Restructured`, `Promoted`, `Best-effort`, or
>    `Catalog entry not auto-restructurable`).
> 3. Re-import affected rows only — the import template is idempotent on `rule_id`, so there is no
>    need to reprocess the whole batch.
> 4. Treat `/* TODO: literal 1 */` markers as a prompt for human review, not a failure: the column
>    exists so views deploy cleanly, but the DBA should refine the CASE before production use.

## Inputs & outputs

| | |
|---|---|
| **Input** | uploaded deploy SQL files; tracker.xlsx; optional runtime counts file (`dbo.DQ_View_Counts`: RuleID, RuleFamily, ViewName, ViewType, zSourceSystemID, RowCount, LastRefreshed); audit knobs (`min_population_for_outlier`, `stale_count_days`, `expected_source_systems`) |
| **Output** | sorted `list[AuditFinding]`, each with severity/category/check_name + opt/rpt counts + `dq_score_pct`/`defect_rate_pct` + optional `remediation_query`; rendered on the [[ref-profiler-and-audit-pages|/audit page]] and via [[ref-exporters|the audit-report exporter]] |
| **Pairs with** | [[ref-sql-validator]] (static mode reuses its catalog); the counts file shape comes from `core/audit_counts_template.py` (the SQL the user runs against the prep DB) |

> [!note] Implementation status
> `tracker-dqops-view-name-mismatch` routes on the `DQ_{id}_` view-name segment equalling the
> tracker DQOPSID. Canonical naming is `DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}` with
> `{system}` = the **production** system ID (e.g. PD1), never the interim QA system. The app emits
> `{system}` consistently across build paths, and the canonical pattern includes the `{desc}` token.
> See [[ref-view-name-token-resolution]]. The audit engine itself is framework-agnostic — it
> consumes uploaded files and returns findings.

## Source

- `core/audit_engine.py:87-95` — `run_full_audit` defaults; `:35-52` `AuditFinding`; `:1-21`
  three-mode docstring.
- `core/audit_engine.py:319-354` — `_pivot_counts`; `:368-613` the 7 runtime groups.
- `core/audit_engine.py:257-311` — `_check_cross_rule`; `:621-782` tracker×SQL alignment.
- `core/audit_counts_template.py` — generates the counts SQL the user runs (`dbo.DQ_View_Counts`).
- Detail: `knowledge-mining/scoring-profiling.md` §6; `knowledge-mining/app-arch-ops.md` §15.

## Related

[[ref-sql-validator]] · [[ref-catalog-promotion]] · [[ref-multi-impl-fan-out-engine]] ·
[[ref-bulk-processor-and-dqops-id-invariants]] · [[ref-profiling-metrics-and-divergence-signals]] ·
[[ref-profiling-view-generation]] · [[ref-view-name-token-resolution]] ·
[[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] · [[ref-profiler-and-audit-pages]] ·
[[ref-exporters]] · [[prn-catalog-promotion-wraps-instead-of-injecting]] · [[prc-audit-rule-quality]]
