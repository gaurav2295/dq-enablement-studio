---
id: prn-adr-015
type: principle
kind: decision
title: ADR D-15 — Parallel-serve cutover — the SPA and the legacy UI run side by side through Stage A/B
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-15
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Parallel-serve cutover — the SPA and the legacy UI run side by side through Stage A/B.

## Rationale

The graph grounding showed the legacy UI as an isolated island touching core only via fetch — a from-scratch rewrite could reach full parity with zero risk to the deterministic core, but cutting over the tool consultants use daily is a separate, much smaller and much more reversible decision than building its replacement. Splitting them means a bad SPA regression discovered after cutover is a link removal / env-var flip, not a code revert.

## Consequence

Mount the React SPA at /app/*; leave every legacy Jinja route byte-untouched except one env-gated pilot link (STUDIO_REACT_PILOT_LINK=1). Flipping which UI is the default (Stage C) and physically removing Jinja (Stage D) are separate, owner-gated follow-ups — not in this build (full detail: docs/plans/stage-cd-cutover.md). NOTE: this decision's own consequence text originally also asserted "the legacy Jinja pages are unprotected page shells even post-auth ... this is intentional ... not a regression to chase" — that narrower sub-claim was a distinct decision (see D-15a), which has since been superseded by D-22 (Finding C1, commit 1a29aa6). D-15 itself — the parallel-serve architecture — is unaffected and remains active.

> [!note] Provenance
> Architecture decision **D-15** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
