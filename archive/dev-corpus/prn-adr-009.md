---
id: prn-adr-009
type: principle
kind: decision
title: ADR D-9 — SQL skeletons live in Python code; regexes + lexicon live in JSON
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
  - relates:gls-sql-skeleton
sources:
  - dq-studio:knowledge/harness/decisions.json#D-9
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

SQL skeletons live in Python code; regexes + lexicon live in JSON.

## Rationale

The pattern shapes need real conditional branching that a JSON template language would have to reinvent from scratch.

## Consequence

core/rule_patterns.py owns the actual CASE/EXISTS SQL as Python f-string builders. knowledge/methodology/rule_patterns.json owns only the intent-detection regexes and the partner-function lexicon. Don't move SQL fragments into the JSON file to make it "more data-driven" — that's the interpreter nobody wants to build. This is the direct precedent Pillar 1 of the harness-v2 design cites when rejecting a generic rule-interpreter over requirements.json.

> [!note] Provenance
> Architecture decision **D-9** in the DQ Studio decision registry, decided 2026-07-14, registry status *active*.
