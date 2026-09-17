---
id: gls-ai-harness
type: glossary
title: AI Harness
domain: ai-enhancement
audience: [developer]
level: practitioner
status: review
links:

  - relates:ref-ai-derive-and-enhance-internals

  - relates:gls-candidate
  - relates:gls-verdict
  - relates:gls-guardrail
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
  - dq-studio:knowledge/harness/requirements.json
tags: [ai, harness, governance]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The mechanism that runs the deterministic checks against an AI-produced artefact, produces a
[[gls-verdict|Verdict]], and records it. It wraps every AI call — the client the Studio actually
calls is a `HarnessedAIClient`, so nothing reaches the caller unjudged.

## Usage

> [!important]
> The harness is **never a second model grading the first one's homework.** Every check inside it
> wraps an already-deterministic validator — the SQL validator, the knowledge-trust checker, the
> rule-name scorer. The [[gls-guardrail|guardrails]] are the rules; the harness is the machinery
> that applies them and keeps the receipt.

Default checks run in a fixed order: table/field trust, rule-name score, SQL validation. The
posture is [[gls-warn-and-stamp|warn-and-stamp]] — the harness records, the compliance gate blocks.
