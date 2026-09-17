---
id: gls-conformity
type: glossary
title: Conformity
domain: dq-fundamentals
audience: [consultant, lead, instructor]
level: foundation
status: review
links:
  - relates:con-dq-dimensions
  - relates:gls-consistency
sources:
  - coe:seven-dimension model per CONFLICT-001
  - vault:dq-methodology/DQ Dimensions.md
tags: [dimensions, foundations]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**Does the value follow the required format, range, or standard?** Conformity is a structural
check — a regex, a length, a domain of allowed codes, a numeric range — testable without any
external reference. It is the canonical dimension in the seven-dimension model
([[con-dq-dimensions]]); earlier training material called this *Validity* and used a
six-dimension model instead. Conformity **subsumes** that legacy term: anything taught as
"Validity" is Conformity under the current vocabulary. See CONFLICT-001 in the conflicts log for
the full resolution.

## Example rule

A business partner's postal code matches the format required by its country (`ADRC-POST_CODE1`
against the country-specific pattern in `T005X`). A US ZIP that's five digits and a German
postcode that's five digits can both pass length while one is structurally wrong for its country
— the rule must be country-aware to be a real Conformity check.

## Cost of a defect

A malformed postal code fails carrier validation, causing returned mail, failed EDI shipments, or
incorrect tax jurisdiction determination on the order. Conformity defects are cheap to detect
(structural) but expensive to leave unchecked, because they silently poison every downstream
process — shipping, tax, reporting — that assumes the format is trustworthy.
