---
id: prn-adr-014
type: principle
kind: decision
title: ADR D-14 — Client overlay import is deliberately narrow — domain_fixed_values only
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-14
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Client overlay import is deliberately narrow — domain_fixed_values only.

## Rationale

A domain's fixed values are a complete, self-contained map; a check_table reference is not — guessing its structure risks a silently wrong lookup, worse than the "add by hand" message it shows instead.

## Consequence

core/dd_overlay_importer.py auto-derives ONLY the domain_fixed_values mechanism. check_table-pointed fields are surfaced informational-only and never auto-written. Don't "improve" this by guessing check_table field names from convention — it needs its own verified source if ever built.

> [!note] Provenance
> Architecture decision **D-14** in the DQ Studio decision registry, decided 2026-07-15, registry status *active*.
