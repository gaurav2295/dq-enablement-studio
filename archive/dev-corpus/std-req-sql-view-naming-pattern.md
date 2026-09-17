---
id: std-req-sql-view-naming-pattern
type: standard
title: REQ-SQL-VIEW-NAMING-PATTERN — View names must follow the DQ Rule Standards naming pattern
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-VIEW-NAMING-PATTERN
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

View names must follow the DQ Rule Standards naming pattern.

## Rationale

DQ_[4-digit RuleNumber]_[System]_[Object]_[Description]_[OptSel|RptSel] is the DQ Rule Standards' required shape (knowledge/methodology/shell_guardrails.yaml) — a name outside that pattern (non-numeric or non-zero-padded rule number, missing segments) breaks tracker/deploy-script name matching.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.view-naming-pattern |
| Since | v3 (v1) |
