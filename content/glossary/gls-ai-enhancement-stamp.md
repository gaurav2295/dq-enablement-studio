---
id: gls-ai-enhancement-stamp
type: glossary
title: AI Enhancement Stamp
domain: ai-enhancement
audience: [developer]
level: practitioner
status: review
links:
  - relates:ref-ai-derive-and-enhance-internals
  - relates:gls-ai-enhance
  - relates:gls-sibling-implementation
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, provenance, persistence]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The record written onto a spec when an AI enhancement is accepted — the
**before** state, the AI warnings, and the fulfilment result — saved with the spec rather than
held only in the current session.

## Usage

The stamp is why the diff, the warnings and the fulfilment verdict survive navigation, reload and
an app restart. Without it, "what did the AI change here?" is answerable only in the session that
made the change.

On a fan-out propagation the stamp is written **for every target**, not just the
representative sibling — otherwise the siblings would look hand-authored
([[gls-sibling-implementation]]).
