---
id: prn-deletion-flags-belong-in-where
type: principle
title: Why Deletion Flags Belong in WHERE
domain: sql-standards
audience: [consultant]
level: practitioner
status: review
links:
  - relates:std-ziserrorflag-convention
  - relates:prn-optsel-is-the-universe
  - relates:prc-audit-rule-quality
  - relates:ref-deletion-flag-resolver
sources:
  - vault:thought-leadership/Why Deletion Flags Belong in WHERE.md
tags: [thought-leadership]
created: 2026-08-20
updated: 2026-08-20
---

A short defence of the rule documented in [[con-deletion-flags-vs-status-fields]] — why deletion
flags belong in the `WHERE` clause and never in the `zIsErrorFlag` `CASE`.

## The principle

A deleted record is **not in the universe** the rule applies to. It's been struck from the
active dataset. Including it in the `CASE` evaluation pretends it's still relevant, then
"discovers" it's deleted, then "reports" the deletion as a defect — three steps to say nothing
useful.

## What is an "active dataset"?

An **active dataset** is every record the engagement has decided is "in scope" for the rule. 
It is defined in the `WHERE` clause and typically includes three filters:

1. **System scope** — `zSourceSystemID = 'SAP'` (which ERP instance)
2. **Deletion flags** — `LVORM <> 'X'` (not marked for deletion in the table)
3. **Status/lifecycle filters** — sometimes; depends on the rule's intent

Examples:

**Materials rule: Only active, non-deleted materials**

```sql
WHERE zSourceSystemID = 'SAP'
  AND LVORM <> 'X'          -- not deleted
  AND MTART NOT IN ('TEST') -- not test type
```

**GL rule: Only posted, non-reversed GL lines**

```sql
WHERE zSourceSystemID = 'SAP'
  AND BSTAT NOT IN ('X')    -- not reversed
  AND BUKRS = '1000'        -- company code scope
```

**The rule:** Once you define "active," apply all those filters in the `WHERE`. 
The `CASE` then checks the error condition against only the active records.

The clean shape:

```sql
WHERE LVORM <> 'X'                    -- universe definition: active records
SELECT
    CASE WHEN MMSTA IN ('01','02','03') THEN 1 ELSE 0 END AS zIsErrorFlag
```

The bad shape:

```sql
WHERE 1=1                             -- universe: everything, including deleted
SELECT
    CASE
        WHEN LVORM = 'X' THEN 1       -- "deletion is an error" -- but is it?
        WHEN MMSTA IN ('01','02','03') THEN 1
        ELSE 0
    END AS zIsErrorFlag
```

## Why someone writes the bad shape

Three common motivations:

1. **"I want to see the deleted records too"** — fair, but that's a separate rule ("List
   deletion-flagged materials") with its own scope. Mashing them together makes the defect count
   meaningless.
2. **"I'll get the same answer either way"** — true for the defect rows, but the opportunity
   count changes. Universe size = denominator. Deleted records inflating the denominator drops
   the defect rate, making the rule's KPI lie.
3. **"I copy-pasted from a different rule"** — old rules from before the convention was stable.
   Reject in [[prc-audit-rule-quality|audit]] and refactor.

## The exception — when deletion IS the rule

Sometimes a rule's purpose IS to find deletion-flagged records that shouldn't be:

> *"A material referenced in an active production order must not be deletion-flagged"*

Here the rule's intent: find materials that are flagged (`LVORM = 'X'`) AND referenced by active
production orders. The deletion flag is the **error condition**, not a universe restriction.

Convention: when deletion is the error, put it in the `CASE`; the `WHERE` then restricts to
records that are referenced by something (in this case, joined to AFKO with active orders).

```sql
WHERE AFKO.AUART IN ('PP01','PP02')        -- universe: active production orders
  AND AFKO.LOEKZ <> 'X'                    -- exclude deleted PROD orders
SELECT
    CASE WHEN MARA.LVORM = 'X' THEN 1 ELSE 0 END AS zIsErrorFlag
                                           -- error: referenced material is deleted
```

## The "no duplicates" rule

Whatever the rule, **a condition should never appear in both `WHERE` and `CASE`**. If LVORM is
in the `WHERE` (excluding deletes from the universe), the `CASE` checking `LVORM = 'X'` is dead
code. If LVORM is in the `CASE` (deletion is the error), the `WHERE` should not also exclude it.

> [!tip]
> Audit's "dead code" check (`grep -F "LVORM" file.sql | wc -l`) catches the duplication at
> sprint-end.

## Related

- [[con-deletion-flags-vs-status-fields]]
- [[std-ziserrorflag-convention]]
- [[prn-optsel-is-the-universe]]
- [[prc-audit-rule-quality]]
- [[ref-deletion-flag-resolver]] — which flag field a table actually uses.
- ref-deletion-flag-normalization-in-sql-gen — how the generator puts it in the `WHERE`.
