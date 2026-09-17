---
id: gls-local-re-derive
type: glossary
title: Local Re-Derive
domain: studio
audience: [developer]
level: practitioner
status: review
links:
  - relates:ref-bulk-pipeline
  - relates:ref-local-deriver
  - relates:gls-ai-enhance
  - relates:gls-deterministic-shell
sources:
  - vault:studio-architecture/Studio — Bulk Processor & DQOps ID Invariants.md
tags: [bulk, derivation]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

Re-running the **deterministic** deriver over a rule after its name or spec changed — the second
step of AI enhancement, and the reason an AI-improved name produces improved SQL rather than just
better prose.

## Usage

The order matters: enhance the name first, then re-derive locally, then (optionally) review the SQL
with AI. A better name matches more knowledge, so the deterministic path gets a second, better
attempt before any model is asked to write SQL.

Catalog-sourced rules **skip** the re-derive — their SQL is authoritative and travels verbatim.
