---
id: prn-adr-006
type: principle
kind: decision
title: ADR D-6 — One version, single-sourced; unknown domains highlight not empty
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-6
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

One version, single-sourced; unknown domains highlight not empty.

## Rationale

version.py must be the only place the version lives (app.py and base.html read from it) so a version is never hardcoded in markup again. Separately, when a rule's domain isn't modelled, silently returning a blank spec or guessing a domain would hide a real coverage gap from the consultant.

## Consequence

Bump version.py + CHANGELOG.md per release, never hardcode a version in markup. The deriver returns an explicit "not in coverage" placeholder that names the miss and lists covered domains whenever a rule's domain isn't modelled.

> [!note] Provenance
> Architecture decision **D-6** in the DQ Studio decision registry, decided 2026-06-30, registry status *active*.
