---
id: std-ziserrorflag-convention
type: standard
title: zIsErrorFlag Convention
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
sources:
  - vault:dq-methodology/zIsErrorFlag Convention.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:con-rule-types
  - relates:con-view-types
  - implements:prn-optsel-is-the-universe
  - relates:prn-ziserrorflag-is-integer
  - relates:prn-profiling-has-no-pass-fail
  - relates:gls-ziserrorflag
---

## What it is

For Error and Info rules, the per-row defect flag. It lives on OptSel; RptSel uses it to filter
the universe down to defects.

## Format

**Integer literal 1 / 0**. Never `'Y'`/`'N'`, never `'Yes'`/`'No'`, never `TRUE`/`FALSE`.

```sql
CASE WHEN <error_condition> THEN 1 ELSE 0 END AS [zIsErrorFlag]
```

RptSel filters with:

```sql
WHERE [zIsErrorFlag] = 1
```

The mapping is fixed: **`1` = defective record, `0` = valid record.** Never the other way round —
downstream defect counts, scoring and SKP's Error Query all assume `1` means "something is wrong
here".

## The main check lives in this field

The DQ Rule Standards put it plainly: *the main check of the rule's logic must be implemented in
this field.* Whatever the rule is fundamentally testing, that test **is** the `CASE` expression.
If you can read a rule's `zIsErrorFlag` and still not know what the rule checks, the logic has
leaked somewhere it shouldn't be — usually into the `WHERE` clause.

## Error-flag design principles — what counts as a defect

Set `zIsErrorFlag = 1` **only when a genuine business defect exists**. Otherwise `0`. A flag that
fires on something a steward cannot act on is noise, and noise erodes trust in the whole rule set
faster than a missing rule does.

Genuine defects the standards doc enumerates:

| Defect class | Typical shape |
|---|---|
| Missing mandatory attribute | A required field is NULL or blank |
| Missing organizational extension | Master record not extended to a plant / sales area / company code it is transacted in |
| Missing reference data | A key points at a check-table entry that does not exist |
| Invalid configuration | A configuration combination the process cannot support |
| Invalid code assignment | A domain value outside the permitted set for this context |
| Duplicate records | Two records representing the same real-world entity |
| Inconsistent cross-table relationships | Header and item, or master and org-level, disagree |
| Invalid date ranges | Valid-from later than valid-to, dates outside plausible bounds |
| Missing descriptions | A record with no readable text in the required language |
| Missing addresses | A partner with no usable address for its role |

The list is illustrative, not closed — "or whatever the specific rule is designed to check". What
makes it a defect is that a person could look at the record and agree it is wrong.

## Why integer, not string

- ADM expects INT — string flags silently fail the defect count.
- Aggregation works trivially — `SUM(zIsErrorFlag)` gives the defect count, `AVG(zIsErrorFlag)`
  gives the defect rate, without CASEs at the dashboard layer.
- Comparison is unambiguous — `WHERE zIsErrorFlag = 1` always works; `WHERE zIsErrorFlag = 'Yes'`
  versus `'Y'` versus `'yes'` is a class of bug we don't have to think about.

## Where the CASE logic lives

**Inside the CASE, not in WHERE.** This is the most common bug pattern in hand-written DQ SQL.

- The **WHERE clause** restricts the OptSel to the candidate universe (e.g. active, non-deleted
  records of the right type).
- The **CASE expression** identifies which of those candidates are defects.

```sql
-- Correct
SELECT
    CASE WHEN MEINS IS NULL OR MEINS = '' THEN 1 ELSE 0 END AS [zIsErrorFlag],
    ...
FROM MARA
WHERE LVORM <> 'X'            -- universe: not deleted
  AND MTART = 'FERT';         -- universe: finished goods
```

```sql
-- Wrong — filters errors out of the universe, OptSel returns no defects
SELECT
    1 AS [zIsErrorFlag],
    ...
FROM MARA
WHERE LVORM <> 'X'
  AND MTART = 'FERT'
  AND (MEINS IS NULL OR MEINS = '');  -- THIS belongs in the CASE!
```

In the wrong example, the OptSel contains only defects (because the WHERE pre-filters), which
violates [[prn-optsel-is-the-universe|OptSel semantics]] and breaks ADM's opportunity-vs-defect
maths.

## Comment the CASE

The CASE expression carries the rule's business logic. Comment it so a reviewer understands the
check without SAP knowledge.

```sql
CASE
    /* Material is missing a base unit of measure — required for all
       finished goods so the planning + costing modules can compute. */
    WHEN MEINS IS NULL OR MEINS = ''
        THEN 1
    ELSE 0
END AS [zIsErrorFlag]
```

## Profiling rules have no zIsErrorFlag

Profiling produces a distribution, not a pass/fail. PrfSel and PrfSum carry **no**
`zIsErrorFlag` column. Suggesting one in an AI-derived profiling rule is a downgrade — see
[[prn-profiling-has-no-pass-fail|Why Profiling Has No Pass-Fail]].

## Related

- [[con-rule-types|Rule Types — Error, Info, Profiling]]
- [[con-view-types|View Types — OptSel RptSel InfSel PrfSel PrfSum]]
- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]]
- [[prn-optsel-is-the-universe|Why OptSel is the Universe and RptSel is the Wrapper]]
- [[prn-ziserrorflag-is-integer|Why zIsErrorFlag is Integer]]
- Studio — zConcatenatedKey & zIsErrorFlag SQL Emission — the generator code that emits this column
