---
id: prn-adr-045
type: principle
kind: decision
title: ADR D-45 — Cross-field comparison rules bind OBJECT to table_field and REFERENCE anchors the SQL comparison
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-45
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Cross-field comparison rules bind OBJECT to table_field and REFERENCE anchors the SQL comparison.

## Rationale

For a cross-field comparison rule ('X must be aligned with Y'), the rule's OBJECT (matched[0]) drives the derived LogicEntry's table_field, while the REFERENCE (matched[1]) anchors the comparison so the generated SQL CASE WHEN evaluates X <> Y in the right direction. This is the fix for a user-reported gap on the GL consistency rule, where the wrong operand was driving the LogicEntry.

## Consequence

Any future comparison-rule phrasing must keep OBJECT and REFERENCE bound in this fixed order; swapping them silently would flip which field is treated as the rule's subject in both the markdown Logic section and the generated SQL.

> [!note] Provenance
> Architecture decision **D-45** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
