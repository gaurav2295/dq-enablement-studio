---
id: prn-adr-010
type: principle
kind: decision
title: ADR D-10 — knowledge_context and extra_info are never merged
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-10
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

knowledge_context and extra_info are never merged.

## Rationale

The two parameters carry different trust levels — knowledge_context is KB-derived fact, extra_info is user-authoritative and should win on conflict.

## Consequence

Every AI-client call that accepts both parameters renders them into SEPARATE, clearly labeled prompt sections — never concatenated. Any new AI-facing parameter carrying KB facts must stay separate from extra_info.

> [!note] Provenance
> Architecture decision **D-10** in the DQ Studio decision registry, decided 2026-07-14, registry status *active*.
