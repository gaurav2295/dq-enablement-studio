---
id: qa-catalog-promotion-injection-edge-cases
type: qa
title: What other SQL patterns broke with the injection approach?
domain: studio
audience: [developer]
level: advanced
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

The principle explains why injection failed for aggregate predicates in HAVING clauses. 
But are there other catalog SQL patterns that broke with injection, beyond aggregates?

## Answer

**Yes. Three other patterns failed with injection:**

### 1. Window functions in subqueries

**Pattern:**
```sql
SELECT 
    MATNR,
    ROW_NUMBER() OVER (PARTITION BY PLANT ORDER BY MATNR) AS rn
FROM MARA
WHERE rn = 1  -- Window function reference
```

**Why injection broke:**
- Injection forced a reformat that moved the `ROW_NUMBER()` out of its OVER context
- Window functions must stay inside subqueries where their PARTITION BY/ORDER BY are in scope
- Reformatting broke the syntax: `rn = 1` couldn't find the aliased column

**Wrapping solution preserves the window function's scope.**

### 2. CTEs (Common Table Expressions) with multiple branches

**Pattern:**
```sql
WITH plant_costs AS (
    SELECT PLANT, SUM(COST) AS total_cost FROM MARC GROUP BY PLANT
),
active_plants AS (
    SELECT PLANT FROM MARA WHERE MMSTA = '01'
)
SELECT m.MATNR, p.PLANT, pc.total_cost
FROM MARA m
JOIN plant_costs pc ON m.PLANT = pc.PLANT
JOIN active_plants ap ON m.PLANT = ap.PLANT
```

**Why injection broke:**
- Injection stripped or moved the CTEs, leaving the main SELECT referencing undefined table aliases
- CTEs are lexically scoped; moving them without the main query breaks resolution

**Wrapping solution keeps CTEs inside the derived table.**

### 3. Scalar subqueries in the SELECT list

**Pattern:**
```sql
SELECT
    MATNR,
    (SELECT MAX(PRICE) FROM MVKE WHERE MVKE.MATNR = MARA.MATNR) AS max_price
FROM MARA
```

**Why injection broke:**
- Injection moved the scalar subquery out of its correlated context
- The subquery lost the outer query's table alias reference (MARA is no longer in scope)
- Result: "MARA.MATNR not found" error

**Wrapping solution preserves the correlation.**

### The common thread

All three patterns have **lexical scope dependencies** — the nested construct needs 
to stay in its original context (OVER clause, CTE scope, correlation scope). 

**Injection violated this:** it extracted parts and reformatted them, breaking the scopes.

**Wrapping respects this:** the entire catalog SQL stays inside the derived table, 
keeping all scopes intact.

### Lesson for custom rules

When authoring local rules with complex SQL:

- Prefer derived tables (`FROM (<complex> ) AS src`) over inserting tech fields 
  into the main SELECT
- Keep aggregates, window functions, CTEs, and scalar subqueries inside the derived table
- Add tech fields only in the outer SELECT where scopes are flat

> [!important]
> Complex SQL patterns have lexical scope requirements. Reformatting breaks them. 
> Wrapping preserves them. This is why the wrapper approach is mechanical and safe; 
> injection is generative and fragile.
