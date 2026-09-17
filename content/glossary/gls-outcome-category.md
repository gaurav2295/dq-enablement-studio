---
id: gls-outcome-category
type: glossary
title: Outcome Category
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: deprecated
links:
  - parent:gls-business-outcome
  - relates:gls-vector-studio
  - relates:con-outcome-hierarchy-l1-l5
sources:
  - bob-dq:CONTEXT.md
  - rule-repo:README.md
tags: [bob-dq, value-chain, outcomes]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The value-library classification a business outcome exports.** Every
[[gls-business-outcome]] maps to one of the BOA value library's **six** outcome categories
through the `OUT_CAT` map.

## Usage

The category is what travels: it is how an outcome chosen in the client's own words lands in the
BOA engine's vocabulary without either side having to rename anything. It also renders as a
sub-label on the outcome card, so the room can see the classification without it dominating the
card.

> [!note]
> Six categories, eighteen levers, six named outcomes plus one candidate — the three lists are
> different sizes on purpose. The category is a coarse bucket for the engine, not a second
> outcome list.

## Also defined by the rule repository

A rule-repo record carries `linkage.outcome_category` — the same six-category vocabulary, applied
to a rule rather than to an outcome, with a `confidence` and a `method` on the edge. The category
list itself is owned by the BOA value library (the `OUT_CAT` map); neither the repository nor an
agent may coin a new one.
