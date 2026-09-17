---
id: qa-deletion-flags-multiple-tables
type: qa
title: When a rule joins multiple tables, which deletion flags belong in WHERE vs CASE?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

When a rule joins MARA + MARC + MVKE, each table has its own deletion flag (LVORM, LOEKZ, etc.). 
How do you decide which flags go in the WHERE clause (universe definition) and which, if any, 
go in the CASE (error logic)?

## Answer

**Rule: All deletion flags belong in WHERE. Never in CASE (unless deletion is the error being detected).**

### Standard scenario: Multi-table join

```sql
WHERE
    MARA.zSourceSystemID = 'SAP'  -- System scope
    AND MARA.LVORM <> 'X'         -- Materials not deleted
    AND MVKE.MANDT = MARA.MANDT   -- Join condition
    AND MVKE.LOEKZ <> 'X'         -- Sales data not deleted
    AND MARC.LOEKZ <> 'X'         -- Plant data not deleted
CASE
    WHEN MARA.MMSTA NOT IN ('01','02','03') THEN 1  -- Error: bad status
    ELSE 0
END AS [zIsErrorFlag]
```

**All three deletion flags (LVORM, LOEKZ, LOEKZ) in WHERE** — universe is "active records across all three tables."

**Error condition in CASE** — check status, not deletion.

### Exception: Deletion is the error being detected

If your rule's purpose IS to find deleted records that shouldn't be:

> *"Find materials referenced by active sales orders that are marked for deletion (LVORM = 'X')"*

Then deletion is the **error condition**, not a universe filter:

```sql
WHERE
    MARA.zSourceSystemID = 'SAP'
    AND MARA.LVORM <> 'X'  -- Only active materials (universe scope)
    AND MVKE.LOEKZ <> 'X'  -- Only active sales data (universe scope)
    AND MARC.LOEKZ <> 'X'  -- Only active plant data (universe scope)
CASE
    WHEN MARA.LVORM = 'X' THEN 1  -- Error: referenced material is flagged for deletion
    ELSE 0
END AS [zIsErrorFlag]
```

Wait — this is contradictory. You can't exclude `LVORM = 'X'` in WHERE and then check for it in CASE.

**Better approach:** Remove LVORM from WHERE if it's your error:

```sql
WHERE
    MARA.zSourceSystemID = 'SAP'
    AND MVKE.LOEKZ <> 'X'         -- Sales data active
    AND MARC.LOEKZ <> 'X'         -- Plant data active
CASE
    WHEN MARA.LVORM = 'X' THEN 1  -- Error: material is deleted
    ELSE 0
END AS [zIsErrorFlag]
```

Now: universe = "all materials (including deleted) that are in active sales & plant data," 
and the error flag catches deleted ones.

### Multi-table deletion flag checklist

For each table in the join:

1. **What's its deletion flag?** (LVORM for MARA? LOEKZ for MVKE?)
2. **Should this table be in the universe?** (Is a deleted record even relevant?)
3. **If yes:** Add the deletion flag to WHERE (exclude deleted from universe)
4. **If no:** Omit the flag from WHERE (let deletion records flow through; don't error on them)

> [!tip]
> The rule: "deleted records are not in the universe" applies per table. 
> For MARA, exclude LVORM. For MVKE, exclude LOEKZ. Never check them in CASE unless 
> deletion itself is the error condition.
