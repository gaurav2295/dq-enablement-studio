---
id: gls-blocking-allowlist
type: glossary
title: Blocking Allowlist
domain: ai-enhancement
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-ai-static-validator-gate
  - relates:std-ai-enhance-guardrails
  - relates:gls-auto-repair
  - relates:gls-warn-and-stamp
  - relates:gls-symmetric-field-join
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [ai, guardrails, gate]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The explicit list of validator checks that **block an AI-Enhance save**. A violation of a listed
check raises a 422 and nothing is persisted; a violation of any other check is stamped and
surfaced but saves.

## Usage

> [!warning] Severity and blocking are separate decisions
> Never raise a check's severity to make it block. Severity is about correctness impact; the
> allowlist is about whether a legitimate exception exists that would false-positive if the check
> blocked everywhere. [[gls-symmetric-field-join|join-missing-system-id-pairing]] is the worked
> example — Medium severity everywhere, blocking on this path only.

The allowlist is a named constant (`AI_ENHANCE_BLOCKING_CHECKS`), reviewed as such. The gate runs [[gls-auto-repair|auto-repair]] first, then enforcement, **before any session
mutation**. Ordinary hand-edit saves and the deliberately incomplete TBD staging workflow are
unaffected.
