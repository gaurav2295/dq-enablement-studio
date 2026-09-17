---
id: prn-adr-052
type: principle
kind: decision
title: ADR D-52 — /api/derive's own telemetry recording is fail-open as a second line of defense
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-52
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

/api/derive's own telemetry recording is fail-open as a second line of defense.

## Rationale

Even if record_generation itself unexpectedly raises — bypassing its own internal try/except entirely, as a badly-behaved mock would — /api/derive must still return its normal 200 payload. api_routes wraps every record_generation call site as a second, outer line of defense on top of record_generation's own internal fail-soft handling.

## Consequence

A broken telemetry recorder must never surface as a broken /api/derive response. Any new call site that records generation telemetry must be wrapped the same defensive way, not assume record_generation's own internal try/except is sufficient on its own.

> [!note] Provenance
> Architecture decision **D-52** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
