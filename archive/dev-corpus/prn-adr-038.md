---
id: prn-adr-038
type: principle
kind: decision
title: ADR D-38 — Boot-time catalog sync is fail-open — a malformed catalog JSON must never block app startup
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-38
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Boot-time catalog sync is fail-open — a malformed catalog JSON must never block app startup.

## Rationale

app.py's lifespan wraps catalog_index.sync_from_disk() in a try/except and just logs an ERROR on failure, proven end-to-end by actually firing the ASGI lifespan against a corpus directory containing garbage. The fail-open behavior deliberately lives at the app.py call site, not inside sync_from_disk() itself — a separate test pins that sync_from_disk() really does propagate the error, so the try/except above is proven necessary rather than accidentally-dead code.

## Consequence

A corrupted or malformed catalog file on disk must degrade to "catalog search unavailable" rather than preventing the app from booting at all. Any future refactor of the boot sequence must keep the try/except at the app.py call site (not push it down into sync_from_disk, which would make the necessity test above meaningless).

> [!note] Provenance
> Architecture decision **D-38** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
