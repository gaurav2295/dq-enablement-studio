---
id: gls-grain
type: glossary
title: Grain
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:con-profiling-concepts
  - relates:con-view-types
  - relates:gls-prfsel
  - relates:gls-prfsum
  - relates:std-sql-performance-standards
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [modelling, profiling]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**What one row of a result means.** 
- **Record grain** = one row per source record (1:1 with the base table)
- **Aggregated grain** = one row per group (system × segment × value; many-to-one)

## Example: Record Grain vs. Aggregated Grain

```sql
-- RECORD GRAIN: One row per material
-- Grain: One row = One material (1:1 with MARA)
SELECT
  MARA.MaterialID,
  MARA.zSourceSystemID,
  MARA.MaterialType,
  MARA.Plant,
  MARA.BaseUnitOfMeasure,
  CASE WHEN MARA.BaseUnitOfMeasure IS NULL THEN 1 ELSE 0 END AS zIsErrorFlag
FROM MARA_Stage AS MARA
WHERE MARA.zSourceSystemID = 'SAP';

-- Result: 10,000 rows if there are 10,000 SAP materials
-- Grain: RECORD (one per source material)


-- AGGREGATED GRAIN: Summary by (system, material type, unit)
-- Grain: One row = One (system, MaterialType, UoM) combination
SELECT
  zSourceSystemID,
  MaterialType,
  BaseUnitOfMeasure,
  COUNT(*) AS Occurrences,
  CAST(100.0 * COUNT(*) / NULLIF(SUM(COUNT(*)) OVER (PARTITION BY zSourceSystemID, MaterialType), 0) AS DECIMAL(5,1)) AS Percentage
FROM MARA_Stage
WHERE zSourceSystemID = 'SAP'
GROUP BY zSourceSystemID, MaterialType, BaseUnitOfMeasure;

-- Result: ~150 rows (one per unique combination)
-- Grain: AGGREGATED (grouped by system × type × UoM)
```

## The Grain Trap

```sql
-- WRONG: Unnecessary DISTINCT changes grain silently
SELECT DISTINCT
  MaterialID,
  zSourceSystemID,
  Plant
FROM MARA_Stage;

-- If a material has 5 plants, MARA has 5 rows. 
-- DISTINCT collapses to 1 row (grain changed!) 
-- But the consultant may not notice — the view still returns *a* number
-- Just the WRONG number

-- RIGHT: Keep record grain, filter if needed
SELECT
  MaterialID,
  zSourceSystemID,
  Plant,
  CASE WHEN BaseUnitOfMeasure IS NULL THEN 1 ELSE 0 END AS zIsErrorFlag
FROM MARA_Stage
WHERE zSourceSystemID = 'SAP';

-- No DISTINCT. Grain is clear: one row per (MaterialID, Plant) combination
```

## Usage

Grain is the first thing to state about any view, because almost every counting mistake is a grain
mistake. [[gls-prfsel|PrfSel]] is record grain by contract; [[gls-prfsum|PrfSum]] is aggregated
grain. An OptSel is record grain — which is why an unnecessary `SELECT DISTINCT` there is a
finding: it silently changes the grain and therefore the
[[gls-opportunity-count|opportunity count]].

A join that fans a row out to many is a grain change too, whether or not it was intended.

### Grain Checklist

- [ ] **Record-grain views** (OptSel, PrfSel): One row per source record or row combination
- [ ] **No accidental DISTINCT** — if you wrote it, you meant to filter, not to collapse
- [ ] **Joins explicit** — if a join changes grain (one-to-many), document it and adjust counts
- [ ] **Aggregated grain explicit** — PrfSum always states GROUP BY and segment dimensions
