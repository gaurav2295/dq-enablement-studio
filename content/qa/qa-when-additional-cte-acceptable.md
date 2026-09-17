---
id: qa-when-additional-cte-acceptable
type: qa
title: Are there situations where adding an additional CTE is acceptable or even preferred?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: approved
sources:
  - coe:std-cte-rules
created: 2026-09-02
updated: 2026-09-02
links:
  - parent:prc-derive-a-dq-rule
  - relates:std-cte-rules
  - relates:gls-cte
  - relates:std-sql-performance-standards
---

## Question

Are there any situations where adding an additional CTE is considered acceptable or even preferred?

## Answer

**Yes — CTEs are not only acceptable, they are the standard approach** for several common scenarios in DQ rules.

### When to Use CTEs (Mandatory Situations)

See [[std-cte-rules|CTE Rules]] for the full standard. Add a CTE when:

1. **Pre-aggregating a child table before joining to the master**
   - Example: Count sales orders per material, then join back to MARA so the material record isn't fanned out to multiple rows
   - **Why:** Without the CTE, a simple join to VBAP (sales order items) would create one result row per sales order, multiplying your error flags

2. **The rule needs to check a related table's status, and the join chain is easier to read as a separate step**
   - Example: Get the most recent approval date per material from an approval history table, then use that in the CASE logic
   - **Why:** Breaking out the aggregation as a named CTE makes the main SELECT clearer and more auditable

3. **A multi-table check is clearer broken into named steps rather than one deeply nested query**
   - Example: Three separate CTEs for goods movements, sales orders, and purchase orders (to check "has material had any activity?")
   - **Why:** Each CTE documents a distinct signal; the main SELECT combines them with clear logic

4. **You need to pre-filter a lookup table on zSourceSystemID before joining**
   - Example: Deduplicate a master table by (system, key) before joining, so you don't get matches from wrong systems
   - **Why:** Cross-system safety — [[std-cte-rules|CTE Rules]] require every CTE to filter on zSourceSystemID internally

### The CTE Rules (All Mandatory)

Once you add a CTE, these rules must be satisfied:

| Rule | Why |
|------|-----|
| **Every CTE must be used** | An unused CTE is unfinished logic and must be removed before the rule ships |
| **Every CTE must output zSourceSystemID** | The outer query needs it to join safely across systems |
| **Every CTE must filter on zSourceSystemID internally** | The CTE never mixes data from two source systems before joining |
| **Every join to a CTE must include zSourceSystemID equality** | Same rule as joining two base tables — system alignment is mandatory |
| **The CTE is implementation detail, not shape change** | The view's outer SELECT still exposes five field sections (Technical → Basic → Org → Value → Activity) |

### Example: Multi-Signal Activity Check

The Material Activity rule uses **three CTEs** to pre-aggregate three independent signals (goods movements, sales orders, purchase orders):

```sql
WITH cte_material_movements AS (
  SELECT MATNR, zSourceSystemID, MAX(BUDAT_MKPF) AS last_movement_date
  FROM MSEG
  WHERE zSourceSystemID = 'Z01'  -- CTE-level system filter
  GROUP BY MATNR, zSourceSystemID
),

cte_sales_orders AS (
  SELECT MATNR, zSourceSystemID, MAX(ERDAT) AS last_sales_date
  FROM VBAP
  WHERE zSourceSystemID = 'Z01'  -- CTE-level system filter
  GROUP BY MATNR, zSourceSystemID
),

cte_purchase_orders AS (
  SELECT MATNR, zSourceSystemID, MAX(BEDAT) AS last_po_date
  FROM EKPO
  WHERE zSourceSystemID = 'Z01'  -- CTE-level system filter
  GROUP BY MATNR, zSourceSystemID
)

SELECT
  mara.MATNR,
  CASE
    WHEN GREATEST(mov.last_movement_date, so.last_sales_date, po.last_po_date) < DATEADD(YEAR, -2, GETDATE())
    THEN 1
    ELSE 0
  END AS [zIsErrorFlag],
  ...
FROM mara
LEFT JOIN cte_material_movements AS mov
  ON mov.zSourceSystemID = mara.zSourceSystemID AND mov.MATNR = mara.MATNR
LEFT JOIN cte_sales_orders AS so
  ON so.zSourceSystemID = mara.zSourceSystemID AND so.MATNR = mara.MATNR
LEFT JOIN cte_purchase_orders AS po
  ON po.zSourceSystemID = mara.zSourceSystemID AND po.MATNR = mara.MATNR
```

**Why three CTEs here?**
- Each CTE pre-aggregates one activity signal independently
- The main query combines all three with GREATEST to find the most recent activity
- Without CTEs, you'd either fan-out the material record to multiple rows, or write a deeply nested subquery

### When NOT to Add Extra CTEs (Anti-Patterns)

- **If a simple LEFT JOIN works** — don't add a CTE just to simplify the join; keep it simple
- **If you can inline the logic in the CASE** — brevity is fine if it's still readable
- **If you're just aliasing a table** — that's not a CTE's job
- **Hiding rule logic inside a CTE** — the error condition belongs in the outer SELECT's CASE, not buried inside a CTE's WHERE
- **Over-CTEing (5+ CTEs)** — if you need this many named steps, consider whether the rule is trying to do too much; a JOIN chain may be clearer, or the rule may need splitting into two rules
- **Redundant CTEs** — the same filter applied twice in different CTEs is a sign of copy-paste rather than deliberate design; consolidate

### The Bottom Line

CTEs are the **standard approach** in DQ rules. Use them liberally when pre-aggregating, pre-filtering on system, or breaking complex multi-table logic into named steps. Just follow the 5 mandatory rules, and you're good.

---

### Related

- [[std-cte-rules|CTE Rules]]
- [[prc-derive-a-dq-rule|Derive a DQ Rule (single rule)]]
- [[prn-optsel-is-the-universe|OptSel Is the Universe, RptSel Is the Wrapper]]
