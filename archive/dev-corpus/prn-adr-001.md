---
id: prn-adr-001
type: principle
kind: decision
title: ADR D-1 — DQOps numbering is counter-owned, not row-owned
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-1
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

DQOps numbering is counter-owned, not row-owned.

## Rationale

Fan-out previously let a row-supplied rule_id seed the first impl, colliding with the auto-counter. Requirement is "incremental from the starting number, never duplicated." Sibling impls each need a distinct id; honouring a row-supplied id breaks both invariants. The old honour-path was already vestigial ("mostly defensive for hand-edited dicts").

## Consequence

The batch counter is the single source of truth for Error/Info DQOps ids; a row-supplied rule_id is not honoured in fan-out. Re-importing an Error rule renumbers it. If stable Error DQOps ids across re-imports are ever needed, use the same claim mechanism the Profiling path uses (SKP-numeric lock), don't reinstate first-impl honouring.

> [!note] Provenance
> Architecture decision **D-1** in the DQ Studio decision registry, decided 2026-06-30, registry status *active*.
