---
id: prn-adr-011
type: principle
kind: decision
title: ADR D-11 — Project memory is capped, visible, and clearable; feedback rides extra_info
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-11
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Project memory is capped, visible, and clearable; feedback rides extra_info.

## Rationale

Learned context that silently grows and never surfaces is a trust hazard; the cap + visibility + clear endpoint make it auditable. A third channel for feedback would duplicate extra_info's existing role.

## Consequence

core/project_memory.py facts are capped at 40 (LRU-ish eviction), fully readable/erasable via GET/DELETE /api/project-memory/{slug}. Feedback text rides the existing extra_info channel, not a third channel. add_fact rejects any text over 300 chars or containing a 6+-digit run — a guard against a client data value leaking into rule knowledge.

> [!note] Provenance
> Architecture decision **D-11** in the DQ Studio decision registry, decided 2026-07-14, registry status *active*.
