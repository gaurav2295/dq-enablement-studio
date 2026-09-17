---
id: prn-adr-016
type: principle
kind: decision
title: ADR D-16 — Harness v1 ships warn-and-stamp; enforcement is a documented, inert knob
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
  - relates:gls-warn-and-stamp
sources:
  - dq-studio:knowledge/harness/decisions.json#D-16
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Harness v1 ships warn-and-stamp; enforcement is a documented, inert knob.

## Rationale

This build's job is to prove the trust signal is real and consistently computed before anything is allowed to act on it. Flipping enforcement on before the checks have run against a full cycle of real usage risks blocking legitimate output on an untuned false positive — a much worse failure mode for a daily-use tool than a warning nobody acts on yet.

## Consequence

HarnessPolicy.fail_status_blocks_accept stays False for this entire release — every Verdict is computed, recorded, and stamped onto the response, but nothing in the pipeline can currently block or reject a candidate. The enforcement knob is the literal next-revision task. Don't flip it without first deciding the UX of a Fail — that product decision was explicitly not made this cycle. (Harness-v2's Pillar 2 is that next-revision task; see D-26/D-27.)

> [!note] Provenance
> Architecture decision **D-16** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
