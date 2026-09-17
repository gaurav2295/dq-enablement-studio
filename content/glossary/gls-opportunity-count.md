---
id: gls-opportunity-count
type: glossary
title: Opportunity Count
domain: rule-design
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-opportunity-universe
  - relates:gls-defect-rate
  - relates:prn-optsel-is-the-universe
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
tags: [scoring, metrics]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The number of records in a rule's [[gls-opportunity-universe|opportunity universe]] — the row
count of its [[gls-optsel|OptSel]], and the **denominator** of the [[gls-defect-rate|defect rate]].

## Why the Denominator Matters

```sql
-- Same defect count (1,000), different opportunity counts = different stories

-- Story A: Only 1,000 defects out of 10,000 opportunities
SELECT
  SUM(CASE WHEN zIsErrorFlag = 1 THEN 1 ELSE 0 END) AS defects,      -- 1,000
  COUNT(*) AS opportunities,                                          -- 10,000
  CAST(100.0 * SUM(CASE WHEN zIsErrorFlag = 1 THEN 1 ELSE 0 END) 
       / COUNT(*) AS DECIMAL(5,1)) AS defect_rate_pct                 -- 10%
FROM [DQ_0042_SAP_KNA1_OptSel];
-- "10% of customers have missing info" ✅ Actionable concern

-- Story B: Same 1,000 defects but only 1,000 opportunities
SELECT
  SUM(CASE WHEN zIsErrorFlag = 1 THEN 1 ELSE 0 END) AS defects,      -- 1,000
  COUNT(*) AS opportunities,                                          -- 1,000
  CAST(100.0 * SUM(CASE WHEN zIsErrorFlag = 1 THEN 1 ELSE 0 END) 
       / COUNT(*) AS DECIMAL(5,1)) AS defect_rate_pct                 -- 100%
FROM [DQ_0042_SAP_KNA1_RECENT_OptSel];
-- "100% of NEW customers have missing info" 🚨 Critical issue

-- Story C: Same 1,000 defects out of 1,000,000 opportunities
SELECT
  SUM(CASE WHEN zIsErrorFlag = 1 THEN 1 ELSE 0 END) AS defects,      -- 1,000
  COUNT(*) AS opportunities,                                          -- 1,000,000
  CAST(100.0 * SUM(CASE WHEN zIsErrorFlag = 1 THEN 1 ELSE 0 END) 
       / COUNT(*) AS DECIMAL(5,1)) AS defect_rate_pct                 -- 0.1%
FROM [DQ_0042_SAP_KNA1_ALL_OptSel];
-- "0.1% of ALL customers..." ✅ Minor issue, well-controlled
```

## Usage

Opportunity count is the number that makes a defect count mean something: 4,000 defects is
alarming out of 12,000 records and unremarkable out of 4,000,000. Both numbers are always quoted
together.

**Golden Rule:** Never report defects without opportunities. The ratio is what matters.

### Red Flags

- **Opportunity count = 0** — Usually means the universe filter is wrong, not that data is clean
- **Opportunity count = 1** — A rule that applies to only one record is usually overfitted or the scope is too narrow
- **Opportunity count >> defect count** — Good baseline, but check for silent changes in scope over time
- **Opportunity count = defect count (100%)** — Either a true crisis or the universe is too narrowly scoped

The audit engine treats 0% and 100% families as outliers worth inspecting (ref-audit-engine).
