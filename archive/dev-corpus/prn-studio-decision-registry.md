---
id: prn-studio-decision-registry
type: principle
title: The Studio Decision Registry (ADRs)
domain: studio
audience: [developer]
level: practitioner
status: approved
links:
  - relates:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/decisions.json
tags: [adr, harness, governance]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

Every consequential architecture decision in the DQ Studio is recorded as an ADR — id, title,
status, decision date, rationale, and consequence — in a machine-readable registry. The 68
decisions are seeded here as child units (`prn-adr-*`, kind `decision`); browse Principles
filtered to the `adr` tag, or follow the Referenced by list.

## Why a registry

A decision that lives only in a commit message gets re-litigated. The registry makes the
"why" durable: when behaviour looks odd, the ADR says whether it is deliberate, what breaks if
you change it, and what the sanctioned alternative is. New decisions append; reversals are new
ADRs that supersede old ones — history is never rewritten.

> [!tip]
> Before "fixing" surprising Studio behaviour, search the ADRs for it. The most expensive bugs
> are reversals of deliberate decisions.
