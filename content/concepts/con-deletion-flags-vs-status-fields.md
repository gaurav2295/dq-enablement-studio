---
id: con-deletion-flags-vs-status-fields
type: concept
title: Deletion Flags vs Status Fields
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: deprecated
links:
  - relates:std-ziserrorflag-convention
  - relates:std-sql-comment-standards
  - relates:prn-deletion-flags-belong-in-where
  - relates:ref-deletion-flag-resolver
  - relates:ref-sap-deletion-flags-vs-status-fields
  - relates:std-deletion-filter-marker
  - relates:con-view-types
  - relates:gls-deletion-flag
  - relates:gls-status-field
sources:
  - vault:dq-methodology/Deletion Flags vs Status Fields.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
---

## The distinction

A class of bug mixes WHERE-clause exclusions with CASE-driven error logic. Keeping them separate
is one of the most important habits in writing readable, correct DQ SQL.

| Field type | SAP examples | Belongs in | Role |
|---|---|---|---|
| **Deletion flag** | LVORM, LOEKZ, LOEVM | **WHERE** clause | Exclude deleted records from the universe |
| **Status field** | MMSTA, PSTAT, STATU, MARC.MMSTA, EBAN.STATU | **CASE** for `zIsErrorFlag` | Drive the error condition for "active / blocked / inactive" checks |

## The worked example

Rule: *"An inspection plan must reference an active material."*

Correct shape:

```sql
SELECT
    ...
    CASE
        /* Material is blocked or inactive at plant level — inspection plans
           must only reference materials with no MMSTA status restriction. */
        WHEN MARC.MMSTA IN ('01', '02', '03')  /* blocked / inactive codes */
            THEN 1
        ELSE 0
    END AS [zIsErrorFlag]
FROM PLKO
INNER JOIN MARA ON PLKO.MATNR = MARA.MATNR
INNER JOIN MARC ON MARA.MATNR = MARC.MATNR AND PLKO.WERKS = MARC.WERKS
WHERE
    /* Exclude inspection plans flagged for deletion */
    PLKO.LOEKZ <> 'X'
    /* Exclude materials flagged for deletion */
    AND MARA.LVORM <> 'X'
    /* Limit to Quality Inspection plan type */
    AND PLKO.PLNTY = 'Q'
```

> [!warning]
> Wrong — duplicates the deletion check in both places:
> ```sql
> WHERE
>     PLKO.LOEKZ <> 'X'
>     AND MARA.LVORM <> 'X'
>     ...
> SELECT
>     CASE
>         WHEN MARA.LVORM = 'X'         /* dead code — WHERE already excluded */
>             OR MARC.MMSTA IN ('01','02','03')
>             THEN 1 ELSE 0
>     END AS [zIsErrorFlag]
> ```
> The `MARA.LVORM = 'X'` branch can never fire — the WHERE already removed those rows. The CASE
> clause reads as if deletion drives the error, but it doesn't — only MMSTA does. Future
> maintainers reading this rule get confused about what's actually being checked.

## The pattern

When designing a rule:

1. **Scope first** — what's the universe of records this rule applies to? → WHERE clauses.
2. **Defect detection second** — given the in-scope records, what's the failure condition? →
   CASE in `zIsErrorFlag`.
3. **No overlap** — a check belongs in *one* of the two, never both.

## SAP deletion flag reference

| Field | Where it lives | Typical value meaning |
|---|---|---|
| **LVORM** | MARA, KNA1, LFA1, T001 (master data) | `'X'` = flagged for deletion |
| **LOEKZ** | EKKO, EKPO, PLKO (transactional headers + items) | `'X'` = flagged for deletion |
| **LOEVM** | KNB1, KNVV (extension tables for customer/vendor) | `'X'` = flagged for deletion |

The Studio's deletion-flag resolver knows which deletion flag applies to which table from the
table-metadata knowledge base — see [[ref-deletion-flag-resolver]] for the 3-tier resolution
algorithm and [[ref-sap-deletion-flags-vs-status-fields]] for the full per-table registry.

## SAP status field reference

| Field | Table | Meaning |
|---|---|---|
| **MMSTA** | MARC | Material status at plant level — blocked, inactive |
| **MSTAE** | MARA | Cross-plant material status |
| **PSTAT** | KNA1 | Account group active/blocked |
| **STATU** | EBAN, EKPO | Document status |
| **GBSTA** | VBUK, VBUP | Goods movement status |

Status codes are tenant-configurable — see the SAP customising for the exact code set in use.

## Related

See [[prn-deletion-flags-belong-in-where]] for the rationale behind why deletion exclusions must
live in WHERE, and [[std-ziserrorflag-convention]] / [[std-sql-comment-standards]] for the
adjacent SQL conventions this pattern depends on. See [[std-deletion-filter-marker]] for the
toggleable marker block that wraps these WHERE exclusions in a generated view, and
[[con-view-types]] for how OptSel/RptSel carry the resulting `zIsErrorFlag`.
