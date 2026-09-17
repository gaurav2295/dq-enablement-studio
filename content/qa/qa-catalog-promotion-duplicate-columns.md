---
id: qa-catalog-promotion-duplicate-columns
type: qa
title: What if the catalog SQL already has a zSourceSystemID column?
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

When promotion wraps catalog SQL as `FROM (<catalog>) AS src`, it adds tech fields in the outer 
SELECT (zSourceSystemID, zConcatenatedKey, zIsErrorFlag). But what if the catalog SQL *already* 
has a zSourceSystemID column? Won't that create a duplicate?

## Answer

**No duplicates. The promoter handles this explicitly.**

### The scenario

Some catalog rules include system-identifier logic in their own SQL:

```sql
-- Catalog SQL (already has zSourceSystemID)
SELECT
    MARA.MATNR,
    MARA.PLANT,
    MARA.zSourceSystemID,  -- Already present!
    COUNT(DISTINCT WERKS) AS plant_count
FROM MARA
GROUP BY MARA.MATNR, MARA.PLANT, MARA.zSourceSystemID
HAVING COUNT(DISTINCT WERKS) > 1
```

When wrapped naively, you'd get:

```sql
SELECT
    src.zSourceSystemID,      -- From wrapper (new)
    CONCAT(...) AS [zConcatenatedKey],
    CASE WHEN ... THEN 1 ELSE 0 END AS [zIsErrorFlag],
    src.MATNR,
    src.PLANT,
    src.zSourceSystemID      -- From catalog (duplicate!)
FROM (<catalog>) AS src
```

❌ Two `zSourceSystemID` columns = error.

### How the promoter prevents it

**The promoter enumerates columns, not `src.*`.** When it builds the column list, it:

1. **Scans the catalog SQL's SELECT list** — finds all columns the catalog returns
2. **Removes duplicates** — if zSourceSystemID, zConcatenatedKey, or zIsErrorFlag appear in the 
   catalog list, they're **excluded** from the enumeration
3. **Emits clean enumeration:**

```sql
SELECT
    src.zSourceSystemID AS [zSourceSystemID],      -- From wrapper (overrides catalog)
    CONCAT(src.MATNR, '|', src.PLANT, '|', src.zSourceSystemID) AS [zConcatenatedKey],
    CASE WHEN ... THEN 1 ELSE 0 END AS [zIsErrorFlag],
    src.MATNR,      -- From catalog (no duplicate)
    src.PLANT,      -- From catalog
    src.plant_count -- From catalog (the GROUP BY result)
FROM (<catalog>) AS src
```

✅ Clean: no duplicate columns, and the wrapper's zSourceSystemID is authoritative.

### Why this matters

The catalog may have computed a system identifier for its own aggregation logic. 
The wrapper *overrides* it with the engagement's canonical zSourceSystemID (which may differ 
if the rule is deployed to a different system code). This is **correct behavior** — the 
promotion is adapting catalog SQL to the deployment context, not preserving every column 
it returns.

### Column enumeration rule

**Never use `src.*` in the wrapper.** Always enumerate:

```sql
SELECT
    src.zSourceSystemID,     -- Add wrapper tech fields first
    CONCAT(...) AS [zConcatenatedKey],
    CASE WHEN ... THEN 1 ELSE 0 END AS [zIsErrorFlag],
    src.col1, src.col2, src.col3, ...  -- Then enumerate catalog columns
FROM (<catalog>) AS src
```

This ensures the tech fields are in the right position (first, per field-section standards) 
and duplicates are impossible.

> [!tip]
> The promoter is defensive: it scans for conflicts and builds the column list explicitly. 
> If you encounter a "duplicate column" error, it means the catalog SQL has one of the tech 
> field names in an unexpected place. Escalate to the catalog maintainer.
