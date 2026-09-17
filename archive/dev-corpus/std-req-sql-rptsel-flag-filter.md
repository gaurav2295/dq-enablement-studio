---
id: std-req-sql-rptsel-flag-filter
type: standard
title: REQ-SQL-RPTSEL-FLAG-FILTER — RptSel must filter [zIsErrorFlag] = 1
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-RPTSEL-FLAG-FILTER
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

RptSel must filter [zIsErrorFlag] = 1.

## Rationale

Without the zIsErrorFlag filter, RptSel reports the full opportunity population instead of just the violations.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Warn |
| Posture | warn |
| Enforced by | sql-validator |
| Codes | sql-validator.rptsel-missing-flag-filter |
| Since | v1 (v1) |
