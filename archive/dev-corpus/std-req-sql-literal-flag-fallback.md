---
id: std-req-sql-literal-flag-fallback
type: standard
title: REQ-SQL-LITERAL-FLAG-FALLBACK — OptSel must not ship the literal-1 zIsErrorFlag fallback unreviewed
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
  - relates:gls-literal-1-fallback
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-LITERAL-FLAG-FALLBACK
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

OptSel must not ship the literal-1 zIsErrorFlag fallback unreviewed.

## Rationale

The catalog promoter's literal-1 fallback flags every row as an error when a per-row predicate couldn't be extracted — must be reviewed and replaced before deployment.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Warn |
| Posture | warn |
| Enforced by | sql-validator |
| Codes | sql-validator.literal-flag-fallback |
| Since | v1 (v1) |
