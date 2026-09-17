---
id: std-req-sql-view-name-rule-id-mismatch
type: standard
title: REQ-SQL-VIEW-NAME-RULE-ID-MISMATCH — The view name's rule id must match the banner's Rule ID
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-VIEW-NAME-RULE-ID-MISMATCH
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

The view name's rule id must match the banner's Rule ID.

## Rationale

A mismatch between the DQ_NNNN_ view name and the '-- Rule ID:' banner indicates a bulk-pipeline replication bug that causes view-name collisions and tracker/SQL drift.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.view-name-rule-id-mismatch |
| Since | v1 (v1) |
