---
id: con-filter-presets
type: concept
title: Filter Presets
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:dq-methodology/Filter Presets.md
tags: [methodology, profiling]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:con-attribute-usage-analysis
  - relates:prc-generate-a-profile-bundle
---

## What a filter preset is

For the Schema Profiler, each target (system × table) picks one of
three filter presets to declare what records to profile.

## The three presets

### `auto_active`

Auto-detect the table's deletion flag via SAP metadata and apply `<flag> <> 'X'`.

- For MARA / KNA1 / LFA1 — applies `LVORM <> 'X'`
- For EKKO / PLKO — applies `LOEKZ <> 'X'`
- For KNB1 / KNVV — applies `LOEVM <> 'X'`
- For Z*/Y* customer tables (no known deletion flag) — degrades to no-filter with a warning

The metadata source is `knowledge/sap/table_metadata.json` — 87 tables with their deletion flag
mapped. Tables not in that file fall through to "no filter" with a clear label in the manifest
so the user can spot the gap.

**Use when:** the standard "active records only" scope is what you want. Most rules.

### `custom`

User-supplied WHERE clause body — no leading `WHERE`, semicolons stripped automatically.

```
filter_text: MATNR IN (SELECT MATNR FROM MARA WHERE MTART IN ('FERT', 'ZFPR', 'ZMDA'))
```

The Studio embeds this verbatim into the profile SQL with a comment showing the literal text.

**Use when:** you need a scope the auto-detect doesn't give you — finished-goods-only, specific
date range, specific plant, etc.

### `no_filter`

Profile every row in the table. Useful for:
- Configuration tables (T-tables) where there's no deletion concept
- Master tables where you genuinely want both active and deleted records (e.g. governance reviews)
- Z*/Y* customer tables where you don't yet know what scope is right

## The manifest tells the truth

The bundle's `Schema_Profile_Manifest.xlsx` Sheet 1 (Targets) lists what filter actually
resolved per target — preset, resolved SQL, audit label. **Always check the manifest** before
running the SQL — that's where you catch typos and unexpected fall-throughs.

## In the targets template

| system    | schema | table   | filter_preset | filter_text                                              |
|-----------|--------|---------|----------------|----------------------------------------------------------|
| ECCZ02100 | dbo    | MARA    | auto_active    |                                                            |
| ECCZ02100 | dbo    | KNA1    | auto_active    |                                                            |
| ECCZ02100 | dbo    | ZCUSTOM | custom         | MANDT = '100' AND STATUS <> 'X'                           |
| ECCZ02100 | dbo    | MAKT    | no_filter      |                                                            |

`filter_text` is ignored unless `filter_preset = custom`.

## Profiling Finished Goods — common preset

For Danone-style FG profiling:

```yaml
filter_preset: custom
filter_text: MATNR IN (SELECT MATNR FROM MARA WHERE MTART IN ('FERT', 'ZFPR', 'ZMDA'))
```

The FERT / ZFPR / ZMDA material types are the FG family. Don't exclude deleted (`LVORM`) — the
FG dataset includes recently-deactivated records you may still want to see in the profile.

## AUA uses `auto_active` by default

[[con-attribute-usage-analysis|Attribute Usage Analysis]] (the schema-profiler deep-dive)
inherits the same filter-preset machinery. `auto_active` is the default for every AUA target and
resolves identically to standard profiling. A per-table `.md` spec can override the deletion
flag explicitly when the table isn't in `org_dimensions.json`; otherwise the same metadata
lookup applies.

The exclusion always sits in the `WHERE` clause — AUA has no per-row pass/fail concept (no
`zIsErrorFlag`), so the deletion check shapes the universe rather than the per-row logic. See
[[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]] for the WHERE-vs-CASE
rationale.
