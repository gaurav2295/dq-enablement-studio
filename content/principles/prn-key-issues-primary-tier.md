---
id: prn-key-issues-primary-tier
type: principle
kind: decision
title: ADR — Key Issues Are the Primary Focus Tier
domain: value-outcomes
audience: [consultant, lead, developer]
level: advanced
status: deprecated
sources:
  - bob-dq:docs/adr/0001-key-issues-are-the-primary-focus-tier.md
links:
  - relates:con-value-chain
  - relates:con-outcome-hierarchy-l1-l5
  - relates:prc-estimate-blueprint-effort
  - relates:prn-value-discipline
  - relates:gls-key-issue
  - relates:gls-business-data-driver
  - relates:gls-bob-vs-boa
  - relates:gls-value-formula
tags: [bob-dq, adr, value-outcomes]
created: 2026-08-20
updated: 2026-08-20
---

**ADR 0001 · dated 2026-08-04 · status: accepted · decided by the offering owner.**

## Context

Two libraries in the estate — both belonging to [[gls-bob-vs-boa|BOA]], the engine repo the
offering consumes from — disagreed about whether key issues are live vocabulary, and the
disagreement blocked the rule repository's linkage design.

BOA's **value library** (v1.1) retired them: its stated principle was that a rule points at ONE
value lever; the lever holds the outcome category, KPI, financial-impact type and value formula,
and value levers replace one-off client key-issue IDs. The rollup it declared was
`rule -> value_lever -> outcome_category -> value`, with no key-issue tier.

BOA's own **key-issue library** (v0.1) kept them — 40 generalised, de-clientified key issues, each
carrying process area, objects, readiness risk, cleanse category, cleanse action and default
criticality (coverage: EAM, FIN and P2P only at the time).

#bob-dq is built on the key-issue tier: the canvas presents key issues to clients as **business
data drivers**, and the board's driver column is populated from real catalogue ids (e.g.
`KI-FIN-009` "AR open items aged >6 months"), each holding its rules. The travelling contract
between the canvas and rule generation carries key issues as "the focusing tier."

**The measured state that forced the decision:** of 497 rules in the repository, **193 link to a
value lever and only 2 link to a key issue.** The repository could not feed the tier the canvas
presents.

## Decision

Key issues are the primary focus tier of the #bob-dq chain, and the key-issue library is extended
beyond EAM/FIN/P2P to cover the remaining process areas.

The chain stands as: `business outcome -> value lever -> key issue (business data driver) -> DQ
rule -> evidenced volume -> quantified value`. See [[con-value-chain]].

Two constraints hold this together and are not up for negotiation by implementation:

1. **Money still aggregates at the value lever, and only there.** The lever owns the KPI, the
   financial-impact type and the formula. Key issues carry no currency. See
   [[prn-value-discipline]].
2. **New key issues are vocabulary, and vocabulary is governed.** Candidates are proposed from the
   rules themselves and enter the library only on the owner's approval. No agent or pipeline
   creates key-issue vocabulary autonomously.

## Consequences

- The client-facing canvas and the export contract are unchanged. Nothing that travels downstream
  to rule generation breaks.
- The rule repository gains a linkage pass: rules link to existing key issues where they genuinely
  fit, and a proposed-vocabulary list is drafted for the process areas not yet covered — O2C, SD,
  PP and MM. Coverage gaps are reported as measured numbers, never filled by forcing a cross-area
  link.
- This revives a tier BOA deliberately retired as a *value aggregation* unit — that tension is
  real and accepted knowingly. This decision does not restore key issues to the value-aggregation
  role; if the two ever share a rollup, constraint 1 above is the contract between them, and the
  value library's principle should be annotated to say so rather than left reading as a blanket
  retirement.
- The key-issue library moves from a BOA-local asset to shared estate vocabulary. Ownership,
  versioning and the sync rule need revisiting when it is extended.

## Alternatives considered

- **Two tiers with distinct jobs** (lever = value, key issue = remediation), leaving the library
  as-is. Required no change to either library, but left most rules unable to reach the driver tier
  the canvas presents.
- **Collapse to levers only.** Simplest taxonomy and matches where rules actually linked at the
  time, but the canvas board changes character (levers are value-shaped, drivers are
  problem-shaped), the export contract's key-issue-id field becomes a breaking change, and the
  cleanse/readiness metadata is lost.
