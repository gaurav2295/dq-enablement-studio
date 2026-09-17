---
id: gls-intent-regex
type: glossary
title: Intent Regex
domain: rule-design
audience: [developer]
level: advanced
status: review
links:
  - parent:gls-rule-pattern
  - relates:std-rule-pattern-library
  - relates:std-pattern-status-field-check

sources:
  - dq-studio:knowledge/methodology/rule_patterns.json
  - dq-studio:docs/RULE_PATTERNS.md
tags: [rule-pattern, detection]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

One of the regular expressions in a [[gls-rule-pattern|pattern's]] `intent` list, matched
case-insensitively against the **rule name** to decide whether that pattern claims the rule.

## Usage

Two conventions carry all the weight:

- **AND semantics.** *Every* regex in the list must match. A single keyword is never enough —
  that is what stops an ordinary block rule from misfiring as a parity rule.
- **First match wins**, so array order is meaningful: the narrower pattern is listed first and the
  broader one last.

When two loose signals could be satisfied by different clauses of the same sentence, **couple them
positionally** (require one within N characters of the other) — the lesson from a real
misfire on a shortened parity rule name. Validate a new regex against the whole test corpus, not
just its own pattern's cases.
