---
id: gls-boa
type: glossary
title: Business Outcomes Activation (BOA)
domain: delivery
audience: [lead, consultant]
level: foundation
status: review
links:
  - relates:gls-vector-studio
  - relates:gls-bob-vs-boa
  - relates:qa-what-is-boa
sources:
  - bob-dq:CONTEXT.md
  - bob-dq:CLAUDE.md
tags: [bob-dq, naming, engine, value]
created: 2026-08-20
updated: 2026-09-03
---

## Definition

**BOA (Business Outcomes Activation)** is a **value framework and reference repository** that translates DQ (Data Quality) results into measurable business outcomes and impact.

## What BOA Is

BOA is **not** a rule generation engine (that's Local Derive / AI Derive in the Studio). Instead, BOA is:

- **A value library** — contains 18 [[gls-value-lever|value levers]] (ways DQ creates value) and 6 [[gls-outcome-category|outcome categories]] (business domains impacted)
- **The honesty discipline** — ensures DQ evidence-based results are presented accurately: "volumes are not value, never inflate, distinct lenses are never summed"
- **The closest implementation of turning DQ results into valued deliverables** — bridges from "we found 500 defects" to "fixing these defects prevents $2M in revenue loss"

## How BOA Relates to the Studio

- **Studio produces:** Rules, specs, SQL, audit trails
- **BOA provides:** The framework for **explaining why those rules matter** to the business

The Studio's job is deriving rules. BOA's job is quantifying their impact.

## BOA vs. BOB (The Offering)

> [!warning] Common confusion
> **BOB** = the DQ offering (what you sell to the client)  
> **BOA** = the engine behind BOB (the value framework)
>
> When speaking to clients, say "the value library" or "the outcomes framework" rather than the acronyms — the distinction is technical and internal.

## Usage in DQ Methodology

BOA is the foundation for:
- **Rule prioritization** — which rules deliver the most business value?
- **Impact estimation** — how much does fixing these defects improve the business?
- **Success metrics** — how do we measure that DQ improvement worked?
