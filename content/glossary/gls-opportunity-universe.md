---
id: gls-opportunity-universe
type: glossary
title: Opportunity Universe
domain: rule-design
audience: [consultant]
level: foundation
status: review
links:
  - relates:prn-optsel-is-the-universe
  - relates:gls-optsel
  - relates:gls-opportunity-count
  - relates:gls-defect-rate
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [scoring, optsel]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **full population a rule applies to** — every record the rule *could* have flagged, defective
or not. Also spoken of as the **opportunity population**, and it is exactly what an
[[gls-optsel|OptSel]] returns.

## The Opportunity Universe Workflow

```
1. DEFINE THE SCOPE (WHERE clause)
   ├─ Which table(s)?
   ├─ Which system(s)? [zSourceSystemID]
   └─ Which records are "in play"? (deleted? inactive? test data?)
   
2. COUNT THE UNIVERSE (OptSel)
   ├─ Run the OptSel: SELECT * WHERE [scope conditions]
   └─ Result: opportunity_count = total rows returned
   
3. COUNT THE DEFECTS (RptSel)
   ├─ Run the RptSel: SELECT * FROM OptSel WHERE zIsErrorFlag = 1
   └─ Result: defect_count = total error rows
   
4. CALCULATE THE DEFECT RATE
   ├─ defect_rate = defects / opportunities
   ├─ Example: 45 defects / 1500 opportunities = 3%
   └─ Publish: "3% of LIVE materials are missing unit of measure"
```

## Example: Active Materials Universe

```sql
-- STEP 1: Define the universe scope
-- Scope: Active SAP materials only (not deleted, not test)

-- STEP 2: Build the OptSel (universe = all active materials)
CREATE VIEW [dbo].[DQ_0101_SAP_MARA_ACTIVE_OptSel] AS
SELECT
  MaterialID,
  zSourceSystemID,
  MaterialType,
  Plant,
  BaseUnitOfMeasure,
  CASE
    WHEN BaseUnitOfMeasure IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM MARA_Stage
WHERE zSourceSystemID = 'SAP'
  AND LOEKZ IS NULL  -- Not marked for deletion
  AND MTART NOT IN ('TEST', 'SAMPLE')  -- Exclude test materials
  -- Result: 1500 total rows (the UNIVERSE)

-- STEP 3: Build the RptSel (defects only)
CREATE VIEW [dbo].[DQ_0101_SAP_MARA_ACTIVE_RptSel] AS
SELECT * FROM [dbo].[DQ_0101_SAP_MARA_ACTIVE_OptSel]
WHERE zIsErrorFlag = 1;
  -- Result: 45 rows (the DEFECTS)

-- STEP 4: Calculate defect rate
SELECT
  COUNT(*) AS opportunity_count,        -- 1500
  SUM(CASE WHEN zIsErrorFlag = 1 THEN 1 ELSE 0 END) AS defect_count,  -- 45
  CAST(100.0 * SUM(CASE WHEN zIsErrorFlag = 1 THEN 1 ELSE 0 END) 
       / NULLIF(COUNT(*), 0) AS DECIMAL(5,1)) AS defect_rate_pct  -- 3.0%
FROM [dbo].[DQ_0101_SAP_MARA_ACTIVE_OptSel];
```

## Usage

The universe is the denominator. A rule that returns only its defects has no universe and
therefore no [[gls-defect-rate|defect rate]] — which is why the OptSel keeps every row and carries
the verdict per row instead of filtering.

Getting the universe right is a design decision, not a technicality: excluding deleted records
from the universe (rather than from the flag) is what makes "3% of *live* materials" a defensible
statement — see [[prn-deletion-flags-belong-in-where]].

### Why This Matters

- **Universe defines the claim** — "3% of ACTIVE materials" vs. "0.5% of ALL materials" (including deleted) are vastly different claims
- **OptSel must return all rows** — filtering defects out would lose the denominator
- **RptSel filters to defects** — the ActOps wraps OptSel to show only the actionable defects
