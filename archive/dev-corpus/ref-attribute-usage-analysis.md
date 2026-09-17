---
id: ref-attribute-usage-analysis
type: reference
title: Attribute Usage Analysis (engine)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - parent:ref-schema-profiler
  - implements:con-attribute-usage-analysis
  - relates:std-aua-spec-template
  - relates:prn-profiling-has-no-pass-fail
  - relates:ref-value-description-resolution
  - relates:ref-deletion-flag-resolver
  - relates:ref-profiling-metrics-and-divergence-signals
  - relates:ref-profiling-view-generation
sources:
  - vault:studio-architecture/Studio — Attribute Usage Analysis (engine).md
tags: [studio, engine, methodology, sap, profiling]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

AUA pivots a low-cardinality attribute across an org dimension into a *tall* result set — gated by
the `qualifies_for_deep_dive` coverage qualifier (`max_distinct=50`, `top_k=20`, `threshold=0.80`,
plus a high-card distinct guard), fed by one of three most-specific-first spec parsers, and emitted
as one SELECT block per `(table × org-breakdown × attribute)` triple with a windowed percentage and
cross-table FK joins.

AUA is the "Deep Dive" sub-section of the [[ref-schema-profiler]]. Logic splits across
`core/attribute_usage.py` (qualifier, org knowledge, spec parsing/merge) and the emitters in
`core/schema_profiler.py`. It is profiling-class: **no `zIsErrorFlag`**.

## What it does

1. **Qualify** candidate columns as genuinely low-cardinality (the coverage qualifier).
2. **Parse** an optional `.md` spec (3 formats) for explicit attributes + org breakdown + scope
   filter; **merge** spec over knowledge-inferred defaults.
3. **Emit** one SQL block per `(table × org-breakdown × low-card attribute)` triple, joining
   value-description lookups and any cross-table scope filters.

## Coverage qualifier — `qualifies_for_deep_dive(...)` (`attribute_usage.py:45-146`)

Returns `True` only when a column is low-cardinality **AND** its top-K values cover the threshold.
Verbatim defaults:

| Param | Value | Meaning |
|---|---|---|
| `max_distinct` | **50** | `distinct_count > 50` → NEVER qualifies, regardless of skew |
| `top_k` | **20** | sum the first 20 ranked value counts |
| `threshold` | **0.80** | pass when `sum(top_k_counts) / sum(all_counts) >= 0.80` |

