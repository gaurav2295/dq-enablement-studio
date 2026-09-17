---
id: std-req-sql-missing-trailing-semicolon
type: standard
title: REQ-SQL-MISSING-TRAILING-SEMICOLON — View body should end with a trailing semicolon
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-MISSING-TRAILING-SEMICOLON
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

View body should end with a trailing semicolon.

## Rationale

A missing trailing semicolon is a structural deviation from the Studio's generated-SQL convention.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Warn |
| Posture | warn |
| Enforced by | sql-validator |
| Codes | sql-validator.missing-trailing-semicolon |
| Since | v1 (v1) |
