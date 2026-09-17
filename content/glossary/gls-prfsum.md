---
id: gls-prfsum
type: glossary
title: PrfSum (Profile Summary view)
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:con-view-types

  - relates:gls-prfsel
  - relates:gls-top-n-distribution
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [views, profiling, prfsum]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **Profile Summary view** — the aggregated half of a Profiling rule's view pair. One row per
`(zSourceSystemID, segment, value)` with an occurrence count and the percentage of that value
*within its segment*.

```sql
CAST(100.0 * [Occurrences]
     / NULLIF(SUM([Occurrences]) OVER (PARTITION BY [zSourceSystemID], [Segment]), 0)
     AS DECIMAL(5,1)) AS [Percentage]
```

## Usage

The `NULLIF(..., 0)` guard on the denominator is mandatory, not defensive style. The
percentage is always **within segment**, never across the whole table; that is what makes a
distribution comparable between systems and company codes.
