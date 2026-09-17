---
id: ref-profiling-view-generation
type: reference
title: Profiling View Generation (PrfSel/PrfSum)
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:ref-generate-sql-dispatcher
  - relates:ref-sql-generator
  - relates:ref-profiling-metrics-and-divergence-signals
  - relates:ref-view-name-token-resolution
  - relates:ref-three-database-architecture
  - relates:ref-multi-impl-fan-out-engine
  - implements:prn-profiling-has-no-pass-fail
  - relates:con-view-types
  - relates:con-profiling-concepts
  - relates:std-view-naming-patterns
sources:
  - vault:studio-architecture/Studio — Profiling View Generation (PrfSel-PrfSum).md
  - dq-studio:.claude/skills_canonical/studio-profiling.md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

Profiling rules emit a `(PrfSel, PrfSum)` pair that — unlike Error/Info views — reads from the
WORKING DB, segments by `zSourceSystemID` with a `GROUP BY` (not `UNION ALL`), and builds
distribution/completeness/uniqueness metrics with windowed percentages plus a C/V/M-gated
`zDomainSegment` column.

`generate_prfsel_pair(spec)` is the profiling branch of the [[ref-generate-sql-dispatcher]].
PrfSel is the per-record detail view; PrfSum is its aggregated summary. They are a
primary/wrapper pair like OptSel↔RptSel: the tracker registers only the primary (PrfSel).

## One spec, two views — the settled model

A profiling row produces **one** `DQRuleSpec` under **one** DQOps ID, carrying both SQL strings:
PrfSel in `sql_optsel`, PrfSum in `sql_rptsel`. `view_type` stays an empty string — labelling the
spec as either view would be ambiguous when it represents both. There is no per-system fan-out and
no per-view-type fan-out.

This matches the SKP-cloud deployment model (one DQOps ID → one tracker row → one enforcement
entity) and halves the AI-Enhance workload on profiling batches. Implemented by the profiling
early-return in `pipeline/bulk_processor.py::_expand_implementations`; see
[[ref-multi-impl-fan-out-engine]].

> [!warning] The two-spec model is dead — CONFLICT-006
> The Studio once emitted two sibling specs distinguished by `view_type`. Code or tests asserting
> `len(profiling_specs) == 2` are stale: the assertion is `== 1` with both SQL slots populated.
> This has been corrected more than once — treat a proposal to reintroduce it as a regression.

## What it does

1. **Resolves inputs** via `_resolve_profiling_inputs` (`sql_generator.py:372`, design comment
   `:326-335`). Reads `spec._profiling_input` (`metric_type`, `profiled_field`, `profiled_table`,
   drill-through keys).
2. **PrfSel (Detail)** — one row per record, no GROUP BY, no `zIsErrorFlag`. Columns:
   `zSourceSystemID`, optionally `zDomainSegment`, `zConcatenatedKey` (CONCAT of system +
   drill-through PKs), the profiled value, and drill-through keys
   (`_prfsel_detail_select_parts`, `:472-550`).
3. **PrfSum (Summary)** — aggregated by the metric (`sql_generator.py:622-895`).
4. **Dispatches the metric** by `_profiling_input.metric_type` through
   `core.profiling_metrics.get_metric` (`:426-440`). Non-live metrics emit a
   `SELECT 1 AS [NotImplemented] /* DO NOT DEPLOY — placeholder */` stub for BOTH views
   (`_prfsel_coming_soon`, `:868-895`).

## Key conventions / algorithm (do / don't)

### FROM target — WORKING DB (WRKDQ)

- **DO** point profiling FROM at `arch.working_db` (`WRKDQ`). Rule views are created in AND read
  from `WRKDQ` — one repository, a same-DB read. Confirmed at `sql_generator.py:270` / comment
  `:326-335`. Profiling already does this correctly; OptSel/InfSel now do the same (B4, fixed
  2026-07-01).

> [!note] Implementation status — Resolved 2026-07-01 (KNOWN-ISSUES B4)
> Canonical layering is `source → SRCECC_DA → WRKDQPREP_ALL (prep: relevancy / merge / aggregate /
> scope) → WRKDQ`. `WRKDQPREP_ALL` is the **upstream prep layer** whose output is **pushed into
> `WRKDQ`** — rules do NOT read it directly. The canonical FROM for every rule view is
> **`WRKDQ`** (one repository, same-DB read): rule views are CREATED in and SELECT FROM `WRKDQ`.
> The app now reads Error/Info rule views FROM/JOIN `working_db` (WRKDQ) — one repository,
> matching profiling; `WRKDQPREP_ALL` is upstream ETL only. The former divergence — reading the
> prep layer directly (`FROM = arch.prep_db or arch.source_db`) — has been reconciled.
> `architecture.md` mermaid is the single source of truth for topology.

