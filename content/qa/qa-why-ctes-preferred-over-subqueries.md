---
id: qa-why-ctes-preferred-over-subqueries
type: qa
title: Why are CTEs preferred over subqueries in DQ rules?
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
  - relates:prn-optsel-is-the-universe
---

## Question

Why are CTEs preferred over subqueries in the context of DQ rules?

## Answer

**Readability and maintainability**, not performance.

Subqueries nest logic inside the SELECT or WHERE, making complex validations hard to follow:

```sql
-- Subquery style (nested, hard to parse)
SELECT MARA.MATNR, 
       CASE WHEN MARA.MATNR NOT IN (
         SELECT VBAP.MATNR FROM VBAP 
         WHERE VBAP.zSourceSystemID = 'Z01' 
         GROUP BY VBAP.MATNR HAVING COUNT(*) > 0
       ) THEN 1 ELSE 0 END AS zIsErrorFlag
FROM MARA
WHERE MARA.zSourceSystemID = 'Z01'
```

CTEs lift the logic into named blocks at the top:

```sql
-- CTE style (named, sequential, auditable)
WITH order_summary AS (
  SELECT VBAP.MATNR, COUNT(*) AS order_count
  FROM VBAP
  WHERE VBAP.zSourceSystemID = 'Z01'
  GROUP BY VBAP.MATNR
)
SELECT MARA.MATNR,
       CASE WHEN order_summary.MATNR IS NULL THEN 1 ELSE 0 END AS zIsErrorFlag
FROM MARA
LEFT JOIN order_summary ON MARA.MATNR = order_summary.MATNR
WHERE MARA.zSourceSystemID = 'Z01'
```

**Why it matters for DQ:**
- A reviewer auditing 50 rules can scan the CTE structure in seconds
- The name (`order_summary`) explains the intermediate result — better than `SELECT ... FROM (SELECT ... FROM ...)`
- Studio's round-trip parser can read CTEs back into structured specs; deeply nested subqueries cannot

## Related

- [[std-cte-rules|CTE Rules]]
- [[prn-optsel-is-the-universe|Why OptSel Is the Universe and RptSel Is the Wrapper]]
