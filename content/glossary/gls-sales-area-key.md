---
id: gls-sales-area-key
type: glossary
title: Sales Area Key
domain: sap
audience: [consultant, developer]
level: practitioner
status: deprecated
links:
  - relates:std-pattern-hierarchy-membership
  - relates:ref-sap-table-families
  - relates:gls-composite-key
  - relates:gls-partner-function
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - vault:sap-knowledge/SAP Table Families.md
tags: [sap, sd, keys]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The three-part organisational key of SAP Sales & Distribution: **sales organisation (`VKORG`) ×
distribution channel (`VTWEG`) × division (`SPART`)**. Together with the customer number
(`KUNNR`) it keys `KNVV` — the customer sales view — and every table hanging off it.

## Usage

Any correlated subquery against a sales-view table correlates on **all four** columns, not just
the customer: `KNVV → KNVH` (customer hierarchy, whose `HKUNNR` names the parent node) and
`KNVV → KNVP` (partner functions) both do. Dropping one dimension quietly compares a customer's
record in one sales area against another's in a different one.

Sales area is the reason a customer can be perfectly maintained in one market and defective in
another — see [[gls-org-vs-central]].
