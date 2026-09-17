---
id: prc-assess-and-discover
type: procedure
title: Assess and Discover a Client Estate
domain: delivery
audience: [consultant, lead]
level: practitioner
status: deprecated
sources:
  - bob-dq:bob-dq-solution-spec.md (§1.4 `#1-d3p` Data Provisioning, Preparation, Profiling)
  - bob-dq:bob-dq-solution-spec.md (§1.1 Infrastructure)
  - bob-dq:business-outcomes-blueprint-solution-overview.md (§3 The Method — Assess → Aggregate → Value → Elevate)
  - bob-dq:business-outcomes-blueprint-solution-overview.md (§4 Architecture — Components & Data Flow)
links:
  - prereq:con-engagement-phases
  - implements:con-solution-components
  - relates:con-value-chain
  - relates:prc-generate-a-profile-bundle
  - relates:con-profiling-concepts
  - relates:prn-profiling-has-no-pass-fail
  - relates:con-engagement-team-shape
  - relates:gls-adm
  - relates:gls-project-spec
  - relates:gls-as-of-date
  - relates:gls-evidenced-volume
  - relates:gls-schema-profile
tags: [bob-dq, delivery, discovery, profiling, d3p]
created: 2026-08-20
updated: 2026-08-20
---

## Goal

Take a client estate from *"we have agreed the outcomes"* to *"the data is provisioned, prepared,
profiled and understood"* — the scope of `#1-d3p` and the exit condition of
[[con-engagement-phases|phase 1 — Prepare]]. This is the discovery method: how the estate is
scoped from the selected outcomes, extracted, prepared, and profiled to the point where rule
derivation can start.

Nothing here is deployed into the client estate. Generation happens on the authoring side; the
client data team executes a bundle in their own environment.

## When to use

- At the start of every engagement, before any rule is generated
- When a new source system enters scope mid-engagement and has to be brought to the same bar
- When sizing the provisioning effort in a proposal (the elapsed time here is the credibility test
  behind any "weeks not months" claim — measure it, do not assert it)

## Prerequisites

- A handed-over [[gls-project-spec|project spec]] with the outcome selection confirmed
- ADM-M hosting chosen — client-hosted or Syniti-hosted (a single variable in the project spec,
  **not a fork in the method**: the scripts are generated either way and handed to the
  implementation team)
- A **named client data executor** and system access or extract capability
- The table/system register for the sources in scope

## The four-stage frame this sits inside

Discovery is the front half of **Assess**. The whole method is four stages, and knowing which
stage owns what keeps the ownership boundaries defensible under challenge.

| Stage | What happens | Who owns it |
|---|---|---|
| **Assess** | Execute defined rules/checks against the client estate; produce counts and populations. | Client data team (supplied bundle) |
| **Aggregate** | Group findings into value levers; deduplicate; establish addressable populations. | The engine |
| **Value** | Apply documented assumptions and client-anchored benchmarks to produce financial magnitude. | Consultant (assumptions explicit and separate) |
| **Elevate** | Roll levers into outcome categories; prioritise; sequence into the blueprint. | Consultant + business owner |

The data flow those stages ride on:

```
Sources            rule specs · catalog SQL · client table/system register
   |
Generation         metric queries — deterministic where SQL exists,
                   assisted derivation only where it doesn't
   |
Bundle             handed to the client data team, executed in their environment
   |
Results contract   fixed schema · volumes and populations ONLY · no currency
   |
Ingestion          validation gates · join to the consultant assumptions sheet
   |
Roll-up            lever -> category -> value, per the spine
   |
Presentation       single-file offline app · published HTML as the shipped artefact
```

## Steps

1. **Scope the estate from the outcomes, not from the schema.** The selected L1 outcomes walk down
   to L3 process areas and L4 data objects (see [[con-outcome-hierarchy-l1-l5]]). Those objects
   determine the tables in scope. An estate scoped from the schema outward is unbounded; an estate
   scoped from the outcomes down is finite and defensible.
2. **Build the extraction list.** ABAP extractor reuse where the source is SAP; direct source
   extraction otherwise. The list is generated from the table/system register, not hand-assembled.
3. **Prepare the data.** SQL-based preparation on the ADM-M environment. Record what the standard
   extraction does *not* cover — bespoke objects and client extensions are the usual gap, and an
   unstated gap becomes a mid-engagement surprise.
4. **Profile it.** Bespoke SQL-based profiling, generated as a schema-profiler bundle —
   see [[prc-generate-a-profile-bundle]] for the mechanics and [[con-profiling-concepts]] for what
   the metrics mean.
5. **Review the profiling output with the client data team.** This is the phase-1 exit condition,
   and it is a *reading* session, not a findings session — profiling describes the estate, it does
   not judge it ([[prn-profiling-has-no-pass-fail]]).
6. **Record the as-of date and the provenance of every extract.** [[gls-as-of-date|As-of dates]]
   are mandatory at ingestion; an extract without one cannot enter the evidence base.
7. **Hand the scripts to the implementation team.** Generation is authoring-side; execution is
   client-side. The handover is the boundary that keeps Syniti out of the client estate.

## Verification

- Every L4 object implied by the selected outcomes has a table in the extraction list, or a
  recorded reason why not
- Profiling output exists for every table in scope and has been reviewed with the client
- Each extract carries an as-of date and a named source system
- The gap list (what standard extraction does not cover) is written down and shared
- Elapsed time and effort for this phase are **measured and recorded by source type** — this is the
  number that decides whether the timeline claim survives the second engagement

## Common pitfalls

- **Starting the clock too early.** The engagement timeline does not start until this phase is
  complete. Say so at mobilisation; it stops provisioning drag from eating the promised weeks.
- **Profiling as a findings exercise.** Divergence signals are input to rule derivation, not
  defects to report. Reporting them as defects burns the credibility you need in phase 3.
- **Letting currency in early.** Nothing in this phase produces a financial figure. Volumes and
  populations only — the results contract carries no currency column at all
  ([[prn-value-discipline]]).
- **Assuming the standard extractor covers everything.** State the coverage assumption explicitly
  and confirm it against the client's actual estate.

## Related

- [[con-solution-components]] — where `#1-d3p` sits among the five components
- [[con-engagement-phases]] — the phase this procedure completes
- [[con-value-chain]] — what the counts and populations feed
- [[prc-derive-a-dq-rule]] — the next step once profiling is reviewed
