---
id: std-req-sql-null-compared-eq
type: standard
title: REQ-SQL-NULL-COMPARED-EQ — SQL must use IS NULL / IS NOT NULL, never = NULL or <> NULL
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-NULL-COMPARED-EQ
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

SQL must use IS NULL / IS NOT NULL, never = NULL or <> NULL.

## Rationale

'= NULL' and '<> NULL' always evaluate to UNKNOWN in T-SQL and silently exclude rows from the result set.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.null-compared-with-eq |
| Since | v1 (v1) |
