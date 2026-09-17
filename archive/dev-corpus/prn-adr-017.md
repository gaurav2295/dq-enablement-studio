---
id: prn-adr-017
type: principle
kind: decision
title: ADR D-17 — Per-user workspaces now; the other three session kinds stay global behind a documented shim
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-17
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Per-user workspaces now; the other three session kinds stay global behind a documented shim.

## Rationale

Workspace concurrency — two consultants staging different rules from different logins at once — was the one multi-user hazard the tool actually has in daily use today. Audit/Profiler/SKP AssetUpload are typically single-operator, single-sitting tasks where process-global state is a lower-risk simplification to carry one more release.

## Consequence

The owner elected the bigger option — a full per-user, SQLite-backed workspace store (core.store.workspace_store) this release, not deferred. Audit, Profiler, and SKP AssetUpload session state stay process-global, with a _LegacyBulkSessionView shim (falls back to user_id=0, unreachable by real users, inert in production but a documented latent footgun). Per-user isolation for the other three session kinds is the explicit, scoped next-revision follow-up — don't assume it's already done because workspaces are.

> [!note] Provenance
> Architecture decision **D-17** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
