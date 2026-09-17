---
id: gls-check-table
type: glossary
title: Check Table
domain: sap
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-coded-field-text-translation
  - relates:gls-coded-field
  - relates:gls-reference-data
sources:
  - vault:sap-knowledge/Value-Description Resolution (4 mechanisms).md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [sap, dictionary, reference-data]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The SAP Data Dictionary table a field's values are validated against — the authoritative list of
legal codes for that field, usually paired with a language-dependent **text table** holding the
descriptions.

## Usage

A check table is the first place to look for two different questions:

- *"Is this value legal?"* — a conformity rule joins the check table and flags rows with no match.
- *"What does this code mean?"* — the text table supplies the
  [[gls-coded-field|coded field's]] translation, filtered on [[gls-spras|SPRAS]].

Where a field has no check table, its legal values may still be fixed in the domain itself — see
[[gls-domain-fixed-values]].
