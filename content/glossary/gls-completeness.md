---
id: gls-completeness
type: glossary
title: Completeness
domain: dq-fundamentals
audience: [consultant, lead, instructor]
level: foundation
status: review
links:
  - relates:con-dq-dimensions
  - relates:gls-integrity
sources:
  - coe:seven-dimension model per CONFLICT-001
  - vault:dq-methodology/DQ Dimensions.md
tags: [dimensions, foundations]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**Is the value present where the business requires it?** Completeness is the simplest dimension
to test — a null check, an empty-string check, a "field not defaulted" check — and often the
highest-volume one in a rule catalogue. It answers presence, not correctness: a populated field
can still fail [[gls-accuracy]] or [[gls-conformity]].

## Example rule

A material master record has a non-null base unit of measure (`MEINS`). Without it, the material
cannot flow through MRP, cannot be used on a purchase order line, and blocks any process that
requires a unit conversion.

## Cost of a defect

A missing base unit of measure stalls the material at creation — no PO, no goods receipt, no MRP
run — until someone manually fills the gap. At scale, Completeness gaps are the most common
cause of blocked transactions in a cutover: a single required field left null on thousands of
records turns into thousands of manual remediation tasks. Completeness gaps also compound with
[[gls-integrity]] gaps — a missing foreign key is simultaneously an incomplete record and a
broken reference, which is why the two dimensions are the pairing most often checked together.