### Segmentation — GROUP BY, not UNION ALL

- **DO** segment multiple source systems with a single FROM and `GROUP BY zSourceSystemID`. This
  is the **preferred** approach per the architecture KB.
- **DON'T** reach for the legacy `WITH source_union AS (... UNION ALL ...)` CTE generators
  (`generate_prfsel_pair_multisystem`, `:911-955`; `_build_multisystem_unions`, `:958-1053`,
  `{system}` token = `"MULTI"` when >1 source). They are kept back-compat only;
  segment-by-`zSourceSystemID` superseded them.
- The generator READS `src.zSourceSystemID` rather than hardcoding the literal, so source-system
  drift surfaces.
- The remaining `profiling_sources`-iterating, UNION-ALL'd generator path is a leftover from when
  each source had its own database. Since the prep-layer consolidation there is one prep DB with
  `zSourceSystemID` populated, so a single SELECT with `WHERE zSourceSystemID IN (...)` is cleaner.
  Backlog item: *Profiling SQL Consolidation (drop UNION ALL across source DBs)*. **Don't fix it as
  a side effect of other work** — it is a medium-effort refactor with its own review needs.

### The three live metrics (`core/profiling_metrics.py`)

`DEFAULT_METRIC_ID = "distribution"`; unknown/blank IDs fall back to default (round-trips stale
specs). 3 live, 11 coming-soon.

| Metric | What PrfSum computes | SQL detail |
|---|---|---|
| **distribution** (default) | Frequency + `[Percentage]` of each value, per segment | `CAST(100.0 * [Occurrences] / NULLIF(SUM([Occurrences]) OVER (PARTITION BY <seg cols>),0) AS DECIMAL(5,1))` (`:675-679`) — a derived-table pattern because MSSQL can't mix `COUNT(*)` with `SUM(COUNT(*)) OVER` in one SELECT |
| **completeness** | % Null / % Populated per segment | empty test `LTRIM(RTRIM(...)) = ''`, `DECIMAL(5,2)` |
| **uniqueness** | distinct count + uniqueness ratio | `COUNT(DISTINCT)` + ratio `DECIMAL(9,6)` |

Coming-soon (deferred stubs): validity, consistency, pattern, statistical, outlier, referential,
temporal, hierarchical, simulation, mapping, volume.

**Do not activate a coming-soon metric without a design pass.** Each one needs three things
settled first: a decision on whether it is pass/fail-shaped or report-shaped, a SQL pattern that
actually fits the metric, and test coverage. They ship as column-shape-only placeholders precisely
so nobody deploys a half-designed metric.

### `_profiling_input` — the transient input dict

`spec._profiling_input` is round-tripped through the API serialisers as `_profiling_input` on the
spec dict:

```python
{
  "profiled_table": "KNVV",
  "profiled_field": "ZTERM",
  "profiled_attribute": "Payment Terms",
  "segment_table": "KNVV",
  "segment_field": "VKORG",
  "segment_by": "Sales Organization",
  "metric_type": "distribution",
  "scope_notes": "...",
  "business_insight": "...",
  "systems": ["Z02", "Z06"],
  "drill_through_keys": ["KUNNR"],
}
```

> [!warning] Known design gap — the input shape suits Distribution only
> This shape (Excel template + UI panel) was designed for Distribution rules. It is **awkward for
> completeness and uniqueness**, which are typically table-wide — many fields, no meaningful
> segment. Consultants end up either filling in ceremonial segment values they don't mean, or
> authoring 30 near-duplicate rows to profile every field of a table.
>
> This is a live backlog investigation (*Non-Distribution Profiling: Better-Suited Tooling for
> Completeness, Uniqueness, and Beyond*), not a bug to patch. In particular, do **not** "just
> expand" the Excel template with extra columns — the design question is genuinely open and
> pre-deciding it in a template change forecloses it.

### zDomainSegment — C/V/M gated only

- **DO** add the `zDomainSegment` column **only** when the profiled table is a
  Customer/Vendor/Material master in `core.multi_impl.DOMAIN_SEGMENT_TABLES`
  (`_profiling_has_domain_segment`, `:448-469`).
