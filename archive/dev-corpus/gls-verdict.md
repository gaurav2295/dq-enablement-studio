---
id: gls-verdict
type: glossary
title: Verdict (harness)
domain: ai-enhancement
audience: [developer]
level: advanced
status: review
links:
  - parent:gls-ai-harness


  - relates:gls-candidate
  - relates:gls-warn-and-stamp
sources:
  - dq-studio:knowledge/harness/requirements.json
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, harness, governance]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The [[gls-ai-harness|harness's]] recorded judgement on a [[gls-candidate|Candidate]]: which checks
ran, what they found, the resulting status, and — since the fail-closed amendment — which checks
**errored** rather than ran.

## Usage

`errored_checks` exists because a check that could not run must not look like a check that ran
clean. Under enforcing mode the decision function fails **closed** on a non-empty
`errored_checks`: an artefact whose judgement is silently missing is unverified, and enforcement
refuses rather than accepting (ADR D-26).

Every Verdict is computed and stamped whatever the posture. What varies is whether anything acts
on it — see [[gls-warn-and-stamp]].
