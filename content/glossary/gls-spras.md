---
id: gls-spras
type: glossary
title: SPRAS
domain: sap
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:std-coded-field-text-translation
  - relates:gls-coded-field
  - relates:gls-check-table
sources:
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [sap, fields, language]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

SAP's **language key** column, present on every text table. `'E'` is English; a text table row
exists per language, so a join that forgets `SPRAS` multiplies rows by the number of installed
languages.

## Usage

Every text-table join in a rule view carries an explicit `SPRAS` predicate. It is also a *literal*
comparison rather than a correlation predicate, so `SPRAS = 'E'` does not count toward a rule
pattern's join-key requirements.

Which language a project uses is a project decision — do not hardcode `'E'` on an engagement whose
master data is maintained in another language.
