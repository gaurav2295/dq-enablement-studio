---
id: gls-tbd-placeholder
type: glossary
title: TBD Placeholder
domain: ai-enhancement
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:prn-no-silent-domain-fallback
  - relates:gls-deterministic-shell
  - relates:gls-domain-unknown
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, guardrails, honesty]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The literal `TBD` the [[gls-deterministic-shell|deterministic shell]] writes where it could not
resolve a fact — a table slot, a field slot, a view-name token. It marks an artefact as
**intentionally un-deployable**.

## Usage

A TBD is a feature: it says "this was not resolved" out loud, where a plausible guess would say
nothing at all. Resolving it is the one *mandatory* AI edit — first TBD is the table position,
second the field position, and inconsistent references elsewhere are corrected to match
([[std-ai-enhance-scope]]).

Two things TBD is **not**: it is not what a PartialFill emits (that names the
missing slot and file instead), and it is not licence to ship — a TBD reaching an export is a
finding.
