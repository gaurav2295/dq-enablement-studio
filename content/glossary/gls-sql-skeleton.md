---
id: gls-sql-skeleton
type: glossary
title: SQL Skeleton
domain: rule-design
audience: [developer]
level: practitioner
status: review
links:
  - relates:gls-rule-pattern
  - relates:gls-deterministic-shell
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - vault:studio-architecture/Studio — SQL Generator (OptSel-RptSel skeleton).md
tags: [generator, structure]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The fixed SQL frame a generator emits around a rule's variable parts — banner, `CREATE VIEW`, the
five output sections, `FROM`/`JOIN`, the `WHERE` exclusions — into which the derived logic is
placed.

## Usage

Skeletons are fixed, not something you edit directly: the branching they need (per-field
boolean-vs-code semantics, a variable number of OR'd parity pairs, comparator selection) doesn't
reduce to a simple template. What you can adjust without touching the skeleton is the part that
varies per rule: intent regexes and lexicons.

A skeleton with an unresolved slot is the honest [[gls-tbd-placeholder|TBD placeholder]] shell,
not a guess.
