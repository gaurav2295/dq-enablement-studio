---
id: std-req-sql-undefined-error-flag
type: standard
title: REQ-SQL-UNDEFINED-ERROR-FLAG — OptSel must not ship zIsErrorFlag as a bare NULL literal
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-UNDEFINED-ERROR-FLAG
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

OptSel must not ship zIsErrorFlag as a bare NULL literal.

## Rationale

A bare NULL zIsErrorFlag means the deriver could not resolve the rule's subject field to a known table/field, so no check condition was ever written — the rule flags nothing and must not be deployed.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.undefined-error-flag |
| Since | v3 (v1) |
