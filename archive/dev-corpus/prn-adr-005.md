---
id: prn-adr-005
type: principle
kind: decision
title: ADR D-5 — Client data stays out of git
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-5
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Client data stays out of git.

## Rationale

Confidentiality. Real client AUA outputs, customer counts, entity names, and knowledge/clients/* dictionaries must never be committed.

## Consequence

knowledge/clients/* is hard-excluded via .gitignore and must stay that way; client deliverables live only in ~/Downloads.

> [!note] Provenance
> Architecture decision **D-5** in the DQ Studio decision registry, decided 2026-06-30, registry status *active*.
