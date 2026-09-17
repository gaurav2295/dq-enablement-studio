---
id: gls-domain-unknown
type: glossary
title: domain_unknown
domain: ai-enhancement
audience: [developer]
level: advanced
status: deprecated
links:
  - relates:prn-no-silent-domain-fallback
  - relates:ref-local-deriver
  - relates:gls-tbd-placeholder
  - relates:gls-deterministic-shell
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, guardrails, honesty]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The deriver path taken when a rule name matches **no known data domain**: the spec is marked
`_domain_unknown`, the main table is left empty and the SQL is an honest
[[gls-tbd-placeholder|TBD]] shell.

## Usage

This is correct behaviour, not a bug — the alternative, silently falling back to Material because
it is the most common domain, produces a rule that looks finished and checks the wrong table
([[prn-no-silent-domain-fallback]]).

The real defect the gate was built for was adjacent: the AI review had **no guardrails when handed
that placeholder as its starting SQL**, and nothing blocked whatever it produced. Unknown domains
are highlighted in the UI, never left empty and quiet (ADR D-6).
