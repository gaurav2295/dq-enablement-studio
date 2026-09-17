---
id: gls-vector-studio
type: glossary
title: vector-studio
domain: delivery
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-dq-studio
  - relates:qa-vector-studio-input-sheet
sources:
  - bob-dq:CONTEXT.md
  - bob-dq:CLAUDE.md
tags: [bob-dq, instruments, blueprint]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**Elevates execution results into the finished blueprint.** It consumes the evaluation sheet;
**it never authors SQL.**

## Usage

vector-studio is the end of the chain — the "up to prove" direction. Where
[[gls-bob-canvas]] walks *down* from an outcome to the rules, vector-studio walks the evidenced
results back *up* into a valued, prioritised, sequenced blueprint.

Its input is a sheet, not a database. This is what keeps the tool clear of customer systems: it
ingests result sheets only.

> [!warning]
> "Never authors SQL" is a boundary, not a limitation. If a rule needs changing, the change is
> made in [[gls-dq-studio]] — which owns the only iteration loop — and re-executed, never patched
> at the presentation end.
