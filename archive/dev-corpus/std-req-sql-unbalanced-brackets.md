---
id: std-req-sql-unbalanced-brackets
type: standard
title: REQ-SQL-UNBALANCED-BRACKETS — SQL must have balanced square brackets
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-UNBALANCED-BRACKETS
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

SQL must have balanced square brackets.

## Rationale

Unbalanced [ ] identifier delimiters are invalid T-SQL and the view will fail to compile.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.unbalanced-brackets |
| Since | v1 (v1) |
