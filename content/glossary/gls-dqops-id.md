---
id: gls-dqops-id
type: glossary
title: DQOps ID (zDQOpsID)
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:gls-fan-out
  - relates:ref-skp-assetupload-and-tracker-flow
sources:
  - vault:studio-architecture/Studio — Bulk Processor & DQOps ID Invariants.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [identifiers, bulk, skp]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The identifier that numbers a **deployable implementation** of a rule in DQOps — not the rule, the
implementation. One imported row that fans out to four systems produces four DQOps ids.

## Usage

Two invariants govern it, and they are the reason bulk output reconciles:

- **Counter-owned, never row-owned** (Error/Info). The id comes from a shared counter as each
  implementation is created; it is never derived from the import row's own number.
- **Profiling keeps its SKP→DQOps lock**, but routes the locked id through the same shared
  counter so it can never collide with a counter-issued id.

`zDQOpsID` is the column form of the same identifier where a view carries it. The tracker and the
SKP AssetUpload both key on it — see [[ref-skp-assetupload-and-tracker-flow]].
