---
id: prn-adr-029
type: principle
kind: decision
title: ADR D-29 — status_field_check (v3.6.0, 4th rule pattern) is scoped precisely: never steals the original 10, correctly claims its 5
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-29
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

status_field_check (v3.6.0, 4th rule pattern) is scoped precisely: never steals the original 10, correctly claims its 5.

## Rationale

status_field_check is deliberately LAST in rule_patterns.json's intent-detection array so it can't shadow the three older patterns. Two separate risks needed to be closed at once: (1) none of the 10 original acceptance-corpus rules should ever shift onto the new pattern — each must keep resolving to its originally-assigned hierarchy_membership / partner_cardinality / org_to_central_parity; (2) the 5 rules formerly pinned as ORDINARY_BLOCK_RULES (an intentionally-unmatched T2b gap) must now all fire the new pattern instead of falling through to None. The owner's own live-test phrasing that motivated the whole pattern (a positive-polarity 'must have' rule on KNA1.SPERZ) is the direct regression case: previously it produced a shell derivation (zIsErrorFlag a literal NULL, a TBD view-name slot, only KNA1.KUNNR surviving as an output field).

## Consequence

Three cross-checked contracts are pinned together: the original 10 rules' pattern assignments are untouched, the 5 target rules now resolve via status_field_check, and the owner's exact reported phrasing derives a real payment-block check rather than a shell. Any future 5th rule pattern must repeat this same three-way non-regression check before it ships.

> [!note] Provenance
> Architecture decision **D-29** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
