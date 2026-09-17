---
id: prn-adr-021
type: principle
kind: decision
title: ADR D-21 — Catalog promotion candidates are git-governed, never a runtime write into the live catalog
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-21
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Catalog promotion candidates are git-governed, never a runtime write into the live catalog.

## Rationale

Mirrors D-12's offline-pipeline-with-provenance discipline for knowledge growth — an admin action that could silently pollute the shared, curated catalog with an unreviewed rule would undo the exact trust the harness exists to build in the first place. Git review is the same audit trail the enrichment pipeline already established for a different mechanism.

## Consequence

POST /api/catalog/promote/{workspace_idx} writes only into knowledge/catalogs/candidates/ — a human reviews and merges each candidate into the actual ~4,800-rule catalog corpus as its own reviewed git change. The endpoint requires the staged rule's last, server-stamped harness verdict to already be "Pass" (never a client-supplied claim); a Warn/Fail/missing verdict 400s with the reason instead of writing anything. Don't "simplify" this by writing straight into knowledge/catalogs/`<domain>`.json on promote. This is also the harness-v2 design's Pillar 2 "promote" entry path — the one already-enforcing gate the v2 posture mechanism generalizes.

> [!note] Provenance
> Architecture decision **D-21** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
