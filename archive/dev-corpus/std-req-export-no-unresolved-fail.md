---
id: std-req-export-no-unresolved-fail
type: standard
title: REQ-EXPORT-NO-UNRESOLVED-FAIL — A shipped rule should not carry an unresolved Fail verdict
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-EXPORT-NO-UNRESOLVED-FAIL
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

A shipped rule should not carry an unresolved Fail verdict.

## Rationale

A rule's last-recorded _harness verdict is Fail on a block-posture requirement — the harness rejected it, and shipping it anyway is a signal worth surfacing at export time, even though export itself never blocks on it (R-4).

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | export |
| Severity | Warn |
| Posture | advisory |
| Enforced by | export-unresolved-fail |
| Codes | export-coverage.unresolved-fail |
| Since | v2 (v1) |
