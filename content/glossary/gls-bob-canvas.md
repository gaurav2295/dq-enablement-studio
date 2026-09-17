---
id: gls-bob-canvas
type: glossary
title: bob-canvas
domain: delivery
audience: [consultant, lead]
level: foundation
status: deprecated
links:
  - relates:gls-dq-studio
  - relates:gls-client-instrument
  - relates:gls-business-outcome
  - relates:gls-snapshot
  - relates:prc-run-the-blueprint-room
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, instruments, canvas]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The prototype.** It defines the outcome and exports the project spec.

Five modes: Introduction, Canvas, Value Studio, Proposal, Rule Explorer.

## Usage

bob-canvas is the front of the chain: the client picks a [[gls-business-outcome]] here, and what
leaves is a project spec that [[gls-dq-studio]] imports. It authors no SQL and runs no rules.

When the rule server is not running it reads from an embedded [[gls-snapshot]] of the rule graph.

> [!warning]
> `bob-canvas` is an **internal tool name**. It never appears in front of a client — see
> [[gls-client-instrument]]. In the room it is *the canvas*.

> [!note]
> **The source counts modes two ways.** This five-mode list names *Proposal*; the tier
> vocabulary names six — five client modes (with *Proposal* written out as
> [[gls-solution-proposal]]) plus the internal *Engagement*, whose id in code is `proposal`.
> So the word `proposal` is doing two jobs, and which one is meant has to be read from context:
> in the mode list it is the client-facing Solution Proposal; in code it is Engagement. Recorded
> as it stands rather than reconciled — see [[gls-internal-workbench]].
