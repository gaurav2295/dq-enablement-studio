---
id: std-req-rulename-full-score
type: standard
title: REQ-RULENAME-FULL-SCORE — A converted rule name should pass all naming heuristics
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-RULENAME-FULL-SCORE
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

A converted rule name should pass all naming heuristics.

## Rationale

A 100% score confirms the name follows every methodology naming heuristic in knowledge/methodology/heuristics.json — an informational confirmation, not a defect.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | rule_spec |
| Severity | Info |
| Posture | advisory |
| Enforced by | rule-name-score |
| Codes | rule-name-score.full-score |
| Since | v1 (v1) |