- Short-circuit on the distinct guard first. **Design:** the Top-N profiler caps at ~50 top values
  (`schema_profiler.py:229`, `TOP_VALUES_CAP_PER_COLUMN`). A truncated denominator inflates the
  coverage ratio and wrongly qualifies skewed high-card columns (the **KNB1.KUNNR explosion bug**,
  Studio Issue #1 / PR #2, fix `6a4c7b0`). The `distinct_count > 50` guard prevents this.
- A high-cardinality PK must never qualify as an attribute even when top-20 coverage ≥ 0.80.
- Empty input → `False`. Accepts canonical `(value_rank, value_count)` OR legacy
  `(rank, Occurrences/count)` field names.

## Spec parsing — 3 formats, most-specific-first (`attribute_usage.py:398-457`)

`parse_aua_spec_md` dispatches in order — **a less-specific format must never shadow a more-specific
one**:

1. **Format 3 — "Data Profiling Specification"** (canonical archival deliverable). Wins on H1
   `# Data Profiling Specification: <TABLE>` (`<TABLE>` matches `^[A-Z][A-Z0-9_]+$`), OR the H3
   fingerprint `### FIELD _(distinct values: N)_`, OR a lean `| TABLE.FIELD | desc |` row. Produces
   an **explicit** attribute list → `attribute_selection = "explicit"` → **skips the coverage
   qualifier entirely**.
2. **Format 1 — multi-table block** (`## Table: X` headers, Studio-canonical).
3. **Format 2 — per-table report-template** (signalled by a `Segmentation Attributes:` line).

Parser fingerprints (get any wrong → fall back to defaults or silently skip the table):

- Org breakdown read from the `- **Organizational column:**` bullet (`**` wraps the colon); **split
  on `+`** for multi-field (`VKORG + VTWEG`), never `,`.
- Attribute list = every `### FIELDNAME _(distinct values: N)_` H3; the `_(distinct values: N)_`
  tail is the fingerprint that distinguishes attribute headers from structural H3s (`### Rule`,
  `### Implementation`). Omit it → attribute dropped → silently incomplete analysis.
- H1 prose instead of a SAP code → falls back to the filename stem.

**Spec wins over inference** (`merge_spec_with_inference`, `:876-930`): spec-mentioned tables use
spec values with gaps filled from knowledge; unmentioned tables auto-infer everything. Default
`attribute_selection = "low_cardinality"` (uses the qualifier).

## Org-dimension knowledge (`attribute_usage.py:154-221`)

Loaded from `knowledge/methodology/org_dimensions.json` (30 tables). `infer_org_dims(table)` →
`[{label, fields}]`; `primary_key_for(table)` composes `zConcatenatedKey`; `deletion_flag_for(table)`.
Missing file/entry → empty (caller falls back). `_FIELD_LABELS` (`:291-325`) maps SAP codes to human
labels (VKORG→"Sales Org", WERKS→"Plant", BUKRS→"Company Code", MTART→"Material Type",
KTOKD/KTOKK→"Account Group"); multi-field joined with ` × `.

## Pivot output shape (`schema_profiler.py` `generate_attribute_usage_script`, `:1072+`)

One SQL block per `(table × org-breakdown × low-card attribute)` triple. **Tall** output (one row
per value), columns:

```
system_id, table_name, org_breakdown_label, org_combination,
org_combination_description, attribute_name, attribute_label,
attribute_value, attribute_value_description, occurrences,
percentage_within_org
```

- `percentage_within_org` (`:1965-1967`):

```sql
CAST(100.0 * COUNT(*) / NULLIF(SUM(COUNT(*)) OVER (PARTITION BY system + breakdown fields), 0) AS DECIMAL(5,2))
```

- Attribute counted only when populated: `<attr> IS NOT NULL` (`:1974`).
- `prep_db` default `"WRKDQPREP_ALL"`; language default `E`.
- `universe_label` default `"Active on Deletion Flag Only"` (deletion-flag exclusion in WHERE; no
  `zIsErrorFlag`).

## Cross-table FK join map — `_KNOWN_FOREIGN_JOIN_KEYS` (`schema_profiler.py:1507-1521`)

`AUATableTarget.additional_filter_sql` may reference OTHER tables (e.g.
`MARA.MTART IN ('FERT','ZFPR','ZMDA')` to scope MARC/MVKE to Finished Goods). The emitter detects the
cross-table ref and adds an INNER JOIN via this `base → {ref: join_field}` map:

- `MARC / MVKE / MARM / MAKT / MBEW / MLAN` → **MARA** on **MATNR**
- `KNB1 / KNVV / KNVP / KNVI` → **KNA1** on **KUNNR**
- `LFB1 / LFM1` → **LFA1** on **LIFNR**

Unknown relationship → emits a guarded `-- TODO` comment; does not break the block.

> [!note] Implementation status
> Canonical FROM target is `WRKDQ` (ONE repository): rule/profiling views are created in AND read
> FROM `WRKDQ` (same-DB read). `WRKDQPREP_ALL` is the **upstream prep layer** — it applies
> relevancy criteria, merges sources, performs logical aggregation, and applies scope; its output is
> **pushed into `WRKDQ`**, and rules do not read it directly. Canonical layering:
> `source → SRCECC_DA → WRKDQPREP_ALL (prep) → WRKDQ (rules created + read here)`. The app reads
> Error/Info rule views FROM/JOIN `WRKDQ` (one repository, matching profiling), and `WRKDQPREP_ALL`
> is used strictly as the upstream ETL/prep layer — no cross-DB read of the prep layer.

## Inputs & outputs

| | |
|---|---|
| **Input** | profile Top-N results (for the qualifier) + optional AUA `.md` spec (Format 1/2/3) |
| **Knowledge** | `org_dimensions.json`, `attribute_value_lookups.json` (236 fields, value-description LEFT JOINs) |
| **Output** | SSMS deep-dive script — tall result sets, one block per triple. AUA outputs are **result sets, not stored views**; if materialised: `DQ_AUA_{table}_{breakdown_alias}_{attribute}` (e.g. `DQ_AUA_MVKE_SalesOrgChannel_MEGRU`) |
| **API** | `POST /api/profiler/aua/generate-script`, `/aua/render-html` |

## Source

- `core/attribute_usage.py:45-146` — `qualifies_for_deep_dive` (50 / 20 / 0.80 + distinct guard)
- `core/attribute_usage.py:154-221` — org-dimension knowledge; `291-325` `_FIELD_LABELS`
- `core/attribute_usage.py:398-457` — `parse_aua_spec_md` (3 formats); `_parse_specification_format`
  (`:115`); `876-930` `merge_spec_with_inference`
- `core/schema_profiler.py:1072-1574` — `generate_attribute_usage_script`; pivot percentage
  `:1965-1967`; `IS NOT NULL` `:1974`; `_KNOWN_FOREIGN_JOIN_KEYS` `:1507-1521`

## Related

[[ref-schema-profiler]] · [[ref-profiling-metrics-and-divergence-signals]] ·
[[ref-profiling-view-generation]] · [[ref-value-description-resolution]] ·
[[ref-deletion-flag-resolver]] · [[ref-knowledge-base-file-inventory]] ·
[[ref-three-database-architecture]] · [[con-attribute-usage-analysis]] ·
[[prc-run-an-attribute-usage-analysis]]
