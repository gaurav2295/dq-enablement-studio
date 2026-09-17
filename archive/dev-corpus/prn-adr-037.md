---
id: prn-adr-037
type: principle
kind: decision
title: ADR D-37 — MDM Decision Input / Decision Input label is removed — replaced by an auto-generated Rule Result Usage value
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-37
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

MDM Decision Input / Decision Input label is removed — replaced by an auto-generated Rule Result Usage value.

## Rationale

The legacy 'MDM Decision Input' / 'Decision Input' label asked the user for a value that should never have been user-input in the first place — it's now auto-generated from the metric type as 'Rule Result Usage'. This spans three surfaces: the Profiling Excel template no longer has an MDM column, no existing profiling spec's exported markdown may surface the old label, and the markdown-export business-context text uses the new label.

## Consequence

No Profiling template, spec, or exported markdown may reintroduce the 'MDM Decision Input' / 'Decision Input' label as a user-facing input; the Rule Result Usage value stays auto-generated. Any future Profiling-template change must keep all three surfaces (template header, parser output dict, markdown export string) in sync.

> [!note] Provenance
> Architecture decision **D-37** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
