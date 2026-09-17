---
id: prn-adr-031
type: principle
kind: decision
title: ADR D-31 — enhance_spec itself is not recorded via on_call — leaf-granularity telemetry
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-31
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

enhance_spec itself is not recorded via on_call — leaf-granularity telemetry.

## Rationale

enhance_spec is a leaf-granularity decision: it is NOT itself recorded via on_call — only its sub-calls (convert_rule_name, derive_table_field, generate_implication) record independently. Recording the wrapper as well as its own leaf calls would double-count every AI Enhance in ai_calls telemetry.

## Consequence

Any future enhance_spec-level instrumentation must not add its own on_call invocation on top of the sub-calls' — that would double the exact telemetry rows this test isolates and pins at zero.

> [!note] Provenance
> Architecture decision **D-31** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
