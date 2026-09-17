---
id: prn-adr-059
type: principle
kind: decision
title: ADR D-59 — An unresolved AssignedTo name passes through verbatim into Impl Implementer, with a precise warning
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-59
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

An unresolved AssignedTo name passes through verbatim into Impl Implementer, with a precise warning.

## Rationale

When AssignedTo carries a display name that doesn't resolve via user_map, the exporter can't fabricate a resolved value SKP could actually process — but silently blocking the row or leaving the cell empty would hide the problem. The verbatim (SKP-unusable) name is written through, and a warning fires so the user notices BEFORE uploading to SKP — but only for the names that are genuinely unresolved in a partial-resolution batch, never when AssignedTo was simply blank to begin with.

## Consequence

All four shapes must keep working together: fully-unresolved, fully-resolved, partially-resolved, and blank AssignedTo each produce the correct cell value and warning presence/absence. Any future change to user_map resolution must re-prove all four cases, not just the common resolved case.

> [!note] Provenance
> Architecture decision **D-59** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
