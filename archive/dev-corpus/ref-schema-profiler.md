---
id: ref-schema-profiler
type: reference
title: Schema Profiler (engine)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-profiling-metrics-and-divergence-signals
  - relates:ref-attribute-usage-analysis
  - relates:ref-profiling-view-generation
  - relates:ref-audit-engine
  - relates:ref-three-database-architecture
  - relates:ref-target-mdm-model-fit
  - relates:gls-schema-profile
sources:
  - vault:studio-architecture/Studio — Schema Profiler (engine).md
tags: [studio, engine, methodology, sap, profiling]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`core/schema_profiler.py` generates a self-contained MS SQL profiling script (no
server-side Python) that scans target tables column-by-column, lands the metrics in a
four-table `run_id`-cascaded star schema, and tags every column with a derived
`profile_signal` — running in one of two modes (`source_db` reads physical DBs
3-part-qualified; `working_db` reads one consolidated DB scoped per `zSourceSystemID`).

This is the SCHEMA profiler (a deploy-and-run SQL artefact for up-front data discovery),
distinct from the rule-level [[ref-profiling-view-generation]]. Output bundle:
`DQ_Schema_Profile.sql`, `Schema_Profile_Manifest.xlsx`, `Sample_Dashboard_Query.sql`,
`README.md`. All dynamic SQL lives in two `CREATE OR ALTER` procs:
`usp_DQ_Profile_OneTable`, `usp_DQ_Profile_TopValues`.

## What it does

Takes a `ProfileRunSpec` (list of `ProfileTarget` rows + global settings) and emits SQL
that, per target: counts rows, runs ONE small `SELECT` per column (≤9 aggregate exprs —
bulletproof against the 1024-column SELECT/temp-table cap on wide tables like MARA ~228
cols), captures Top-N value distributions, and inserts everything keyed by a single
`run_id`.

## Two modes (`ProfileRunSpec.mode`)

| | `source_db` (default) | `working_db` |
|---|---|---|
| Where data lives | each target's `system` = a physical SQL Server DB name | source already consolidated into the working DB |
| Read qualification | 3-part `[<system>].[<schema>].[<table>]` | current DB, no 3-part qual |
| System scoping | none injected (the source DB *is* the source) | auto `zSourceSystemID = N'<system>'` predicate per target |
| `source_db` / `system_filter` | `system` / `NULL` | `NULL` / `zSourceSystemID = N'<sys>'` |
| DDIC enrichment | DD02T/DD03L/DD04T snapshot (Section 0 raises if DD% missing) | skipped (no source DBs to reach) |

Both modes feed the same `DQ_Profile_*` staging tables, so the divergence view + target-fit
reports work identically. The `inclusion_filter` audit column records the COMBINED filter
(system AND user) so scope is visible end-to-end.

## Key thresholds — `ProfileRunSpec` defaults (verbatim)

| Field | Default | Why |
|---|---|---|
| `working_db` | `"WRKDQ"` | Syniti working-DB convention |
| `top_n` | `50` | raised 10→50 so the dashboard value-distribution chart shows the long tail (still inside Excel/render budget) |
| `top_n_skip_threshold` | `100_000` | skip Top-N when `distinct_count` exceeds this (free-text columns where Top-N has no meaning) |
| `approx_distinct_threshold` | `1_000_000` | use `APPROX_COUNT_DISTINCT` (SQL 2019+, ~2% error) at/above this row count; exact `COUNT(DISTINCT)` below |
| `retention_runs` | `12` | history depth; retention = one `DELETE FROM DQ_Profile_Run` |
| `mode` | `"source_db"` | `"source_db"` \| `"working_db"` |
| `system_discriminator_column` | `"zSourceSystemID"` | per-source discriminator (overridable per project) |

## RFC-padded-blank-as-NULL handling

SAP RFC/BAPI extracts emit `CHAR(N)` values **space-padded** (or `''` for NVARCHAR) instead
of true `NULL`, which would otherwise inflate `non_null_pct`. So null detection is **per
kind**:

- **String columns (`'S'`)** — logical-null =
  `col IS NULL OR LTRIM(RTRIM(CAST(col AS NVARCHAR(MAX)))) = ''` (catches empty + whitespace
  + tab pads).
- **Numeric (`'N'`) / date (`'D'`)** — strict `IS NULL` only (RFC doesn't pad these;
  string-casting would mis-bucket valid zeros).
