---
id: gls-slotfill
type: glossary
title: SlotFill
domain: rule-design
audience: [developer]
level: advanced
status: review
links:
  - parent:gls-rule-pattern
  - relates:std-rule-pattern-library
  - relates:gls-partialfill
  - relates:gls-first-writer-wins
sources:
  - dq-studio:docs/RULE_PATTERNS.md
tags: [rule-pattern, derivation]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The result of resolving a [[gls-rule-pattern|pattern's]] abstract slots — universe table, joined
table, key fields, comparator, [[gls-polarity|polarity]] — into **concrete, knowledge-base-verified
facts** for one rule.

## Usage

Every slot has a named source: curated join definitions, the status-field and parity registries,
the domain map, the partner lexicon, and the SAP baseline used only to *confirm* a column exists
before trusting it. Nothing in a SlotFill is inferred from the rule text beyond what the
[[gls-intent-regex|intent regexes]] captured.

That provenance is the first layer of the pattern trust chain: because every slot is
KB-verified by construction, pattern-derived rules skip the AI-unverified-field check entirely.
If any slot cannot resolve, the filler returns a [[gls-partialfill]] instead.
