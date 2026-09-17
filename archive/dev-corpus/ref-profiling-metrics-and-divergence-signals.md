---
id: ref-profiling-metrics-and-divergence-signals
type: reference
title: Profiling Metrics & Divergence Signals
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - prereq:ref-profiling-view-generation
  - relates:ref-schema-profiler
  - relates:ref-attribute-usage-analysis
  - relates:ref-exporters
  - relates:ref-value-description-resolution
  - relates:ref-target-mdm-model-fit
sources:
  - vault:studio-architecture/Studio — Profiling Metrics & Divergence Signals.md
tags: [studio, engine, methodology, sap, course]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

The profiling layer has three contracts to know: the metric catalog (3 live —
`distribution`/`completeness`/`uniqueness` — plus 11 coming-soon stubs), the cross-system
`divergence_signal` severity bands (`0.50` / `0.20` / `0.05` in shipped code), and
`EXPECTED_SECTION_OUTPUTS`, the 10-section dashboard upload contract whose column lists ARE the
parser fingerprint.

These three sit downstream of [[ref-profiling-view-generation]] and feed the
[[ref-schema-profiler]] dashboard.

## 1. The metric catalog (`core/profiling_metrics.py`)

Each metric is a `MetricDef(id, label, short_desc, live, aggregation, grain)`.
`DEFAULT_METRIC_ID = "distribution"`. Unknown/blank IDs fall back to the default (graceful
round-trip for stale specs) — never raise. Helpers: `all_metrics()`, `live_metrics()`,
`coming_soon_metrics()`, `get_metric(id)`, `is_live(id)`.

**Live (3) — have real SQL generators:**

| id | label | aggregation | grain |
|---|---|---|---|
| `distribution` (default) | Distribution | `COUNT, COUNT DISTINCT` | Segment × Profiled Value |
| `completeness` | Completeness | `COUNT, SUM(CASE NULL/empty), % Null` | Segment |
| `uniqueness` | Uniqueness | `COUNT, COUNT DISTINCT, Uniqueness Ratio` | Segment |

**Coming-soon (11) — render in the UI but SQL generation returns a commented stub until built:**
`validity`, `consistency`, `pattern` (Pattern/Format), `statistical` (numeric), `outlier`,
`referential` (Referential Integrity), `temporal` (Temporal/Trend), `hierarchical` (Hierarchical
Consistency), `simulation` (Rule Simulation), `mapping` (Value Mapping/Standardization), `volume`
(Data Volume & Coverage).

- **DO** drive non-live metrics through the placeholder path — see the
  `SELECT 1 ... /* DO NOT DEPLOY — placeholder */` stub in [[ref-profiling-view-generation]].
- **DON'T** teach a coming-soon metric as deployable; only the 3 live ones emit runnable SQL.

## 2. Cross-system divergence — `DQ_Profile_System_Compare`

The view aggregates per `(run × schema × table × column)` across `WHERE systems_observed >= 2`.
The key signal is `non_null_pct_spread = MAX(non_null_pct) - MIN(non_null_pct)` (it also computes
stdev and distinct-count spread). The coarse band is `divergence_signal`:

```sql
CASE
  WHEN systems_observed < 2        THEN 'single-system'
  WHEN non_null_pct_spread IS NULL THEN 'unknown'
  WHEN non_null_pct_spread >= 0.50 THEN 'high-divergence'
  WHEN non_null_pct_spread >= 0.20 THEN 'medium-divergence'
  WHEN non_null_pct_spread >= 0.05 THEN 'low-divergence'
  ELSE                                  'aligned'
END AS divergence_signal
```

Read it as: same column shaped very differently across systems (`>= 0.50`) down to basically
aligned (`< 0.05`). Example — a field populated 98% in PD1 but 41% in a second system has spread
`0.57` → `high-divergence`, a strong signal that the field's meaning or load differs by source.

> [!note] Authoritative bands are 0.50 / 0.20 / 0.05
> The shipped code uses **0.50 high / 0.20 medium / 0.05 low**. A proposed tightening to
> **0.02 / 0.10 / 0.30 is BACKLOG only and NOT implemented** — do not teach it as current. (A
> separate `>= 0.99` distinct-density cut flags candidate keys; that is unrelated to
> `divergence_signal`.)

## 3. The dashboard upload contract — `EXPECTED_SECTION_OUTPUTS`

Single source of truth for what the profiler exports and what the dashboard validates on upload.
A tuple of `(section_key, canonical_filename, column_count, columns)`. **The column list IS the
contract** — the dashboard parser fingerprints on lower-snake-case column names, so changing a
section's columns requires updating dashboard ingestion in lock-step. 10 sections:

| # | section_key | filename | cols |
|---|---|---|---|
| 1 | `system_tables` | "1. System × Table summary.txt" | 9 |
| 2 | `top_null` | "2. All columns.txt" | 8 |
| 3 | `candidate_keys` | "3. Candidate Keys.txt" | 6 |
| 4 | `low_cardinality` | "4. Low-Cardinality Columns.txt" | 5 |
| 5 | `top_values` | "5. Top-N Values.txt" | 7 |
| 6 | `trending` | "6. Run-over-Run Trending.txt" | 6 |
| 7 | `divergence` | "7. Cross-System Divergence.txt" | 10 |
| 8 | `ddic_tables` | "8. DDIC Tables.txt" | 3 (OPTIONAL, tier-1 desc) |
| 9 | `ddic_columns` | "9. DDIC Columns.txt" | 4 (OPTIONAL) |
| 10 | `attribute_usage` | "10. Attribute Usage.txt" | 8 |

Section 7 (`divergence`) carries the spread metrics from §2; section 10 is the
[[ref-attribute-usage-analysis]] pivot. DDIC sections (8/9) are optional and, when present, drive
tier-1 of [[ref-value-description-resolution]]. The contract is consumed by the manifest xlsx,
MANIFEST.md, and the upload validator.

## Inputs & outputs

| | |
|---|---|
| **Metric input** | a `metric_id` string on the profiling spec → `MetricDef` |
| **Divergence input** | `DQ_Profile_Columns` (per system_id) → `DQ_Profile_System_Compare` view |
| **Contract output** | 10 named `.txt` section exports validated against `EXPECTED_SECTION_OUTPUTS` |

## Source

- `core/profiling_metrics.py:46-145` — `_CATALOG` (3 live + 11 coming-soon), `DEFAULT_METRIC_ID`,
  `get_metric`/`is_live`
- `core/schema_profiler.py:415-457` — `DQ_Profile_System_Compare` view + `divergence_signal` CASE
- `core/schema_profiler.py:2629-2668` — `EXPECTED_SECTION_OUTPUTS` (the 10-section column contract)

## Related

[[ref-schema-profiler]] · [[ref-profiling-view-generation]] · [[ref-attribute-usage-analysis]] ·
[[ref-profiler-and-audit-pages]] · [[ref-exporters]] · [[ref-value-description-resolution]] ·
[[ref-target-mdm-model-fit]]
