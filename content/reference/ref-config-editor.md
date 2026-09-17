---
id: ref-config-editor
type: reference
title: Session Setup & Settings
domain: studio
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:prc-studio-onboarding
  - relates:con-multi-implementation-model
  - relates:ref-home-page
  - relates:ref-bulk-pipeline
  - relates:std-view-naming-patterns
  - relates:std-zsourcesystemid-convention
  - relates:gls-system-alias
  - relates:gls-working-db
sources:
  - vault:studio-architecture/Studio — Config Editor.md
  - coe:rewritten to usage level for consultant enablement, 2026-08-21
tags: [studio, config, sap, course]
created: 2026-08-20
updated: 2026-08-21
---

## Summary

Session Setup (the Settings space) is where you tell the Studio **which client landscape you are
working in**: the source systems in scope, their aliases, the databases, the profiling sources and
the ERP flavour. Everything downstream — the system filter on every generated rule, how many
implementations a rule fans out to, what the view names say — comes from what you set here.

It is the first thing you touch on a new engagement and the last thing you should change mid-sprint
without telling the team.

## When to use it

- Standing up a new client project before any profiling or rule work
- Adding a source system that came into scope mid-engagement
- Switching between an ECC and an S/4HANA landscape
- Checking, before you trust a batch, that the systems and databases are what you think they are

## What you set here

| Setting | Why it matters to your rules |
|---|---|
| **Source systems / system aliases** | The single most consequential setting. Drives the per-system filter on every rule and the number of implementations a rule fans out to |
| **Excluded systems** | Systems present in the data but out of scope for this engagement |
| **Databases** | Which working, prep and source databases the generated SQL points at |
| **Profiling sources** | Where the Profile space reads from |
| **Project name** | Labels the package and the tracker |

**Aliases are a map from the real system code to a friendly name** — for example the actual
`zSourceSystemID` value on the left, and the short name the client uses on the right. The code is
what filters the data; the alias is what appears in the view name. Because both come from one
entry, the filter and the name can never drift apart. This is also what
[[con-multi-implementation-model|the fan-out model]] counts to decide how many implementations a
rule produces. Read the codes out of the data, not off a slide.

## What to expect

- **Some settings are not editable from the screen.** Naming patterns, the ERP pack, SKP defaults
  and layer strategy are held in the project file and preserved exactly as they are when you save.
  Changing those is a deliberate, hand-edited change — talk to your lead first.
- **Saving from the screen removes the comments** a teammate may have written into the project
  file to explain a choice. If those comments matter, make the change by hand instead of saving
  from the UI.
- **Switching ERP takes effect immediately** — the Studio reloads the knowledge for the new
  landscape without a restart. It is a clean break, not a merge: anything you had in progress in
  another space should be exported first.
- **Two projects ship by default**, one for ECC and one for S/4HANA. Start from the closer of the
  two rather than building from nothing.

> [!warning] Changing systems mid-sprint invalidates work already derived
> Rules derived before the change carry the old system filter and the old view names. If the system
> list changes, re-derive and re-package rather than assuming existing output still matches. Say so
> in the sprint notes.

## Common mistakes

- **Editing the project file by hand and then also saving from the screen.** The save rewrites the
  whole file. Pick one editing path per change.
- **Putting the friendly name where the system code belongs.** The filter then matches nothing and
  the rule quietly returns zero rows — which reads as a clean pass.
- **Leaving the default project settings on a client engagement.** The shipped projects are
  starting points, not client configuration.
- **Assuming the Studio will warn you about an out-of-scope system.** It filters to what you told
  it; it cannot know a system was missing from the list.

## Verification

Before profiling or deriving anything for a client, confirm on screen that the system list matches
the systems actually present in the data, that the databases are the client's, and that the
alias values are the ones the client will recognise in a view name.

## Related

[[prc-studio-onboarding]] · [[ref-home-page]] · [[con-multi-implementation-model]] ·
[[std-view-naming-patterns]] · [[std-zsourcesystemid-convention]] · [[ref-bulk-pipeline]]
