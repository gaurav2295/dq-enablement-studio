---
id: con-multi-implementation-model
type: concept
title: Multi-Implementation Model
domain: rule-design
audience: [consultant]
level: practitioner
status: approved
sources:
  - vault:dq-methodology/Multi-Implementation Model.md
  - dq-studio:.claude/skills_canonical/studio-multi-impl.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:std-skp-rule-identifier-convention
  - relates:std-zsourcesystemid-convention
  - relates:ref-system-aliases-map
  - relates:std-clientref-convention
  - relates:std-view-naming-patterns
  - relates:con-rule-types
  - relates:std-studio-config-shape
  - relates:con-profiling-concepts
  - relates:gls-fan-out
  - relates:gls-sibling-implementation
  - relates:prc-fan-out-a-rule-per-system
---

## The model

One **conceptual rule** fans out to **N per-system implementations**. The same business intent
("a material must have a base UoM") becomes a separate deployable artefact for each source
system (P02, P03, P06, PG3…).

Two words, used precisely throughout the methodology:

- A **rule** is conceptual. It has no DQOps ID. It is identified by its `SKP_RULE_NNNN`.
- An **implementation** is deployable. It owns one DQOps `rule_id`, one SQL view, one tracker row,
  one SKP enforcement entity.

An implementation is not the same as a view. An Error implementation ships a **pair** of views
(OptSel + its RptSel wrapper) under one DQOps ID — the pair is one implementation, not two. Same
for Profiling, which ships PrfSel + PrfSum under one ID.

## Why split, not unify

A single rule view filtering across all systems via `WHERE zSourceSystemID IN ('P02','P06','PG3')`
would:
- Make SKP's per-system tracker rows impossible to align
- Prevent per-system deployment ordering (deploy to P02 first, validate, then P06)
- Mash all systems' defects into one report — hard to triage by region/team

So we split. Each system gets its own view name, its own DQOps `rule_id`, its own tracker row.
But they share one **SKP_RULE_NNNN** so they're grouped on the SKP side.

## What's shared vs per-implementation

| Field | Shared across siblings | Per-implementation |
|---|---|---|
| Rule name | yes (one conceptual rule) | |
| Domain, attribute, dimension | yes | |
| Description (Implication) | yes | |
| SKP_RULE_NNNN | yes | |
| Parent rule key | yes | |
| DQOps `rule_id` | | yes (sequential per-impl) |
| View names | | yes (system in the slot) |
| `zSourceSystemID = '<code>'` filter | | yes |
| `system_filter` + `system_alias` on the spec | | yes |

## Fan-out scope

The project YAML's `system_aliases` map defines which systems a rule fans out to:

```yaml
system_aliases:
  SRCECCZ02100: P02
  SRCECCZ03100: P03
  SRCECCZ06100: P06
  SRCS4SG2100:  PG3
```

Keys = authoritative deployment scope. Values = the friendly alias used in view names. So
`SKP_RULE_0042` → 4 implementations (P02, P03, P06, PG3), each with its own DQOps id.

### Example: SKP_RULE_0042 Through Fan-Out

**Conceptual rule:** "A material must have activity in the last two years"  
**SKP_RULE_ID:** SKP_RULE_0042 (shared)

**Project config systems:**
```yaml
system_aliases:
  SRCECCZ02100: P02
  SRCECCZ03100: P03
  SRCECCZ06100: P06
  SRCS4SG2100:  PG3
```

**After fan-out, the rule exists as 4 implementations:**

| Implementation | DQOps ID | View Names | Filter | Deploy To |
|---|---|---|---|---|
| **Lead (P02)** | 0001 | DQ_0001_P02_MARA_Activity_OptSel | `zSourceSystemID = 'SRCECCZ02100'` | SAP ECC P02 |
| **Sibling (P03)** | 0002 | DQ_0002_P03_MARA_Activity_OptSel | `zSourceSystemID = 'SRCECCZ03100'` | SAP ECC P03 |
| **Sibling (P06)** | 0003 | DQ_0003_P06_MARA_Activity_OptSel | `zSourceSystemID = 'SRCECCZ06100'` | SAP ECC P06 |
| **Sibling (PG3)** | 0004 | DQ_0004_PG3_MARA_Activity_OptSel | `zSourceSystemID = 'SRCS4SG2100'` | SAP S/4HANA PG3 |

**Key observations:**
- ✅ All 4 share `SKP_RULE_0042` (same business rule)
- ✅ Each has a unique `DQOps ID` (0001–0004) for deployment tracking
- ✅ View names include the system alias (P02, P03, P06, PG3)
- ✅ Filter value matches the system code (SRCECCZ02100, SRCECCZ03100, etc.)
- ✅ **Single spec** fed all 4 implementations; changes to the lead sync to siblings

**Tracker output example:**
```
ClientRef          | DQOps ID | ViewName                      | zSourceSystemID
SKP_RULE_0042      | 0001     | DQ_0001_P02_MARA_Activity... | SRCECCZ02100
SKP_RULE_0042      | 0002     | DQ_0002_P03_MARA_Activity... | SRCECCZ03100
SKP_RULE_0042      | 0003     | DQ_0003_P06_MARA_Activity... | SRCECCZ06100
SKP_RULE_0042      | 0004     | DQ_0004_PG3_MARA_Activity... | SRCS4SG2100
```

`excluded_systems` in the YAML lets you keep a system in the alias map (so view-name resolution
still works) but skip it during fan-out — useful for systems configured but not yet ready for
production.

The alias **value** is decoration. Editing `P02` to read `PROD-02` changes what appears in view
names and UI cells and changes nothing about where the rule deploys; the SQL filter always uses the
raw code. See [[std-studio-config-shape|Project Config Shape]] for the invariants.

## Profiling is different

Profiling rules **do not** fan out per system. They segment cross-system via `zSourceSystemID` in
the SELECT + GROUP BY instead. So a profiling rule has exactly **one** implementation, carrying two
views:

- PrfSel (record-level detail)
- PrfSum (aggregated summary)

One DQOps `rule_id`, one tracker row — the tracker's ViewType cell reads `PrfSel + PrfSum` rather
than naming a single view. A `systems` value on a profiling row becomes a
`WHERE zSourceSystemID IN (...)` filter **inside** that one view; it is not a fan-out trigger.

> [!warning] This corrects an earlier model
> The Studio once produced two sibling implementations for profiling, distinguished by view type.
> That model was replaced: one row → one spec → one DQOps ID. If you meet a tracker, an export or a
> test that expects two profiling implementations, it predates the correction. Recorded as
> CONFLICT-006.

See [[con-rule-types|Rule Types — Error, Info, Profiling]] for the full three-way split this
modifies.

## In the Studio

For each rule × system combination, the Studio:
- Appends the `zSourceSystemID = '<code>'` inclusion filter
- Adds a WHERE-clause comment `Limit to source system <alias>`
- Resolves the alias from the project's `system_aliases` map

## Related

- [[std-skp-rule-identifier-convention|SKP_RULE Identifier Convention]]
- [[std-zsourcesystemid-convention|zSourceSystemID Convention]]
- [[ref-system-aliases-map|System Aliases Map]]
- [[std-clientref-convention|ClientRef Convention]]
- [[std-view-naming-patterns|View Naming Patterns]]
- [[prc-fan-out-a-rule-per-system|Fan Out a Rule Per System]]
