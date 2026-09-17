---
id: gls-adm-rule-name
type: glossary
title: adm_rule_name
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-dq-rule
  - relates:std-rule-name-heuristics
  - relates:prc-write-a-quality-rule-name
  - relates:std-view-naming-patterns
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, rules, naming]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The business-readable, heuristics-compliant rule name** — the identifier of a
[[gls-dq-rule]] across the value methodology. At most **100 characters**.

`adm_rule_name` is **not** the technical ADM view name. `adm_view_name` is reserved for that and
**is not yet in use**.

## Usage

Because it is the identifier, `adm_rule_name` is what the rule repository, the canvas snapshot
and the explorer all join on. Two rules with the same name are the same rule; a renamed rule is
a new identity, so names are not edited casually.

"Heuristics-compliant" means it passes the naming heuristics — see
[[std-rule-name-heuristics]] for the enumerated set and [[prc-write-a-quality-rule-name]] for
how to write one that scores. The 100-character cap is **not** one of those scored heuristics:
it is the ADM field limit, enforced where the name is built, so a name can score full marks and
still be too long.

> [!warning]
> Do not put a technical view name into `adm_rule_name`, and do not populate `adm_view_name`
> speculatively. The separation is the reason a business-readable identifier can exist at all.
