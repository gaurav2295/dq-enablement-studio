---
id: gls-rule-package
type: glossary
title: Rule Package
domain: studio
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:ref-exporters

  - relates:gls-tracker
  - relates:gls-batch-summary
sources:
  - vault:studio-architecture/Studio — Exporters (Tracker-Deploy-Audit-Dashboard).md
  - dq-studio:docs/Studio_Overview.md
tags: [exports, deliverable]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

`DQ_Rule_Package.zip` — the shippable bundle a Studio run produces: the deploy script, per-rule
SQL, markdown specs, spec JSON, the [[gls-tracker|tracker]], [[gls-batch-summary|Batch_Summary]]
and per-rule unit tests.

## Usage

The package is the unit of delivery, which is why its **internal consistency** is a contract in
its own right: the SQL, the specs and the tracker must describe the same set of rules
(REQ-EXPORT-PACKAGE-INTEGRITY).

Two export contracts travel with it: a shipped rule should have been judged by the harness at
least once, and should not carry an unresolved `Fail` verdict.
