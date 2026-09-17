---
id: prn-adr-002
type: principle
kind: decision
title: ADR D-2 — Profiling keeps its SKP→DQOps lock, made collision-safe
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-2
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Profiling keeps its SKP→DQOps lock, made collision-safe.

## Rationale

Preserves the re-import/tracker join (1 SKP = 1 DQOps) while guaranteeing it can't clash with an auto-assigned id in a mixed batch.

## Consequence

Profiling rules still lock DQOps to the SKP number, but the id is now claimed in the shared used-id set.

> [!note] Provenance
> Architecture decision **D-2** in the DQ Studio decision registry, decided 2026-06-30, registry status *active*.
