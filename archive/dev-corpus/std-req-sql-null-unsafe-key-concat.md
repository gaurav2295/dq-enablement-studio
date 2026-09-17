---
id: std-req-sql-null-unsafe-key-concat
type: standard
title: REQ-SQL-NULL-UNSAFE-KEY-CONCAT — zConcatenatedKey should not rely on plain + concatenation
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-NULL-UNSAFE-KEY-CONCAT
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

zConcatenatedKey should not rely on plain + concatenation.

## Rationale

A NULL in any component of a + concatenation yields a NULL key, breaking row identity — informational until observed to matter for a given source.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Info |
| Posture | advisory |
| Enforced by | sql-validator |
| Codes | sql-validator.null-unsafe-key-concat |
| Since | v1 (v1) |
