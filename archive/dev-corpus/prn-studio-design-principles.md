---
id: prn-studio-design-principles
type: principle
title: The Seven Studio Design Principles
domain: studio
audience: [developer, lead]
level: practitioner
status: approved
sources:
  - dq-studio:.claude/skills_canonical/studio-design-rules.md
tags: [studio, governance, doctrine, engine]
created: 2026-08-20
updated: 2026-08-20
links:

  - relates:prn-studio-non-negotiables
  - relates:prn-studio-workflow-guardrails
  - relates:std-studio-config-shape
  - relates:prn-no-silent-domain-fallback
  - relates:ref-architecture-context-and-project-yamls

---

## What this is

Seven cross-cutting principles that govern design calls in the DQ Studio. They are not aspiration —
they are **this list reverse-engineered from real defects**. Every one of them was written after a
user pushback caught a violation that tests had passed. Cite them by name when justifying a design
call.

Three doctrine units sit side by side and do different jobs. An ADR
records *what* was decided about one specific thing. [[prn-studio-non-negotiables]] fixes the shape
of the artefacts the engines emit, and [[prn-studio-workflow-guardrails]] fixes what the application
will and will not do on the user's behalf. These seven record *how* decisions get made across
everything else.

## 1. Independence of concerns

If two things can vary independently, they **must** be separate fields. Conflation for convenience
always breaks down.

Enforced examples:

- `source_db` (provenance) ≠ `prep_db` (prep layer) ≠ `working_db` (rule repository)
- fan-out scope ≠ `system_aliases` display values
- `rule_id` (per implementation) ≠ `skp_rule_id` (per conceptual rule)

When proposing a new field, ask: would a user ever want this to vary while a related field stays
fixed? If yes, it is a separate field.

## 2. No silent magic

If the system has a default behaviour, the user must **see it before the action runs**. An
invisible default is an unreported bug.

- Defaults appear as read-only indicators on the page that consumes them.
- Behaviour changes are telegraphed in the UI — banner, hint, badge.
- Anything pulled from the environment (env vars, config files) is surfaced through the API status
  endpoints.

## 3. Fail loudly, not silently

Generic errors and silent fallbacks are how a system hides its defects. Surface failures with
enough context to diagnose them.

- Reject malformed input with a message naming the field **and** the expected shape.
- Declare parameter types explicitly at API boundaries — e.g. `Form()` for multipart, because
  multipart silently drops untyped fields.
- Give diagnostics their own endpoints (`/api/config/ai/test-connection`) so a failure is isolated
  from the workflow it would otherwise poison.

## 4. Author at the right granularity

The user describes intent at the level that is **logically meaningful**, not at the level the
system happens to deploy at.

- One Excel row per conceptual rule; the Studio handles fan-out.
- DQOps IDs are assigned at generation, not authored.
- Project-level config is edited once, not per rule.

Don't ask for 30 rows when one row plus a project default will do. Equally, don't ask someone to
edit one thing that silently reshapes 30 artefacts they cannot see.

## 5. Editable where edited, configurable where configured

UI for things actively edited; YAML for things set once; code or JSON for things that are part of
the engine.

| Home | What lives there |
|---|---|
| UI (Configuration page) | `source_systems`, `system_aliases`, `databases`, `source_system` |
| YAML only | `naming:` patterns, `layer_strategy`, `skp` defaults |
| Code / JSON only | Knowledge base (domains, joins, primary keys, heuristics), profiling metric definitions |

## 6. Trust but verify

A change that is "wired up" is not proven until it has been verified end-to-end through the running
app.

1. Run the unit suite (`python3 -m pytest tests/ -q`).
2. Restart the app.
3. Smoke the actual endpoint (curl).
4. Confirm the user-visible behaviour matches the intent.

The Excel-upload `Form()` defect was a unit-tests-passed, integration-broken case. Only step 3
catches that class.

## 7. Bias to additive change

New fields, new endpoints, new options are additive. Removing or re-shaping existing surface needs
explicit approval.

- New spec fields are added alongside existing ones, never replacing them.
- Soft-migration aliases (the `filter_db` → `prep_db` property, the `databases.prep → filter →
  source` fall-through) keep legacy YAMLs, saved specs and tests working.
- Defaults are preserved across versions; new behaviour is opt-in.

## Decision-time checklist

Run this before proposing an approach:

- Does this conflate two independently-varying concepts? (1)
- Is the resulting behaviour visible in the UI *before* the user acts on it? (2)
- If this goes wrong, will the error message diagnose it? (3)
- Am I asking the user to author at the right level — not too fine, not too coarse? (4)
- Is this edited often enough to warrant UI, or is YAML the right home? (5)
- Have I verified it end-to-end in the running app, not just in tests? (6)
- Does this break legacy projects or saved data, and if so is there a soft-migration path? (7)

If any answer is uncomfortable, surface it before proceeding.

## The defects these came from

| Defect | Principles violated |
|---|---|
| Silent fan-out across alias keys | 1, 2 |
| `filter_db` doing both prep and filter work | 1 |
| Excel `start_id` silently defaulting to 1 | 3, 6 |
| Default Systems picker on the bulk page | 4, 5 |
| The two-spec model for profiling | 1 |
| `ANTHROPIC_BASE_URL` hijacking the AI client | 3 |

> [!tip] When someone pushes back on a design call
> It is almost always one of these principles flagging a violation. Map the pushback to the
> principle, acknowledge the violation, propose the fix. Arguments from convenience or "it works
> for now" lose to the principles in this project, every time.

## Related

prn-studio-decision-registry · [[std-studio-config-shape]] ·
[[ref-architecture-context-and-project-yamls]] · std-harness-requirements ·
[[prn-no-silent-domain-fallback]]
