---
id: std-req-sql-section-header-order
type: standard
title: REQ-SQL-SECTION-HEADER-ORDER — SELECT-list section comments must appear in the standard order
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-SECTION-HEADER-ORDER
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

SELECT-list section comments must appear in the standard order.

## Rationale

Syniti Technical Fields, Basic Fields, Organizational Context, Value Context, Activity Context must appear in that order (core/sql_generator.py's _SECTION_ORDER) — an out-of-order section is a structural deviation from the methodology template, not a parse failure.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Info |
| Posture | advisory |
| Enforced by | sql-validator |
| Codes | sql-validator.section-header-order |
| Since | v3 (v1) |
