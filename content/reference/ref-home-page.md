---
id: ref-home-page
type: reference
title: The Studio Home Screen
domain: studio
audience: [consultant, instructor]
level: foundation
status: review
links:
  - relates:prc-studio-onboarding
  - relates:con-studio-capabilities
  - relates:ref-single-rule-designer
  - relates:ref-bulk-pipeline
  - relates:ref-profiler-and-audit-pages
  - relates:ref-config-editor
  - relates:gls-dq-studio
sources:
  - vault:studio-architecture/Studio — Home Page.md
  - coe:rewritten to usage level for consultant enablement, 2026-08-21
tags: [studio, orientation, course]
created: 2026-08-20
updated: 2026-08-21
---

## Summary

The home screen is the Studio's **project hub**: it tells you which client project is active, lets
you switch to another, and points into the five spaces where the work actually happens. It is a
starting point, not a workbench — nothing is derived, profiled or shipped from here.

If you are opening the Studio for the first time, work through
[[prc-studio-onboarding|Studio Onboarding — Your First Hour]] rather than exploring from here.

## What you see

- **The active project.** Every piece of work you do belongs to a project — the client landscape
  set up in [[ref-config-editor|Session Setup]]. The hub names the active one.
- **The project switcher.** Move between client projects, or between the shipped ECC and S/4HANA
  starting points.
- **The navigation into the five spaces**, present on every screen.
- **The version badge** in the sidebar footer. Note it before raising an issue or comparing notes
  with a colleague — behaviour differs between versions, and the number is the fastest way to tell
  which one you are describing.

## The five spaces

| Space | What you do there | Unit |
|---|---|---|
| Session Setup | Confirm source systems, aliases and databases for the engagement | [[ref-config-editor]] |
| Schema Profile | Table and Distribution profiling — the per-field census before rule work | [[ref-profiler-and-audit-pages]] |
| DQ Rules (Workspace) | Describe, derive, score and refine rules — one at a time or in bulk | [[ref-single-rule-designer]] · [[ref-bulk-pipeline]] |
| Attribute Usage | Pivot a field's values by org and system to see where a standard is really local | [[prc-run-an-attribute-usage-analysis]] |
| Ship | Package the tracker, deploy SQL, specs and tests for handover | [[prc-generate-the-skp-assetupload]] |

Session Setup and Ship bracket the engagement; the three in between are where the work is done.
Audit and Validate sits alongside the rule work as the quality gate before Ship — see
[[ref-profiler-and-audit-pages]].

The client-facing framing of the same ground — purpose, benefit, impact, what we need from you —
is [[con-studio-capabilities|The Four Studio Capabilities]]. Use that in a scoping conversation;
use the space names above when you are working.

## What to expect

- **No login, no account.** The Studio runs locally. If a guide describes registering an account or
  creating an organisation, it is describing something that does not ship.
- **Old links still work.** Bookmarks to the earlier per-page addresses redirect into the space
  that replaced them. You have not gone somewhere wrong; the layout changed.
- **Switching project switches everything.** The systems, databases and knowledge behind every
  space follow the active project. Export anything in progress before you switch.

## Common mistakes

- **Treating the hub as a dashboard.** There is no engagement status here — the reconciliation
  table in a bulk run and the audit findings are where you read progress.
- **Starting work without checking the active project.** Deriving a client's rules against the
  default project is the single easiest mistake to make, and it is invisible until the view names
  and system filters come out wrong.
- **Quoting the wrong version number.** The version that matters is the one in the sidebar footer.

## Related

[[prc-studio-onboarding]] · [[con-studio-capabilities]] · [[ref-config-editor]] ·
[[ref-single-rule-designer]] · [[ref-bulk-pipeline]] · [[ref-profiler-and-audit-pages]]
