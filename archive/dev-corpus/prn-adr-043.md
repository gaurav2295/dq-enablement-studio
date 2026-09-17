---
id: prn-adr-043
type: principle
kind: decision
title: ADR D-43 — requirement_for() resolves active requirements only — a superseded requirement sharing a code must never win
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-43
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

requirement_for() resolves active requirements only — a superseded requirement sharing a code must never win.

## Rationale

Fast-follow to the T2 adversarial review: a superseded requirement sharing a requirement code with the active requirement that replaced it must never win the lookup — and must never resolve at all when the superseded entry is the ONLY entry for that code (i.e. no active replacement exists yet).

## Consequence

requirement_for() filters strictly to status == "active" before resolving by code. Any future requirement-lookup helper (mirroring decision_for()'s own status handling) must apply the same active-only filter, not resolve the newest entry by decided_on or list order.

> [!note] Provenance
> Architecture decision **D-43** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
