---
id: ref-deliverables-inventory
type: reference
title: Deliverables Inventory — What the Client Is Left With
domain: delivery
audience: [consultant, lead]
level: foundation
status: deprecated
sources:
  - bob-dq:business-outcomes-blueprint-solution-overview.md (§9 Outputs — What the Client Is Left With)
  - bob-dq:business-outcomes-blueprint-solution-overview.md (§4 Architecture, §5 The Contract & Governance Model, §7 Auditability, Honesty Limits & Assurance)
  - bob-dq:bob-dq-solution-spec.md (§1.4 `#4-present-vector-studio`)
links:
  - prereq:con-engagement-phases
  - relates:con-value-chain
  - relates:prn-value-discipline
  - relates:prc-qa-a-blueprint
  - relates:con-solution-components
  - relates:gls-blueprint
  - relates:gls-evaluation-sheet
  - relates:gls-vector-studio
  - relates:gls-value-context
  - relates:gls-evidenced-volume
  - relates:gls-indicative
  - relates:gls-tracker
tags: [bob-dq, delivery, deliverables, outputs]
created: 2026-08-20
updated: 2026-08-20
---

## What ships

The argument this inventory has to land: **a blueprint the client owns and can re-run — not a
slide-only readout.**

| Deliverable | Form | Why it matters |
|---|---|---|
| The Blueprint (interactive) | Published single-file HTML, offline | The evidence and drill-through, permanently |
| Executive readout | Deck | The board conversation |
| Evidence workbooks | Excel | The audit trail |
| Value model | Reusable model + assumptions | Re-runnable on the next data cycle |
| Prioritised action roadmap | The blueprint itself | Sequenced value pathways |

Five items, three jobs: **prove it** (blueprint + workbooks), **land it** (readout), **repeat it**
(value model + roadmap). A blueprint that lands but cannot be repeated has sold one conversation;
the re-runnable half is what turns an assessment into a programme.

## Deliverable by deliverable

### The Blueprint

Published single-file HTML, offline, zero-install — no server, no framework, no client-side
install. The client receives a file they can open, and keeps it. It carries the whole
[[con-value-chain|value chain]] as drill-through: outcome → lever → business data driver → rule →
evidenced volume → quantified value → prioritised action. It is the deliverable the term
[[gls-blueprint|Blueprint]] names, and the prioritisation inside it is precisely what makes it a
Blueprint rather than an Assessment.

### Executive readout

The deck for the board conversation. It is a *view onto* the blueprint, never a separate set of
numbers — every figure in it must be reachable in the blueprint by drill-through. A readout figure
with no drill-through path behind it is the classic credibility leak.

### Evidence workbooks

The audit trail: the rule-level results behind every rolled-up figure. Reproducibility is the
property being delivered here — same inputs, same numbers.

### Value model

The reusable model plus its **assumptions sheet**, kept separate and consultant-owned. This is what
makes the engagement re-runnable on the next data cycle: the client re-executes the rule bundle,
drops in new volumes, and the same documented assumptions produce the new figures. See
[[prn-value-discipline]] for the arithmetic rules the model obeys.

### Prioritised action roadmap

Not a separate artefact — the blueprint *is* the roadmap, sequenced. Sequencing is an output of the
Present component, not a named phase of its own.

## The artefact chain behind them

The client-facing five are the end of a chain of internal artefacts. Knowing the chain is how you
answer *"where did this number come from?"* without leaving the room.

| Artefact | Produced by | Contract |
|---|---|---|
| Project spec | bob-canvas | Outcomes, key issues, rule scope, levers, ROM assumptions (canvas → dq-studio) |
| Rule bundle + unit tests + deploy scripts | dq-studio | Executed by the client data team on their environment |
| Results contract | The bundle's output | Fixed schema · volumes and populations ONLY · **no currency** |
| Assumptions sheet | Consultant | Separate, documented, owned — the only place currency enters |
| 38-column evaluation sheet | dq-studio | Rule facts → key-issue assignment → outcome mapping → quantification → value evidence (dq-studio → vector-studio) |
| The published blueprint | vector-studio | The client-facing artefact |

## What is deliberately *not* delivered

- **No software into the client estate.** The derivation engine is authoring-side only and is never
  shipped. The client runs SQL they can read and receives an HTML file they can open.
- **No grand total.** Distinct lenses over the same estate overlap; summing them would be
  double-counting. The headline is the largest single exposure, and the reason is stated inline
  every time.
- **No gross-count valuation.** Value is calculated against the addressable population — what could
  realistically be remediated — never the gross record count.
- **No unlabelled directional figure.** Directional and audited figures are explicitly labelled and
  never blurred ([[gls-indicative]]).

> [!warning]
> **[[gls-coverage|Coverage]] means which outcomes *could be evidenced* given engagement scope.** It
> is not a completeness score, and scope not covering something is **not** evidence that no value
> exists there. Excluded and netted items stay excluded and stay flagged: what is presented is a
> defensible subset, not a gross total. We do not inflate.

## Before any of it ships

Every client-facing artefact is human-reviewed, and the QA rubric it has to clear is
[[prc-qa-a-blueprint]]. Disclaimer language is reviewed by Legal/Compliance before external use; if
the assessed data includes personal data, the Data Privacy Officer is involved.
