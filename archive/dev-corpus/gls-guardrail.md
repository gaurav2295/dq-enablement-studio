---
id: gls-guardrail
type: glossary
title: Guardrail (deterministic)
domain: ai-enhancement
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:std-ai-enhance-guardrails
  - relates:ref-sql-validator
  - relates:gls-ai-harness
  - relates:gls-blocking-allowlist
  - relates:prn-studio-workflow-guardrails
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, guardrails]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A **mechanical check on SQL text and structure** — same input, always the same result. Guardrails
are the rules; the [[gls-ai-harness|harness]] is the mechanism that runs them and records what
they found.

## Usage

Keeping the two words apart matters when reading Studio material. "Guardrail" never means "the
model was told not to" — a prompt instruction is advice, and advice is not a guardrail until a
deterministic check enforces it. Every finding the harness reports traces back to one of these
checks.

Adding a guardrail is a four-part change: the check function, its registration, its tunables, and a
requirement contract it maps to — a live-coverage test enforces that every emittable code maps to
exactly one active requirement (std-harness-requirements).
