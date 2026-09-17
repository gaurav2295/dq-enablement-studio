---
id: prn-adr-047
type: principle
kind: decision
title: ADR D-47 — zDomainSegment: Profiling rules are included, and its source table is picked by a deterministic precedence
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
  - relates:gls-zdomainsegment
sources:
  - dq-studio:knowledge/harness/decisions.json#D-47
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

zDomainSegment: Profiling rules are included, and its source table is picked by a deterministic precedence.

## Rationale

Two related decisions about the zDomainSegment column: (1) Profiling rules also get zDomainSegment when targeting a Customer/Vendor/Material master table, not just Error/Info rules; (2) when more than one master table could qualify it, the user's stated precedence resolves the ambiguity: rule name wins first (for multi-domain ambiguity), falling through to data_domain, then main_table, then a deterministic declared order — never an arbitrary or unstable choice.

## Consequence

Any future rule-type or domain addition that touches zDomainSegment assignment must extend Profiling coverage the same way, and must resolve source-table ambiguity through this exact precedence chain, not a new ad hoc rule.

> [!note] Provenance
> Architecture decision **D-47** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
