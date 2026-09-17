---
id: prn-adr-004
type: principle
kind: decision
title: ADR D-4 — Pre-existing test failures are NOT blockers for these fixes
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-4
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Pre-existing test failures are NOT blockers for these fixes.

## Rationale

Verified (by stashing) that a 13-failure cluster fails identically without the workstream's own changes — it is independent config-vs-test drift, not caused by or blocking that work.

## Consequence

Shipped v3.1 and v3.2 with the 13-failure cluster still red; a pre-existing red cluster is not, by itself, a reason to block an unrelated fix, provided the stash-verification discipline is repeated to confirm independence.

> [!note] Provenance
> Architecture decision **D-4** in the DQ Studio decision registry, decided 2026-06-30, registry status *active*.
