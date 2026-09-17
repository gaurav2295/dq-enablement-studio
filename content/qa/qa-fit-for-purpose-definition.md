---
id: qa-fit-for-purpose-definition
type: qa
title: How do we determine that data is fit for purpose?
domain: dq-fundamentals
audience: [consultant, lead]
level: foundation
status: review
sources:
  - coe:changeset-5-sql-fundamentals
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:con-dq-lifecycle
  - relates:prn-fetch-check-return
---

## Question

How do we determine that data is fit for purpose? Is it based on all rules passing, a quality score threshold, or business sign-off?

## Answer

"Fit for purpose" is *not* a purely technical metric — it's a **business judgment call** that combines three signals:

### 1. Technical signal: Rule execution results

- Error rules flag defects; you fix them and recheck (Remediate → Recheck cycle in the lifecycle)
- A dataset where *all critical Error rules pass* is technically clean
- But "pass" doesn't automatically mean "ready"

### 2. Quantitative signal: Acceptable defect rates

- Some businesses tolerate 0.1% defects in non-critical fields; others demand 99.9% perfection
- You might define thresholds: "Materials with <1% missing UoM = acceptable; >5% = halt and fix"
- These thresholds vary by domain (master data is stricter; analytical datasets more forgiving)

### 3. Stakeholder signal: Business sign-off

- A data steward or domain owner reviews the results and says "yes, this is good enough for our use case"
- They may accept known defects in low-value records while demanding perfect data in high-value ones
- This is where the business context (what the data is *for*) enters the decision

### The lifecycle view

The DQ Lifecycle cycle repeats (Profile → Rule → Remediate → Recheck). "Fit for purpose" isn't a one-time gate — it's the state you reach when:
- Rules execute (Rule step)
- Defects are fixed (Remediate step)
- Checks pass (Recheck step)
- **AND** business stakeholders confirm the quality is sufficient for the planned use

If new defects appear in the next cycle, you remediate again. The cycle never stops.

## Related

- [[con-dq-lifecycle|The DQ Lifecycle]]
- [[prn-fetch-check-return|Why Fetch-Check-Return]]
