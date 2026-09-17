---
id: prn-adr-007
type: principle
kind: decision
title: ADR D-7 — Deletion-detection rules are the deliberate exception to "flags are exclusions"
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
  - relates:gls-deletion-detection-rule
sources:
  - dq-studio:knowledge/harness/decisions.json#D-7
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Deletion-detection rules are the deliberate exception to "flags are exclusions".

## Rationale

For a detection rule ("must not be marked for deletion") there is no WHERE clause to rely on, so excluding the deletion flag would remove the very records being flagged. The exception is opt-in (_deletion_is_error), so it never affects normal rules.

## Consequence

The methodology default holds — deletion flags (LVORM/LOEKZ/LOEVM) are WHERE exclusions, never in the zIsErrorFlag CASE — except when the rule's subject IS the deletion status, where the flag drives the CASE and is suppressed from the WHERE. The PIR→MARA "only when material still active" cross-check is still NOT auto-derived from the bare name (carried unresolved).

> [!note] Provenance
> Architecture decision **D-7** in the DQ Studio decision registry, decided 2026-06-30, registry status *active*.
