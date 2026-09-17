---
id: std-req-sql-unbalanced-parens
type: standard
title: REQ-SQL-UNBALANCED-PARENS — SQL must have balanced parentheses
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-UNBALANCED-PARENS
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

SQL must have balanced parentheses.

## Rationale

Unbalanced parentheses are invalid T-SQL and the view will fail to compile.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.unbalanced-parens |
| Since | v1 (v1) |
