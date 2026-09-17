---
id: prc-qa-a-blueprint
type: procedure
title: QA a Blueprint Before It Ships
domain: delivery
audience: [consultant, lead]
level: advanced
status: deprecated
sources:
  - bob-dq:bob-canvas/concept-stress-test.md
  - bob-dq:handover/b2-walkability-2026-08-06.md
links:
  - prereq:ref-deliverables-inventory
  - relates:con-engagement-phases
  - relates:prn-value-discipline
  - relates:std-client-vocabulary
  - relates:prc-handle-the-cold-room
  - relates:prc-run-the-blueprint-room
  - relates:prc-audit-rule-quality
  - relates:con-outcome-hierarchy-l1-l5
  - relates:con-audience-altitude
  - relates:gls-walkability
  - relates:gls-indicative
  - relates:gls-provenance
tags: [bob-dq, delivery, qa, credibility, stress-test]
created: 2026-08-20
updated: 2026-08-20
---

## Goal

Put a blueprint — or any client-facing instrument that carries value figures — through the
credibility gates **before** it goes in front of an executive audience. The rubric below is the
stress-test protocol distilled into a reusable checklist: what to test, how hard each failure
bites, and which failures are not allowed out of the room at all.

## When to use

- Before any client-facing walkthrough of a blueprint, canvas or value instrument
- After any change that touches a figure, a label, an assumption or a narrative surface
- When validating that an outcome is fit to be published at all (the walkability gate below)

## Prerequisites

- The artefact in its shipping form (published HTML, offline, as the client will open it)
- The [[ref-deliverables-inventory|deliverables inventory]] for the engagement, so you know which
  surfaces exist
- The assumptions sheet and the export/working file, because they are tested as surfaces too

## The central risk the rubric attacks

**Value potential is value living in the data — the size of a business case that could be built and
evidenced — not money bookable to the P&L, and not a forecast.** Any surface that invites the profit
reading fails the instrument *the moment a CFO checks it*. Every gate below exists to make that one
misreading impossible.

## Severity and mode

| Severity | Meaning |
|---|---|
| **SEV-1** | Must not go in front of an executive audience failing |
| **SEV-2** | Damages credibility under challenge |
| **SEV-3** | Polish |

| Mode | Meaning |
|---|---|
| **AUTOMATED** | Script-evaluable, no interpretation |
| **JUDGED** | A reading agent applies the criterion; comprehension judgements use a **fresh** reader given only the specified surface text |

The "fresh reader" rule is load-bearing. Anyone who helped build the artefact cannot judge whether
it reads correctly cold, and the room will read it cold.

## The check families

| Family | What it tests | Peak severity |
|---|---|---|
| **CI · Concept integrity** | The single-euro walk completes on screen; every driver traces to its rules; tallies agree across every surface; no orphan assertions | 1 |
| **CO · Comprehension** | A naive reader draws the right conclusions from the text alone | 1 |
| **PL · P&L misreading hunt** | No surface, standing alone, invites the booked-money reading | 1 |
| **HD · Honesty discipline** | Every figure carries indicative + basis; measured vs assumed never blurred; no invented sources | 1 |
| **AD · Adversarial personas** | Sceptical CFO, hostile data lead, procurement buyer — answerable from screen | 1 |
| **NC · Narrative coherence** | One vocabulary, one story from opening to summary | 2 |
| **TC · Tone conformance** | No internal shorthand reaches a client surface | 1 |
| **FR · Functional + regression** | Arithmetic invariants, round-trips, zero console errors, offline integrity | 1 |
| **AX · Accessibility** | Contrast, keyboard reach, reduced motion, zoom reflow | 2 |
| **SR · Spec reconciliation** | Every spec assertion recorded BUILT-AS-SPECCED / DIVERGED / ABSENT | 2 |

## The naive-reader statement test (CO-1)

Extract the artefact's narrative text only. A fresh reader marks each statement TRUE / FALSE /
CANNOT SAY.

| # | Statement | Expected |
|---|---|---|
| S1 | Indicative range, not a commitment | TRUE |
| S2 | Value that could be evidenced in the data — the size of a business case | TRUE |
| S3 | Every part traces to a named rule that would run on their data | TRUE |
| S4 | The assumptions can be opened and changed | TRUE |
| S5 | Nothing measured yet; the engagement replaces assumptions with evidence | TRUE |
| S6 | This money will be booked to the P&L | **FALSE** |
| S7 | This is a forecast of next year's savings | **FALSE** |
| S8 | The figure has been audited/validated against their data | **FALSE** |
| S9 | The top of the range is what they should expect to achieve | FALSE |
| S10 | The figure can be added to other business cases | FALSE |

**Pass:** S6, S7 and S8 all FALSE — **zero tolerance**; at least 8 of 10 overall; no critical
CANNOT SAY. Re-run the same test on the main working surface with the introduction skipped: S6/S7/S8
must still come out FALSE, because a reader who joins the session late never sees the intro.

## The P&L misreading hunt (PL)

Take each surface **standing alone** — collapsed summary, cards, expanded rows, summary panel,
package modal, exported file read cold — and ask:

1. Is it labelled indicative on or adjacent to the figure?
2. Is the basis reachable in **at most one interaction**?
3. Does any word imply booked money, savings, profit or forecast?
4. Would a CFO reading only this surface have grounds to say *"that's €X to my P&L"*?

