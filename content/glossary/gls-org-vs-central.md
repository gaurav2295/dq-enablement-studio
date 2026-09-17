---
id: gls-org-vs-central
type: glossary
title: Org-Level vs Central-Level Record
domain: sap
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-pattern-org-to-central-parity
  - relates:ref-sap-table-families
  - relates:gls-parity-pair
  - relates:gls-composite-key
  - relates:gls-organizational-context
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - vault:sap-knowledge/SAP Table Families.md
tags: [sap, master-data, structure]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

SAP master data is split in two tiers. The **central** record is the one-per-business-partner
header (`KNA1`, `LFA1`, `MARA`). An **org-level** record extends it for one organisational unit —
company code (`KNB1`, `LFB1`), sales area (`KNVV`), plant (`MARC`), purchasing org (`LFM1`).

## Usage

The distinction drives a whole family of rules, because a fact can be true centrally and false
locally. Two shapes recur:

- **Parity** — a central flag must match the all-or-nothing state of its org children
  ([[gls-parity-pair]], [[std-pattern-org-to-central-parity]]).
- **Extension completeness** — a customer that trades in a sales area must actually have the
  org-level record for it.

An org-level record always carries the central key plus its org dimension, so its
[[gls-composite-key|composite key]] is wider than the central one.
