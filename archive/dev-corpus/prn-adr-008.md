---
id: prn-adr-008
type: principle
kind: decision
title: ADR D-8 — The rule-pattern branch runs BEFORE, and gates, deletion detection
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-8
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The rule-pattern branch runs BEFORE, and gates, deletion detection.

## Rationale

Precedence order alone isn't enough once two detectors can claim the same textual signal — the gate has to be explicit, or a deletion-detection phrasing could get silently consumed by the pattern library instead.

## Consequence

core/local_deriver.py's pattern-library step (5a) runs BEFORE the deletion-detection step (5b), and 5b is explicitly gated off (pattern_match is None) whenever a pattern matched — even a PartialFill. Any FUTURE pattern whose intent regexes could overlap deletion-detection phrasing must also gate 5b.

> [!note] Provenance
> Architecture decision **D-8** in the DQ Studio decision registry, decided 2026-07-14, registry status *active*.
