---
id: prn-adr-030
type: principle
kind: decision
title: ADR D-30 — Golden byte-identity hashes pin the empty-knowledge_context prompt path
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-30
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Golden byte-identity hashes pin the empty-knowledge_context prompt path.

## Rationale

Each hash in TestKnowledgeContextByteParity was captured from the SAME prompt-building code path immediately before knowledge_context was introduced (verified byte-for-byte against a pre-Phase-3 copy of the module from git history). Any future edit that changes what gets sent to Claude on the default (empty-context) path — even reordering whitespace — must be caught immediately, without duplicating the ~90-line static SAP reference block or the ~140-line SQL review prompts verbatim in the test file. One hash (generate_implication) was deliberately re-pinned once, for the v3.5.4 Fix B concision tightening, while the sibling derive_table_field/review_sql hashes stayed frozen — establishing the precedent for when a golden-hash change is intentional vs. a regression.

## Consequence

A future prompt-building change on the empty-context path must either leave these hashes untouched, or deliberately re-pin the specific hash(es) that changed together with a comment explaining why (mirroring the v3.5.4 Fix B precedent) — never a silent bulk re-pin.

> [!note] Provenance
> Architecture decision **D-30** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
