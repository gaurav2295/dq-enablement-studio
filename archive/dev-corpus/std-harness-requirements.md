---
id: std-harness-requirements
type: standard
title: The Harness Requirement Contracts
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - relates:gls-ai-harness
  - relates:gls-candidate
  - relates:gls-verdict
sources:
  - dq-studio:knowledge/harness/requirements.json
  - dq-studio:knowledge/harness/enforcement.json
tags: [requirement, harness, governance]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

The DQ Studio enforces its methodology through **machine-readable requirement contracts** — 36
formal rules, each with an id (`REQ-SQL-…`, `REQ-SPEC-…`, `REQ-TRACKER-…`), the artifact it
governs, a rationale, a severity (`Fail` or `Warn`), an enforcement posture, and the harness
check that enforces it. Every AI-produced artifact is stamped with a verdict against these
contracts; promotion requires `Pass`.

Each contract is a child unit of this one (`std-req-*` — see the Referenced by list below once
built, or browse Standards filtered to the `requirement` tag).

## Why contracts instead of prose

A standard written only in prose drifts: reviewers apply it unevenly and AI output can't be
gated on it. A contract with an id, a severity and an enforcing check is testable — the
methodology stops being advice and becomes an invariant.

## Enforcement postures

Enforcement is configured per entry point (AI call, save, export…), each with a mode and
rationale. A `block` posture stops the pipeline on `Fail`; softer postures record the verdict
and let a human decide. The posture registry lives beside the contracts in the Studio's
harness knowledge (`knowledge/harness/enforcement.json`).

> [!note]
> The contracts are versioned (`version`, `since`) and never silently deleted — a withdrawn
> contract is marked `status: retired` in the registry, and its unit here is deprecated.
