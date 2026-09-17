---
id: gls-domain-fixed-values
type: glossary
title: Domain Fixed Values
domain: sap
audience: [consultant, developer]
level: practitioner
status: review
links:

  - relates:gls-check-table
  - relates:gls-coded-field
sources:
  - vault:sap-knowledge/Value-Description Resolution (4 mechanisms).md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [sap, dictionary, reference-data]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The legal values declared on a SAP **domain** itself (`DD07T` territory) rather than in a separate
[[gls-check-table|check table]] — a short, closed list carried in the dictionary with its
descriptions.

## Usage

Domain fixed values are the second of the four value-description mechanisms, and the one most
often client-extended: `domain_fixed_values` is the **only** thing a client overlay import is
allowed to add, deliberately. A narrow overlay surface is what keeps a
client's Z-values from silently rewriting SAP baseline knowledge.
