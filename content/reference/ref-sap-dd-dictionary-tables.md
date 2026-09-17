---
id: ref-sap-dd-dictionary-tables
type: reference
title: SAP DD% Dictionary Tables
domain: sap
audience: [consultant]
level: foundation
status: review
links:
  - relates:prn-3-tier-description-resolution
  - relates:ref-building-a-per-client-dd-dictionary
  - relates:ref-sap-baseline-model
  - relates:ref-profiler-and-audit-pages
sources:
  - vault:sap-knowledge/SAP DD%25 Dictionary Tables.md
tags: [sap, industry-knowledge, dd-percent]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

The SAP Data Dictionary — the metadata that describes every table and field. Three tables you'll
repeatedly extract from for description enrichment.

## The three core tables

| Table | Grain | What it carries |
|---|---|---|
| **DD02T** | Table × Language | Table descriptions (e.g. MARA → *"General Material Data"*) |
| **DD03L** | Table × Field | Maps a (table, field) pair to its *data element* (ROLLNAME) |
| **DD04T** | Data Element × Language | Data element descriptions (e.g. MATNR → *"Material Number"*) |

Together they let you go from a technical name like `MARA.MATNR` to the human label *"Material
Number"* via a two-step join:

```
DD03L (MARA, MATNR) → ROLLNAME = MATNR
DD04T (MATNR, 'E') → DDTEXT = 'Material Number'
```

## Why three tables, not one

SAP's data dictionary is normalised: many fields share the same **data element**, which carries
the description. `MARA.MATNR`, `MARC.MATNR`, `EKPO.MATNR`, `VBAP.MATNR` all map to the data
element `MATNR` — the description lives once in DD04T, not duplicated 50× across DD03L.

So:

- DD03L: 6.8 million rows (every field on every table)
- DD04T: ~85,000 rows (one description per data element per language)

## DDLANGUAGE filter

Both DD02T and DD04T carry descriptions for **every language SAP supports**. Always filter to
English:

```sql
WHERE DDLANGUAGE = 'E'
```

Mass-extract without the language filter returns ~15× too many rows.

## Per-client snapshots

The Studio supports **per-client DD% dictionaries** — see
[[ref-building-a-per-client-dd-dictionary|Building a Per-Client DD% Dictionary]] for how to
build one.

Current Studio snapshots:

- **bacardi** — 683 MB, 520K table descriptions, 6.85M (table, field) descriptions
- **danone** — comparable size

Lookups against the SQLite are sub-millisecond. The Studio's profiler dashboard (see
[[ref-profiler-and-audit-pages|Profiler & Audit Pages]]) uses them as **tier 2** of the
[[prn-3-tier-description-resolution|3-Tier Description Resolution]] chain — falling back from the
in-run snapshot.

## In-run snapshot (tier 1)

Recent Studio versions can pull DD% directly during a profile run: it verifies DD02T/DD03L/DD04T
are reachable and English-populated on each source DB, then snapshots the relevant rows for the
dashboard to read from — so descriptions match the run exactly.

This is **tier 1** of the resolver — always fresh, always matches the profile data.

## Why this matters for DQ rules

When a defect lands on a reviewer's desk reading just `MARC.MMSTA = '02'`, they need to know:

- What's MARC? → DD02T = "Plant Data for Material"
- What's MMSTA? → DD04T = "Plant-Specific Material Status"
- What's '02'? → from MARC's domain or a config table

DD02T + DD03L + DD04T cover the first two. The third (value meaning) lives in domain tables that
vary per client — see
[[ref-value-description-resolution|Value-Description Resolution (4 mechanisms)]].

## Related

- [[prn-3-tier-description-resolution|3-Tier Description Resolution]]
- [[ref-building-a-per-client-dd-dictionary|Building a Per-Client DD% Dictionary]]
- [[ref-sap-baseline-model|SAP Baseline Model (logical vs physical)]]
- [[ref-value-description-resolution|Value-Description Resolution (4 mechanisms)]]
- [[ref-profiler-and-audit-pages|Profiler & Audit Pages]]
