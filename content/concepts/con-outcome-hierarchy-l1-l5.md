---
id: con-outcome-hierarchy-l1-l5
type: concept
title: The Business Outcome Hierarchy — L1 to L5
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: deprecated
sources:
  - bob-dq:bob-dq-solution-spec.md (§1.3 The business outcome hierarchy — the spine)
links:
  - relates:con-value-chain
  - relates:prc-estimate-blueprint-effort
  - relates:con-rule-types
  - relates:prc-derive-a-dq-rule
  - relates:con-audience-altitude
  - relates:gls-business-outcome
  - contrast:ref-cleanse-process-areas
  - relates:gls-walkability
  - relates:gls-outcome-category
tags: [bob-dq, outcome-hierarchy, value-outcomes]
created: 2026-08-20
updated: 2026-08-20
---

## What it is

Five levels, each matched to an audience and a register. It is the **spine** of the Business
Outcomes Blueprint (#bob-dq) method — the structure a client conversation walks down (to sell)
and evidence walks up (to prove). See [[con-value-chain]] for how each level's contents are
produced and rolled up.

| Level | Audience | What is expressed | Register |
|---|---|---|---|
| **L1** | C-suite | The business outcome, named — e.g. *working capital* | Qualitative / strategic |
| **L2** | VP · Director · Head of Department | The same outcome, quantified — the empirical number the role owns | Quantitative · empirical |
| **L3** | Process owner · Programme director | The process area where the number is made or lost | Operational |
| **L4** | — | The data objects involved | Structural |
| **L5** | — | The DQ rules that measure them | Technical |

L3's "process area" is **not yet reconciled** with the cleanse-execution process-area taxonomy —
see [[ref-cleanse-process-areas]] (CONFLICT-002, open). For how the levels are narrated to each
audience in the room, see [[con-audience-altitude]].

## One outcome, two altitudes

L1 names the outcome for the C-suite; L2 is the *same* outcome expressed as the empirical measure
the VP/Director is accountable for — e.g. working capital (L1) becomes DSO / overdue AR /
unapplied cash (L2). The canvas walk is: name the outcome, choose the number that proves it, then
walk down to the rules.

## The walkability rule (inclusion criterion)

The L1 outcome catalogue is finite and published — it bounds the à-la-carte promise ("what can I
get for my budget?"). An outcome enters the catalogue only if **all five levels are walkable
today**: nameable L2 measures, known L3 process areas, L4 objects in a typical SAP estate, and
**L5 rule seeds that already exist** in the repositories the method converts (Data Jumpstart, DAE,
prior projects). No speculative outcomes — candidates that fail validation are cut, not padded.

Beyond the published catalogue, sales/delivery may bring a statement or set of facts and have the
outcome *derived* into the hierarchy (AI-assisted, in the canvas app). A derived outcome must pass
the same walkability test before it enters an engagement's scope.

## The v1 catalogue

Validated against a 447-rule catalogue. Six outcomes published; one candidate cut. The outcomes
themselves are defined term-by-term in [[gls-business-outcome]].

| # | L1 outcome | Notes |
|---|---|---|
| 1 | Working capital | The worked example — DSO, overdue AR, unapplied cash, DPO |
| 2 | Revenue leakage / assurance | Pricing errors, blocked billing, credit-note exposure |
| 3 | Procurement & spend | Maverick spend, duplicate vendors/payments, contract leakage |
| 4 | Inventory & supply reliability | Excess/obsolete stock, OTIF, master-data-driven stockouts |
| 5 | Process & compliance exposure | Blocked orders, failed postings, audit findings |
| 6 | Digital transformation readiness | The peer-level item derived from C-suite transformation initiatives (S/4 migration readiness, AI-adoption readiness); activates the Data-Readiness rule family. Held as preview-strength: 19 rules, the weakest passing substrate. |

**Cut:** *Reduce unplanned downtime* — the manufacturing/EAM outcome surfaced in early feedback.
It failed the L5 walkability test (6 rules across 2 drivers, 16 of 18 EAM drivers empty). Kept as
a re-propose candidate once manufacturing rules land, not deleted from the record.

> [!note]
> A possible C-suite need-quadrant *above* L1 — Buy (money out) · Sell (money in) · Make
> (product out) · Innovate (grow) — is held as context, deliberately not modelled. The hierarchy
> is not over-engineered until prototype feedback says the layer earns its place.

## Why this matters

The hierarchy is what makes "down to sell, up to prove" a single structure instead of two
disconnected narratives: the same L1–L5 spine that opens a sales conversation at C-suite altitude
is the spine the evidence climbs back up through after the [[prc-derive-a-dq-rule|DQ rules]] at
L5 have run. See [[prn-key-issues-primary-tier]] for the tier that sits between L3/L4 and L5 in
the delivery chain, and [[prc-estimate-blueprint-effort]] for how L5 rule counts turn into a
staffing estimate.