- Two surfaced columns: `empty_string_count` = strict `''`; `whitespace_count` = non-null,
  non-empty, trims to `''` (the RFC-padded pattern) — so the reader sees which mechanism the
  source uses.

## `profile_signal` derived labels (CASE, first match wins — verbatim)

Per-column label written into `DQ_Profile_Columns.profile_signal`:

| Label | Condition |
|---|---|
| `all-null` | `null_count = row_count_active` |
| `mostly-null` | `null_count >= 0.95 * row_count_active` |
| `unique-key` | `distinct_count = (row_count_active - null_count) AND row_count_active > 1` |
| `low-cardinality` | `distinct_count <= 10` |
| `high-cardinality` | `distinct_count >= 0.95 * row_count_active` |
| `normal` | else |

Related per-column metrics: `distinct_density = distinct_count / (row_count_active -
null_count)`; `excluded_pct = 1.0 - (row_count_active / row_count_raw)`; raw count via
`sys.partitions` (instant, falls back to `COUNT_BIG(*)` if denied); `value_pct` in
TopValues = share of the top-N total, NOT the whole table.

## Star schema — four tables, `run_id` cascade

| Table | Grain | PK |
|---|---|---|
| `DQ_Profile_Run` | run dimension (one row per execution) | `run_id UNIQUEIDENTIFIER` |
| `DQ_Profile_Tables` | table-grain fact | `run_id, system_id, schema_name, table_name` |
| `DQ_Profile_Columns` | column-grain fact | + `column_name` |
| `DQ_Profile_TopValues` | value-grain fact | + `rank` |

- **Every child FK is `ON DELETE CASCADE` on `run_id` ONLY** — retention is one
  `DELETE FROM DQ_Profile_Run` and children follow. Cascade is via `run_id` (not the Tables
  FK) to dodge SQL Server's multiple-cascade-paths error; `Run` is the canonical lifetime
  owner. Single-key cascade also lets Power BI / Tableau / dbt auto-discover the
  relationships.
- Cross-system view `DQ_Profile_System_Compare` aggregates per
  `(run × schema × table × column)` across ≥2 systems and emits `divergence_signal`
  (`high`/`medium`/`low`/`aligned`) — covered in
  [[ref-profiling-metrics-and-divergence-signals]].

> [!note] Divergence bands are 0.50 / 0.20 / 0.05 — not 0.02/0.10/0.30
> The shipped `divergence_signal` cut points are **high 0.50 / medium 0.20 / low 0.05** on
> `non_null_pct_spread`. A tightening to 0.02/0.10/0.30 is backlog only — do not teach it as
> current.

## Inputs & outputs

| | |
|---|---|
| **Input** | `ProfileRunSpec` (targets + `mode`, `top_n`, thresholds, `working_db`); each `ProfileTarget` has `system`, `schema`, `table`, `filter_preset`, `filter_text` |
| **Filter presets** | `auto_active` (deletion-flag from SAP metadata, prefers `common_filters[0]`, degrades to no-filter and SAYS so), `no_filter`, `custom` (verbatim WHERE body); `resolve_filter()` returns `(filter_sql, filter_label)`, `filter_sql` NEVER has a leading `WHERE` |
| **Output** | the 4-file bundle; runtime artefacts are the `DQ_Profile_*` tables + `DQ_Profile_System_Compare` view |

## Source

- `core/schema_profiler.py:196-238` — `ProfileRunSpec` defaults (two-mode docstring,
  thresholds)
- `core/schema_profiler.py:246-302` — `resolve_filter` (auto_active / no_filter / custom)
- `core/schema_profiler.py:313-403` — `_STAGING_DDL` (four-table star schema, run_id
  cascade)
- `core/schema_profiler.py:415-457` — `DQ_Profile_System_Compare` (divergence_signal)
- `core/schema_profiler.py:662-803` — per-column scan (approx-distinct strategy, RFC
  logical-null, profile_signal CASE)

## Related

[[ref-profiling-metrics-and-divergence-signals]] · [[ref-attribute-usage-analysis]] ·
[[ref-profiling-view-generation]] · [[ref-audit-engine]] · [[ref-three-database-architecture]]
· [[ref-architecture-context-and-project-yamls]] · [[ref-deletion-flag-resolver]] ·
[[ref-profiler-and-audit-pages]] · [[ref-target-mdm-model-fit]]
