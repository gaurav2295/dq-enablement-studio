---
id: prn-adr-028
type: principle
kind: decision
title: ADR D-28 — Rule-pattern precision fix: deletion-intent parity, not the inverted-semantics LOEVM CASE
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-28
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Rule-pattern precision fix: deletion-intent parity, not the inverted-semantics LOEVM CASE.

## Rationale

Before this fix, "marked for deletion across all Company Codes" phrasing tripped _detect_deletion_intent (no domain field bound + deletion-intent phrasing) and derived CASE WHEN KNA1.LOEVM = 'X' THEN 1 ELSE 0 END — confidently wrong, since it flags every centrally-deleted customer as a defect regardless of whether its Company-Code children are also deleted, the OPPOSITE of what "must also be marked for deletion" parity means. The rule-pattern branch (D-8) must run before and gate deletion-detection so this phrasing resolves to org_to_central_parity (an EXISTS/NOT EXISTS parity CASE) instead.

## Consequence

Rule 4's exact phrasing is pinned end-to-end: it must resolve to org_to_central_parity and must never regress to the inverted LOEVM CASE. Any future change to the deletion-detection or rule-pattern precedence (D-8) must keep this acceptance-corpus case passing.

> [!note] Provenance
> Architecture decision **D-28** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
