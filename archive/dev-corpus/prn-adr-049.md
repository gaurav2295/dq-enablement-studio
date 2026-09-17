---
id: prn-adr-049
type: principle
kind: decision
title: ADR D-49 — Starting SKP Rule ID is page-level and threads through the Excel-upload endpoint's multipart form
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-49
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Starting SKP Rule ID is page-level and threads through the Excel-upload endpoint's multipart form.

## Rationale

The bulk page exposes a "Starting SKP Rule ID" integer input that seeds the SKP_RULE_`<n>` counter for auto-generated ids, mirroring the existing DQOps starting-number input (the Excel template can't enumerate every fanned-out id, so both starting numbers are page-level, not per-row). Without explicit Form(...) annotations on the /api/bulk/upload-excel endpoint, FastAPI silently treats start_id/start_skp_id as query params, ignores the multipart values, and the bulk processor falls back to defaults — making the bulk page's input fields silent no-ops on the Excel-upload path specifically.

## Consequence

/api/bulk/upload-excel must bind start_id and start_skp_id from the multipart form body. A row that explicitly sets skp_rule_id keeps that value verbatim; the auto-counter still starts from start_skp_id and is never bumped by a user-supplied row override, matching how row-level DQOps overrides are already handled (D-1).

> [!note] Provenance
> Architecture decision **D-49** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
