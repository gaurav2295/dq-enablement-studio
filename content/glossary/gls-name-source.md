---
id: gls-name-source
type: glossary
title: name_source / implication_source
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: deprecated
links:
  - relates:gls-implication
  - relates:gls-adm-rule-name
  - relates:std-implication-template
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, rules, provenance]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**How the rule's *text* came to exist.** Each takes one of two values — `catalogue` or
`generated`:

| Field | What it stamps |
|---|---|
| `name_source` | Where the [[gls-adm-rule-name]] came from |
| `implication_source` | Where the [[gls-implication]] came from |

## Usage

These are kept separate from [[gls-provenance]] on purpose: **writing a name for a real rule
does not make the rule less real**. A `field_proven` rule with a `generated` name is still a
rule that has run; a `derived` rule with a `catalogue` name has still never run.

Two independent axes, four honest combinations:

| provenance | name_source | What you may say |
|---|---|---|
| `field_proven` | `catalogue` | Ran in the field, named in the catalogue |
| `field_proven` | `generated` | Ran in the field, name written for this blueprint |
| `derived` | `catalogue` | Never run; borrows a catalogued name |
| `derived` | `generated` | Never run; authored for lever walkability |

> [!tip]
> When a reader challenges a rule name, check `name_source` before defending it. A `generated`
> name is a proposal and can be improved; a `catalogue` name is governed vocabulary and changing
> it needs an owner ruling.
