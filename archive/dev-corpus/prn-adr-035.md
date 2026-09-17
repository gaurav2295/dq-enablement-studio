---
id: prn-adr-035
type: principle
kind: decision
title: ADR D-35 — AUA deep-dive qualifier rejects a column on true distinct_count alone, regardless of top-K skew
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-35
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

AUA deep-dive qualifier rejects a column on true distinct_count alone, regardless of top-K skew.

## Rationale

This is product policy, not pure algorithm: a column must fail the AUA deep-dive qualifier if its true distinct_count exceeds max_distinct (default 50), even if its top-K values look heavily concentrated in a truncated profile sample. The named regression case is KNB1.KUNNR (~3,000 distinct customers): the profile capper truncates to 20,000 rows, so coverage in that truncated space can exceed 0.80 even though the column is genuinely high-cardinality — without the distinct_count guard, the column would wrongly qualify and explode the AUA output into a per-value breakdown nobody asked for.

## Consequence

The guard is opt-in via an explicit distinct_count parameter, so legacy callers that don't pass it keep the old coverage-only behavior. Any future AUA qualifier change must preserve this precedence: true cardinality always overrides a skewed truncated-sample coverage number.

> [!note] Provenance
> Architecture decision **D-35** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
