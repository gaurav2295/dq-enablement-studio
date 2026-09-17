---
id: gls-reference-data
type: glossary
title: Reference Data
domain: sap
audience: [consultant]
level: foundation
status: review
links:
  - relates:ref-sap-table-families
  - relates:con-profiling-concepts
  - relates:gls-check-table
  - relates:gls-domain-fixed-values
sources:
  - vault:sap-knowledge/SAP Table Families.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [sap, data-types]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The configuration and code-list data master records **point at** — country keys, currencies,
units of measure, account groups, order reasons, payment terms. Small, slow-moving, and shared.

## Usage

Reference data is the third kind of table a DQ engagement meets, alongside master data and
transactional data, and it behaves differently from both: low row counts, high fan-in, and
defects that are configuration decisions rather than data-entry mistakes.

Most integrity rules are really reference-data rules — a master record naming a code that does not
exist in its [[gls-check-table|check table]] is a broken reference, not a typo.
