---
id: gls-internal-workbench
type: glossary
title: Internal Workbench (Engagement mode)
domain: delivery
audience: [consultant, lead]
level: foundation
status: deprecated
links:
  - contrast:gls-client-instrument
  - relates:gls-solution-proposal
  - relates:gls-work-lanes
  - relates:gls-dq-studio
  - relates:prc-estimate-blueprint-effort
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, instrument, tiers, internal]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The Engagement mode** — internal id `proposal`, display name renamed — and the only tier that
carries commercials.

It holds intake, sizing, documents and the dq-studio handover.

## Usage

The workbench is where hours, rates, capacity and investment live, which is precisely why it is
not part of [[gls-client-instrument]]. Its **one client-visible artefact** is the finished
"Solution Proposal — Detailed" document, presented full-screen — see
[[gls-solution-proposal]].

> [!note]
> The internal id is still `proposal` while the display name is *Engagement*. When reading code
> or a spec, do not assume `proposal` means the Solution Proposal mode; check which of the two
> is meant.

The [[gls-work-lanes]] capacity check lives here: internally the lanes carry hours and a live
check, and the rule is *do not quote a duration the capacity check refuses*.
