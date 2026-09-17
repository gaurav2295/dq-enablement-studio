---
id: qa-ziserrorflag-aggregate-rules
type: qa
title: How should aggregate/GROUP BY rules derive zIsErrorFlag?
domain: sql-standards
audience: [developer]
level: advanced
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

For aggregate or GROUP BY rules, the error condition is evaluated at the grouped level 
(e.g., "COUNT(DISTINCT col) > 1"), not at the row level. How should zIsErrorFlag be 
derived in this case?

## Answer

**Option 1: Emit the aggregate as a column, then flag rows in the outer SELECT (cleanest)**

```sql
CREATE VIEW OptSel AS
SELECT
    src.zSourceSystemID,
    CONCAT(...) AS [zConcatenatedKey],
    CASE WHEN src.duplicate_count > 1 THEN 1 ELSE 0 END AS [zIsErrorFlag],
    src.MATNR,
    src.PLANT,
    src.duplicate_count
FROM (
    SELECT
        MATNR, PLANT, zSourceSystemID,
        COUNT(DISTINCT WERKS) AS duplicate_count
    FROM MARA
    GROUP BY MATNR, PLANT, zSourceSystemID
) AS src
```

**Why this works:**
- The aggregate (duplicate_count) lives inside the derived table's GROUP BY
- The outer SELECT sees it as a simple column (not an aggregate function)
- The CASE can reference it cleanly
- Each grouped row gets flagged independently

### Option 2: Fallback to literal-1 (when no distinguishing column exists)

If the error condition uses an aggregate function directly (e.g., `SUM(amount) < threshold`) 
and you can't extract a clean column, use literal-1:

```sql
CASE WHEN 1 = 1 THEN 1 ELSE 0 END AS [zIsErrorFlag]  /* TODO: aggregate at group level */
```

**Mark as TODO** — the DBA will decide if literal-1 is correct or if the rule should be redesigned.

### Option 3: Explode the group into rows (least clean, avoid if possible)

```sql
CASE WHEN RNUM = 1 AND duplicate_count > 1 THEN 1 ELSE 0 END AS [zIsErrorFlag]
```

Joins back a row-numbering query to flag only the first row per group. This is complex and 
should be avoided — use Option 1 instead.

### Pattern: The derived table is your friend

**The key insight:** Aggregate queries become simpler when the GROUP BY logic stays inside 
a derived table and the outer SELECT only references the grouped columns (not aggregate functions).

This is why [[prn-catalog-promotion-wraps-instead-of-injecting]] uses derived tables:
- Catalog SQL (with aggregates) stays inside the FROM subquery
- Outer SELECT references only the aggregate columns
- Tech fields are added cleanly in the outer SELECT

### Checklist for aggregate rules

- [ ] Does the rule have a GROUP BY?
- [ ] Is the error condition expressed as an aggregate function (COUNT, SUM, etc.)?
- [ ] If yes, can you convert it to a grouped column (Option 1)?
- [ ] If no, does literal-1 (Option 2) make sense for this rule's intent?
- [ ] If unsure, use literal-1 and mark TODO for the DBA to decide

> [!important]
> Aggregate rules are the exception where zIsErrorFlag logic is complex. 
> Always prefer Option 1 (derived table with aggregate as column) when possible.
