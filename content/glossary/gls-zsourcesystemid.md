---
id: gls-zsourcesystemid
type: glossary
title: zSourceSystemID
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:std-zsourcesystemid-convention
  - relates:gls-system-alias
  - relates:gls-syniti-technical-fields
  - relates:gls-fan-out

sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [technical-fields, multi-system]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **source-system identifier** carried on every row of every Studio-generated view — which
system this record came from. It is a real column on the prepared tables, selected as
`MARA.zSourceSystemID AS [zSourceSystemID]`.

## Three Jobs at Once

1. **Identify the row's origin** — which source system this record came from
2. **Scope a fanned-out implementation** — `WHERE zSourceSystemID = 'SAP'` vs. `WHERE zSourceSystemID = 'LEGACY'`
3. **Pair symmetric-field joins** — ensures joins never accidentally cross systems

## Example: Multi-System Material Check

```sql
-- Prepared table: materials from two systems
SELECT
  MaterialID,
  'SAP' AS zSourceSystemID,           -- SAP materials
  MaterialName,
  Plant,
  BaseUnitOfMeasure
FROM [SAP_ECC].[dbo].[MARA]

UNION ALL

SELECT
  MaterialID,
  'LEGACY' AS zSourceSystemID,        -- Legacy system materials
  MaterialName,
  Plant,
  BaseUnitOfMeasure
FROM [LEGACY_ERP].[dbo].[MARA];
```

Then in a rule:

```sql
-- Rule checks EACH SYSTEM separately
SELECT
  MaterialID,
  zSourceSystemID,
  CASE
    WHEN BaseUnitOfMeasure IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM MARA_Stage
WHERE zSourceSystemID = '{{SYSTEM}}'  -- Template: substituted per system at deploy time
  AND MaterialID = ref_mat.MaterialID
  AND zSourceSystemID = ref_mat.zSourceSystemID;  -- Full key: prevents cross-system joins
```

Result: Two separate implementations deployed, one for SAP, one for LEGACY.

## Usage Rules

> [!warning]
> **Never a string literal.** `'P03' AS [zSourceSystemID]` is a High-severity, save-blocking
> violation on anything the Studio generates or enhances. The one exception is the repository
> **template** form `'{{SYSTEM}}'`, which the generator substitutes per system before deploy.

The codes themselves come from the project's [[gls-system-alias|system alias]] keys, and the
Studio flags a code outside the configured scope.
