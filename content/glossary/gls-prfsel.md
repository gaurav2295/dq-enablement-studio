---
id: gls-prfsel
type: glossary
title: PrfSel (Profile Detail view)
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:con-view-types

  - relates:prn-profiling-has-no-pass-fail
  - relates:gls-prfsum
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [views, profiling, prfsel]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **Profile Detail view** — the record-grain half of a Profiling rule's view pair. One row per
source record, carrying the segmentation columns plus the profiled attribute. No aggregation, no pass/fail.

## Example: Material Unit of Measure Distribution

Profile the distribution of `BaseUnitOfMeasure` across materials, segmented by `MaterialType`:

```sql
CREATE VIEW [dbo].[DQ_0101_SAP_MARA_MEINS_PrfSel] AS

SELECT
  -- Identity and system scope
  MARA.MaterialID,
  MARA.zSourceSystemID,
  
  -- Segmentation: how to slice the population
  MARA.MaterialType,
  
  -- Subject: the attribute being profiled
  MARA.BaseUnitOfMeasure,
  
  -- No zIsErrorFlag — profiling has no pass/fail
  
FROM MARA_Stage AS MARA
WHERE MARA.zSourceSystemID IN ('SAP', 'LEGACY')
ORDER BY MARA.MaterialType, MARA.BaseUnitOfMeasure;
```

Notice: **One row per material** — the profiled value (`BaseUnitOfMeasure`) appears as-is, no aggregation.

## Usage

PrfSel is **record-level by contract**: no `GROUP BY`, no aggregate function. It also carries **no**
`zIsErrorFlag` — a Profiling rule has no pass/fail, so there is nothing to flag
([[prn-profiling-has-no-pass-fail]]).

Its partner [[gls-prfsum]] does the aggregation. The two always ship together, share one rule id,
and — unlike Error/Info rules — do **not** fan out per source system; the systems in scope become
an `IN (...)` filter instead.
