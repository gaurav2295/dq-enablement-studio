---
id: std-req-sql-concat-key-missing-field
type: standard
title: REQ-SQL-CONCAT-KEY-MISSING-FIELD — zConcatenatedKey must reference every field the DQ Rule Standards require
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-CONCAT-KEY-MISSING-FIELD
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

zConcatenatedKey must reference every field the DQ Rule Standards require.

## Rationale

zConcatenatedKey must include zSourceSystemID (and any other field configured in shell_guardrails.yaml's concat_key_must_reference) so the key is unique per record across systems, not just within one.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Warn |
| Posture | warn |
| Enforced by | sql-validator |
| Codes | sql-validator.concat-key-missing-field |
| Since | v3 (v1) |
