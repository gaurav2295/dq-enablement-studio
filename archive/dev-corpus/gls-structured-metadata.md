---
id: gls-structured-metadata
type: glossary
title: STRUCTURED METADATA Block
domain: ai-enhancement
audience: [developer]
level: advanced
status: review
links:
  - parent:gls-rule-fulfilment-review
  - relates:std-ai-enhance-scope
  - relates:gls-logicentry
  - relates:gls-round-trip-parse
sources:
  - dq-studio:docs/ai_enhance_instructions.md
tags: [ai, contract, parsing]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The JSON block a rule-fulfilment response carries alongside its corrected SQL, describing every
output column, join and logic condition that ended up in that SQL — so the caller can refresh its
own metadata **without re-parsing the SQL text**.

## Usage

It exists because free-text SQL is not reliably machine-parseable once a model has restructured it
— the [[gls-round-trip-parse|round-trip parser]] can read the Studio's own shapes, not arbitrary
rewrites.

Two conventions: `section` is one of `Tech` / `Basic` / `Org` / `Value` / `Activity`, and the
Syniti Technical Fields are assumed present and never listed. Include an entry **only where the
corrected SQL genuinely differs** — and omit a key entirely rather than guessing, because the
caller fills mechanical defaults for anything left out.
