---
id: gls-zdomainsegment
type: glossary
title: zDomainSegment
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-output-field-sections
  - relates:gls-syniti-technical-fields
  - relates:qa-zdomainsegment-example-impact
sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [technical-fields, segmentation]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A **classification column** — the account-group-derived segment of a Customer, Vendor or Material
master record (`KNA1.KTOKD`, `LFA1.KTOKK`, `MARA.MTART` are the underlying classifiers). It rides
in the [[gls-syniti-technical-fields|Syniti Technical Fields]] section when the rule's tables
intersect one of those three master domains.

## Usage

Three rules govern how it is emitted:

- **A plain table reference** — `KNA1.zDomainSegment AS [zDomainSegment]`. Never a JOIN to a
  lookup, never a `CASE`: the DQ Pipeline pre-computes the column on the master tables and the
  Studio only references it.
- **A classification, not an identifier** — so it never enters the
  [[gls-zconcatenatedkey|zConcatenatedKey]] recipe and is never marked as a key output field.
- **Never added to catalog-sourced SQL**, which ships verbatim by contract.

Profiling rules *are* included, and when a rule spans two domains the source table is chosen by a
deterministic precedence.
