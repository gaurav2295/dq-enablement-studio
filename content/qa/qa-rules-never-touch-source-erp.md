---
id: qa-rules-never-touch-source-erp
type: qa
title: What does "Rules never touch the source ERP system" mean?
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-sql-comment-standards
---

## Question

Could we elaborate on the statement "Rules never touch the source ERP system"?

## Answer

DQ rules are **read-only views into the working database**, never the live SAP systems (PRD, QA, DEV).

Architecture:

```
SAP Source Systems (SRCECC, SRCS4, etc.)
        ↓
ETL / Replication
        ↓
Working Database [WRKDQ] ← DQ rules read FROM here only
        ↓
SKP (reporting)
```

**Why this rule exists:**

1. **Safety** — you can't accidentally modify SAP data while developing a rule
2. **Isolation** — rule SQL failures don't lock SAP tables or block business processes
3. **Performance** — staging tables are optimized for analysis; live tables are optimized for transactions
4. **Auditability** — all rule reads are logged; live SAP reads would pollute transaction logs

**What "never touch" means:**

❌ **WRONG:**
```sql
FROM [SRCECC].[dbo].[MARA]  -- reading directly from source
FROM [SAP_PROD].[dbo].[KNA1]  -- live SAP database
```

✅ **CORRECT:**
```sql
FROM [WRKDQ].[dbo].[MARA]  -- consolidated staging table
```

The **three-part qualified name always starts with `[WRKDQ]`** — the working database. If you see any view reading from `SRCECC` or a live SAP database in a DQ rule, that is a critical defect.

This is enforced by [[std-sql-comment-standards|SQL Comment Standards]] validation: any three-part name not starting with `[WRKDQ]` fails the build.

## Related

- [[std-sql-comment-standards|SQL Comment Standards]]
