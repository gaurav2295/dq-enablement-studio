---
id: gls-symmetric-field-join
type: glossary
title: Symmetric-Field Join
domain: sql-standards
audience: [developer]
level: advanced
status: review
links:
  - relates:std-ai-enhance-guardrails
  - relates:gls-zsourcesystemid
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [sql, joins, guardrails]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A join whose `ON` matches **the same column name on both sides** (`t009.PERIV = t001.PERIV`) —
the shape that says the two tables hold the same business key. Every such join must also pair
[[gls-zsourcesystemid|zSourceSystemID]], or it can match rows from different source systems.

## Usage

The check `join-missing-system-id-pairing` detects it. Its severity and its blocking status are
deliberately different decisions: **Medium** severity everywhere (legitimate FK-lookup joins would
false-positive), but **on** the AI-Enhance blocking allowlist, because
on that path the pairing is never legitimately absent.

The check's regex accepts bracket-quoted names on either side — a real regression shipped past it
when it matched bare identifiers only.
