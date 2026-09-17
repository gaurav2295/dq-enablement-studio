---
id: std-studio-config-shape
type: standard
title: Project Configuration — The Four Settings
domain: studio
audience: [consultant, lead]
level: practitioner
status: approved
kind: pattern
sources:
  - dq-studio:.claude/skills_canonical/studio-config-shape.md
  - coe:usage rewrite for consultants
tags: [studio, config, convention]
created: 2026-08-20
updated: 2026-08-21
links:
  - relates:std-view-naming-patterns
  - relates:std-zsourcesystemid-convention
  - relates:con-multi-implementation-model
  - relates:prc-fan-out-a-rule-per-system
  - relates:gls-system-alias
---

## The standard

Every engagement has a **project configuration** that the Studio reads before it derives anything.
Four settings in it look alike and are constantly confused with each other. They are independent,
and treating them as independent is the rule.

| Setting | What it means | What it changes |
|---|---|---|
| **Default source system** | The single system id used when a rule does not name one | The value that fills the system token in a view name |
| **Fan-out scope** | Which systems an Error or Info rule is deployed to | How many sibling implementations a rule fans out into |
| **Display aliases** | Cosmetic labels: source code → friendly name | How the system appears in view names and on screen |
| **Databases** | The prep database and the working database | Which database rule views are created in and read from |

## The invariants

- **An alias is a label, nothing else.** Editing aliases must never change which systems get
  deployed to. If changing a label changed a deployment, that would be a defect.
- **A system in scope with no alias** still deploys — the view name simply uses the raw code.
- **An alias for a system not in scope** is dead decoration. It never causes a deployment.
- **SQL always uses the raw code, never the alias.** A filter reads `zSourceSystemID = 'Z06'` even
  when the alias shows `P06`. See [[std-zsourcesystemid-convention]] and
  [[std-view-naming-patterns]].
- **The prep and working databases stay separate**, even when one is empty. Never infer one from
  the other.

## What you may edit, and where

Edit in the Studio's **Configuration** page: project name, default source system, fan-out scope,
display aliases, and the database names. These are the settings that legitimately change per
engagement and per sprint.

Leave to a CoE change: naming patterns, layer strategy, SKP enforcement defaults, the knowledge
base and the profiling metric definitions. These are set once for the methodology, not tuned per
client.

Scope belongs to the project, not to a batch. There is deliberately no per-batch system picker on
the bulk page — the bulk page shows the project's scope as a **read-only indicator** so you can see
what will happen before you run it. If a batch needs a different scope, change the project
configuration.

## What to expect when you save

- **Only the four settings above are touched.** Everything else in the configuration is preserved
  exactly as it was.
- **Lists are cleaned up:** blanks are dropped and duplicates removed, keeping the order you
  entered them in.
- **A blank alias falls back to the code itself**, so a half-filled alias table is harmless.
- **Saving twice changes nothing.** Re-saving the same values produces an identical file.
- **Comments in the configuration file are lost** on save. The page warns you. If a client-specific
  note matters, keep it in the engagement notes, not in the configuration file.

> [!warning] Check the scope before a bulk run
> Fan-out scope is the setting with real cost attached: it multiplies every Error and Info rule in
> the batch. Confirm the read-only scope indicator on the bulk page matches what the client
> actually has in production before you press run. See [[prc-fan-out-a-rule-per-system]].

## Common mistakes

- Adding a friendly alias and expecting a new system to be deployed to. Add it to the **scope**.
- Removing an alias to "stop deploying" to a system. The deployment continues, only the label
  changes.
- Using the alias in a SQL filter because the view name shows it. The data holds the raw code.
- Pointing the prep and working databases at the same value because a client "only has one". Ask;
  they are different layers and the answer is usually no.

## Related

[[std-view-naming-patterns]] · [[std-zsourcesystemid-convention]] ·
[[con-multi-implementation-model]] · [[prc-fan-out-a-rule-per-system]] · [[gls-system-alias]]
