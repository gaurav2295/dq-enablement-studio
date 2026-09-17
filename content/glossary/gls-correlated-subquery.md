---
id: gls-correlated-subquery
type: glossary
title: Correlated Subquery
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-rule-pattern-library
  - relates:std-sql-performance-standards
  - relates:gls-rule-pattern
  - relates:gls-composite-key
  - relates:gls-cte
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [sql, structure]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A subquery whose `WHERE` references the outer row — an `EXISTS`, `NOT EXISTS` or `COUNT` evaluated
*per record of the universe*. It is what a rule needs when the defect is defined by rows in
another table, not by the row's own fields.

## Example: Parent Existence Check

Check whether each customer in the customer master (`KNA1`) has at least one corresponding sales view (`KNVV`). This is a correlated subquery:

```sql
WITH customer_main_system AS (
  SELECT CustomerID, CompanyCode, zSourceSystemID
  FROM KNA1_Stage
  WHERE zSourceSystemID = 'SAP'
)

SELECT
  CustomerID,
  CompanyCode,
  zSourceSystemID,
  -- Does this customer have ANY sales view for this company?
  CASE
    WHEN EXISTS (
      SELECT 1
      FROM KNVV_Stage AS knvv
      WHERE knvv.CustomerID = cust.CustomerID
        AND knvv.CompanyCode = cust.CompanyCode
        AND knvv.zSourceSystemID = cust.zSourceSystemID  -- Full key!
    ) THEN 0
    ELSE 1
  END AS zIsErrorFlag
FROM customer_main_system AS cust;
```

Notice: The `WHERE` inside the `EXISTS` references the **outer row** (`cust.CustomerID`, `cust.CompanyCode`, `cust.zSourceSystemID`) — that is the correlation.

## Usage Patterns

Three of the four [[gls-rule-pattern|rule patterns]] are correlated-subquery shapes:
- **Parent node exists** — Does a related row exist?
- **Enough related rows exist** — COUNT check on related rows
- **Org children agree with central** — Cross-system alignment check

## Two Critical Rules

- **Correlate on the full key**, including [[gls-zsourcesystemid|zSourceSystemID]] — a subquery
  that omits it silently reaches into another system's data.
- Prefer `EXISTS` over `COUNT(*) > 0`, and do not nest a correlated subquery inside a
  correlated subquery — see [[std-sql-performance-standards]].
