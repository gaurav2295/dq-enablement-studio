---
id: gls-partialfill
type: glossary
title: PartialFill
domain: rule-design
audience: [developer]
level: advanced
status: review
links:
  - parent:gls-rule-pattern
  - relates:std-rule-pattern-library
  - relates:prn-no-silent-domain-fallback
  - relates:gls-slotfill
  - relates:gls-tbd-placeholder
sources:
  - dq-studio:docs/RULE_PATTERNS.md
tags: [rule-pattern, guardrails]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

What slot filling returns when a pattern's intent fired but a fact could not be resolved: a
**named-slot warning** carrying the pattern id, the domain, the exact slot that failed, and the
knowledge-base file or entry that would fix it.

## Usage

A PartialFill is the pattern library's expression of the no-silent-fallback doctrine
([[prn-no-silent-domain-fallback]]): an unresolvable fact produces an actionable warning, never a
guess and never a bare "TBD". A unit test pins that the word *TBD* never comes out of this path.

The rest of the spec falls through to the ordinary keyword-matched path unchanged, so a
PartialFill degrades one slot, not the whole rule.
