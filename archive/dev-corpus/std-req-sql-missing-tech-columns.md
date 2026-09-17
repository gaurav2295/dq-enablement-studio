---
id: std-req-sql-missing-tech-columns
type: standard
title: REQ-SQL-MISSING-TECH-COLUMNS — OptSel/InfSel must expose the Syniti Technical Fields
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
  - relates:gls-syniti-technical-fields
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-MISSING-TECH-COLUMNS
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

OptSel/InfSel must expose the Syniti Technical Fields.

## Rationale

Methodology requires zSourceSystemID, zConcatenatedKey, and (Error rules) zIsErrorFlag on every OptSel/InfSel — downstream tooling and the RptSel filter depend on them.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.missing-tech-columns |
| Since | v1 (v1) |
