---
id: std-req-trust-ai-unverified-field
type: standard
title: REQ-TRUST-AI-UNVERIFIED-FIELD — An AI-proposed table.field must be knowledge-base or SAP-baseline verified
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-TRUST-AI-UNVERIFIED-FIELD
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

An AI-proposed table.field must be knowledge-base or SAP-baseline verified.

## Rationale

A table/field pair the AI proposed but that the knowledge base and SAP baseline cannot confirm may be a hallucination — must be verified before deploying.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | rule_spec |
| Severity | Warn |
| Posture | warn |
| Enforced by | table-field-trust |
| Codes | table-field-trust.ai-unverified-field |
| Since | v1 (v1) |
