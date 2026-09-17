---
id: prn-adr-019
type: principle
kind: decision
title: ADR D-19 — The per-project-key plaintext-vs-encrypted question is N/A this release — the whole design is deferred, not just the storage choice
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-19
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The per-project-key plaintext-vs-encrypted question is N/A this release — the whole design is deferred, not just the storage choice.

## Rationale

The full api_keys/api_key_projects design (masked admin CRUD, a request > project > session > env resolution order) was scoped and B-gate-confirmed but explicitly deferred by the owner — the harness had to land first, and the current single-session-key model is adequate until multi-project key isolation becomes an actual operational need.

## Consequence

Today's key resolution order (request-supplied key > session-global in-memory key > ANTHROPIC_API_KEY from the environment) is unchanged. No API key is written to disk by this release at all. When that design is picked up, settle the at-rest storage question then — masked display (key[:6]…key[-4:]) is the stated minimum bar. Don't let a future implementer assume "we already decided plaintext is fine for keys" — nothing has been decided, because nothing is persisted yet.

> [!note] Provenance
> Architecture decision **D-19** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
