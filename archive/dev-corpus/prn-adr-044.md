---
id: prn-adr-044
type: principle
kind: decision
title: ADR D-44 — verify_table_field checks the curated domain-engine registry first; the SAP baseline loads only on a miss
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-44
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

verify_table_field checks the curated domain-engine registry first; the SAP baseline loads only on a miss.

## Rationale

engine.find_field is consulted FIRST when verifying a table field's trust status — if the curated domain-engine registry already verifies the field, the (larger, slower) SAP baseline must never even be loaded.

## Consequence

The baseline load is proven skipped, not just "not needed": the test makes baseline-loading raise and still passes, so an engine hit genuinely short-circuits before the baseline is touched. Any future trust-verification change must preserve this precedence order.

> [!note] Provenance
> Architecture decision **D-44** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
