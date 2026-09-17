---
id: ref-rule-catalog-structure
type: reference
title: Rule Catalog Structure
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-catalog-deriver
  - relates:ref-catalog-promotion
  - relates:ref-datastore-substitution-and-erp-compat-check
  - relates:ref-zconcatenatedkey-and-ziserrorflag-sql-emission
  - relates:ref-knowledge-base-file-inventory
  - relates:ref-bulk-processor-and-dqops-id-invariants
  - relates:gls-op-report-query
sources:
  - vault:studio-architecture/Studio — Rule Catalog Structure.md
tags: [studio, engine, catalog, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

The Syniti AI Generated Rule Catalog 2025 is a ~14 MB JSON of ~4,828 hand-authored Error + Info
rules (Profiling is never catalogued), loaded as a lazy singleton via `get_catalog()`; each
`CatalogEntry` is keyed by its `adm_rule_name` and carries `op_query_sql` (the universe) plus
`report_query_sql` (the defects), in both T-SQL and HANA variants, with a `{datastore}` DB
placeholder the caller substitutes later.

This note covers the catalog *data + loader* (`core/rule_catalog.py`). The engine that consumes
it — wrapping the SQL into a deployable spec — is [[ref-catalog-deriver]]; the Info→Error
transform is [[ref-catalog-promotion]].

## What it does

`core/rule_catalog.py` exposes the catalog to the rest of Studio: a `CatalogEntry` dataclass, a
thread-safe `RuleCatalog` loader, the `get_catalog()` accessor, and `substitute_datastore()`. The
catalog is the authoritative SQL for the ~4,800 Error/Info rules — Studio never re-derives that
SQL; it preserves it.

## CatalogEntry fields (`rule_catalog.py:56-97`)

| Field | Meaning |
|---|---|
| `adm_rule_name` | **Catalog primary key** (= ADMRuleName), e.g. `tvCSKB_KATYP_KSTAR_Costelementclassification_RptSel`. `entries` is a dict keyed by this. |
| `rule_type` | `"Error"` or `"Info"` only — see Profiling exclusion below. |
| `rule` / `warning` / `implication` | Human business text; `implication` feeds the rule description. |
| `op_query_sql` | T-SQL **OptSel = the universe** (all candidate rows, no error WHERE). |
| `report_query_sql` | T-SQL **RptSel = defects only** (universe + the error WHERE/HAVING). |
| `op_query_hana` / `report_query_hana` | HANA variants, stored for future ERP support; **unused by the current MS-SQL pipeline**. |
| `tables` | Array of SAP tables the rule touches. |
| `subject_area`, `business_process`, `sub_business_process`, `primary_data_object` | Taxonomy/traceability. |

The op/rpt split is the canonical source of Studio's whole methodology: **OptSel returns the
universe with a per-row flag; RptSel is the universe filtered to defects.** See
[[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]].

## Catalog file (`knowledge/catalogs/syniti_ai_generated_rule_catalog_2025.json`)

- `_meta.entry_count = 4828`; `type_counts = {Error: 2263, Info: 2565}`; `skipped_duplicate: 75`;
  `schema_version: 1`.
- Sourced from `AI Rule Content SQL (1).xlsx`, sheet "in".
- `entries` is a **dict** keyed by `adm_rule_name` (not a list) — O(1) lookup by catalog ID.
- Top subject areas: FI 916, MM 767, SD 766, HCM 361, PP 286, CO 285, PM 211, APO 165, QM 159,
  WM 157 (19 subject areas total).
- SQL uses the `{datastore}` placeholder for the DB, e.g. `FROM {datastore}.CSKA AS cska`.

## Key conventions (do / don't)

- **Profiling is NEVER in the catalog** (`:30-33`). Catalog scope = Error + Informational only.
  Profiling rules are derived from scratch — see [[ref-profiling-view-generation]].
- **Lazy-loaded singleton** via `get_catalog()` with thread-safe double-checked locking
  (`:119-142`). Don't reach for the JSON directly — go through the accessor.
- **Why it's separate from [[ref-knowledge-base-file-inventory|KnowledgeEngine]]** (`:8-33`):
  (1) the ~14 MB JSON would add
  200-500 ms to *every* startup; (2) lifecycle — the catalog is global, the engine is per-ERP;
  (3) optionality — a rule only hits the catalog when a bulk row carries an explicit
  `catalog_id`.
- **Missing file fails soft.** "catalog lookups disabled", empty `entries` — callers fall back to
  the rule-name derivation flow rather than crashing.
- **`get_entry()` returns `{datastore}` STILL PRESENT** (`:165-184`). Substitution is the
  **caller's** responsibility because the target DB depends on per-rule project context. Don't
  assume an entry's SQL is runnable as-is.
- **`substitute_datastore()`** (`:244-263`): `{datastore}` → `[<db>].[dbo]`. Canonically the rule
  views are created in AND read FROM the single `WRKDQ` repository (a same-DB read), e.g.
  `FROM {datastore}.CSKA AS cska` → `FROM [WRKDQ].[dbo].CSKA AS cska`. Empty DB → the
  `{datastore}.` prefix is stripped entirely. (Note: the shipped deriver now resolves Error/Info
  rule views FROM/JOIN the single `WRKDQ` working DB — one repository, matching profiling;
  `WRKDQPREP_ALL` is upstream ETL only — KNOWN-ISSUES B4, fixed 2026-07-01.)

## Inputs & outputs

- **In:** a `catalog_id` (= `adm_rule_name`), optionally the JSON path (defaults to
  `knowledge/catalogs/syniti_ai_generated_rule_catalog_2025.json`).
- **Out:** a `CatalogEntry`, or empty/None when absent. Consumers: [[ref-catalog-deriver]] (spec
  build), [[ref-catalog-promotion]] (Info→Error),
  [[ref-bulk-processor-and-dqops-id-invariants]] (per-row catalog lookup).

## Source

- `core/rule_catalog.py:1-263` — `CatalogEntry` (`:56-97`), `RuleCatalog`/`get_catalog`
  (`:100-236`), `substitute_datastore` (`:244-263`).
- `knowledge/catalogs/syniti_ai_generated_rule_catalog_2025.json` — the data; `_meta` block
  carries the counts.
- Detail: `knowledge-mining/knowledge-data-config.md` §1.5, `knowledge-mining/derivation-spec.md`
  §7.

> [!note] Implementation status — Resolved 2026-07-01
> The shipped code now implements the canonical decisions below — see KNOWN-ISSUES:
> - **B3** — `zConcatenatedKey` separator is now `_` (underscore) on BOTH paths: the
>   catalog/promotion path was changed from `'|'` (pipe) to `'_'`, matching local-derive.
>   `CONCAT` is NULL-safe (a NULL column no longer nulls the whole expression) and the keyless
>   fallback emits `''` rather than NULL, so keys are NEVER NULL and IDENTICAL across catalog and
>   local-derive paths. No space (ADM requirement).
> - **B4** — canonical FROM is **WRKDQ** (one repository): rule views are created in AND read
>   FROM `WRKDQ` (a same-DB read). The app now reads Error/Info rule views FROM/JOIN `WRKDQ` —
>   one repository, matching the profiling views. `WRKDQPREP_ALL` is upstream ETL only (applies
>   relevancy/merge/aggregation/scope across source systems) whose OUTPUT is pushed INTO `WRKDQ`;
>   rules do not read it directly. `architecture.md` owns the topology (source → SRCECC_DA →
>   WRKDQPREP_ALL → WRKDQ).

## Related

[[ref-catalog-deriver]] · [[ref-catalog-promotion]] ·
[[prn-catalog-promotion-wraps-instead-of-injecting]] ·
[[ref-datastore-substitution-and-erp-compat-check]] · [[ref-sql-parser]] ·
[[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] · [[ref-knowledge-base-file-inventory]] ·
[[ref-local-deriver]] · [[ref-bulk-processor-and-dqops-id-invariants]]
