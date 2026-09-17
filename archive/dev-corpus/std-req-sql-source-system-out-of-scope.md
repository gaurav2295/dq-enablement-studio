---
id: std-req-sql-source-system-out-of-scope
type: standard
title: REQ-SQL-SOURCE-SYSTEM-OUT-OF-SCOPE — A fanned-out implementation's system code must be in the project's configured scope
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-SOURCE-SYSTEM-OUT-OF-SCOPE
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

A fanned-out implementation's system code must be in the project's configured scope.

## Rationale

When spec.system_filter is set (a per-system fan-out implementation), its value must be one of the project's configured source_systems (core/spec_model.py ArchitectureContext) — a code outside that scope was never meant to be deployed and indicates stale or hand-typed fan-out data. Skipped entirely for the single-system/legacy-default derive path, where system_filter is blank.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Warn |
| Posture | warn |
| Enforced by | sql-validator |
| Codes | sql-validator.source-system-out-of-scope |
| Since | v3 (v1) |
