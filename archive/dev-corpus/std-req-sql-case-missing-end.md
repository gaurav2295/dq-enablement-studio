---
id: std-req-sql-case-missing-end
type: standard
title: REQ-SQL-CASE-MISSING-END — Every CASE expression must have a matching END
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-CASE-MISSING-END
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

Every CASE expression must have a matching END.

## Rationale

A CASE with no matching END is invalid T-SQL and the view will fail to compile.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.case-missing-end |
| Since | v1 (v1) |
