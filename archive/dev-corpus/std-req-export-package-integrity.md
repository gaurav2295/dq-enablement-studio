---
id: std-req-export-package-integrity
type: standard
title: REQ-EXPORT-PACKAGE-INTEGRITY — A SQL-bearing export package must be internally consistent
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-EXPORT-PACKAGE-INTEGRITY
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

A SQL-bearing export package must be internally consistent.

## Rationale

Deterministic, structural checks over the batch of specs about to ship: a SQL-bearing export (sql/deploy_script/package) with no spec carrying generated SQL will ship an empty deploy script or SQL folder, and two specs whose generated asset filename collides will silently overwrite one another's sql/ package member.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | export |
| Severity | Warn |
| Posture | warn |
| Enforced by | export-package-integrity |
| Codes | export-coverage.package-empty-sql, export-coverage.package-duplicate-sql-member |
| Since | v2 (v1) |
