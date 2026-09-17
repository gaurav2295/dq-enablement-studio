---
id: std-sql-performance-standards
type: standard
title: SQL Performance Standards
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [methodology, convention, sql, performance, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:std-cte-rules
  - relates:std-optsel-select-structure
  - relates:std-zconcatenatedkey-convention
  - implements:prn-optsel-is-the-universe
  - relates:con-view-types
---

## What it is

Seven performance requirements every DQ rule's SQL must meet. They are part of the DQ Rule
Standards, not optional tuning advice — a rule that violates them is not finished, however
correct its logic.

The context these run in is unforgiving: an OptSel is the **whole population** of a master-data
object across every in-scope system, refreshed on the engagement's DQ cadence, and a RptSel plus a
dashboard sit on top of it. A rule that is merely slow in a sandbox becomes a rule that misses the
refresh window in production.

## The seven requirements

| # | Requirement | Why |
|---|---|---|
| 1 | **Use CTEs whenever possible** | A named `WITH` block is optimised once and read many times; it also keeps the rule readable, which is the other half of the standard |
| 2 | **Avoid unnecessary nested queries** | Nested scalar subqueries in the SELECT list re-execute per row; a CTE plus a join does the same work set-based |
| 3 | **Select only required columns** | Every column is carried through the OptSel into the RptSel into the dashboard extract — a `SELECT *` on a wide SAP table multiplies that cost at every layer |
| 4 | **Avoid `SELECT DISTINCT` unless necessary** | `DISTINCT` usually hides a fan-out join that should have been fixed at the join, and it forces a sort over the full population |
| 5 | **Build reusable CTE structures for complex validations** | Multi-step checks (aggregate, then compare, then flag) read and tune far better as named steps than as one nested expression |
| 6 | **Ensure `zConcatenatedKey` remains unique** | A duplicated key collapses two opportunities into one in ADM — a correctness failure that surfaces as a performance smell (row counts that do not reconcile) |
| 7 | **Ensure Report Views depend only on Opportunity Views** | A RptSel that re-reads source tables doubles the source scan and can drift out of step with its OptSel |

## SELECT DISTINCT is a symptom, not a fix

The most common way a DQ rule ends up slow is a one-to-many join — say `MARA` to `MARC` — where
the author wanted "materials that have any plant with a problem" and got one row per plant. Adding
`DISTINCT` makes the row count look right and makes the query sort the entire population.

```sql
-- Symptom: DISTINCT papering over a fan-out
SELECT DISTINCT
    MARA.MATNR AS [Material Number],
    ...
FROM MARA
INNER JOIN MARC ON MARC.MATNR = MARA.MATNR
```

```sql
-- Fix: aggregate the child in a CTE, keep the grain at one row per material
WITH PlantIssues AS (
    /* One row per material: does it have any plant with the defect? */
    SELECT
        MARC.MATNR,
        MAX(CASE WHEN MARC.MMSTA IN ('01','02','03') THEN 1 ELSE 0 END) AS HasBlockedPlant
    FROM MARC AS MARC
    GROUP BY MARC.MATNR
)
SELECT
    MARA.MATNR AS [Material Number],
    ...
FROM MARA AS MARA
LEFT OUTER JOIN PlantIssues AS PI
    ON PI.MATNR = MARA.MATNR
    /* Pre-aggregated plant status — keeps the grain at one row per material */
```

The CTE version keeps `zConcatenatedKey` unique (requirement 6) as a side effect, because the
grain never fans out in the first place.

> [!tip] The uniqueness check that catches fan-out early
> Before shipping, run the OptSel and compare `COUNT(*)` against
> `COUNT(DISTINCT zConcatenatedKey)`. If they differ, a join has fanned out — fix the join, do not
> add `DISTINCT`.

## Where these standards get enforced

- The Studio flags a `SELECT DISTINCT` on an OptSel for review.
- The Studio also checks that requirement 7 is met — the Report View exists and wraps its
  Opportunity View.
- Requirements 1, 2, 3 and 5 are review-time judgements, not automated checks. They belong on the
  rule-review checklist.

Requirements 1 and 5 are the *what* and the *why*; the mechanics of writing a compliant CTE — every
CTE used, every CTE carrying and filtering on `zSourceSystemID`, every join to one carrying a system
equality — live in [[std-cte-rules|CTE Rules]].

## Related

- [[std-cte-rules|CTE Rules]] — how to write the CTEs requirements 1 and 5 ask for
- [[std-optsel-select-structure|OptSel SELECT Structure]]
- [[std-zconcatenatedkey-convention|zConcatenatedKey Convention]]
- [[prn-optsel-is-the-universe|OptSel Is the Universe, RptSel Is the Wrapper]]
- [[con-view-types|View Types — OptSel RptSel InfSel PrfSel PrfSum]]
