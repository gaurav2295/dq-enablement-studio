---
id: gls-timeliness
type: glossary
title: Timeliness
domain: dq-fundamentals
audience: [consultant, lead, instructor]
level: foundation
status: review
links:
  - relates:con-dq-dimensions
sources:
  - coe:seven-dimension model per CONFLICT-001
  - vault:dq-methodology/DQ Dimensions.md
tags: [dimensions, foundations]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**Is the data current enough for the decision it supports?** Timeliness is the only dimension
that is inherently relative — "current enough" depends on how fast the underlying fact changes
and how often the business acts on it. A field can be present, correctly formatted, and entirely
consistent, and still be Timeliness-defective if it was last touched long before it should have
been.

## Example rule

A material master's last-change date (`AENAM`/`LAEDA`) falls within N months, or a price
condition's validity end date (`KONH-DATBI`) has not already passed at the time it is used in a
sales order. The threshold N is business-defined per material type, not a fixed universal rule.

## Cost of a defect

A stale price condition ships an order at last quarter's cost, eroding margin on every order that
slips through before someone notices. A stale material record drives MRP off outdated lead times,
causing stockouts or overstock. Timeliness defects rarely block a transaction the way Integrity
or Completeness gaps do — they let the transaction through wrong, which makes them harder to
detect and more likely to compound into a financial or planning loss before anyone catches them.
