---
id: prn-adr-063
type: principle
kind: decision
title: ADR D-63 — The hand-edit bypass-gap harness gate always recomputes server-side and never rejects (Task C-gamma, C11)
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-63
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The hand-edit bypass-gap harness gate always recomputes server-side and never rejects (Task C-gamma, C11).

## Rationale

/api/workspace/update/{idx} runs every hand-edited spec through core.harness.session_gate.harness_stamp_spec_dict before it lands in the session — the bypass-gap gate for a hand-edit that never went through an AI call, so it never got a Verdict from HarnessedAIClient any other way. Server-recomputed _harness/_validator_findings must win over whatever the client forged in its POST body, and the gate must never reject the write, even when it can't run at all (an internal exception is fail-soft: the spec is stored exactly as sent, with no partial/garbage _harness key). A dedicated E-2 review fix further ensures the RESPONSE body itself carries the freshly-stamped verdict, since the Workspace SPA's Promote-button state is built directly from this response, not a follow-up GET — before that fix, a save that just earned a fresh verdict left the UI showing "no verdict yet" until the rule was deselected and reselected.

## Consequence

Any future change to the workspace hand-edit save path must preserve all three properties together: server-side recompute always wins over client-forged fields, the write never rejects on any verdict (including Fail) or on an internal gate exception, and the response body — not just the stored session — carries the fresh stamp. Sibling call sites for the same bypass-gap contract exist at harness_stamp_spec_dict directly and at /api/bulk/update-session; if harness-v2 enforcement is ever added, all such call sites must move together.

> [!note] Provenance
> Architecture decision **D-63** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
