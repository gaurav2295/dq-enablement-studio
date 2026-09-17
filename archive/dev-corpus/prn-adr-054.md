---
id: prn-adr-054
type: principle
kind: decision
title: ADR D-54 — The AI-review prompt may reference zIsErrorFlag only in a 'DO NOT add this' context for Profiling rules
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-54
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The AI-review prompt may reference zIsErrorFlag only in a 'DO NOT add this' context for Profiling rules.

## Rationale

zIsErrorFlag is an Error-rule-only construct. The Profiling review prompt is allowed to mention it, but only to explicitly instruct the model NOT to add it — teaching the zIsErrorFlag CASE pattern as valid for Profiling rules would let the model reproduce an Error-only construct in output that must never carry it.

## Consequence

Any future edit to the profiling review prompt must preserve the negative framing around zIsErrorFlag mentions; a prompt change that presents it as an example of valid Profiling SQL would violate this contract even if the mention itself isn't removed.

> [!note] Provenance
> Architecture decision **D-54** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
