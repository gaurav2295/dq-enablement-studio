---
id: gls-implication
type: glossary
title: Implication
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:std-implication-template
  - relates:prn-fetch-check-return
  - relates:prc-format-an-implication
  - relates:gls-dq-rule
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, rules, implication]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**What it costs the business when a rule fails.** Two to three sentences, roughly **40 words**,
covering business, financial, operational or compliance impact.

This is dq-studio's definition; the value methodology **uses** it and does not redefine it. See
[[std-implication-template]] for the authoring template and [[prc-format-an-implication]] for
the procedure.

## Usage

The implication is the sentence that carries a rule up into the outcome conversation — it is
the bridge between a failing record and a business consequence a stakeholder recognises.

Distinct from `description`, which is the longer **Fetch / Check / Return** block describing what
the rule does mechanically.

| Field | Length | Answers |
|---|---|---|
| `implication` | ~40 words, 2–3 sentences | What does it cost when this fails? |
| `description` | Fetch / Check / Return block | What does this rule actually do? |

> [!warning]
> An implication states consequence, not currency. It never contains a `$` figure — that belongs
> to the [[gls-value-lever]] with its as-of date and confidence label.
