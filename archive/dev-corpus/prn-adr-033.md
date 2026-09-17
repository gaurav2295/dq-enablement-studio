---
id: prn-adr-033
type: principle
kind: decision
title: ADR D-33 — StoreRecorder's fail-open guarantee holds at every call site, not just the unit level
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-33
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

StoreRecorder's fail-open guarantee holds at every call site, not just the unit level.

## Rationale

tests/test_harness_storage.py proves StoreRecorder's write is fail-open at the unit level, but that alone doesn't guarantee every caller actually benefits from it. Two separate call-site tests close that gap end-to-end: /api/ai/enhance must still return its normal 200 payload even if StoreRecorder's own write blows up, and the bypass-gap harness session gate (harness_stamp_spec_dict) must still stamp _harness/_validator_findings onto the spec dict even when the DB write underneath it is broken — only the DB write itself is swallowed, never the whole run.

## Consequence

Any new call site that writes a harness_verdicts row via StoreRecorder must be proven fail-open the same way (a broken DB must never surface as a 5xx or a missing verdict stamp) before it ships. If a future call site turns out NOT to be fail-open, that's a bug against this decision, not a silent exception.

> [!note] Provenance
> Architecture decision **D-33** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
