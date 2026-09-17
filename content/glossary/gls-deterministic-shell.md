---
id: gls-deterministic-shell
type: glossary
title: Deterministic Shell
domain: ai-enhancement
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:ref-local-deriver
  - relates:prn-no-silent-domain-fallback
  - relates:gls-ai-enhance
  - relates:gls-tbd-placeholder
  - relates:gls-sql-skeleton
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, derivation]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The rule artefact the **local deriver** produces before any model is involved: output fields
already sectioned, joins and filters applied, deletion handling resolved, the SQL skeleton emitted.
Same input, same output, every time.

## Usage

The shell is the baseline everything else is measured against. The AI is handed the shell and
diffed against it; the harness judges the AI's output against the shell's structure; the compliance
gate refuses anything that broke it.

When no domain matches, the shell produces an **honest, intentionally un-deployable placeholder**
— empty main table, `FROM /* TBD */` — rather than a confidently-wrong guess
([[prn-no-silent-domain-fallback]]). That placeholder is correct behaviour, and it is the reason
the AI path needed its own guardrails: an unguarded model handed a shell will fill the blanks with
plausible fiction.