- It is a **classification**, not an identifier: excluded from `zConcatenatedKey` (`key=""`). The
  header table (KNA1 / LFA1 / MARA) carries the classifier; "rule name wins" disambiguation
  applies (see [[ref-local-deriver]]).

### View naming — {system} omitted by default

- Default profiling patterns are `DQ_{id}_{table}_{field}_PrfSel` / `..._PrfSum` — **no
  `{system}` token** (`spec_model.py:107-121`; YAML resolver `architecture.py:262-272`). `{field}`
  = `_profiling_input.profiled_field` (fallback first ORG/BASIC output field, excluding tech
  fields); `{table}` = `profiled_table` (`sql_generator.py:2053-2090`). Per-system profiling can
  opt in to `{system}` via project YAML.

> [!note] Implementation status — Resolved 2026-07-01 (KNOWN-ISSUES B2)
> There is now one canonical view-name pattern: the YAML resolver defaults were aligned to the
> `spec_model` dataclass so `{system}` is present consistently across both code paths. The YAML
> resolver is the production path and is now the single canonical pattern set. Profiling views
> omit `{system}` by default in both paths.

## Inputs & outputs

| | |
|---|---|
| **Input** | `DQRuleSpec` with `rule_type = PROFILING` and `_profiling_input` (metric_type, profiled_field/table, drill-through keys) |
| **Output** | `(PrfSel, PrfSum)` strings → `spec.sql_optsel` (primary) / `spec.sql_rptsel` (secondary) |
| **FROM** | `arch.working_db` (WRKDQ) |
| **Header label** | PrfSel → "Profiling Report — Detail (PrfSel)"; PrfSum → "Profiling Report — Summary (PrfSum)" |

> [!note] Round-trip — KNOWN-ISSUES B13
> The [[ref-sql-parser]] only reverse-imports OptSel/RptSel; PrfSel/PrfSum fall through to
> name-based routing. Documented limitation, not a silent bug.

## Common bugs to avoid

- Producing two sibling specs distinguished by `view_type`. One spec, two views.
- Adding per-system fan-out to profiling rows. Profiling is cross-system by design.
- Adding `{system}` to profiling view-name patterns.
- Activating a coming-soon metric type without a design pass and test coverage.
- Expanding the Excel template ad hoc to cover completeness/uniqueness.
- Applying the five-section Error/Info SELECT layout to profiling SQL — profiling has its own
  structure and the section comments do not apply.

## Verification

```bash
# Profiling = one spec with both SQL slots populated:
python3 -m pytest tests/test_multi_impl.py::TestBulkFanOut::test_profiling_row_produces_one_spec_with_paired_views -v

# Profiling view names drop {system}:
python3 -m pytest tests/test_sql_generator.py::TestPrfSumViewNaming::test_rendered_profiling_view_name_has_no_system -v

# The generator produces both PrfSel and PrfSum:
python3 -m pytest tests/test_sql_generator.py::TestProfiling -v
```

## Source

- `core/local_deriver.py::_build_profiling_spec_from_input` — builds a profiling spec from the
  structured input dict; `parse_profiling_to_input` — narrative parser ("Distribution of X by Y")
  → `profiling_input`.
- `core/profiling_metrics.py::get_metric` — metric registry with live / coming-soon status and UI
  metadata.
- `pipeline/bulk_processor.py::_expand_implementations` — profiling early-return (one spec, no
  fan-out).
- `core/sql_generator.py:318-440` — `generate_prfsel_pair`, `_resolve_profiling_inputs` (`:372`),
  metric dispatch (`:426-440`)
- `core/sql_generator.py:448-469` — `_profiling_has_domain_segment` (C/V/M gate)
- `core/sql_generator.py:472-550` — `_prfsel_detail_select_parts` (Detail columns)
- `core/sql_generator.py:622-895` — PrfSum aggregation (distribution `:675-679`, coming-soon stub
  `:868-895`)
- `core/profiling_metrics.py:129-139` — `get_metric`, metric catalog
- `core/multi_impl.py` — `DOMAIN_SEGMENT_TABLES`

## Related

[[ref-generate-sql-dispatcher]] · [[ref-sql-generator]] ·
[[ref-profiling-metrics-and-divergence-signals]] · [[ref-schema-profiler]] ·
[[ref-view-name-token-resolution]] · [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] ·
[[ref-three-database-architecture]] · [[ref-architecture-context-and-project-yamls]] ·
[[ref-sql-parser]] · [[ref-multi-impl-fan-out-engine]] · [[prn-profiling-has-no-pass-fail]] ·
[[con-view-types]] · [[ref-local-deriver]]
