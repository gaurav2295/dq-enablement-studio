---
id: gls-cte
type: glossary
title: CTE (Common Table Expression)
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-cte-rules
  - relates:std-sql-performance-standards
  - relates:gls-correlated-subquery
  - relates:gls-zsourcesystemid
sources:
  - academy:landing.html#ctes
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [sql, structure]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A `WITH`-clause named subquery used to stage an intermediate result before the main `SELECT`.
In Syniti DQ SQL a CTE is a readability and correctness device — a way to name a population once
and reuse it — not a performance trick.

## Why CTEs Over Subqueries?

- **Readability** — A CTE names its population explicitly. A reviewer sees `WITH mara_open_orders AS (...) SELECT ... FROM mara_open_orders`
  and immediately knows what population is under test.
- **Correctness** — A named CTE is a contract. Every reference to that population uses the same definition; subqueries invite copy-paste drift.
- **Join safety** — A CTE that filters on [[gls-zsourcesystemid|zSourceSystemID]] upfront prevents accidental cross-system joins where a nested subquery might silently expand scope.
- **Testing and audit** — A rule auditor can isolate the CTE and run it standalone to verify the population. Subqueries bury population logic inside the main query.

For detail, see [[qa-why-ctes-preferred-over-subqueries]].

## Example

```sql
-- CTE approach: clear, named, testable
WITH customer_main_system AS (
  SELECT
    CustomerID,
    CustomerName,
    SAP_CreatedDate,
    zSourceSystemID
  FROM Customers_Stage
  WHERE zSourceSystemID = 'SAP'
)

SELECT
  CustomerID,
  CustomerName,
  SAP_CreatedDate,
  CASE
    WHEN SAP_CreatedDate IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM customer_main_system;
```

Contrast with inline subquery: same logic, but the population definition is buried and reused repeatedly without naming.

## Usage Rules

The standing rules are in [[std-cte-rules]]; the two most-missed:

- **Every CTE filters on [[gls-zsourcesystemid|zSourceSystemID]]** in the same way the main table
  does. A CTE that forgets it silently joins across systems.
- **A CTE is not a place to hide rule logic.** The `zIsErrorFlag` `CASE` stays in the OptSel
  `SELECT` where a reviewer expects to find it.

`CTE` is also a known noise token in table extraction — the rule repository filters it out of
`tables[]` so a catalogue entry never asserts `CTE` as a source table.
