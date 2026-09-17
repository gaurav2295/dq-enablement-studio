---
id: gls-candidate
type: glossary
title: Candidate (harness)
domain: ai-enhancement
audience: [developer]
level: advanced
status: review
links:
  - parent:gls-ai-harness

  - relates:gls-verdict
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The artefact submitted to the [[gls-ai-harness|harness]] for judgement — an AI-produced rule name,
spec or SQL pair, together with the context a check needs to judge it.

## Usage

"Candidate" is deliberate: at this point the output is a *proposal*, not a saved artefact. It
becomes real only after its [[gls-verdict|Verdict]] is recorded and, on the AI-Enhance-accept path,
after the compliance gate lets it through.

Reading the word as "candidate for promotion" is the right instinct — the same posture the
rule catalogue takes with promotion candidates, which are git-governed rather than written live.
