---
id: std-req-sql-trailing-comma
type: standard
title: REQ-SQL-TRAILING-COMMA — OptSel/RptSel must not have a trailing comma before FROM
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-TRAILING-COMMA
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

OptSel/RptSel must not have a trailing comma before FROM.

## Rationale

A dangling comma before FROM is invalid T-SQL and fails at deploy time.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.trailing-comma-before-from |
| Since | v1 (v1) |
