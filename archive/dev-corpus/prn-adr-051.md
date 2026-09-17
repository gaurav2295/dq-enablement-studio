---
id: prn-adr-051
type: principle
kind: decision
title: ADR D-51 — v3.6.1 fix: the missing-SQL validator gate was moved, not silenced
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-51
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

v3.6.1 fix: the missing-SQL validator gate was moved, not silenced.

## Rationale

v3.6.1 regression pair: any rule that generates real OptSel+RptSel SQL must never see missing-optsel/missing-rptsel false-positive warnings in its response chips — but the fix that removed the false positive must not have silenced the validator gate entirely; it must still fire on genuinely incomplete SQL once it runs on a real (but broken) case.

## Consequence

Both halves are pinned together: valid, complete SQL produces zero missing-sql warnings, and deliberately-incomplete SQL still trips the validator. Any future change to where this gate runs must re-prove both halves, not just the false-positive fix in isolation.

> [!note] Provenance
> Architecture decision **D-51** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
