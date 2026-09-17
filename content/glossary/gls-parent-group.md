---
id: gls-parent-group
type: glossary
title: Parent Group
domain: studio
audience: [developer]
level: practitioner
status: review
links:
  - relates:ref-bulk-pipeline
  - relates:gls-sibling-implementation
  - relates:gls-fan-out
sources:
  - vault:studio-architecture/Studio — Bulk Processor & DQOps ID Invariants.md
tags: [bulk, dedupe]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The set of [[gls-sibling-implementation|sibling implementations]] that came from one import row —
the unit of **dedupe** in the bulk pipeline.

## Usage

The parent group is why bulk AI cost scales with *rules*, not with *implementations*: the rule-name
enhance runs **once per parent group** and siblings inherit the result by textual swap of the
system token. Reconciliation counts, too, are grouped by parent so a four-system rule reads as one
rule with four implementations rather than four unrelated rows.
