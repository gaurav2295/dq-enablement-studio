---
id: std-req-profiling-percentage-nullif-guard
type: standard
title: REQ-PROFILING-PERCENTAGE-NULLIF-GUARD — Profiling PrfSum [Percentage] must guard its denominator with NULLIF(..., 0)
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-PROFILING-PERCENTAGE-NULLIF-GUARD
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

Profiling PrfSum [Percentage] must guard its denominator with NULLIF(..., 0).

## Rationale

The mandatory PrfSum formula (integrations/ai_client.py's profiling review prompt, rule #3) is CAST(100.0 * [Occurrences] / NULLIF(SUM([Occurrences]) OVER (PARTITION BY ...), 0) AS DECIMAL(5,1)) — an unguarded denominator is a live divide-by-zero on any segment with zero rows.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | profiling-sql |
| Codes | profiling-sql.percentage-missing-nullif-guard |
| Since | v2 (v1) |
