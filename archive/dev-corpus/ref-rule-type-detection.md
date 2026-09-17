---
id: ref-rule-type-detection
type: reference
title: Rule-Type Detection (business categories)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - parent:ref-local-deriver
  - relates:ref-logic-builder-templates
  - relates:ref-dqrulespec-data-model
  - relates:ref-logic-case-predicate-templates
  - relates:ref-field-matching
  - relates:ref-output-section-builders
  - relates:con-dq-dimensions
  - contrast:con-rule-types
sources:
  - vault:studio-architecture/Studio — Rule-Type Detection (business categories).md
tags: [studio, engine, derivation, methodology]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`_detect_rule_type` scans the lowercased rule name against an *ordered* list of regex patterns
and returns the FIRST match as one of six business categories — Consistency, Completeness,
Accuracy, Uniqueness, Timeliness, Relevancy (default Completeness) — a soft signal that shapes
the logic template only, NOT the canonical Error/Info/Profiling [[ref-dqrulespec-data-model]]
RuleType enum.

This is step 2 of the [[ref-local-deriver]] pipeline. The result is fed to
[[ref-logic-builder-templates]] to pick which `LogicEntry` template to emit. It does **not**
decide whether the rule generates an OptSel/RptSel pair vs an InfSel — that distinction is the
*canonical* `RuleType`, which comes from the caller's `report_type` argument, never from the rule
name.

## What it does

`_detect_rule_type(rule_lower: str) -> str` walks `_RULE_TYPE_PATTERNS` (a `List[tuple[str,
re.Pattern]]`) top to bottom and returns the category of the first pattern whose `.search()`
hits. No match → `"Completeness"`.

The ordering is load-bearing: **Consistency is checked before Completeness on purpose**, so that
phrasing like *"must have consistent X"* classifies as Consistency (the `must have consistent`
pattern wins) rather than being swallowed by Completeness's broad `must have` pattern.

## The categories & patterns (first-match wins, in order)

| # | Category | Phrasing patterns (regex alternations, IGNORECASE) |
|---|---|---|
| 1 | **Consistency** | `must be consistent` · `must have consistent` · `consistent \w+ (and\|with)` · `must match` · `must equal` · `must align` · `must be aligned` · `aligned with` · `consistent with` · `consistency` |
| 2 | **Completeness** | `must be populated` · `must have` · `must not be empty` · `must not be blank` · `must contain` · `completeness` |
| 3 | **Accuracy** | `must be valid` · `must be correct` · `must be accurate` · `accuracy` |
| 4 | **Uniqueness** | `must be unique` · `must not be duplicate` · `uniqueness` |
| 5 | **Timeliness** | `must be current` · `must have activity` · `within.*month` · `timeliness` |
| 6 | **Relevancy** | `must be relevant` · `must be active` · `relevancy` |
| — | *default* | no match → **Completeness** |

> [!important] Category ≠ canonical RuleType
> These six are the **legacy business categorisation** used only to *shape* the logic template.
> The canonical `RuleType` enum is **Error / Info / Profiling** ([[con-rule-types]]) and is
> supplied by the caller's `report_type`. A rule whose name reads "Accuracy" can still be an Info
> rule (no `zIsErrorFlag`) — the two axes are independent. Do not conflate them.

## How the category drives logic

[[ref-logic-builder-templates]] branches on the returned category:

- **Completeness** → `"<desc> is Missing"` (NULL / `''` / `'0'` check).
- **Consistency w/ ≥2 matched fields** → comparison: `"<X.desc> must align with <Y.desc>"`,
  predicate `X.tf <> Y.tf`.
- **Consistency w/ 1 match** → `"<desc> is Inconsistent"` (values match across org levels).
- **Accuracy / Uniqueness / Timeliness / Relevancy** → generic `"<desc> Check"` with `1 - If
  condition fails / 0 - If condition passes`.

So Consistency is the only category that meaningfully forks the template; the latter four
collapse to the same generic check. The flag emitted is always INTEGER `1` (defect) / `0` (pass)
— see [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]].

## Inputs & outputs

- **In:** `rule_lower` — the rule name lowercased.
- **Out:** one of the six category strings (default `"Completeness"`).
- **Consumed by:** `_build_logic` (template selection) and `_build_description` (Completeness vs
  other `condition_text`/`check_text`).
- **Independent of:** the canonical Error/Info/Profiling decision (driven by `report_type`).

> [!note] Implementation status — Resolved 2026-07-01
> The pattern table above is the **canonical** set (`core/local_deriver.py:77-161`), and the app
> now implements it in full. The earlier `syniti-methodology-studio-v1.0-20260507` build carried
> a *narrower* Consistency pattern — `must be consistent | must match | must equal | must align |
> consistency` — missing `must have consistent`, `consistent \w+ (and|with)`, `must be aligned`,
> `aligned with`, and `consistent with`, so "must have consistent X" fell through to
> **Completeness**, exactly the mis-classification the ordering is meant to prevent. That deriver
> gap has been closed as part of the KNOWN-ISSUES cleanup shipped 2026-07-01 (see
> [[ref-local-deriver]]): `_RULE_TYPE_PATTERNS` now carries all ten Consistency alternations, so
> "must have consistent X" correctly classifies as Consistency. All six categories now match the
> canonical set.

## Source

- `core/local_deriver.py:77-161` — `_RULE_TYPE_PATTERNS` (the ordered list) + `_detect_rule_type`
  (first-match loop, default `"Completeness"`).
- Detail: `knowledge-mining/derivation-spec.md` §2 (step 2) and §4 (pattern enumeration).

## Related

[[ref-local-deriver]] · [[ref-logic-builder-templates]] · [[ref-field-matching]] ·
[[ref-dqrulespec-data-model]] · [[ref-logic-case-predicate-templates]] ·
[[ref-output-section-builders]] · [[con-dq-dimensions]] · [[con-rule-types]]
