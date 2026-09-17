---
id: gls-process-area
type: glossary
title: Process Area
domain: cleanse
audience: [consultant, lead]
level: practitioner
status: review
links:
  - relates:ref-cleanse-process-areas
  - relates:gls-business-process-area
sources:
  - cleanse-canvas:docs/CONTEXT.md
  - cleanse-canvas:docs/DATA-MODEL.md
  - bob-dq:bob-dq-solution-spec.md
tags: [taxonomy, cleanse, value-chain]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**Two different things share this name, and they are not reconciled.**

| Source | What "process area" means there |
|---|---|
| Cleanse execution (data-cleanse-canvas) | A **cleanse-delivery grouping** of objects that get worked together because they sit in the same functional neighbourhood — twelve of them in the worked example, the aggregation tier of the cleanse-atom view. |
| Value/outcomes (bob-dq) | The **L3 tier of the L1–L5 outcome hierarchy** — the process owner's altitude, between the VP-level lever and the data objects. Also one of the five attributes a key issue carries. |

## Usage

Both are legitimate in their own lens; the failure mode is assuming the names line up. A cleanse
process area is a *delivery convenience*; an outcome-hierarchy process area is meant to mirror how
the business describes itself.

> [!warning]
> Reconciling the two taxonomies is an open CoE decision — logged as **CONFLICT-002** in
> `docs/CONFLICTS.md`. Until it is decided, say which lens you mean.

Coarser still, and separate again, is the [[gls-business-process-area|Business Process Area]].
