---
id: gls-business-rule
type: glossary
title: Business Rule
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-dq-rule
  - relates:gls-business-data-driver
  - relates:con-rule-types
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, value-chain, client-language]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The client-facing name for a DQ rule**: a plain statement of what "correct" looks like that a
computer can test.

One key issue holds many business rules.

## Usage

*Business rule* and [[gls-dq-rule]] are two names for the same object — the first for the room,
the second for the spec, the catalogue and the code. The pairing mirrors
[[gls-business-data-driver]] / key issue exactly: client language on the outside, internal
language on the inside, one record underneath.

Use *business rule* in the canvas, the value studio and the proposal. Use *DQ rule* in
dq-studio, in the rule repository and in anything that carries an `adm_rule_name`.

> [!tip]
> The test of a good business rule statement: read it aloud to a process owner. If they can say
> whether it is true of their business without asking what a field is, it is written correctly.
