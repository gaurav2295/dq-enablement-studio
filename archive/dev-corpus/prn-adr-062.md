---
id: prn-adr-062
type: principle
kind: decision
title: ADR D-62 — v3.5.1 Fix C: empty/whitespace-only workspace_iterate feedback is 'plain enhance', not a 400
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-62
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

v3.5.1 Fix C: empty/whitespace-only workspace_iterate feedback is 'plain enhance', not a 400.

## Rationale

Empty or whitespace-only feedback used to be rejected with a 400. ui/static/js/workspace.js's wsAIEnhanceViaIterate relies on being able to route a plain AI Enhance (no user feedback at all) for a rule with fan-out siblings through this same endpoint by passing feedback:"" — so the empty case had to become a supported, first-class input rather than an error.

## Consequence

feedback:"" (or whitespace-only) now runs plain-enhance semantics through /api/workspace/iterate/{idx} with a 200, and no feedback-log entry is recorded for an enhance-only call (there's no feedback text to log). Any future validation tightening on this endpoint must keep the empty-feedback path as a supported no-op, not reintroduce the 400.

> [!note] Provenance
> Architecture decision **D-62** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
