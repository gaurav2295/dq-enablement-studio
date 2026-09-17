---
id: qa-main-table-system-id
type: qa
title: What is the main table's system ID in a CTE?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-cte-rules
  - relates:std-zsourcesystemid-convention
---

## Question

What is meant by 'the main table's system ID'? Does this refer to the source system of the table being queried inside the CTE? or the table that the CTE is ultimately joined to?

## Answer

It refers to **the primary table the rule is checking**, not the table inside the CTE.

Example: In a rule checking materials (MARA), the main table is MARA. If the rule has a CTE joining to sales orders (VBAP), the CTE must:
1. **Filter internally** on `VBAP.zSourceSystemID` (the table inside the CTE)
2. **BUT output** `VBAP.zSourceSystemID` for the join
3. **AND the outer query filters** on `MARA.zSourceSystemID` (the main table)

```sql
WITH order_summary AS (
  SELECT
    vbap.zSourceSystemID,  -- Output the CTE's source system
    vbap.MATNR,
    COUNT(*) AS order_count
  FROM vbap
  WHERE vbap.zSourceSystemID = 'Z01'  -- Filter the CTE internally
  GROUP BY vbap.zSourceSystemID, vbap.MATNR
)
SELECT
  mara.MATNR,
  CASE WHEN order_summary.MATNR IS NULL THEN 1 ELSE 0 END AS zIsErrorFlag
FROM mara
LEFT JOIN order_summary
  ON mara.zSourceSystemID = order_summary.zSourceSystemID  -- Join includes system match
  AND mara.MATNR = order_summary.MATNR
WHERE mara.zSourceSystemID = 'Z01'  -- Main table filter
```

The **main table's system ID** = MARA's zSourceSystemID. The CTE outputs and filters on its own table's system ID (VBAP's). Both must match in the JOIN for safety.

## Related

- [[std-cte-rules|CTE Rules]]
- [[std-zsourcesystemid-convention|zSourceSystemID Convention]]
