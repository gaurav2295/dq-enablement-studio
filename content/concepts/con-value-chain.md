---
id: con-value-chain
type: concept
title: The Value Chain — Outcome to Evidence
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: deprecated
sources:
  - bob-dq:business-outcomes-blueprint-solution-overview.md (§3 The Method, §5 The Contract & Governance Model, §8 Delivery Approach & Timeline, §9 Outputs)
  - bob-dq:bob-dq-solution-spec.md (§1.4b The value model)
  - bob-dq:docs/adr/0001-key-issues-are-the-primary-focus-tier.md
links:
  - relates:con-outcome-hierarchy-l1-l5
  - relates:prn-value-discipline
  - relates:prc-derive-a-dq-rule
  - relates:con-rule-types
  - relates:gls-business-outcome
  - relates:gls-blueprint
  - relates:gls-evidenced-volume
  - relates:gls-iteration-loop
  - relates:gls-kpi
tags: [bob-dq, value-chain, value-outcomes]
created: 2026-08-20
updated: 2026-08-20
---

## What it is

The single chain that connects a technical finding to a number an executive can act on — and
interrogate. It is one structure read in two directions: **down to sell** (the client picks an
outcome and the method shows what proves it), **up to prove** (evidence runs and rolls back up
into a valued blueprint). It is the operational spine underneath [[con-outcome-hierarchy-l1-l5]].

```
business outcome
   -> value lever
      -> key issue (business data driver)
         -> DQ rule
            -> evidenced volume
               -> quantified value
                  -> prioritised action     <- what makes it a Blueprint
```

The chain connects each outcome to the value lever it owns, then to the key issues nested under
that lever, then to the rules that measure them. This unit is about how they connect.

## The four stages (down-to-sell reading)

| Stage | What happens | Who owns it |
|---|---|---|
| **Assess** | Execute defined rules/checks against the client estate; produce counts and populations | Client data team (bundle supplied) |
| **Aggregate** | Group findings into value levers; deduplicate; establish addressable populations | The engine |
| **Value** | Apply documented assumptions and client-anchored benchmarks to produce financial magnitude | Consultant (assumptions explicit and separate) |
| **Elevate** | Roll levers into outcome categories; prioritise; sequence into the blueprint | Consultant + business owner |

Prioritise/sequence is what makes the output a *Blueprint* rather than an *Assessment* — it is
the step that separates the two.

In delivery those four stages sit inside six phases — **Mobilise → Assess → Aggregate → Value →
Elevate → Handover** — and they assume four things from the client: system access or extract
capability, a named data-team executor, a named business owner per outcome domain, and access to
the financial anchors the Value stage needs.

## The results contract

The interface between Assess and Aggregate is a **fixed results schema**, defined once: upstream
only has to produce it, downstream only has to consume it. Contract-first is what makes the
numbers reproducible and the ownership boundaries defensible. Two rules hold it together.

- **Volumes are not value.** SQL certifies counts and populations — objective, owned by the
  client data team. Currency is volume × a documented assumption — consultant-owned, in a
  separate sheet. *Nothing in the SQL ever emits a currency figure.*
- **Validation gates on ingestion.** Defects cannot exceed population; as-of dates are mandatory;
  ids are unique; the deterministic path carries fingerprint/provenance checks.

## The three tiers (up-to-prove reading)

Each entity in the chain lives at a tier, and cardinality shrinks sharply as it climbs — the
focused effort of the Value stage happens at roughly twenty outcome rows, not hundreds of rules
(cardinalities below are observed on the reference engagement the method was grounded in).

| Tier | Entity | Cardinality (reference) | Carries |
|---|---|---|---|
| Operational | DQ rules | ~159 | Defect counts, populations — SQL-certified |
| Tactical | Key issues | ~40 | Grouping + counts (`errors_sum`) — money never attaches here |
| Strategic | Outcome rows (outcome × primary lever) | ~20 | Evidence lines |

**Value context = evidence lines**, attached per outcome × lever: a narrative, a generated
evidence query (SQL over the member rules' deployed report views + source tables, FX-normalised),
a declared type (Count or Value-USD), and the result.

> [!note]
> The key-issue tier sits between value levers and DQ rules and is presented to clients as
> [[gls-business-data-driver|business data drivers]]. See [[prn-key-issues-primary-tier]] for why
> this tier is the primary focus of the chain rather than the value lever alone.

## Why generation, not hand-authoring

The manual original of this method — a spreadsheet workbook — contained a copy-pasted wrong
query, a spreadsheet formula error, a badly-scaled denominator presented as a headline, and
"sum the others" pseudo-queries. Those defect classes are eliminated by making evidence queries a
**generated artefact**, with provenance headers (member rules, views, template id, fingerprint)
rather than a hand-built spreadsheet.

## The iteration loop

First-pass evidence queries are candidates — quantification quality is unknown until rule results
run. Weak evidence is flagged downstream (in the presentation layer), regenerated upstream (in
rule generation). Scope does not reopen; assets iterate.

## What the chain leaves the client

The chain is not a readout — it ends in artefacts the client owns and can re-run on the next data
cycle.

| Deliverable | Form | Why it matters |
|---|---|---|
| The Blueprint (interactive) | Published single-file HTML, offline | The evidence and drill-through, permanently |
| Executive readout | Deck | The board conversation |
| Evidence workbooks | Excel | The audit trail |
| Value model | Reusable model + assumptions | Re-runnable on the next data cycle |
| Prioritised action roadmap | The blueprint itself | Sequenced value pathways |

See [[prn-value-discipline]] for the arithmetic rules that govern how the Value stage turns
volumes into figures, and [[con-outcome-hierarchy-l1-l5]] for the audience-facing structure this
chain fills in.
