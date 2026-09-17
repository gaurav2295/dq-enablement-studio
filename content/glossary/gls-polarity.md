---
id: gls-polarity
type: glossary
title: Polarity
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - parent:std-pattern-status-field-check

  - relates:gls-status-field
  - relates:gls-ziserrorflag
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - dq-studio:knowledge/methodology/rule_patterns.json
tags: [rule-pattern, logic]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

Which state of a field is **the error**. A **positive**-polarity rule says the field must be set
(error when blank); a **negative**-polarity rule says it must not be set (error when set).
Detected from a `must` / `should` + optional `not` phrase in the rule name.

## Usage

Polarity and field **type** together decide the predicate, and neither can be skipped:

| Type | Positive (must have) | Negative (must not have) |
|---|---|---|
| boolean | error when `COALESCE(f,'') <> 'X'` | error when `COALESCE(f,'') = 'X'` |
| code | error when `COALESCE(f,'') = ''` | error when `COALESCE(f,'') <> ''` |

Getting polarity backwards produces a rule that runs perfectly and reports exactly the wrong
population — the failure mode that is hardest to spot in a review, because the SQL is valid.
