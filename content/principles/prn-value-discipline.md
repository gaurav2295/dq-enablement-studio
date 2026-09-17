---
id: prn-value-discipline
type: principle
title: Value Discipline — Money Aggregates at the Lever Only
domain: value-outcomes
audience: [consultant, lead]
level: practitioner
status: deprecated
sources:
  - bob-dq:bob-dq-solution-spec.md (§1.4b The value model; changelog A7 "directional" → "indicative")
  - bob-dq:business-outcomes-blueprint-solution-overview.md (§6 The Valuation Method, §7 Auditability, Honesty Limits & Assurance)
links:
tags: [bob-dq, value-outcomes, honesty-discipline]
created: 2026-08-20
updated: 2026-08-20
---

> [!warning]
> This unit is **deprecated** and hidden from the webapp. Value methodology is under review.

## The rule

Money aggregates at the [[gls-value-lever|value lever]], and only there. The lever owns the KPI,
the financial-impact type and the formula. DQ rules and key issues carry counts and populations —
never currency. See [[con-value-chain]] for where the lever sits in the chain.

## What "value potential" means

[[gls-value-potential|Value potential]] is the value evidenced in the client's data — the scale
of an opportunity a business case could be built against, provable rule by rule. It is **not**
booked value, **not** a forecast, and **not** a saving anyone has promised. What makes it
credible is that every component traces to a rule and every assumption behind it can be changed
in front of the client.

## Two-stage value discipline

- **The canvas** produces an [[gls-indicative|indicative]] aggregate of per-measure ranges, for
  shaping scope in the room. Every surface showing it says so, and states that overlapping
  categories are never double-counted.
- **The blueprint** produces *evidenced value* under the headline discipline below.

These are deliberately different arithmetic for different jobs. The canvas never claims the
blueprint's discipline.

## Headline discipline (applies to the delivered blueprint)

- The lever headline is the **largest single evidenced exposure — never a sum**.
- Assumption-based figures are computed as **volume × documented rate** and labelled as such.
- **Distinct lenses are never summed** — lenses over the same estate overlap; a grand total would
  double-count.
- The single all-in figure, where one is shown at all, is gated and anchor-checked.

## Valuation method — the supporting rules

- **Value levers** are a finite, published catalogue mapping findings to economic mechanisms.
- **Benchmark anchoring** — magnitudes are anchored to the client's own financial statements
  rather than industry averages, wherever possible.
- **Addressable population** — value is calculated against what could realistically be
  remediated, not the gross record count.
- **FX and currency policy** — one documented rate table, one conversion point.

## Honesty limits

- **Indicative vs audited** — explicitly labelled, never blurred. The source overview words this
  as "directional vs audited"; *directional* was retired in favour of *indicative* by a later
  ruling, and the retired word must not come back into client language — see [[gls-indicative]].
- **[[gls-coverage|"Coverage"]] means which outcomes *could be evidenced*** given engagement
  scope. It is not a completeness score, and scope not covering something is not evidence that no
  value exists there.
- Excluded and netted items stay excluded and stay flagged. Figures presented are a defensible
  *subset*, not a gross total. The discipline is: do not inflate.
- **Reproducibility** — same inputs, same numbers; regression-tested.

## What an evidence trace typically contains

An evidence trace for a value figure includes:

1. **Source rule** — which DQ rule identified the defect? (e.g., "DQ_0087: GL posting missing cost center")
2. **Defect count** — how many records were affected? (e.g., "1,247 postings in November 2026")
3. **Addressable population** — how many of these can actually be fixed? (e.g., "1,100 of 1,247 are auto-correctable")
4. **Value lever** — which business lever applies? (e.g., "Finance Reconciliation → FTE savings")
5. **Impact assumption** — what work is saved if fixed? (e.g., "1.6 hours/week per month reconciliation time saved")
6. **Cost basis** — what is the unit cost? (e.g., "€1,042/week per FTE")
7. **Validation** — who reviewed this? (e.g., "Client Finance Controller signed off")

**Example trace entry:**
```
€413,136 annual savings
← Source rule: DQ_0087 (1,247 defects, 1,100 addressable)
← Lever: Finance → FTE savings (€1,042/week unit cost)
← Assumption: Reconciliation time drops from 8 hrs to 1.6 hrs/week (if defects fixed)
← Validation: Client Finance Controller, 2026-09-05
← Confidence: HIGH (all inputs measured, 1 assumption, reviewed)
```

A complete trace lets an external auditor validate every number independently.

> [!important]
> Every figure carries an evidence trace; every assumption carries a caveat. A currency figure
> never appears without a visible value lever, an as-of date and a confidence label.
