---
id: std-req-tracker-unresolved-findings
type: standard
title: REQ-TRACKER-UNRESOLVED-FINDINGS — A tracker row's spec should not still carry unresolved validator findings at export
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-TRACKER-UNRESOLVED-FINDINGS
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

A tracker row's spec should not still carry unresolved validator findings at export.

## Rationale

Formalizes core.audit_engine's ad hoc tracker-consistency checks as a harness-native surface: a tracker row reconciled against its session spec at export time should surface when that spec still carries open validator findings, so the owner sees it at the tracker boundary, not just buried in the spec's own _validator_findings.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | tracker |
| Severity | Warn |
| Posture | warn |
| Enforced by | tracker-consistency |
| Codes | tracker-consistency.unresolved-findings-at-export |
| Since | v2 (v1) |
