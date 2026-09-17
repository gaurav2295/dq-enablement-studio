---
id: std-req-sql-unresolved-aliases
type: standard
title: REQ-SQL-UNRESOLVED-ALIASES — Column references must use a declared FROM/JOIN alias
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-UNRESOLVED-ALIASES
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

Column references must use a declared FROM/JOIN alias.

## Rationale

A column reference to an alias never introduced by FROM/JOIN is a silent runtime failure — the view either won't compile or won't return the intended rows.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.unresolved-aliases |
| Since | v1 (v1) |
