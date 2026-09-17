---
id: prn-adr-032
type: principle
kind: decision
title: ADR D-32 — AIClient's _safe_record wrapper must never let a broken on_call hook break the AI call chain
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-32
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

AIClient's _safe_record wrapper must never let a broken on_call hook break the AI call chain.

## Rationale

_safe_record exists specifically so a broken on_call telemetry hook (the caller-supplied observer) can never take down the underlying AI call it is merely observing. Telemetry is a side-channel; the AI call itself is the thing the user is waiting on.

## Consequence

Any future on_call hook, however it fails, must be swallowed by _safe_record without affecting the AI call's own result or exception propagation. Don't remove this wrapper to "simplify" telemetry wiring.

> [!note] Provenance
> Architecture decision **D-32** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
