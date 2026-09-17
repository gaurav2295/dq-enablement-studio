---
id: prn-adr-066
type: principle
kind: decision
title: ADR D-66 — Promote's kill-switch is pinned True at the call site, not a live config knob — rollback is per-requirement posture + per-path mode
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-66
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Promote's kill-switch is pinned True at the call site, not a live config knob — rollback is per-requirement posture + per-path mode.

## Rationale

HarnessPolicy.fail_status_blocks_accept is documented (D-16; Design doc §Pillar 2) as the harness's master safety switch — “a single-flag rollback if enforcement ever misbehaves in production”, forcing advisory everywhere even where an entry path's mode is enforcing. Task T6 wires promote through core.harness.enforcement.decide() (api/catalog.py::_decide_safe), but does so by constructing HarnessPolicy(fail_status_blocks_accept=True) as a Python literal at that one call site — there is no config file, env var, or request-time source for this value in v2. Per Amendment A5, promote is the ONLY entry path that actually consults decide() this cycle; building a shared, externally-toggleable kill-switch value for a mechanism only one caller uses would be speculative configurability (karpathy) ahead of the need.

## Consequence

The kill-switch as originally envisioned (one flag, flips enforcement off everywhere) is not an operable lever today — flipping it would require a code change to api/catalog.py::_decide_safe, not a knowledge-file edit. What IS operable without a code change: (1) a requirement's posture in knowledge/harness/requirements.json (block -> warn/advisory) changes which findings can ever reach _harness_gate's posture-block branch (FIX 2, adversarial review of T6); (2) knowledge/harness/enforcement.json's promote row mode (enforcing -> advisory) makes decide() return allowed=True regardless of posture, disabling that same branch. CRITICALLY, neither lever touches _harness_gate's other two refusals: the pre-T6 Pass-required status check (a hardcoded string compare that never consulted decide(), even before T6) and the belt-and-suspenders errored-checks refusal (T7 gate follow-up: read directly off the stored _harness dict, deliberately independent of decide()/the registries so a corrupted registry can never silently allow an unverified verdict through — see api/catalog.py::_harness_gate). So 'rollback' in v2 is scoped to the posture-block mechanism only, not a system-wide disable. A real config-driven kill-switch value is future work, gated on a second entry path (save/AI-call/export) actually going live and needing its own independently-toggleable value — building it for promote alone would be premature.

> [!note] Provenance
> Architecture decision **D-66** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
