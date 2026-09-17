---
id: gls-dq-score
type: glossary
title: DQ Score
domain: rule-design
audience: [consultant, lead]
level: practitioner
status: review
links:
  - relates:gls-defect-rate
  - relates:con-studio-capabilities
  - relates:con-dq-dimensions
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
  - dq-studio:docs/Studio_Overview.md
tags: [scoring, metrics]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

An aggregate quality figure rolled up from rule-level [[gls-defect-rate|defect rates]] — by
object, by domain, by dimension or by system.

## Usage

A DQ score is a **summary of rules that ran**, never a statement about data the rules do not
cover. Two rules of hygiene:

- Say what is in the roll-up. A score computed over eight rules on one object is not "the
  customer data quality score".
- Do not mix Profiling output into it — Profiling has no pass/fail to contribute.

The same caution applies as to [[gls-coverage|coverage]]: a single percentage invites the reader
to hear a completeness claim the number cannot support.
