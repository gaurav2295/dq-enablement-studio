---
id: prn-adr-023
type: principle
kind: decision
title: ADR D-23 — RuleNameScoreCheck suspends scoring entirely for Info/Profiling rule types (proposed for ratification)
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-23
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

RuleNameScoreCheck suspends scoring entirely for Info/Profiling rule types (proposed for ratification).

## Rationale

core/harness/checks/rule_name_score_check.py's _SKIP_RULE_TYPES = {"info", "profiling"} encodes a real, undocumented decision: Info (and Profiling) rule names use a different naming style (descriptive, no "must" modal — see AIClient.convert_rule_name's is_relaxed branch), so the 19 Error-rule heuristics don't apply and scoring is suspended entirely rather than adapted. Today this is enforced only implicitly, by test behavior, never stated as a reviewable decision. Harness-v2 design Amendment A3 (Open Question O-8) seeds it here as `proposed`, not `active`, specifically so the owner explicitly ratifies or challenges it rather than it staying silently baked into `_SKIP_RULE_TYPES`.

## Consequence

Gate-recommended answer (owner confirms in morning review): keep the skip as-is. If challenged instead, an Info-appropriate heuristic set would need to be designed before scoring could resume for Info/Profiling rule types — this entry flips to `active` (skip ratified) or is superseded by a new entry (skip reversed) once the owner decides.

> [!note] Provenance
> Architecture decision **D-23** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
