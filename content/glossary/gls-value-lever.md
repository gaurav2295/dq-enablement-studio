---
id: gls-value-lever
type: glossary
title: Value Lever
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: deprecated
links:
  - prereq:gls-business-outcome
  - relates:prn-value-discipline
  - relates:con-value-chain
  - relates:gls-key-issue
  - relates:gls-propose-and-promote
sources:
  - bob-dq:CONTEXT.md
  - bob-dq:CLAUDE.md
  - rule-repo:README.md
tags: [bob-dq, value-chain, valuation]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The mechanism by which an outcome becomes money.** A value lever owns three things and is the
only construct in the chain that owns them:

- the **KPI** it moves,
- the **financial-impact type** (the shape of the benefit),
- the **value formula** that turns evidenced volume into currency.

There are **18 value levers**, defined in the BOA value library (`value-library.json`).

## Usage

**Money aggregates at the lever and only at the lever.** Outcomes do not carry currency; key
issues do not carry currency; rules do not emit currency. A `$` figure that cannot be traced to
a named lever is not a figure the instrument is allowed to show.

Lever availability is a function of client commitment and data access. Scope the claim to the
levers actually available and say which ones were not — see [[gls-coverage]].

> [!warning]
> Distinct lenses are never summed. Two levers reading the same population from different angles
> do not add up to a bigger number; presenting them as a total inflates.

## Say / never say

- **Say**: "this lever's formula turns the evidenced volume into an indicative range".
- **Never say**: a currency amount with no visible lever, as-of date and confidence label.

## Also defined by the rule repository

`value_lever` is one of the three linkage edges a rule-repo record carries
(`linkage.outcome_category`, `linkage.value_lever`, `linkage.key_issue_ids[]`), each edge stamped
with a `confidence` (0-1) and a `method` (`lexical` | `adjudicated`). The two definitions agree —
the repository stores *which* lever a rule reaches; bob-dq's value library defines *what the lever
is* and owns its KPI, financial-impact type and formula. **Empty linkage is a legitimate, honest
outcome** there: coverage gaps are reported, never papered over by forcing an edge.
