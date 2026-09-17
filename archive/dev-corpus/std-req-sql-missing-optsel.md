---
id: std-req-sql-missing-optsel
type: standard
title: REQ-SQL-MISSING-OPTSEL — OptSel SQL must be present for any non-Profiling rule
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-MISSING-OPTSEL
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

OptSel SQL must be present for any non-Profiling rule.

## Rationale

A rule with no OptSel view has no opportunity population defined — there is nothing to validate or deploy.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.missing-optsel |
| Since | v1 (v1) |
