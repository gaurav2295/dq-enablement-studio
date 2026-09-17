---
id: prn-adr-064
type: principle
kind: decision
title: ADR D-64 — Workspace-migration is idempotent — existing session rows block a legacy file from overwriting live data
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-64
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Workspace-migration is idempotent — existing session rows block a legacy file from overwriting live data.

## Rationale

Belt-and-suspenders: if workspace_sessions already has ANY row (meaning real per-user usage has already happened), a legacy pre-migration file that somehow still exists on disk must never be allowed to overwrite that live data on a subsequent migration run.

## Consequence

The migration checks for existing rows before touching the legacy file path at all. Any future migration or backfill script that reads a legacy file must add the same already-populated guard before it writes anything.

> [!note] Provenance
> Architecture decision **D-64** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
