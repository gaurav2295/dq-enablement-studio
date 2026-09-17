---
id: gls-ai-enhance
type: glossary
title: AI Enhance
domain: ai-enhancement
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:std-ai-enhance-scope
  - relates:std-ai-enhance-guardrails
  - relates:ref-ai-derive-and-enhance-internals
  - relates:gls-deterministic-shell
  - relates:gls-rule-fulfilment-review
sources:
  - dq-studio:docs/ai_enhance_instructions.md
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, workflow]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The Studio action that hands an already-derived rule to a model and asks it to **improve** the
rule name, the implication and — through the
[[gls-rule-fulfilment-review|rule-fulfilment review]] — the SQL's error logic.

## Usage

AI Enhance is a **bounded editor, not an author**. The [[gls-deterministic-shell|deterministic
shell]] owns the artefact's structure; the model is licensed to change the
[[gls-ziserrorflag|zIsErrorFlag]] logic, joins that prevent the rule fulfilling its purpose, added
output fields, and [[gls-tbd-placeholder|TBD placeholders]] — and nothing else
([[std-ai-enhance-scope]]).

The full chain is six steps: shell → enhance call → rule-fulfilment review → accept → compliance
gate → persist with an [[gls-ai-enhancement-stamp|_ai_enhancement stamp]]. Everything the model
proposes is re-checked deterministically before it can be saved.
