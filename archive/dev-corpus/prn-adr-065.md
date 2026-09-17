---
id: prn-adr-065
type: principle
kind: decision
title: ADR D-65 — workspace_sessions.user_id has no foreign key onto users, so the synthetic test-user id=0 can read/write
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-65
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

workspace_sessions.user_id has no foreign key onto users, so the synthetic test-user id=0 can read/write.

## Rationale

Migration 5 deliberately dropped the FK from workspace_sessions.user_id onto users, specifically so user_id=0 — the conftest auth-bypass's synthetic test-user, and also the fallback id D-17's _LegacyBulkSessionView shim uses — can read/write a workspace row without a matching users row existing at all. Pre-migration-5 this would raise sqlite3.IntegrityError.

## Consequence

This is the concrete schema mechanism behind D-17's per-user-workspace design: any future schema change to workspace_sessions must not reintroduce a FK onto users, or it would break both the test-user bypass and D-17's shim fallback. If real per-user isolation is ever added for the other three session kinds (D-17's stated follow-up), this same FK-free schema choice should be revisited deliberately, not accidentally reinstated.

> [!note] Provenance
> Architecture decision **D-65** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
