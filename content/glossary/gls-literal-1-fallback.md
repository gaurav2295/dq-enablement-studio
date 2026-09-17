---
id: gls-literal-1-fallback
type: glossary
title: Literal-1 Fallback
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: deprecated
links:
  - relates:gls-ziserrorflag
  - relates:gls-catalog-promoter
sources:
  - dq-studio:docs/DQ_RULE_STANDARDS.md
  - vault:studio-architecture/Studio — Catalog Promotion (wrap not inject).md
tags: [guardrails, promotion]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

`1 AS [zIsErrorFlag]` — the placeholder a promoted catalog rule carries when no per-row error
condition could be determined for it. Every row is flagged, because the source query already *was*
the defect set.

## Usage

It is a legitimate intermediate state and an illegitimate shipping state: an OptSel whose flag is
a literal `1` has no [[gls-opportunity-universe|universe]], so it cannot produce a
[[gls-defect-rate|defect rate]].

A rule like this should never ship **unreviewed** — the reviewer either supplies the real
predicate or knowingly accepts the rule as a defect-only extract.
