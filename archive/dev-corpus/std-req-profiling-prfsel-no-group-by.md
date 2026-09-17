---
id: std-req-profiling-prfsel-no-group-by
type: standard
title: REQ-PROFILING-PRFSEL-NO-GROUP-BY — Profiling PrfSel (Detail) must be record-level — no GROUP BY or aggregation
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-PROFILING-PRFSEL-NO-GROUP-BY
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

Profiling PrfSel (Detail) must be record-level — no GROUP BY or aggregation.

## Rationale

Profiling's Detail view is record-level by definition (integrations/ai_client.py's profiling review prompt, mandatory rule #2) — a GROUP BY or aggregate function in PrfSel is a structural error, not a style nit, and breaks the record-level drill-through PrfSum depends on.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | profiling-sql |
| Codes | profiling-sql.prfsel-has-group-by |
| Since | v2 (v1) |
