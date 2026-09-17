---
id: std-req-sql-missing-semicolon-before-go
type: standard
title: REQ-SQL-MISSING-SEMICOLON-BEFORE-GO — A batch's GO terminator should be preceded by a semicolon
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-MISSING-SEMICOLON-BEFORE-GO
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

A batch's GO terminator should be preceded by a semicolon.

## Rationale

SQL Server recommends a semicolon before a GO batch terminator; omitting it is a structural deviation, not a parse failure.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Warn |
| Posture | warn |
| Enforced by | sql-validator |
| Codes | sql-validator.missing-semicolon-before-go |
| Since | v1 (v1) |
