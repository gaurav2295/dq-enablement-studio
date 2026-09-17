---
id: prn-adr-015a
type: principle
kind: decision
title: ADR D-15a — Legacy Jinja pages render unauthenticated page shells (pre-auth HTML exposure is intentional)
domain: studio
audience: [developer]
level: advanced
status: deprecated
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-15a
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Legacy Jinja pages render unauthenticated page shells (pre-auth HTML exposure is intentional).

## Rationale

A narrower sub-decision embedded in D-15's original consequence text and encoded (pre-fix) in tests/test_auth.py's TestUnprotectedSurface class: the legacy Jinja pages' HTML shell was allowed to render for an unauthenticated GET (their /api/* calls would still 401 like everything else) because the SPA shell needs to load to show a login form. Documented in stage-cd-cutover.md as intentional, not a regression to chase.

## Consequence

SUPERSEDED 2026-07-27 by D-22 (Finding C1): an unauthenticated GET of any of the 7 legacy Jinja page routes stranded the user with a fully-normal-looking shell whose every API call silently 401'd, with no redirect and no hint — this was reclassified from "intentional" to a Critical finding and reversed by commit 1a29aa6. TestUnprotectedSurface (the class that used to pin this decision) was itself rewritten by commit 8527856 to assert the opposite (a login redirect) — its current form no longer supports this superseded decision, which is why no test is cited below.

> [!note] Provenance
> Architecture decision **D-15a** in the DQ Studio decision registry, decided 2026-07-27, registry status *superseded*.
