---
id: std-req-sql-catalog-methodology-bypass
type: standard
title: REQ-SQL-CATALOG-METHODOLOGY-BYPASS — Catalog-sourced views must carry a methodology banner
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
  - relates:gls-methodology-banner
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-CATALOG-METHODOLOGY-BYPASS
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

Catalog-sourced views must carry a methodology banner.

## Rationale

A catalog-sourced view with no promoter banner shipped raw, bypassing the Syniti technical fields and per-row error CASE the bulk pipeline is supposed to apply.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Fail |
| Posture | block |
| Enforced by | sql-validator |
| Codes | sql-validator.catalog-methodology-bypass |
| Since | v1 (v1) |
