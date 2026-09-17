---
id: gls-key-issue
type: glossary
title: Key Issue
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: deprecated
links:
  - relates:gls-business-data-driver
  - relates:gls-business-rule
  - relates:ref-key-issue-vocabulary
sources:
  - bob-dq:CONTEXT.md
  - rule-repo:README.md
  - cleanse-canvas:docs/CONTEXT.md
tags: [bob-dq, value-chain, key-issues]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**A recognisable, repeating problem in the data that holds an outcome back.** A key issue
carries five attributes:

| Attribute | What it records |
|---|---|
| Process area | Where in the business the problem lives |
| Objects | The data objects it touches |
| Readiness risk | What it threatens in a transformation |
| Cleanse action | The remediation shape it implies |
| Criticality | How badly it bites |

## Usage

The key issue is **the primary focus tier of the chain** — decided in bob-dq's ADR 0001, carried
here as [[prn-key-issues-primary-tier]] — the level at which
the conversation is most productive, because it is concrete enough to recognise and general
enough to price through a lever. Client-side it is spoken of as a
[[gls-business-data-driver]]; one key issue holds many [[gls-business-rule]] instances.

> [!important]
> **A key issue carries no currency.** It sits between the lever (which owns the money) and the
> rules (which own the evidence), and it borrows from neither.

## Say / never say

- **Say**: "this driver is what's holding the outcome back, and here are the rules that measure
  it".
- **Never say**: "this key issue is worth $X" — value belongs to the lever.

## The same term in two other places

- **Rule repository** — `linkage.key_issue_ids[]` on a rule record: which key issues this rule
  evidences, each edge carrying a `confidence` and a `method`. Same concept, stored from the rule's
  side.
- **Cleanse execution** — the *process area* and *cleanse action* attributes a key issue carries are
  the cleanse vocabulary's own terms, and the process-area taxonomies are **not reconciled** across
  the two lenses. See [[gls-process-area]] and CONFLICT-002.
