---
id: gls-walkability
type: glossary
title: Walkable / Walkability
domain: value-outcomes
audience: [consultant, lead]
level: practitioner
status: deprecated
links:
  - relates:con-outcome-hierarchy-l1-l5
  - relates:con-rule-provenance-model
  - relates:gls-provenance
sources:
  - bob-dq:CONTEXT.md
  - bob-dq:bob-dq-solution-spec.md
tags: [bob-dq, value-chain]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

Whether the chain can actually be **walked** from an outcome down to rules that measure it — an
outcome is walkable when every step between it and at least one DQ rule exists.

## Usage

Walkability is the test a candidate outcome has to pass before it joins the instrument: an outcome
with no lever, or a lever with no rules, is a slide, not a path.

It is also why rules exist with [[gls-provenance|provenance `derived`]] — authored to make a lever
walkable, never yet run in the field. The distinction is load-bearing: "this works" and "this
should work" are different claims, and a walkable chain built from derived rules is honest only
while it says so.
