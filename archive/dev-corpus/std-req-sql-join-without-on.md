---
id: std-req-sql-join-without-on
type: standard
title: REQ-SQL-JOIN-WITHOUT-ON — Non-CROSS JOINs must carry an ON predicate
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-JOIN-WITHOUT-ON
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

Non-CROSS JOINs must carry an ON predicate.

## Rationale

A JOIN with no ON clause (and not a deliberate CROSS JOIN) is invalid T-SQL and the view will fail to compile.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.join-without-on |
| Since | v1 (v1) |
