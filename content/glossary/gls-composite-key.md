---
id: gls-composite-key
type: glossary
title: Composite Key
domain: sap
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:std-zconcatenatedkey-convention
  - relates:ref-sap-table-families
  - relates:gls-zconcatenatedkey
  - relates:ref-sap-key-fields-and-critical-data-elements
sources:
  - vault:sap-knowledge/SAP Table Families.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [sap, keys]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A primary key made of **more than one field** — the normal case in SAP org-level tables. `KNB1` is
keyed by customer *and* company code; `KNVV` by customer, sales org, distribution channel and
division; `MARC` by material and plant.

## Usage

Every field of the composite key must appear in the rule's
[[gls-zconcatenatedkey|zConcatenatedKey]], or two genuinely different records collapse to one key
and the defect extract cannot be actioned.

The same fields are the correlation pairs of any correlated subquery against that table — a
subquery matched on customer alone, where the table is keyed on customer plus sales area, is
matching the wrong thing.
