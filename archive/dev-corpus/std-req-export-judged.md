---
id: std-req-export-judged
type: standard
title: REQ-EXPORT-JUDGED — A shipped rule should have been judged by the harness at least once
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-EXPORT-JUDGED
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

A shipped rule should have been judged by the harness at least once.

## Rationale

A rule with no _harness stamp at all was never judged (predates the harness or was hand-loaded) — the export observer cannot vouch for it, which the owner should be able to see.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | export |
| Severity | Warn |
| Posture | advisory |
| Enforced by | export-no-verdict |
| Codes | export-coverage.no-verdict |
| Since | v2 (v1) |
