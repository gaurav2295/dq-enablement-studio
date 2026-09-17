---
id: con-profiling-concepts
type: concept
title: Profiling Concepts
domain: rule-design
audience: [consultant]
level: practitioner
status: approved
sources:
  - vault:dq-methodology/Profiling Concepts.md
  - dq-studio:.claude/skills_canonical/studio-profiling.md
tags: [methodology, profiling]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:con-rule-types
  - prereq:con-view-types
  - relates:con-filter-presets
  - relates:con-multi-implementation-model
  - relates:con-attribute-usage-analysis
  - relates:prn-profiling-has-no-pass-fail
  - relates:ref-profiler-and-audit-pages
  - relates:gls-cardinality
  - relates:gls-grain
  - relates:gls-top-n-distribution
---

## The core idea

Profiling rules don't pass-or-fail records — they **describe** the distribution of a value
across systems. Used to inform governance, mastering, standardisation.

## What a profile actually returns

For a profiling rule on `Profit Center across Controlling Area`:

| zSourceSystemID | Controlling Area | Profit Center | Occurrences | Percentage |
|---|---|---|---|---|
| SRCECCZ02100 | 1000 | PC_1010 | 15,432 | 38.4 |
| SRCECCZ02100 | 1000 | PC_1020 | 11,002 | 27.4 |
| SRCECCZ02100 | 1000 | PC_1030 | 8,761 | 21.8 |
| SRCECCZ02100 | 1000 | (NULL) | 5,003 | 12.4 |
| SRCECCZ03100 | 2000 | PC_2010 | 24,887 | 65.1 |

Percentage = within-segment (Controlling Area in this example), not across the whole table.

## Key concepts

### Metric Type
What kind of distribution? Three metric types are **live** in the Studio today:

| Metric | What it answers | What the SQL does |
|---|---|---|
| **distribution** (default) | "How is this value spread?" | `GROUP BY` profiled field + segment, counts, and percent-within-segment via `100.0 * count / SUM(count) OVER (PARTITION BY segment)` |
| **completeness** | "How much of this is populated?" | NULL count + populated percentage per profiled field |
| **uniqueness** | "How distinct is this?" | `COUNT(DISTINCT ...)` + a uniqueness ratio |

Eleven more are **reserved but not built** — validity, consistency, pattern, statistical, outlier,
referential, temporal, hierarchical, simulation, mapping, volume. They are selectable and generate
a clearly-marked placeholder view; they are not deployable. If a client scenario needs one, it is a
design conversation with the CoE, not a rule to write.

> [!warning] Completeness and uniqueness are awkward to author today
> The profiling input shape (Excel template + UI panel) was designed for Distribution, which always
> has a meaningful segment. Completeness and uniqueness are usually **table-wide** — many fields, no
> segment — so consultants end up inventing ceremonial segment values or authoring one near-duplicate
> row per field. Better tooling for non-Distribution profiling is an open backlog investigation.
> Until it lands, keep the row count honest and say so in the scope notes rather than padding the
> template.

### Segmentation
The column(s) to GROUP BY on top of `zSourceSystemID`. E.g. profiling Profit Center across
Controlling Area uses Controlling Area as the segmentation. Drives the PARTITION BY of the
percentage window.

### Profiled Attribute
The column whose distribution is being measured. Goes into both the SELECT (as the value
column) and the GROUP BY.

### Grouping
The full GROUP BY list — typically `zSourceSystemID + segmentation + profiled attribute`. Often
includes lookup descriptions joined in for human readability.

## Window function — the percentage math

```sql
CAST(100.0 * [Occurrences]
     / NULLIF(SUM([Occurrences]) OVER (PARTITION BY [zSourceSystemID], [Segment]), 0)
     AS DECIMAL(5,1)) AS [Percentage]
```

The `NULLIF(..., 0)` is **mandatory** — without it, segments where every record has the same
value crash the view (`100 / 100` is fine, but if the OVER window happens to land on an empty
partition, you get a divide-by-zero).

## What profiling is for

- **Standardisation decisions**: "Profit Centers vary 40+ ways across 4 systems — which are
  real, which are typos?"
- **Mastering inputs**: "VAT formats per country in our customer base — what variants do we have
  to support in the merge logic?"
- **Coverage check**: "What % of materials have a UoM populated, per plant?"

It's **not** for finding defects — that's Error rules. Profiling output is grist for *human*
decisions about reference data, MDM scope, and remediation priority.

## Cross-system semantics

Profiling rules **do not** fan out per-system like Error rules. They segment **by**
`zSourceSystemID` and emit one cross-system view per rule. So:

- One profiling rule → **one** implementation, never N. That single implementation carries both
  views (PrfSel detail + PrfSum summary) under one DQOps ID and one tracker row, whose ViewType
  cell reads `PrfSel + PrfSum`.
- `SKP_RULE_NNNN` still applies; for profiling it is 1:1 with the DQOps ID rather than grouping
  siblings.
- Listing systems on a profiling row does **not** fan it out — the list becomes a
  `WHERE zSourceSystemID IN (...)` filter inside the one view.

See [[con-multi-implementation-model|Multi-Implementation Model]] for the contrast with
Error/Info rules.

## Deep-dive variant — Attribute Usage Analysis

Standard profiling answers *"how is column X distributed globally?"*. Its deep-dive sibling —
[[con-attribute-usage-analysis|Attribute Usage Analysis]] — answers *"how is column X
distributed **within each organisational slice**?"* (e.g. MTART pivoted by WERKS × BUKRS). AUA
depends on standard profiling — it reads the same Top-N output to apply its low-cardinality
qualifier (top 20 ≥ 80% coverage).

| | Standard profiling | Attribute Usage Analysis |
|---|---|---|
| Question | Column distribution | Column distribution **per org slice** |
| View types | PrfSel + PrfSum | One-off SELECT result sets (not stored as views) |
| Output shape | Wide pivot at the column grain | Tall pivot at (org × attribute × value) grain |
| Threshold | All columns profiled | Top-20 ≥ 80% qualifier |
| Filter preset | Any | `auto_active` by default |
| Cross-system | Cross-system (segment by zSourceSystemID) | Cross-system (segment by zSourceSystemID + org) |

AUA is a sub-section of the Schema Profiler, not a separate page. See
[[ref-profiler-and-audit-pages|Studio — Profiler & Audit Pages]].

## Related

- [[con-rule-types|Rule Types — Error, Info, Profiling]]
- [[con-view-types|View Types — OptSel RptSel InfSel PrfSel PrfSum]]
- [[con-filter-presets|Filter Presets]]
- [[con-attribute-usage-analysis|Attribute Usage Analysis]]
- [[prn-profiling-has-no-pass-fail|Why Profiling Has No Pass-Fail]]
