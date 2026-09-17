---
id: prn-adr-042
type: principle
kind: decision
title: ADR D-42 — The deploy-script generator's DROP VIEW guard uses the real extracted view name, never a naive [dbo].[dbo] fallback
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-42
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The deploy-script generator's DROP VIEW guard uses the real extracted view name, never a naive [dbo].[dbo] fallback.

## Rationale

Regression for the package-27 bug: feeding a 2-part-named CREATE VIEW into the deploy-script generator used to produce a DROP VIEW guard that targeted the wrong (naive, double-[dbo]) name for every rule, not the actual extracted view name.

## Consequence

The DROP VIEW guard must always use the name actually extracted from the CREATE VIEW statement it is guarding, end-to-end. Considered borderline by the human audit pass (a bug-fix pin rather than a deliberate policy choice) but recorded here for completeness of the audit trail, per the T4 gate's broader marker-expansion sweep.

> [!note] Provenance
> Architecture decision **D-42** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
