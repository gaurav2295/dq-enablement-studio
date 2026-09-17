---
id: gls-ai-sql-review
type: glossary
title: AI SQL Review
domain: ai-enhancement
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:ref-ai-static-validator-gate
  - relates:ref-bulk-pipeline
  - relates:gls-ai-enhance
  - relates:gls-local-re-derive
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
  - vault:studio-architecture/Studio — Bulk Processor & DQOps ID Invariants.md
tags: [ai, bulk, review]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The optional third step of bulk AI enhancement: send each rule's generated SQL to the model for
correction, then run the static validator on what comes back, retrying **once** if it finds a
High-severity issue and stamping the findings either way.

## Usage

It is **off by default in bulk**, deliberately: at batch scale it is the expensive step, and the
Audit page is the structural gate that catches the same class of defect for a fraction of the time
(a 96×4 batch drops from roughly 64–96 minutes to 16–24).

The retry budget is exactly one. A rule that still fails ships **with** its findings recorded, not
suppressed — the human reviewer is the final gate, not the model.
