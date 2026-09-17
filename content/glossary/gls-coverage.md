---
id: gls-coverage
type: glossary
title: Coverage
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: deprecated
links:
sources:
  - bob-dq:CONTEXT.md
  - bob-dq:CLAUDE.md
tags: [bob-dq, evidence, honesty]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**Which outcomes *could be evidenced* given the scope in play.**

Coverage is **not a completeness score**, and is never presented as one.

## Usage

Coverage answers a scoping question, not a quality question: with the rules, objects and data
access currently in scope, which [[gls-business-outcome]] entries can be backed by evidence at
all? An outcome outside coverage is not failing — it is simply not being evidenced by this
engagement.

Because lever availability depends on client commitment and data access, coverage moves as scope
moves. Scope the claim to the levers you have and **say which ones you did not have**.

## Say / never say

- **Say**: "four of the six outcomes are covered by the rules in scope; the other two need
  billing data we don't have access to".
- **Never say**: "we have 67% coverage" — a percentage invites the reader to hear a completeness
  or quality score, which is exactly what coverage is not.

> [!warning]
> Coverage is also not the same as [[gls-value-potential]]. Coverage says *what can be shown*;
> value potential says *how big what was shown is*.

## A second, unrelated sense — see CONFLICT-018

The Studio uses "coverage" for something else entirely, and computes it as a ratio:

- **System coverage** in the audit engine — whether a rule family spans every expected source
  system (ref-audit-engine).
- **The coverage qualifier** in Attribute Usage — the share of a column's rows captured by its
  top-K values, thresholded to decide whether a column is a low-cardinality attribute at all
  ([[con-attribute-usage-analysis]]).

Both are legitimate engineering measures. Neither is the client-facing word above, and the two must
not meet in the same sentence — a percentage labelled "coverage" in front of a client reads as the
completeness score this term explicitly is not. Logged as **CONFLICT-018**.
