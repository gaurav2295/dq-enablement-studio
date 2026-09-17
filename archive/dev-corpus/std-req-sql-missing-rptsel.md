---
id: std-req-sql-missing-rptsel
type: standard
title: REQ-SQL-MISSING-RPTSEL — Error rules must ship an RptSel partner alongside OptSel
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-MISSING-RPTSEL
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

Error rules must ship an RptSel partner alongside OptSel.

## Rationale

An Error rule with an OptSel but no RptSel has no reportable-population view — the rule cannot surface its own violations.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.missing-rptsel |
| Since | v1 (v1) |
