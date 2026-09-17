---
id: gls-warn-and-stamp
type: glossary
title: Warn-and-Stamp
domain: ai-enhancement
audience: [developer, lead]
level: practitioner
status: review
links:

  - relates:ref-ai-static-validator-gate
  - relates:gls-verdict
  - relates:gls-blocking-allowlist
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, harness, posture]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The [[gls-ai-harness|harness's]] shipping posture: **compute every [[gls-verdict|Verdict]], record
it on the artefact, block nothing.** Enforcement exists as a documented, inert knob.

## Usage

The reason it ships this way is a product decision, not an oversight: nobody had decided what a
`Fail` should *do* to a consultant mid-flow, and shipping enforcement without that answer would
have made the harness something people route around (ADR D-16).

Blocking happens elsewhere and narrowly — the AI-Enhance compliance gate with its explicit
[[gls-blocking-allowlist|blocking allowlist]]. Keep the two apart when reading a finding: a
stamped `Fail` is information for a reviewer; a 422 is a refusal to save.
