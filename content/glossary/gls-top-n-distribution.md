---
id: gls-top-n-distribution
type: glossary
title: Top-N Distribution
domain: rule-design
audience: [consultant]
level: foundation
status: review
links:
  - relates:con-profiling-concepts
  - relates:gls-schema-profile
  - relates:gls-cardinality
  - relates:gls-prfsum
sources:
  - dq-studio:docs/Studio_Overview.md
  - vault:dq-methodology/Profiling Concepts.md
tags: [profiling, metrics]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The value-level view of a column: its **most frequent values**, how often each occurs, each one's
share of the population, and where the long tail begins.

## Usage

It answers *"what values are actually in here, and in what mix?"* — the question that turns a
null-rate into a rule. A code that should have five values and has forty is a conformity rule
waiting to be written; a 92%-one-value column is usually a default nobody maintains.

High-cardinality columns are skipped by threshold. In deployed rules the same shape is what
[[gls-prfsum|PrfSum]] produces, as a percentage **within segment**.
