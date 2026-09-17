---
id: ref-system-aliases-map
type: reference
title: System Aliases Map
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - vault:dq-methodology/System Aliases Map.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:std-zsourcesystemid-convention
  - relates:con-multi-implementation-model
  - relates:std-view-naming-patterns
  - relates:gls-system-alias
---

## What it is

The **System Aliases Map** is a project-level dictionary that maps the raw `zSourceSystemID`
values stored in the data to short, friendly aliases used in view names and the UI.

## Where it lives

In each project's YAML under `system_aliases:`.

```yaml
# config/projects/sap_ecc.yaml (Danone-style ECC project)
system_aliases:
  SRCECCZ02100: P02
  SRCECCZ03100: P03
  SRCECCZ06100: P06
  SRCS4SG2100:  PG3
```

```yaml
# Bacardi-style project (different convention)
system_aliases:
  P01: P01     # alias == code; map identity-resolves
```

## Keys vs values — which is what

| | Stored in | Used as |
|---|---|---|
| **Key** (e.g. `SRCECCZ02100`) | The actual `zSourceSystemID` value in `WRKDQ` (carried through from the upstream `WRKDQPREP_ALL` prep layer, whose output is pushed into `WRKDQ`) | Filter literal: `zSourceSystemID = 'SRCECCZ02100'` |
| **Value** (e.g. `P02`) | Cosmetic / display | View name slot: `DQ_0042_P02_MARA_...`, WHERE-clause comment: `Limit to source system P02` |

The **keys are authoritative** — a code appears in `source_systems` (the fan-out scope) iff it
is a key in `system_aliases`.

## Resolution rules

- If alias == code, the label is just the alias (e.g. `P01`).
- If alias ≠ code, the WHERE-clause comment combines them: `Limit to source system P02
  (SRCECCZ02100)` (canonical), or just `Limit to source system P02` (bare-alias form, simpler;
  what the JS sibling-replicator emits).

Both forms are valid. Recent Studio versions emit the bare alias for visual consistency with the
lead rule.

## Excluded systems

Sometimes you want a system **configured and named** but **not deployed** — for example, `P03`
might exist but the project isn't live there yet. Use the `excluded_systems` block:

```yaml
system_aliases:
  SRCECCZ02100: P02
  SRCECCZ03100: P03
  SRCECCZ06100: P06
  SRCS4SG2100:  PG3

excluded_systems:
  - SRCECCZ03100   # configured but not yet deployed
```

The bulk fan-out skips excluded systems when a row's `systems` column is blank and the default
fan-out applies. Per-row overrides still work — you can deploy a single rule to `P03` manually by
setting its `systems` cell.

## Common mistakes

> [!warning] Keys swapped with values
> Writing `P02: SRCECCZ02100` instead of `SRCECCZ02100: P02`. The Studio reads keys as the
> literal filter value; a reversed map breaks filters.

- **Missing entries** — a tracker row references a system that isn't in the map, so fan-out
  skips it silently. Always cross-check `system_aliases` against the actual systems in scope
  before bulk generation.
- **Whitespace in values** — `SRCECCZ02100: " P02"` (leading space) renders view names with a
  leading space. Keep values quote-free in YAML.

## Related

- [[std-zsourcesystemid-convention|zSourceSystemID Convention]] — the column whose values this map aliases
- [[std-view-naming-patterns|View Naming Patterns]] — where the alias appears in view names
- [[con-multi-implementation-model|Multi-Implementation Model]] — the fan-out scope this map drives
- Project YAMLs
