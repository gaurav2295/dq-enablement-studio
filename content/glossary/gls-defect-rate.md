---
id: gls-defect-rate
type: glossary
title: Defect Rate
domain: rule-design
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-opportunity-count
  - relates:gls-opportunity-universe
  - relates:prn-optsel-is-the-universe
  - relates:prn-profiling-has-no-pass-fail
  - relates:gls-dq-score
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
tags: [scoring, metrics]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**`defects / opportunities`** — the share of a rule's [[gls-opportunity-universe|universe]] that fails it. 

ADM computes it from the [[gls-optsel|OptSel]]/[[gls-rptsel|RptSel]] pair, which is why both counts have to come from the same view.

## Calculation Example

```sql
-- Rule: Customer master must have a valid currency code
-- Universe: All active customers

-- STEP 1: Get opportunity count (from OptSel)
SELECT COUNT(*) AS opportunity_count
FROM [DQ_0001_SAP_KNA1_ACTIVE_OptSel];
-- Result: 5,000 total customers in scope

-- STEP 2: Get defect count (from RptSel)
SELECT COUNT(*) AS defect_count
FROM [DQ_0001_SAP_KNA1_ACTIVE_RptSel]
WHERE zIsErrorFlag = 1;
-- Result: 450 customers with missing/invalid currency

-- STEP 3: Calculate defect rate
-- defect_rate = 450 / 5,000 = 0.09 = 9%

SELECT
  450 AS defects,
  5000 AS opportunities,
  CAST(100.0 * 450 / 5000 AS DECIMAL(5,1)) AS defect_rate_pct;

-- Result: 9.0% defect rate
-- Claim: "9% of ACTIVE customers are missing a valid currency code"
```

## The Universe Determines the Claim

| Universe Definition | Defect Count | Opportunities | Defect Rate | Claim |
|---|---|---|---|---|
| All customers (including deleted) | 450 | 50,000 | 0.9% | "Nearly all customers are valid" ❌ Misleading |
| Active customers only | 450 | 5,000 | 9.0% | "9% of active customers lack currency" ✅ Honest |
| Customers created in last 90 days | 150 | 800 | 18.8% | "New customers have higher error rate" ✅ Specific |

**The denominator must be stated or the number lies.**

## Usage

A defect rate is only comparable when its denominator is stated. "12% of live vendors" and "12% of
all vendor records including deletions" are different claims.

Profiling rules have **no** defect rate — there is no pass/fail to divide
([[prn-profiling-has-no-pass-fail]]). Rolling defect rates up across rules gives a
[[gls-dq-score|DQ score]], with all the caveats that carries.

### When Defect Rates Mislead

- **Changing universe over time** — "Last month 5%, this month 3%" might mean the universe shrank (more deletions), not improvement
- **Mixing base tables** — Rolling up across OptSels with different universes (some with deleted rows, some without)
- **Silent grain changes** — A DISTINCT or unnecessary join changes the opportunity count invisibly
- **Profiling masquerading as error** — "Distribution of values" is not a defect rate
