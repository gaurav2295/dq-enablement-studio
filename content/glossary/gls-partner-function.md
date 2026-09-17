---
id: gls-partner-function
type: glossary
title: Partner Function (PARVW)
domain: sap
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-pattern-partner-cardinality
  - relates:ref-sap-table-families
  - relates:gls-cardinality
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - vault:sap-knowledge/SAP Table Families.md
tags: [sap, sd, partners]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The role a partner plays on a customer's sales area — sold-to (`AG`), ship-to (`WE`), bill-to
(`RE`), payer (`RG`). Stored in `KNVP.PARVW`.

## Usage

Partner-function rules are almost always **cardinality** rules: "every sold-to must have exactly
one payer", "every customer must have at least one ship-to". The Studio maps the business word to
its code through the pattern library's `partner_lexicon` — payer→`RG`, ship-to→`WE`, sold-to→`AG`,
bill-to→`RE` — so a new phrasing is a lexicon change, not a code change.

`KNVP` is keyed at [[gls-sales-area-key|sales area]] level plus the partner function and counter,
so the correlated count is always scoped to one sales area.
