---
id: con-cleanse-execution-model
type: concept
title: Cleanse Execution Model — Objects, Actions, Tasks
domain: cleanse
audience: [consultant, lead]
level: practitioner
status: deprecated
links:
  - relates:con-cleanse-action-categorization
  - relates:con-cleanse-task-anatomy
  - relates:ref-cleanse-process-areas
  - relates:con-dq-dimensions
  - relates:gls-crossover
  - relates:gls-sow
sources:
  - cleanse-canvas:docs/DATA-MODEL.md
  - cleanse-canvas:docs/PLAN-operational-layer.md
  - cleanse-canvas:docs/CONTEXT.md
  - cleanse-canvas:docs/DECISIONS.md
tags: [methodology, cleanse-execution, roll-up]
created: 2026-08-20
updated: 2026-08-20
---

## Why a three-layer model

Cleanse execution needs to answer three different questions at three different altitudes, and
one flat list of objects cannot answer all three at once:

| Layer | Question it answers | Unit |
|---|---|---|
| Strategic | Are we on track to business-ready data, and where's the risk? | Process area, SoW, Business Process Area, outcomes/KPIs |
| Tactical | What must be cleansed, in what order, by whom? | Object × Cleanse action, with dependencies |
| Operational | What's the next concrete piece of work, and is it done? | Cleanse Task (subset-scoped) |

Granularity increases downward and **progress rolls up**: task → action → object → process
area → programme. The tactical layer (object × action) is the plan-of-record; the operational
layer (task) is where execution is actually tracked; the strategic layer is the rolled-up
story told to leadership.

## The three entities

### Object

The thing being cleansed — a master-data, transactional, configuration, or document entity in
scope for the engagement. Carries the attributes that place it in the plan: which Statement of
Work (SoW) workstream it belongs to, which delivery phase it lands in, which process area it
aggregates into (see [[ref-cleanse-process-areas]]), and its prerequisite dependencies (below).

An object can span more than one SoW workstream — a **crossover** object — in which case a
primary/secondary ownership split is defined (typically by a data-readiness charter or
equivalent governing document) rather than assigning it to one workstream alone.

### Object Action

One record per **object + cleanse-action-type** combination. An object commonly needs more
than one kind of remediation, so this is modelled as its own layer rather than squashed into a
single flag per object:

- **`actionType`** — *what is done to the data*. See [[con-cleanse-action-categorization]] for
  the categorization and its operational vocabulary.
- **`method`** — `Source` or `Staged`: *where* the cleanse happens. `Source` cleanses the
  record directly in its system of record; `Staged` cleanses it in a staging/prep layer ahead
  of load. This is an attribute of the action, not the action itself, and defaults to `Source`.
- **`applicable`** — `yes` or `tbc`: whether this action-type genuinely applies to this object
  is sometimes still pending confirmation against a per-object execution guideline. No task
  should be seeded for a `tbc` action until it is confirmed `yes` — seeding on an unconfirmed
  applicability manufactures false backlog.
- **`status`** — a roll-up derived from the action's constituent tasks (see below), not a field
  set directly.

An object's **scope classification** (e.g. "in scope for cleanse rules" vs "profile & assess
only" vs "out of scope") is a separate attribute from `actionType` — scope says *how much* work
this object gets; `actionType` rows are the actual units of work once scope has admitted them.

### Cleanse Task

The granular, subset-scoped execution unit — one concrete slice of work against one Object
Action. See [[con-cleanse-task-anatomy]] for its full anatomy (scope, waves, records,
evidence).

## Object dependencies

Objects are sequenced by **prerequisite dependencies** — standard cross-object dependencies
(e.g. a transactional object depending on its master-data objects) plus any
engagement-specific customization. Each dependency records a **basis**:

- `assumed-sap` (or equivalent standard-model basis) — seeded from the standard object model,
  not yet validated by the workstream. Render these as provisional ("to confirm") until
  confirmed.
- `stated` — explicitly documented by the client or workstream lead.
- `none` — no known dependency.

Direction convention is consistent everywhere: **prerequisite → dependent** (the arrow points
at the object that depends on the other). Dependencies are aggregated upward too — an
area-to-area dependency edge is derived from the object-level edges that cross between two
process areas, carrying a count and a flag for whether every underlying edge is still
unconfirmed.

## Status model

**Cleanse Task** carries the richest status, because it is the layer where work is actually
performed:

```
not_started → ready → in_progress → blocked → in_review → complete
```

`blocked` is a flag/side-state surfaced prominently rather than a strict linear stage — a task
can be blocked from any in-flight state and unblocked back into it.

**Object Action** status is not set directly — it is **derived** by rolling up its tasks:

- all tasks complete → `complete`
- any task `in_progress` or `in_review` → `in progress`
- any task `blocked` → carries a `blocked` flag
- otherwise → `not_started`

This keeps the tactical layer honest: an action can only report a status its operational work
actually supports.

## Roll-up arithmetic

Progress is **quantitative and volume-weighted**, not just a count of green/amber/red flags:

- **Task % complete** = `recordsCleansed / recordsTarget` (0 if the target is 0 or unknown).
- **Action roll-up** = `Σ recordsCleansed / Σ recordsTarget` across its tasks, alongside an
  `x / y tasks complete` count.
- **Object roll-up** = volume-weighted across the object's actions' tasks.
- **Process-area / SoW / Business-Process-Area / programme roll-ups** = volume-weighted across
  their constituent objects.

Two disciplines apply at every level:

1. **Auditability** — every rolled-up percentage must be traceable back down to the underlying
   tasks that produced it. A dashboard tile is a claim; the tasks are the evidence.
2. **Directional vs measured** — where `recordsTarget` is not yet known (commonly because DQ
   profiling hasn't populated it yet), the roll-up is marked **directional**, not given false
   precision. Target volumes are a **data dependency on profiling**: until profiling data is
   loaded, `recordsTarget` is a manual estimate and every roll-up built on it inherits that
   caveat.

## What each layer looks like

Each layer has a natural primary view, and the three are navigable as one stack rather than
three unrelated reports:

- **Strategic — a dashboard.** Roll-up tiles by SoW, by process area, and by Business Process
  Area, each showing % records cleansed, tasks complete, status heat, records remaining and
  blocked count; outcome/KPI cards linked to the areas and BPAs that drive them; and a
  programme timeline of phases and waves with a burn-up of records cleansed over time against
  a forecast completion line.
- **Tactical — the plan-of-record canvas.** Object and action nodes show *task-derived*
  progress (a progress bar plus `x / y tasks`) rather than a single hand-set status flag, with
  a drill-to-tasks affordance on any node.
- **Operational — a Kanban board.** See [[con-cleanse-task-anatomy]].

Navigation runs both ways: **drill down** from an outcome, area or BPA tile into the filtered
tactical view and on into the operational board scoped to that object × action, and **roll up**
back out again. Filters (SoW, process area, BPA, object, owner, wave) persist across layers
wherever they still mean something, so the same slice of the programme can be followed from
leadership tile to individual task.

## The legacy boolean summary

An older, coarser representation kept an object-level boolean map (one flag per action-type,
true/false) purely for backward compatibility with tooling built before the Object Action /
Cleanse Task layers existed. It is **retained, not replaced** — a normalized summary view, not
the source of truth. The first-class `Object Action` / `Cleanse Task` layers are the model
going forward; anywhere the boolean summary and the first-class layers could disagree, the
first-class layers win.
