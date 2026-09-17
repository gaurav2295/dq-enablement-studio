---
id: prn-adr-018
type: principle
kind: decision
title: ADR D-18 — SQLite, not Postgres — behind a swap seam, not a rewrite
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-18
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

SQLite, not Postgres — behind a swap seam, not a rewrite.

## Rationale

The program's own scale (one CoE team, one host) is comfortably inside WAL-mode SQLite's envelope; staying stdlib-only kept the plan's "zero new Python runtime deps" budget intact for the whole build.

## Consequence

data/studio.db (stdlib sqlite3, WAL, check_same_thread=False, a single write-lock, corrupt-DB rename-aside recovery) is the store for this release. Every table access goes through core/store/*.py's repository functions — never raw SQL scattered through route handlers. If the CoE ever outgrows single-host SQLite, the swap target is Postgres behind the same repository layer. Don't let a future call site start assuming SQLite-specific SQL dialect outside that layer, or the seam stops being a seam. (This is also harness-v2's own zero-new-dep budget precedent, D-18, cited by the design for why requirements.json/decisions.json are JSON not YAML.)

> [!note] Provenance
> Architecture decision **D-18** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
