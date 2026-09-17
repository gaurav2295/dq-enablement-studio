---
id: con-engagement-phases
type: concept
title: The Three Engagement Phases — Prepare, Execute, Present
domain: delivery
audience: [consultant, lead]
level: foundation
status: review
sources:
  - bob-dq:bob-dq-solution-spec.md (§1.5 Implementation plan)
  - bob-dq:bob-dq-solution-spec.md (§1.4 Solution components)
  - bob-dq:business-outcomes-blueprint-solution-overview.md (§8 Delivery Approach & Timeline)
links:
  - relates:gls-project-spec
  - relates:gls-adm
  - relates:gls-iteration-loop
  - relates:gls-time-to-value
tags: [bob-dq, delivery, phases, entry-exit]
created: 2026-08-20
updated: 2026-08-20
---

## What it is

The implementation plan of a #bob-dq engagement: **three phases**, each a named set of
[[con-solution-components|solution components]] with explicit **entry and exit criteria**. A simple
approach, leveraging application components as required. The criteria are the point — each phase
ends on a *condition*, not on a date, and the conditions are what make the promised timeline hold.

Client-facing material describes the same delivery arc at a finer grain — **Mobilise → Assess →
Aggregate → Value → Elevate → Handover** — where the middle four are the method stages of
[[con-value-chain]]. Internally, plan against the three phases below.

## `#phase1-prepare`

| | |
|---|---|
| **Components** | `#0-sc-engage` · `#0-engage-info-gathering` · `#1-d3p` |
| **Purpose** | Get data in and understood; capture process-vs-value context without burning client goodwill |
| **Entry** | Signed SOW · ADM-M hosting chosen · named client data executor · **handed-over project spec** |
| **Exit** | Data provisioned, prepared, profiled; profiling output reviewed |
| **Key property** | **The timeline of #bob-dq does not start until this phase is complete** |

The key property is a deliberate insulation, not an excuse: provisioning drag is the single most
common cause of a slipped assessment, so the clock is defined to start after it. Say this at
mobilisation, not when the date slips. The work of this phase is [[prc-assess-and-discover]].

## `#phase2-execute`

| | |
|---|---|
| **Components** | `#2-rules` · `#3-validate-improve` · **mockup** `#4-present-vector-studio` |
| **Purpose** | Derive, deploy and execute the outcome-linked rule set; stabilise results; stand up the presentation mockup in parallel |
| **Entry** | Profiled data available; outcome selection confirmed in the project spec |
| **Exit** | Rule set stable · results accepted as evidence base · contract validated · **mockup agreed** |
| **Why mockup here** | It makes phase 3 a **population exercise, not a design exercise** — this is how the timeline holds |

> [!important]
> **The agreed mockup is a phase-2 exit criterion, not a phase-3 activity.** If it slips into phase
> 3, phase 3 becomes a design exercise and the timeline is gone. This is the single most commonly
> attacked exit criterion in the plan — hold it.

## `#phase3-present`

| | |
|---|---|
| **Components** | `#4-present-vector-studio` |
| **Purpose** | Elevate DQ results and the Business Outcomes Summary into the published blueprint |
| **Entry** | Accepted evidence base · agreed mockup · assumptions sheet populated · financial anchors available |
| **Exit** | Blueprint published · readout delivered · next steps costed and owned |

Note what the entry criteria imply: the **assumptions sheet is populated before phase 3 starts**,
and financial anchors are already available. Valuation is not something the consultant improvises in
the last week — see [[prn-value-discipline]]. What leaves the engagement is
[[ref-deliverables-inventory]]; the bar it must clear before it ships is [[prc-qa-a-blueprint]].

## What the client has to bring

Four prerequisites are assumed by the plan and belong in the SOW, not in a mid-engagement
conversation.

- System access or extract capability
- A **named data-team executor** (the client runs the bundle; Syniti does not touch the estate)
- A **named business owner per outcome domain** (for the Elevate/prioritisation step)
- Access to the **financial anchors** the valuation stage needs

Assumptions and exclusions are stated explicitly at the same point. That statement is what prevents
scope disputes later.

## Reading the phases against the components

| Phase | Components active | The question it answers |
|---|---|---|
| Prepare | Engage · info-gathering · d3p | *Do we understand the estate, and is the data ready?* |
| Execute | Rules · validate-improve · presentation mockup | *Are the results stable and accepted as evidence?* |
| Present | Present | *Is the value elevated, prioritised, owned and published?* |

Durations are engagement variables, sized from the rule cart rather than assumed — see
[[prc-estimate-blueprint-effort]] for the arithmetic and [[con-engagement-team-shape]] for the team
the arithmetic sizes.
