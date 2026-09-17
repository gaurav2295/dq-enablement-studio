---
id: gls-first-writer-wins
type: glossary
title: First Writer Wins
domain: rule-design
audience: [developer]
level: advanced
status: review
links:
  - relates:std-pattern-status-field-check
  - relates:std-rule-pattern-library
  - relates:gls-slotfill
  - relates:gls-status-field
sources:
  - dq-studio:docs/RULE_PATTERNS.md
tags: [rule-pattern, convention]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The tie-break convention in slot filling: when a registry holds **more than one** entry matching a
slot's criteria, the **first entry in registry order** wins.

## Usage

The worked case is a vendor purchasing block, where the registry has both `LFA1.SPERM` (boolean)
and `LFA1.SPERQ` (code) at central level for the same category — the first entry is chosen and the
choice is deterministic, repeatable, and visible in the registry file rather than buried in code.

The consequence to remember: **registry order is a decision.** Re-ordering
`status_fields.json` silently changes which field a class of rules checks, so it is a reviewed
change, not a tidy-up.
