---
id: std-req-ai-edit-scope
type: standard
title: REQ-AI-EDIT-SCOPE — AI Enhance's SQL Review may only change joins and error-flag logic
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-AI-EDIT-SCOPE
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

AI Enhance's SQL Review may only change joins and error-flag logic.

## Rationale

review_sql returns a full SQL rewrite, but the deterministic shell (core/local_deriver.py + core/sql_generator.py) owns output-field structure, the Syniti Technical Fields block, and WHERE-exclusion clauses. AIEditScopeCheck diffs the AI's corrected SQL against the pre-AI shell section-by-section (knowledge/methodology/shell_guardrails.yaml: ai_enhance_scope) so an edit outside joins/logic is visible instead of silently accepted.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Warn |
| Posture | warn |
| Enforced by | ai-edit-scope |
| Codes | ai-edit-scope.out-of-scope-edit |
| Since | v3 (v1) |
