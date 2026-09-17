---
id: std-cte-rules
type: standard
title: CTE Rules
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - academy:landing.html#ctes
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:std-sql-performance-standards
  - relates:std-optsel-select-structure
  - relates:std-sql-comment-standards
  - relates:prn-optsel-is-the-universe
  - relates:gls-cte
---

## What it is

A CTE (the `WITH ... AS (...)` block at the top of a query) lets you name an intermediate result
and reuse it later in the same query. In DQ rules, CTEs are the standard way to pre-aggregate or
pre-filter a related table before joining it to the main table.

"Use CTEs whenever possible" and "build reusable CTE structures for complex validations" are
requirements 1 and 5 of [[std-sql-performance-standards|SQL Performance Standards]]; this unit is
the mechanics of satisfying them.

## When to use a CTE

- Pre-aggregating a child table before joining it to the master (e.g., counting sales orders per
  material)
- The rule needs to check a related table's status, and the join chain is easier to read as a
  separate step
- A multi-table check is clearer broken into named steps rather than one deeply nested query

## The CTE rules (all are mandatory)

1. **Every CTE must be used.** If you define a CTE, it must be joined or selected from in the
   outer query. An unused CTE doesn't just add clutter — some engines will error on it, and it
   always signals unfinished logic.

2. **Every CTE must output `zSourceSystemID`.** Select it explicitly from the base table inside
   the CTE, even if nothing else in the CTE needs it — the outer query needs it to join safely.

3. **Every CTE must filter on `zSourceSystemID` internally.** Inside the CTE's own `WHERE`,
   reference the main table's system ID so the CTE never mixes data from two source systems
   before it's even joined.

4. **Every join to a CTE must include a `zSourceSystemID` equality** alongside the natural key
   columns — the same rule that applies to joining two base tables applies to joining a CTE.

5. **The CTE is an implementation detail, not a shape change.** The view's outer `SELECT` must
   still expose the five field sections in order (Technical → Basic → Org → Value → Activity).
   Using a CTE internally never changes what the view looks like from the outside.

> [!warning]
> An unused CTE is never acceptable — it is a dangling CTE and a sign of unfinished logic that
> must be fixed before the rule ships.

> [!warning] Never hardcode zSourceSystemID
> The system ID must always be a column reference from the table, never a string literal or template token in the view itself. 
> 
> ✅ **CORRECT:**
> ```sql
> SELECT vbap.zSourceSystemID, ...
> WHERE vbap.zSourceSystemID = 'Z01'
> ```
>
> ❌ **WRONG:**
> ```sql
> SELECT 'Z01' AS zSourceSystemID, ...
> WHERE '1' = '1'  -- hardcoded system ID
> ```
>
> Hardcoding prevents the rule from working across systems, breaks the multi-implementation model, and makes the rule unmigrable. Always use the live column from the base table.

## Worked example: pre-aggregating a child table

**Scenario:** Flag materials that have zero sales orders — the rule needs a count from a child
table (VBAP, sales order items) before it can decide.

```sql
-- ============================================================
-- DQ Rule: Material must have at least one sales order line
-- Rule ID: MM-0042
-- View:    Opportunity View (OptSel)
-- Generated: 2026-08-18
-- Target: MS SQL Server
-- ============================================================
WITH order_summary AS (
  -- Count sales order lines per material, scoped to the same source system
  SELECT
    vbap.zSourceSystemID,
    vbap.MATNR,
    COUNT(*) AS order_line_count
  FROM vbap  -- Sales order item table
  WHERE vbap.zSourceSystemID = 'Z01'  -- CTE-level system filter (mandatory)
  GROUP BY vbap.zSourceSystemID, vbap.MATNR
)
SELECT
  -- Syniti Technical Fields
  mara.zSourceSystemID,
  CONCAT(mara.zSourceSystemID, '_', mara.MATNR) AS zConcatenatedKey,
  CASE
    WHEN order_summary.MATNR IS NULL THEN 1  -- No sales order lines found = error
    ELSE 0
  END AS zIsErrorFlag,
  -- Basic Fields
  mara.MATNR,
  mara.MAKTX,
  -- Activity Context
  mara.ERSDA
FROM mara
LEFT JOIN order_summary
  ON mara.zSourceSystemID = order_summary.zSourceSystemID  -- CTE join carries zSourceSystemID
  AND mara.MATNR = order_summary.MATNR
WHERE mara.zSourceSystemID = 'Z01'  -- Main table system filter (mandatory)
  AND mara.LVORM = ''  -- Exclude materials marked for deletion
```

Notice: the CTE (`order_summary`) is used in the outer join, filters on `zSourceSystemID`
internally, and outputs `zSourceSystemID` so the outer join can match it safely. The outer query
still shows Technical Fields first, then Basic, then Activity Context — the CTE never changed
that shape.

## Questions from consultants

- [[qa-why-ctes-preferred-over-subqueries|Why are CTEs preferred over subqueries?]]
- [[qa-main-table-system-id|What is the main table's system ID in a CTE?]]
- [[qa-when-additional-cte-acceptable|When is it acceptable to add an additional CTE?]]
