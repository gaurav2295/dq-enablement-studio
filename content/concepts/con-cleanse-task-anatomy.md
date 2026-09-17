---
id: con-cleanse-task-anatomy
type: concept
title: Cleanse Task Anatomy
domain: cleanse
audience: [consultant, lead]
level: practitioner
status: deprecated
links:
  - parent:con-cleanse-execution-model
  - relates:con-cleanse-action-categorization
  - relates:ref-cleanse-process-areas
sources:
  - cleanse-canvas:docs/PLAN-operational-layer.md
  - cleanse-canvas:docs/DATA-MODEL.md
tags: [methodology, cleanse-execution, operational]
created: 2026-08-20
updated: 2026-08-20
---

## What a Cleanse Task is

A Cleanse Task is a **granular, subset-scoped execution of one cleanse action on one object**.
It turns a single coarse flag on an object ("Obsolete this object's dead records") into
trackable increments that can each be planned, owned, and evidenced separately. See
[[con-cleanse-execution-model]] for how tasks sit under Object Actions and roll up into
higher-layer progress.

## Anatomy

| Field | What it captures |
|---|---|
| `actionId` / `objectId` | The Object Action this task executes against, and the object it belongs to. |
| `title` | A verb-led, human-readable description of the increment — the verb is fixed per action type (Obsolescence → "Obsolete", Deduplication → "Deduplicate", Enrichment → "Enrich", Profile & Assess → "Profile & Assess"), then the object, then the scope. |
| `scopeType` | `all` (covers the whole object under this action) or `subset` (a bounded slice). |
| `scopeCriteria` | The filter/definition of the subset — e.g. an inactivity threshold or a status condition — left blank for `all`-scoped tasks. |
| `recordsTarget` / `recordsCleansed` | Volume in scope, and progress against it — the numerator and denominator behind the roll-up arithmetic. |
| `status` | The six-state operational status (below). |
| `owner` | The person or team accountable for the task. |
| `wave` | An optional delivery wave/sprint tag for grouping tasks into delivery increments. |
| `plannedStart` / `plannedEnd` / `actualStart` / `actualEnd` | Planning and actual dates. |
| `dependsOnTasks` | Optional task-level sequencing — finer-grained than the object-level `dependsOn`, for ordering within (or across) a wave. |
| `evidence` | What proves the task is done — e.g. the DQ rule and report that surfaced and measured it. Auditability, not decoration. |
| `notes` | Free text. |

## Scope: all vs subset

Most tasks start life `scopeType: "all"` — one seed task per active Object Action, covering the
whole object under that action, so nothing falls through the cracks the moment task-level
tracking is introduced. Planning then **splits** an `all` task into multiple `subset`-scoped
tasks against the *same* Object Action as the work is actually broken down — for example,
turning "obsolete this object's dead records" into separately trackable increments such as
"inactive beyond a defined threshold" and "no transaction history," each with its own
`scopeCriteria`, owner, and volumes.

This is why `cleanseTasks` is a **separate, one-to-many array** keyed off the Object Action
rather than fields bolted onto the Object Action record: one action can and typically does
decompose into several tasks over the life of the engagement.

## Seeding

On first introducing task-level tracking, auto-generate exactly **one `scopeType: "all"` task
per active Object Action** (i.e. per action marked `applicable: yes`) as a baseline backlog.
This keeps prior coverage intact — every action that was already in scope gets a task — and
gives teams an immediate operational backlog to refine, rather than an empty board they have to
populate from scratch. Actions still marked `tbc` (applicability unconfirmed) get **no** seed
task; seeding one would manufacture false backlog before the action is even confirmed in scope.

## Operational status

```
not_started → ready → in_progress → blocked → in_review → complete
```

Richer than a simple pass/fail because a task is real, ongoing work: `ready` marks a task whose
prerequisites are satisfied and can start; `blocked` is a flag/side-state that can interrupt any
in-flight status and is surfaced prominently rather than buried in a dropdown; `in_review`
separates "the work is done" from "the work is confirmed done." Status should stay consistent
with volume progress (100% cleansed implies `complete`), but the two are tracked independently
so a task can be flagged `blocked` mid-way without losing its partial progress.

## The natural view: a Kanban board

Because a task is a discrete, ownable, stateful unit of work, the natural way to work the
operational layer is a **Kanban board**: columns = the status states, cards = tasks (title,
object · action, scope, owner, a records-progress bar, wave, blocked flag), with optional
swimlanes by object or process area and column headers that show WIP count plus a records
roll-up. Filters reuse the same dimensions as the tactical layer (SoW, process area, Business
Process Area, object, action, owner, wave, status), and dragging a card between columns is the
status-change interaction.

## Evidence

Every task's `evidence` field exists so a claimed percentage is never just an assertion — it
names the DQ rule, report, or artefact that measured and proves the increment's completion.
This carries the same evidence-first discipline through to the most granular layer of the
model: a programme-level roll-up is only as trustworthy as the tasks under it, and a task is
only trustworthy if its evidence field actually points at something.
