---
id: prn-adr-053
type: principle
kind: decision
title: ADR D-53 — system_discriminator_column overrides reach the generated profiling SQL verbatim
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-53
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

system_discriminator_column overrides reach the generated profiling SQL verbatim.

## Rationale

Some client projects use a non-default column name for the system discriminator (e.g. 'source_sys_id' instead of the usual convention). The override must reach the generated SQL exactly as configured, not get silently normalized or ignored in favor of the default column name.

## Consequence

Any future profiling-SQL code path that references the system discriminator column must read it from the project's configured override, never hardcode the default column name.

> [!note] Provenance
> Architecture decision **D-53** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
