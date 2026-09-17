---
id: prn-adr-055
type: principle
kind: decision
title: ADR D-55 — The SQL validator flags sibling-replication drift, literal-flag fallbacks, and raw catalog-methodology bypass
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-55
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The SQL validator flags sibling-replication drift, literal-flag fallbacks, and raw catalog-methodology bypass.

## Rationale

Regression checks for issues the bulk-pipeline audit fixes caught: (1) a sibling-replicated rule whose banner still carries the LEAD rule's id while the view name carries the SIBLING's id (or vice versa) is flagged High as view-name-rule-id-mismatch, tolerant of zero-padding (0042 vs 42 is still a match); (2) a zIsErrorFlag that falls back to a literal instead of a real CASE is flagged Medium as literal-flag-fallback; (3) a raw Syniti-Rule-Catalog passthrough with no methodology-promoter banner is flagged High as catalog-methodology-bypass.

## Consequence

These three checks must keep firing on the exact shapes the bulk-pipeline audit found, and must stay clean on the corresponding fixed shapes (matched ids, a real CASE, a methodology promoter banner present). Any future SQL-validator check addition in this family should follow the same clean/dirty paired-test shape.

> [!note] Provenance
> Architecture decision **D-55** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
