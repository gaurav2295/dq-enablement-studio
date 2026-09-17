---
id: gls-system-alias
type: glossary
title: System Alias
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:ref-system-aliases-map
  - relates:std-view-naming-patterns
  - relates:gls-fan-out
  - relates:gls-zsourcesystemid
  - relates:con-multi-implementation-model
sources:
  - vault:dq-methodology/System Aliases Map.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [multi-system, configuration]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A project-config entry mapping a **real source-system code** (the `zSourceSystemID` value, e.g.
`SRCECCZ02100`) to the **short token** that appears in a view name (e.g. `P02`).

## Usage

The **keys are authoritative**: they are the values the `WHERE` filter compares against and the
scope a rule fans out over. The value only fills the cosmetic view-name slot — which is precisely
why filter and view name cannot drift apart.

> [!note] Which key is the fan-out scope — CONFLICT-005
> The corpus follows `system_aliases` keys, with `source_systems` as the legacy fallback and a
> one-time warning when both are set and disagree.

The alias token must be the **production** system or the agreed alias, never the interim QA
system — a view name is forever.
