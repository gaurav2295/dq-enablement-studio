---
id: gls-batch-summary
type: glossary
title: Batch_Summary
domain: studio
audience: [consultant, lead]
level: practitioner
status: review
links:
  - relates:ref-exporters
  - relates:ref-bulk-pipeline
  - relates:gls-tracker
  - relates:gls-parent-group
sources:
  - vault:studio-architecture/Studio — Bulk Processor & DQOps ID Invariants.md
tags: [exports, bulk, reconciliation]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

`Batch_Summary.xlsx` — the bulk run's own report, carrying a **Reconciliation** sheet (what went
in, what came out, what each rule produced) and a **Failed Rules** sheet.

## Usage

Reconciliation is the point: rules in, implementations out, and the arithmetic between them
visible. A four-system rule should appear as one [[gls-parent-group|parent group]] with four
implementations — a count that does not reconcile means a fan-out or dedupe defect, not a
reporting one.

Validator findings stamped during the run surface here too, which is how a batch shows what was
caught without anyone opening 400 SQL files.
