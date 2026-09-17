---
id: prn-adr-003
type: principle
kind: decision
title: ADR D-3 — Pin to current-generation model IDs, honour the user's named tier
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-3
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Pin to current-generation model IDs, honour the user's named tier.

## Rationale

Dated snapshot model IDs get retired and 404. Bare current-generation IDs are stable.

## Consequence

Sonnet 4.6 / Opus 4.6 / Haiku 4.5 (the exact IDs the user named) are used. When migrating later, the canonical source for valid IDs is the claude-api skill / Anthropic models docs — never hand-construct dated IDs.

> [!note] Provenance
> Architecture decision **D-3** in the DQ Studio decision registry, decided 2026-06-30, registry status *active*.
