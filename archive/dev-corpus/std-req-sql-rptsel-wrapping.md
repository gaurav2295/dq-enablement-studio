---
id: std-req-sql-rptsel-wrapping
type: standard
title: REQ-SQL-RPTSEL-WRAPPING — RptSel must reference its OptSel partner
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-RPTSEL-WRAPPING
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

RptSel must reference its OptSel partner.

## Rationale

Methodology expects RptSel to be SELECT * FROM `<OptSel>` WHERE [zIsErrorFlag] = 1 — an RptSel that never references OptSel has drifted from the canonical pattern.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Warn |
| Posture | warn |
| Enforced by | sql-validator |
| Codes | sql-validator.rptsel-not-wrapping-optsel |
| Since | v1 (v1) |
