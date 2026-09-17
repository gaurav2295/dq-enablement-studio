---
id: gls-auto-repair
type: glossary
title: Auto-Repair
domain: ai-enhancement
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-ai-static-validator-gate
  - relates:ref-sql-validator
  - relates:gls-blocking-allowlist
  - relates:gls-zsourcesystemid
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, guardrails, gate]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The mechanical, regex-only correction pass that runs before the
[[gls-blocking-allowlist|blocking allowlist]] — fixing violations with **zero semantic ambiguity**
rather than refusing the save.

## Usage

Three repairs are in scope today: a hardcoded [[gls-zsourcesystemid|zSourceSystemID]] literal
swapped for the column reference, a pipe delimiter in
[[gls-zconcatenatedkey|zConcatenatedKey]] swapped for an underscore, and verbose
performance/index/uniqueness commentary stripped — never touching the header banner or a
legitimate short business comment.

> [!warning]
> Extend auto-repair (`attempt_ai_enhance_autorepair`, which runs before
> `enforce_ai_enhance_compliance`) **only** where the fix has one possible meaning. Never auto-repair by removing
> a `WHERE` clause or inventing a join condition: a silent semantic change is worse than a block.
