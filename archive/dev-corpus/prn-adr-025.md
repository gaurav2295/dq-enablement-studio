---
id: prn-adr-025
type: principle
kind: decision
title: ADR D-25 — ai_calls under-counts retried review_sql calls (retry-telemetry undercount)
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-25
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

ai_calls under-counts retried review_sql calls (retry-telemetry undercount).

## Rationale

Today's ai_calls table gets exactly ONE row per review_sql call, retried or not — the retry attempt is passed _record=False (core/harness/wrap.py's review_sql, mirroring the pre-refactor inline retry loop's own never-wrapped-in-_safe_record behavior) so it never fires record_ai_call. This under-counts real API usage on a retried call.

## Consequence

Recording the retry would be more truthful, but it's a deliberate, separately-tracked follow-up, not decided this cycle. harness_verdicts still records the retried call's FINAL verdict exactly once with retry_count=1, so the retry IS visible through that field — only the raw ai_calls API-usage count under-counts. Recorded here per harness-v2 design Amendment O-6 so this known-accepted gap is explicit and reviewable.

> [!note] Provenance
> Architecture decision **D-25** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
