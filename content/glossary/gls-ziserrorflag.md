---
id: gls-ziserrorflag
type: glossary
title: zIsErrorFlag
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:std-ziserrorflag-convention
  - relates:prn-ziserrorflag-is-integer
  - relates:gls-optsel
  - relates:gls-syniti-technical-fields

sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [technical-fields, optsel]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **error-detection flag** — the single column that carries a DQ rule's verdict on a record.
An **INTEGER**: `1` = the record is a **business defect**, `0` = it passes. Emitted as a `CASE`
expression in the OptSel `SELECT`, never as a literal.

## Usage

`zIsErrorFlag` is the whole point of an Error rule — everything else in the view is context for
the person fixing the record. Three standing rules:

- **Integer, not string.** ADM counts defects arithmetically; a `'Y'`/`'N'` flag silently breaks
  the denominator ([[prn-ziserrorflag-is-integer]]).
- **Never a bare `NULL` or a literal `1`.** Both mean "the logic was never written" and are
  caught as validation findings.
- **Error rules only.** Info rules carry `[Implication]` instead; Profiling rules carry neither.

Its logic is the one region of a generated view that [[gls-ai-enhance|AI Enhance]] is licensed to
rewrite — see [[std-ai-enhance-scope]].
