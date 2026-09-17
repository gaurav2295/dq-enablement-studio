---
id: gls-cardinality
type: glossary
title: Cardinality
domain: rule-design
audience: [consultant]
level: foundation
status: review
links:
  - relates:con-profiling-concepts
  - relates:con-attribute-usage-analysis
  - relates:gls-schema-profile
  - relates:gls-grain
  - relates:gls-top-n-distribution
sources:
  - vault:dq-methodology/Profiling Concepts.md
  - dq-studio:docs/Studio_Overview.md
tags: [profiling, metrics]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**How many distinct values** a column holds. Low cardinality means a short code list; high
cardinality means an identifier or free text.

## Usage

Cardinality decides what a field *is* and therefore what can be done with it:

- **Low** — a coded attribute: distribution profiling and value-level rules make sense.
- **High** — a key or free text: distribution is meaningless, and the profiler skips it by
  threshold to keep a run fast.

A skewed high-cardinality primary key can look like an attribute if you judge it by top-N
coverage alone. True distinct count is the qualifier, whatever the skew says.
