---
id: prn-adr-013
type: principle
kind: decision
title: ADR D-13 — Pattern reconciliation must be durable across re-derives, not one-shot
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-13
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Pattern reconciliation must be durable across re-derives, not one-shot.

## Rationale

Sourcing original_rule_name from the CURRENT display name works for the first AI-conversion but breaks on every subsequent one — a second re-derive would read the already-converted name, find no pattern match, and silently fall back to a TBD placeholder, reproducing the original bug one round later.

## Consequence

The phrasing that triggers a rule-pattern match is stashed as a durable spec._pattern_source_name the FIRST time it's ever discovered, persisted through every session/response path _rule_pattern already uses. Any NEW re-derive caller must thread _pattern_source_name the same way — grep for it before adding a new re-derive call site.

> [!note] Provenance
> Architecture decision **D-13** in the DQ Studio decision registry, decided 2026-07-15, registry status *active*.
