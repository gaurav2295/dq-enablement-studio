---
id: gls-business-data-driver
type: glossary
title: Business Data Driver
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-business-rule
  - relates:std-client-vocabulary
  - relates:qa-business-data-driver-key-issue
sources:
  - bob-dq:CONTEXT.md
  - bob-dq:CLAUDE.md
tags: [bob-dq, value-chain, client-language]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The client-facing name for a key issue.** The same thing, said in the room's language.

There is no second data model behind the driver — it is a translation, and the translation lives
in exactly one place: the `TERMS` map in the canvas prototype.

## Usage

Use *business data driver* in any client-facing surface; use *key issue* internally, in specs
and in the data model. Because both names point at one record, changing the wording is a `TERMS`
edit, never a schema change.

> [!warning]
> Do not maintain a second list of drivers alongside the key issues. Two lists drift; the whole
> point of the single `TERMS` map is that they cannot.

Vocabulary here is **governed**: driver names, and their mapping to value levers, are created or
changed only by an explicit owner ruling (ADR 0001 and the rule repository's ADR 0002). Agents
may propose; they never invent vocabulary autonomously.
