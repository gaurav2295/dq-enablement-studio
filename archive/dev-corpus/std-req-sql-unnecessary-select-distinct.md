---
id: std-req-sql-unnecessary-select-distinct
type: standard
title: REQ-SQL-UNNECESSARY-SELECT-DISTINCT — OptSel should avoid SELECT DISTINCT unless de-duplication is genuinely required
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-UNNECESSARY-SELECT-DISTINCT
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

OptSel should avoid SELECT DISTINCT unless de-duplication is genuinely required.

## Rationale

SELECT DISTINCT on the Opportunity View is usually masking a join fan-out bug rather than a genuine requirement — the DQ Rule Standards call this out as a performance/correctness smell to review, not a hard block.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Info |
| Posture | advisory |
| Enforced by | sql-validator |
| Codes | sql-validator.unnecessary-select-distinct |
| Since | v3 (v1) |
