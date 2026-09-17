---
id: std-req-rulename-partial-score
type: standard
title: REQ-RULENAME-PARTIAL-SCORE — A converted rule name should not fail naming heuristics
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-RULENAME-PARTIAL-SCORE
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

A converted rule name should not fail naming heuristics.

## Rationale

A partial score means one or more of the naming heuristics in heuristics.json failed — the name may not read as a clear, testable DQ rule statement.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | rule_spec |
| Severity | Warn |
| Posture | warn |
| Enforced by | rule-name-score |
| Codes | rule-name-score.partial-score |
| Since | v1 (v1) |
