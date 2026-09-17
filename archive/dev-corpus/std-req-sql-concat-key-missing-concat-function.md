---
id: std-req-sql-concat-key-missing-concat-function
type: standard
title: REQ-SQL-CONCAT-KEY-MISSING-CONCAT-FUNCTION — zConcatenatedKey must be built with CONCAT(...)
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-CONCAT-KEY-MISSING-CONCAT-FUNCTION
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

zConcatenatedKey must be built with CONCAT(...).

## Rationale

The DQ Rule Standards require zConcatenatedKey to use CONCAT(...) with null-safe COALESCE/TRIM guards, not manual + concatenation (which yields a NULL key when any component is NULL — see the existing null-unsafe-key-concat check for that anti-pattern).

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Warn |
| Posture | warn |
| Enforced by | sql-validator |
| Codes | sql-validator.concat-key-missing-concat-function |
| Since | v3 (v1) |
