---
id: gls-coded-field
type: glossary
title: Coded Field
domain: sql-standards
audience: [consultant]
level: foundation
status: review
links:
  - relates:std-coded-field-text-translation
  - relates:gls-check-table
  - relates:gls-spras
sources:
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [sap, output-fields]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A SAP column whose stored value is a **code**, not a word — account group, material type, order
reason, country key, blocking reason. The code is meaningful to SAP and opaque to the business
reader of a defect extract.

## Usage

The standing rule: **a coded field carries its text translation** into the view, side by side with
the code ([[std-coded-field-text-translation]]). Four mechanisms resolve the text — a
[[gls-check-table|check table]] join, [[gls-domain-fixed-values|domain fixed values]], a client
overlay, or the field catalog's own description — see [[ref-value-description-resolution]].

Text tables are language-dependent, so the join is filtered on [[gls-spras|SPRAS]].
