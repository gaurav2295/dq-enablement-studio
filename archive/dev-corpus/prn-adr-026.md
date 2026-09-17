---
id: prn-adr-026
type: principle
kind: decision
title: ADR D-26 — Verdict gains errored_checks; decide() is fail-closed on it under enforcing mode (A1)
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-26
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Verdict gains errored_checks; decide() is fail-closed on it under enforcing mode (A1).

## Rationale

Before T1 landed, the pipeline's fail-soft except (pipeline.py:82-93) swallowed a raising Check — it stayed in checked_by but contributed zero findings, so a check that couldn't run was indistinguishable from one that ran clean. That's a silent trust hole once enforcement becomes real. Adversarial gate-approved amendment A1 (design doc header, 2026-07-27) has two halves. Half 1 (field + stamping) is DONE: T1 (commit f37fe1e, landed 2026-07-27) added Verdict.errored_checks: list[str], appended to in that except branch and serialized in to_dict() (additive) — tested by tests/test_harness_pipeline.py::TestFailSoft::test_raising_check_lands_in_errored_checks. Half 2 (enforcement) is DONE: T5 (commits 1b3cd10, 2d7ddd5; landed 2026-07-27) added core/harness/enforcement.py's decide(), keyed off core.harness.pipeline.HarnessPolicy.fail_status_blocks_accept as the kill-switch, plus knowledge/harness/enforcement.json. Under enforcing mode with the kill-switch on, decide() fails CLOSED when errored_checks is non-empty — a Check that couldn't run means the artifact is unverified, so enforcement refuses rather than accepting on the strength of a verdict silently missing a judgment, exactly as this decision specifies.

## Consequence

Fail-soft to observe is TRUE (errored_checks is populated and visible on every Verdict, per T1). Fail-closed to enforce LANDED with T5 (commit 1b3cd10, 2026-07-27): core/harness/enforcement.py's decide() reads errored_checks and blocks under enforcing mode + the kill-switch, covered by tests/test_harness_enforcement.py::TestDecideErroredChecksFailClosed's posture x mode x kill-switch x errored_checks truth table. Flipped proposed -> active on 2026-07-27 accordingly. Note: T5 wires decide() as a pure seam only — per Amendment A5 no live call site (not even promote's) consults it yet; that wiring is a later task.

> [!note] Provenance
> Architecture decision **D-26** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
