---
id: gls-integrity
type: glossary
title: Integrity
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

**Do references resolve — no orphans, no broken keys?** Integrity is the dimension for foreign
keys: a field that stores an identifier is only as good as whether that identifier still exists
in the table it points to. It earns its own dimension, separate from [[gls-completeness]],
because referential breakage — not missing values — is the single most common and most expensive
SAP master-data failure mode.

## Example rule

A cost element's profit center exists as an active record in `CEPC`. The cost element itself can
be fully populated and correctly formatted; if the profit center it references was deleted,
renamed, or never migrated, every posting against that cost element fails or lands in the wrong
place.

## Cost of a defect

A broken reference blocks the posting outright — a document parked pending correction, a payment
run that skips the vendor, a GL entry that can't find its cost object. Integrity defects are
disproportionately expensive because they surface downstream of data entry, in the transaction
that depends on the reference, often well after the bad record was created — which is why
Integrity checks are run alongside Completeness checks rather than instead of them: a null
foreign key and a broken one both need catching, by different rules.
