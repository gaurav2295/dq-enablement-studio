---
id: gls-business-friendly-alias
type: glossary
title: Business-Friendly Alias
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:std-output-field-sections
  - relates:std-sql-comment-standards
  - relates:gls-field-classification
sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [naming, output-fields]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The bracketed, human-readable name every real SAP column is given in a rule view's `SELECT` —
a short Title Case phrase derived from the field's catalog `description`.

| Field | Catalog description | Alias |
|---|---|---|
| `LIFNR` | Account Number of Vendor or Creditor | `[Vendor Number]` |
| `SKONT` | Cash Discount Percentage | `[Cash Discount Percent]` |
| `ERDAT` | Date on Which the Record Was Created | `[Created On]` |

## Usage

Two rules travel together: alias every real column, and **fully qualify** it with its table alias
(`LFA1.LIFNR`, never bare `LIFNR`) so each section stays unambiguous across joins. The alias is
what a business reviewer reads in the defect extract — a view full of raw SAP mnemonics forces
every reviewer to translate, every time.
