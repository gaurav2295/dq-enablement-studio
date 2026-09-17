---
id: gls-snapshot
type: glossary
title: Snapshot (rule graph)
domain: delivery
audience: [consultant, lead]
level: foundation
status: review
links:
  - parent:gls-rule-repository
  - relates:ref-rule-record-schema
sources:
  - bob-dq:CONTEXT.md
  - bob-dq:CLAUDE.md
tags: [bob-dq, instruments, honesty]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The offline copy of the rule graph embedded in the prototype**, used when the rule server is
not running.

**Always labelled as a snapshot with its date; never presented as live.**

## Usage

The snapshot exists so a client session can run with no network and no server — the same
offline-by-default discipline as the rest of the instrument. What it must not do is let the room
believe it is looking at the current catalogue.

Hence the two-part label: the word *snapshot* **and** its date, together, every time. A date
without the word invites "so it's live?"; the word without a date invites "how old?".

> [!warning]
> A snapshot going stale is a normal condition, not a fault — but an **unlabelled** snapshot is a
> defect, because it makes a claim the data cannot support. Same posture as
> [[gls-indicative]]: state how the thing was made.
