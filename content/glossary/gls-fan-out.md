---
id: gls-fan-out
type: glossary
title: Fan-Out
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:con-multi-implementation-model
  - relates:prc-fan-out-a-rule-per-system
  - relates:gls-sibling-implementation
  - relates:gls-dqops-id
sources:
  - vault:studio-architecture/Studio — Bulk Processor & DQOps ID Invariants.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [multi-system, bulk]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

Expanding **one rule** into **one deployable implementation per source system**. One imported row
covering four systems fans out to four implementations, each with its own view name, its own
`WHERE zSourceSystemID = ...` filter and its own [[gls-dqops-id|DQOps id]].

## Usage

- **Error and Info rules fan out per system.** Scope precedence: the row's `systems` list →
  project [[gls-system-alias|system alias]] keys → the legacy `source_systems` list.
- **Profiling rules do not.** A Profiling rule is always exactly two implementations
  ([[gls-prfsel|PrfSel]] + [[gls-prfsum|PrfSum]]) sharing one rule id; its systems become an
  `IN (...)` filter instead.

`FAN OUT` is also the name of the workspace action that re-derives a rule across its siblings —
see [[gls-sibling-implementation]].
