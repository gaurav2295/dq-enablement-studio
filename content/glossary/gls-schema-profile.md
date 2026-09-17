---
id: gls-schema-profile
type: glossary
title: Schema Profile
domain: studio
audience: [consultant]
level: foundation
status: review
links:
  - relates:con-studio-capabilities
  - relates:con-profiling-concepts
  - relates:gls-cardinality
  - relates:gls-top-n-distribution
sources:
  - dq-studio:docs/Studio_Overview.md
  - vault:studio-architecture/Studio — Schema Profiler (engine).md
tags: [profiling, capability]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The per-field **census** of a set of tables — row counts (raw vs active), null and populated
rates, distinct [[gls-cardinality|cardinality]], min/max and length statistics, and a derived
signal for what each field actually holds.

## Usage

The Schema Profile runs **before** anyone writes a rule: it turns "we think this field is mostly
populated" into a measured baseline, so scoping, estimation and rule design start from evidence.

It is generated as pure MS SQL writing into staging tables, so it executes inside the client's own
environment with **no data leaving it** — the reason it can run on day one, before any data-sharing
question is settled. The same run produces the value-level
[[gls-top-n-distribution|Top-N distribution]].
