---
id: prc-generate-a-profile-bundle
type: procedure
title: Generate a Profile Bundle
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:sops/SOP — Generate a Profile Bundle.md
tags: [sop, profiling]
created: 2026-08-20
updated: 2026-08-21
links:
  - relates:con-filter-presets
  - relates:prn-3-tier-description-resolution
  - relates:con-profiling-concepts
  - relates:ref-profiler-and-audit-pages
---

## Goal

How to take a list of (system × table) targets and produce a runnable SSMS profile script +
downstream dashboard. End-to-end.

## When to use

- Initial discovery on a new sprint — what's the shape of the data we'll be writing rules
  against?
- Mid-sprint drill-in on a single domain (e.g. Finished Goods profiling)
- Pre-deployment validation — does the data still look the way it did when we authored rules?

## Prerequisites

- Studio running locally
- A target list either authored manually in the targets template xlsx, or generated from the
  project's table registry filtered to the domain
- SQL Server access (where you'll run the generated script)
- DD% reachable on each source DB (the prereq check enforces this)

## Steps

### 1. Build the target list

Open `/profile` and download the targets template xlsx. Columns:

| system | schema | table | filter_preset | filter_text |
|---|---|---|---|---|

- `system` = the source DB name (e.g. ECCZ02100, S4SG2100)
- `schema` = `dbo` (default) — almost always
- `table` = the SAP table to profile
- `filter_preset` = one of `auto_active` / `custom` / `no_filter`
- `filter_text` = the WHERE-clause body, only when `filter_preset = custom`

For Finished Goods profiling, the standard preset is `custom` with:

```sql
MATNR IN (SELECT MATNR FROM MARA WHERE MTART IN ('FERT', 'ZFPR', 'ZMDA'))
```

See [[con-filter-presets|Filter Presets]] for the full preset reference.

### 2. Upload the target list

Drop into `/profile` — the page lists the targets, validates filter presets, confirms the
systems are configured in the project YAML.

### 3. Generate the bundle

Click **Generate Profile Bundle**. The Studio produces a zip with:

- `DQ_Schema_Profile.sql` — the runnable SSMS script
- `Sample_Dashboard_Query.sql` — for inspecting the staged results
- `README.md` — install + run notes
- `Schema_Profile_Manifest.xlsx` — Targets / Systems / Generation / ExpectedOutputs sheets
- `MANIFEST.md` — canonical filenames per section

### 4. Run the script

Open `DQ_Schema_Profile.sql` in SSMS, connect to the target SQL Server, execute. The script:

1. **Section 0** — DD% prereq check; PRINTs which source DBs have DD% reachable. Warning only,
   doesn't halt.
2. **Section 0a** — Creates staging tables (Run / Tables / Columns / TopValues) if missing
3. **Section 0b** — Creates DDIC snapshot tables (Tables / Columns)
4. **Section 1a/1b** — Defines helper procs (top-N + profile-one-table)
5. **Section 2** — Inserts a Run record + loops over `#targets`, executing one helper proc call
   per row
6. **Section 4** — Snapshots DD% from each source DB into `DQ_Profile_DDIC_*`
7. **Section 3** — Retention (keeps last N runs)

Run time: ~1-5 minutes per table depending on row count + filter.

### 5. Export the results

The dashboard query produces 7-9 result sets. Export each via SSMS "Results to Text" or "Save
as CSV". Canonical filenames (see MANIFEST.md):

| # | File | What |
|---|---|---|
| 1 | `1. System × Table summary.txt` | One row per (system, table) — row counts, column counts |
| 2 | `2. All columns.txt` | One row per (system, table, column) — null %, distinct count, signal |
| 3 | `3. Candidate Keys.txt` | Columns where distinct = row count |
| 4 | `4. Low-Cardinality Columns.txt` | Columns with 2-100 distinct values |
| 5 | `5. Top-N Values.txt` | Top 20K values per column |
| 6 | `6. Run-over-Run Trending.txt` | non_null_pct across last 5 runs |
| 7 | `7. Cross-System Divergence.txt` | Per-column divergence across systems |
| 8 | `8. DDIC Tables.txt` (optional) | From `DQ_Profile_DDIC_Tables` — for tier-1 description enrichment |
| 9 | `9. DDIC Columns.txt` (optional) | From `DQ_Profile_DDIC_Columns` |

### 6. Render the dashboard

Back in `/profile`, upload the files (or a zip of them). The Studio produces a standalone HTML
dashboard with KPI bar, per-system table lists, drill-into-column drawer, cross-system
divergence, low-cardinality + candidate-key shortlists, top-N values, trending.

Optionally enrich descriptions via:

- Tier 1 (snapshot) — automatic if you upload the DDIC files
- Tier 2 (client) — pick from "Client SAP dictionary" dropdown (bacardi, danone, etc.)
- Tier 3 (internal) — automatic fallback

The provenance badge shows the mix. See
[[prn-3-tier-description-resolution|3-Tier Description Resolution]].

## Verification

- Dashboard renders without console errors
- KPI bar shows non-zero system + table counts
- Spot-check a column with a known long-tail distribution — Top-N values render with sensible
  percentages

## Common pitfalls

- **MANIFEST.md mentions section 2 but the export only has section 1's content** — common SSMS
  export bug (forgot to switch result-set tabs). Fix: re-run, export each result separately.
- **File names don't match** — dashboard uses filename hints to route. If you rename them, the
  header-fingerprint fallback usually catches it but check the dashboard's "Skipped files"
  notice.
- **Dashboard descriptions are mostly blank** — DD% snapshot didn't reach the dashboard. Either
  upload sections 8+9, or pick a client SQLite dictionary.

## Related

- [[con-filter-presets|Filter Presets]]
- [[prn-3-tier-description-resolution|3-Tier Description Resolution]]
- Studio — Schema Profiler
- [[ref-profiler-and-audit-pages|Studio — Profiler & Audit Pages]] (the dashboard renderer)
