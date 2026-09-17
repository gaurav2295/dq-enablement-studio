---
id: qa-consolidated-staging-table
type: qa
title: What is a consolidated staging table?
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-zsourcesystemid-convention
  - relates:con-multi-implementation-model
---

## Question

What is a 'consolidated staging table'?

## Answer

A **working database table that contains data from multiple source systems**, unified with a common structure.

In a typical DQ architecture:

```
Source Systems (MARA_Z01, MARA_Z02, MARA_Z06)
        ↓
ETL extracts and standardizes each
        ↓
WRKDQPREP_ALL (consolidated staging)
        ↓
zSourceSystemID column identifies which system each row came from
```

The consolidation means:
- All materials from all systems (Z01, Z02, Z06) are in **one table** (e.g., `[WRKDQPREP_ALL].[dbo].[MARA]`)
- **Not** separate tables per system (no `MARA_Z01`, `MARA_Z02`, `MARA_Z06`)
- The `zSourceSystemID` column tells you which system row came from: `Z01`, `Z02`, or `Z06`

This consolidation is **why** zSourceSystemID is so critical — without it, you'd need separate rule logic per system. With it, one rule (with per-system filter) works across all systems.

## Related

- [[std-zsourcesystemid-convention|zSourceSystemID Convention]]
- [[con-multi-implementation-model|Multi-Implementation Model]]
