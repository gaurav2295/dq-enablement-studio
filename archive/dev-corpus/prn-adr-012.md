---
id: prn-adr-012
type: principle
kind: decision
title: ADR D-12 — Enrichment is an offline pipeline with provenance; runtime never scrapes
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-12
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Enrichment is an offline pipeline with provenance; runtime never scrapes.

## Rationale

Runtime scraping would make rule derivation non-deterministic, network-dependent, and impossible to audit after the fact.

## Consequence

scripts/enrich_knowledge.py is a standalone, manually-run, stdlib-only script with a provenance sidecar. The running Studio app never makes an outbound web request at request-serving time. Any future knowledge-growth mechanism should follow the same offline-pipeline-plus-provenance shape — see D-21, which applies this same discipline to catalog promotion. The harness-v2 design's Pillar-4 test-suite audit (scripts/audit_decisions.py) explicitly follows this same discipline: it proposes, a human merges, it never writes the active registry.

> [!note] Provenance
> Architecture decision **D-12** in the DQ Studio decision registry, decided 2026-07-14, registry status *active*.
