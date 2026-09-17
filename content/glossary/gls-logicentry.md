---
id: gls-logicentry
type: glossary
title: LogicEntry
domain: rule-design
audience: [developer]
level: advanced
status: review
links:
  - relates:gls-ziserrorflag
  - relates:gls-rule-pattern
sources:
  - vault:studio-architecture/Studio — Logic Builder Templates.md
  - dq-studio:docs/RULE_PATTERNS.md
tags: [spec, logic, data-model]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The spec object describing **one condition** of a rule's error logic — the element being tested,
its `table.field`, an operator and any value — that becomes part of the rule's
[[gls-ziserrorflag|zIsErrorFlag]] logic.

## Usage

`spec.logic` is the list of these entries, and it is the part of a spec a reviewer reads to answer
"what does this rule actually check?" without reading SQL.

A [[gls-rule-pattern|pattern]]-derived rule works differently: it carries the exact SQL text for
its condition, comment and all, instead of a field-by-field description. That is how a pattern
owns the exact SQL text that ships.
