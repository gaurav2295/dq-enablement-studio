---
id: prn-adr-036
type: principle
kind: decision
title: ADR D-36 — The HTML AUA dashboard resolves project-overlay value lookups the same way the SQL-script generator does
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-36
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The HTML AUA dashboard resolves project-overlay value lookups the same way the SQL-script generator does.

## Rationale

Before this fix, the HTML AUA dashboard only consulted the shared seed file for value-lookup descriptions, silently dropping any field that exists ONLY in a client project's overlay (config/projects/`<slug>`/attribute_value_lookups.json) — even though core.schema_profiler.generate_attribute_usage_script already resolved those same overlays via load_value_lookups(project_overlay_path=...). Two exports of the same underlying data disagreeing on overlay resolution is a cross-export consistency bug.

## Consequence

A field defined only in a project overlay must be found by the HTML dashboard's backfill, and fields already covered by the shared seed (no overlay involved) must keep resolving exactly as before — self_describing values are never duplicated, domain_fixed_values inline enums still resolve. Any future AUA export path must resolve overlays through the same mechanism, not reinvent a seed-only lookup.

> [!note] Provenance
> Architecture decision **D-36** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
