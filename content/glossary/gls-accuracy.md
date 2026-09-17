---
id: gls-accuracy
type: glossary
title: Accuracy
domain: dq-fundamentals
audience: [consultant, lead, instructor]
level: foundation
status: review
links:
  - relates:con-dq-dimensions
  - relates:gls-completeness
sources:
  - coe:seven-dimension model per CONFLICT-001
  - vault:dq-methodology/DQ Dimensions.md
tags: [dimensions, foundations]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**Does the value reflect the real-world fact it claims to represent?** Accuracy is the dimension
of correctness — not "is something here" (that's [[gls-completeness]]) but "is
what's here true". It is the hardest dimension to test with SQL alone, because SQL cannot compare
a field against reality — only against another trusted source or a validated rule (a checksum, a
lookup table, a format that only correct values can satisfy).

## Example rule

A customer's VAT registration number (`STCEG`) passes an EU VAT format check and a Luhn-style
checksum. The field can be non-null, correctly formatted, and still wrong — Accuracy is the
dimension that catches a transposed digit a Conformity check would let through.

## Cost of a defect

An inaccurate VAT number fails tax authority validation at invoice time, blocking outbound
billing or triggering downstream compliance penalties. Inaccurate master data is the most
expensive class of DQ defect to detect after the fact — it passes every structural check and
surfaces only when a transaction, an audit, or a customer complaint exposes it.
