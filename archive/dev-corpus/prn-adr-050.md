---
id: prn-adr-050
type: principle
kind: decision
title: ADR D-50 — DeriveRequest.profiling_input is Optional[dict] = None — an explicit JSON null must not 422
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-50
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

DeriveRequest.profiling_input is Optional[dict] = None — an explicit JSON null must not 422.

## Rationale

Latent v3.4.0 bug: DeriveRequest.profiling_input was typed dict = None instead of Optional[dict], so pydantic v2 rejected an explicit JSON null for the field (only the unvalidated Python-side default was permitted). Any caller that serializes the field explicitly — e.g. a client round-tripping a spec dict verbatim — would 422 on a perfectly ordinary, non-profiling rule.

## Consequence

api/routes.py's DeriveRequest.profiling_input stays Optional[dict] = None. Any future request-model field with a None default must use Optional[...] explicitly rather than relying on pydantic to infer it from the default value alone.

> [!note] Provenance
> Architecture decision **D-50** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
