---
id: gls-ai-additions
type: glossary
title: AI ADDITIONS
domain: ai-enhancement
audience: [consultant, developer]
level: practitioner
status: review
links:
  - parent:gls-rule-fulfilment-review
  - relates:std-ai-enhance-scope
  - relates:std-ai-enhance-guardrails
sources:
  - dq-studio:docs/ai_enhance_instructions.md
tags: [ai, review, provenance]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The response section in which the model must declare **what it added and why** — fields introduced,
joins touched, and for a restructure the before shape, the after shape and the reason. `"No
additions."` when nothing changed.

## Usage

This is the provenance half of the AI licence: the model may add a field or a join, but it may not
add one *invisibly*. A reviewer reads `AI ADDITIONS` to see the delta without diffing SQL.

Anything the model introduces that was not already in the spec is **unverified until proven
otherwise** and must be flagged as such — enforced by the table/field trust check
(REQ-TRUST-AI-UNVERIFIED-FIELD).
