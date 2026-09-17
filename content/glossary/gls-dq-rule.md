---
id: gls-dq-rule
type: glossary
title: DQ Rule
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-business-rule
  - relates:gls-adm-rule-name
  - relates:con-rule-types
sources:
  - bob-dq:CONTEXT.md
  - bob-dq:CLAUDE.md
tags: [bob-dq, value-chain, rules]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The internal name for a [[gls-business-rule]]** — the same object, addressed by the people who
build and run it. Identified by `adm_rule_name`.

## Usage

In the value methodology the DQ rule is the bottom of the chain and the only tier that touches
data. It certifies counts and populations; it never emits currency. The step from an evidenced
volume to a `$` figure happens at the [[gls-value-lever]], through a documented assumption owned
separately from the SQL.

Rules reaching the value chain carry two provenance facts that the chain depends on:
[[gls-provenance]] (did this rule ever run in the field?) and [[gls-name-source]] (where did its
text come from?).

> [!important]
> *No SQL ever emits a currency figure.* Volumes are not value. This separation is what lets the
> instrument give a number and show its provenance in the same breath.

For rule anatomy, types and scoring inside the Studio, see [[con-rule-types]] and
ref-dqrulespec-data-model.
