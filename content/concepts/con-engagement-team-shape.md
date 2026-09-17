---
id: con-engagement-team-shape
type: concept
title: Engagement Team Shape
domain: delivery
audience: [consultant, lead]
level: practitioner
status: deprecated
sources:
  - bob-dq:bob-dq-solution-spec.md (§1.7 Resourcing & enablement)
  - bob-dq:bob-dq-solution-spec.md (§1.5 Implementation plan)
links:
  - prereq:con-engagement-phases
  - relates:prc-estimate-blueprint-effort
  - relates:con-solution-components
  - relates:prc-assess-and-discover
  - relates:con-value-chain
  - relates:gls-work-lanes
  - relates:gls-gdc
  - relates:gls-capacity-check
  - relates:gls-time-to-value
  - relates:gls-internal-workbench
tags: [bob-dq, delivery, resourcing, team, enablement]
created: 2026-08-20
updated: 2026-08-20
---

## What it is

The **shape** of a #bob-dq engagement team — which roles exist, at what allocation, and which lane
each one belongs to. This unit is the shape; the **arithmetic that sizes it** is
[[prc-estimate-blueprint-effort]]. Read them together: shape without maths is a wish, maths without
shape produces a number nobody can staff.

The shape is deliberately small. It has to be — the offering promises a bounded, low-friction
engagement, and a team that needs a governance layer to coordinate itself has already broken that
promise.

## Roles per client

Working assumption, pending a formal resourcing decision.

| # | Role | Allocation | Notes |
|---|---|---|---|
| 1 | **DP** — non-specialised | **No hours allocated — investment** | Delivery, Presales or AE |
| 2–3 | **Working assumption: hybrid C4** | **75% · C4** | Single blended role (qualitative + coordination), replacing the C5+C3 split as the ROM base |
| — | *Alternative retained:* Lead 25% C5 + delivery 50% C3 | — | Fallback for engagement #1 while artefacts harden |
| 4 | **GDC Lead Executor** | Sized per engagement | Execution lead in the [[gls-gdc|GDC]] |
| 5 | **GDC Capacity** | Sized per engagement | Scalable execution capacity |

Two things to read out of that table.

- **The blended C4 is a decision, not a rounding.** The earlier shape split a senior lead (C5) from
  a delivery consultant (C3). Collapsing them into one blended role is what makes the ROM base
  stable across engagements — one rate, one allocation, one person accountable for both the
  qualitative work and the coordination.
- **"No hours — investment" is a real commitment.** The DP role carries no allocated hours because
  the opportunity-start work is an investment in the pipeline, not billable delivery. It still needs
  a governance owner; unowned investment time is the first thing to disappear under pressure.

## The two lanes

The team splits across the [[gls-work-lanes|two work lanes]], and they are costed separately.

| Lane | Who | What they do | Sized by |
|---|---|---|---|
| **Qualitative** | DP + blended C4 | Outcome selection, facilitation, valuation, business ownership, the readout | Engagement shape and duration |
| **Quantitative** | GDC lead executor + GDC capacity | Rule execution, deployment, results | [[prc-estimate-blueprint-effort]] — rules per person-week, object and rule complexity factors |

Conflating the lanes is the standard resourcing error: the quantitative lane scales with the rule
cart, the qualitative lane scales with the number of outcome domains and business owners. They do
not move together, and a single blended headcount number hides that.

## How this becomes costable now

The canvas console **computes ROM and timeline from these assumptions** — team shape, duration and
scope breadth are editable variables, and every figure is labelled with the assumption behind it.
The formal resourcing and duration decisions will overwrite the defaults; **the mechanism survives
the decision**. That is why an unresolved decision does not block quoting: the assumption is
visible, changeable and attributed, rather than buried.

> [!warning]
> Internal day rates never reach a client surface. The console shows client anchors and hosting
> only; rates live as pre-session constants behind the interface. See [[std-client-vocabulary]].

## Enablement that the shape assumes

The team shape only works if five capabilities exist in the field.

| # | Need | Audience | Form |
|---|---|---|---|
| E1 | Run the outcomes canvas live with a client | GTM / AE / Presales | Guided walkthrough + demo script |
| E2 | Scope and quote from canvas output | GTM + Finance-facing | ROM guardrails + worked example |
| E3 | Execute `#1-d3p` and `#2-rules` | Central delivery + GDC | Runbook + dq-studio training |
| E4 | Populate and publish via vector-studio | Delivery + outcome lead | Template + method rules |
| E5 | Handle *"are these numbers real?"* | Everyone client-facing | Live drill-through demo |

> [!important]
> **Enablement principle:** if a component needs a training course, it is too complex for the
> timeline this offering promises. Enablement should be **reference material plus one demo**.

E5 has its own procedure — [[prc-handle-the-cold-room]] — because it is the capability that decides
whether the blueprint survives contact with a sceptical room.
