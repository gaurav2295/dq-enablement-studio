---
id: prn-adr-020
type: principle
kind: decision
title: ADR D-20 — Bootstrap is env-mandatory on any non-loopback deployment
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-20
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Bootstrap is env-mandatory on any non-loopback deployment.

## Rationale

The loopback binding is intentional and race-safe for the laptop-first case the bootstrap endpoint was originally designed for; a server operator behind nginx never has a 127.0.0.1 request to make, so an env-var seeded first-admin path is the only mitigation, not a nice-to-have.

## Consequence

POST /api/auth/bootstrap only succeeds while the users table is empty (race-safe, one-time). Every server deployment MUST set STUDIO_ADMIN_PASSWORD (enforced as a required Compose variable, ${VAR:?...}) to get an admin account at all on a networked deployment. This is a flagged, owner-visible deviation from the original decision that bootstrap works identically "in every mode" — mitigated, not silently different. docs/DEPLOY-LINUX.md is the authoritative first-boot sequence; keep it in sync if this posture ever changes.

> [!note] Provenance
> Architecture decision **D-20** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