**Pass = (1) or (2), AND (3) and (4) clear.** Add an automated forbidden-framing scan for
`profit`, `P&L`, `bottom line`, `savings`, `you will save`, `guarantee`, `payback`, `forecast` —
hits are cleared individually, since deliberate *negations* ("not a forecast") are correct usage.

> [!warning]
> Two failures found by this hunt in the reference run are the ones to look for first: **summary
> tiles that carry no indicative marker**, and **a bare ratio figure** (value ÷ investment) presented
> without its qualifier. The ratio is the strongest profit invitation any value surface can make.
> The fix pattern: label it a ratio of two indicative figures, not a promised return — and suppress
> it entirely when the ratio is implausibly large, rather than printing an absurd headline.

## Honesty discipline (HD)

- Every figure carries **indicative + basis**
- **No invented named sources, no fake URLs** — in the interface, the export and every popover
- Demo or sample context is **badged on every path**: card, chip, popover, toast and export
- **Measured vs assumed is never blurred**; counts are correct; nothing claims "measured" that isn't
- Applying a context layer changes figures **visibly and reversibly** — reset restores the baseline
- Double-counting caveats are inventoried: any summed surface must adjacently frame the sum as an
  illustrative aggregate, distinct from the delivered blueprint headline ([[prn-value-discipline]])

## Adversarial personas (AD)

Answers may use **only what is on screen**. If the answer needs the facilitator's background
knowledge, the artefact fails — the room will read it without you.

| Persona | The three questions |
|---|---|
| **Sceptical CFO** | "Is this in my P&L next year?" · "Who says that recovery rate is achievable?" · "What if I halve every assumption?" |
| **Hostile data lead** | "These rules are boilerplate." · "Show me what you'd actually run." · "How does what we agree survive into delivery?" |
| **Procurement buyer** | "What's your day rate?" (no client surface may show rates) · "Where does that investment figure come from?" · "Cut the timeline — does the price drop?" |

## Tone conformance (TC)

Scan every state, both themes, three viewports — including `title` and `aria-label` attributes —
for internal shorthand: application code-names, environment names, `ROM`, `key issue`, `DQ rule`,
`KI`, `AE`, `RDL`, `SoW`, `facilitator`, `persona`, `altitude`, phase tags. Code-only occurrences
are exempt; anything rendered is a failure. The client-facing translation is
[[std-client-vocabulary]].

Two rulings worth inheriting: **rates were removed from the interface entirely** rather than hidden
behind an "internal" marker, and the export was **kept internal with the action renamed** rather
than sanitised — deciding an artefact's audience is cleaner than trying to make one artefact serve
two.

## The walkability gate (before an outcome is published at all)

An outcome enters a published catalogue only if **all five levels are walkable today** — nameable
L2 measures, known L3 process areas, L4 objects in a typical estate, and **L5 rule seeds that
already exist**. Candidates that fail are **cut, not padded**.

How to run the check:

1. Measure against the *ratified* rule catalogue, with every rule outcome-linked.
2. Count, per candidate: **rules · governed drivers · distinct data objects · distinct business
   processes · value levers**.
3. Re-check marginal calls at **lever and driver level** — a value lever is the precise instrument,
   and one outcome category can hold two candidates whose substrate differs sharply.
4. Split any driver family that *looks* like support before counting it. In the reference run, a set
   of rules filed under an asset-hierarchy driver turned out to belong to the finance asset
   register, not maintenance — they inflated a candidate that was actually empty.
5. Record a verdict per candidate: **PASS**, **PASS (qualified)**, **MARGINAL — hold** (walkable
   end to end but on the weakest substrate: publish as preview-strength, and promise no depth it
   cannot evidence), or **FAIL — cut** (re-propose when the missing rules land).

> [!important]
> **The deck may only promise what survived.** A cut outcome may appear as a roadmap item, never as
> evidenced scope. And name the gap rather than hiding it — "these drivers exist in the vocabulary
> but carry zero rules" is a quantified target for the next rule intake, and stating it honestly is
> what makes the rest of the coverage claim believable ([[gls-coverage]]).

## Verification

- Every SEV-1 family has been run and passes; SEV-2 failures are either fixed or logged with a
  decision
- The naive-reader test passes on **both** the full narrative and the main surface alone
- No internal shorthand and no rate reaches any client surface
- Every published outcome passed the walkability gate; every cut is recorded with its counts
- Zero console errors, zero network requests (the artefact is offline by construction)

## Common pitfalls

- **Trusting a failing test.** Three of the four failures in the reference run's first pass were
  faults in the *test*, not the build: an assertion that fired mid-animation, a regex that matched
  the source comment stating the discipline it was checking, and a contrast routine that treated
  translucent overlays as opaque. Confirm the failure is real before you change the artefact — and
  record the correction, because a silently-dropped "failure" and a silently-dropped defect look
  identical afterwards.
- **Judging comprehension with the author.** Use a reader who has not seen the build.
- **Testing only the interface.** The exported working file, read cold by someone who was not in the
  room, is a SEV-1 surface like any other.
- **Fixing a label instead of the invitation.** If a surface invites the profit reading, relabelling
  is often not enough — suppressing the figure is a legitimate fix.

## Related

- [[ref-deliverables-inventory]] — the artefacts this rubric gates
- [[prn-value-discipline]] — the arithmetic rules the figures must obey
- [[prc-handle-the-cold-room]] — what to do when the challenge lands live anyway
- [[prc-audit-rule-quality]] — the equivalent bar one level down, on the rules themselves
