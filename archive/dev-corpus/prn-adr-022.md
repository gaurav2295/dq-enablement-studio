---
id: prn-adr-022
type: principle
kind: decision
supersedes: prn-adr-015a
title: ADR D-22 — Legacy Jinja page routes redirect an unauthenticated GET to the SPA login (Finding C1)
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-22
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Legacy Jinja page routes redirect an unauthenticated GET to the SPA login (Finding C1).

## Rationale

Finding C1 (Critical): an unauthenticated GET of any of the 7 legacy Jinja page routes (/, /workspace, /profile, /ship, /audit, /settings, /methodology) rendered a fully-normal-looking shell whose every API call silently 401'd, stranding the user with no redirect and no hint. Fixed by commit 1a29aa6 ("fix(auth): redirect unauthenticated legacy pages to /app/login").

## Consequence

These 7 routes now check the session cookie directly (via the same validate_session get_current_user uses) and 302 to the SPA login with `next` pointing at the /app twin when there's no valid session. /health, /static/*, /app/*, and all /api/* behavior are untouched. Supersedes D-15a.

> [!note] Provenance
> Architecture decision **D-22** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
