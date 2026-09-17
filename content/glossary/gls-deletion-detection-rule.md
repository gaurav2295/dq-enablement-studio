---
id: gls-deletion-detection-rule
type: glossary
title: Deletion-Detection Rule
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:gls-deletion-flag
  - relates:prn-deletion-flags-belong-in-where
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - vault:sap-knowledge/SAP Deletion Flags vs Status Fields.md
tags: [rule-design, deletion]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The one rule shape where a [[gls-deletion-flag|deletion flag]] is the **subject** rather than an
exclusion — "a material flagged for deletion must have zero stock", "a customer flagged for
deletion must have no open orders". The flag moves from the `WHERE` into the `zIsErrorFlag` logic.

## Usage

This is the deliberate exception to "flags are exclusions" — and it has
to be, or the rules that police an incomplete deletion process could not be written at all.

Detection order matters: the Studio runs [[gls-rule-pattern|rule-pattern]] detection **before**
keyword-based deletion detection and gates the latter off whenever a pattern matched, so a
parity or status rule that merely mentions deletion is not hijacked.
