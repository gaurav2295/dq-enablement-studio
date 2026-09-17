---
id: qa-value-confidence-labels
type: qa
title: How is the confidence label assigned to a value figure?
domain: value-outcomes
audience: [consultant, lead]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

When a value figure is presented (e.g., "€413,136 in annual savings"), it carries a confidence label 
(e.g., "Indicative", "Audited", "High confidence"). How is that label assigned? What factors influence it?

## Answer

**Confidence is determined by three factors: data provenance, assumption count, and validation status.**

### The three factors

| Factor | High Confidence | Low Confidence |
|--------|-----------------|----------------|
| **Provenance** | Derived from actual rule output | Based on estimates/benchmarks |
| **Assumptions** | 0–1 documented assumptions | 3+ undocumented assumptions |
| **Validation** | Reviewed by SME/Finance; validated | Unreviewed; one-time calculation |

### Confidence levels

**HIGH CONFIDENCE (Audited)**

- All inputs from actual rule findings (defect counts, record volumes)
- ≤ 1 assumption; fully documented
- Calculation validated by client's Finance team
- Example: "€413k annual savings (Audited) based on measured 2.5% defect rate × documented 8 hrs/week reconciliation cost"

**MODERATE CONFIDENCE (Indicative)**

- Mix of measured (rule findings) and estimated (volume / cost assumptions)
- 2–3 documented assumptions
- Reviewed by engagement lead; not formally validated by Finance
- Example: "€200k annual savings (Indicative) assuming new GL system reduces posting errors by 30%"

**LOW CONFIDENCE (Directional)**

- Mostly estimates; few actual measurements
- 4+ assumptions, some undocumented
- Single author; no review
- Example: "€1M potential (Directional) if we could automate all cost-center matching"

### How labels are assigned

**During value calculation:**

1. **Count the assumptions** — how many "if" statements are in the calculation?
   - 0–1 assumptions → HIGH
   - 2–3 assumptions → MODERATE
   - 4+ assumptions → LOW

2. **Check data provenance** — are inputs measured or estimated?
   - All measured → HIGH
   - Mix → MODERATE
   - All estimated → LOW

3. **Assess validation** — who has reviewed this?
   - Client Finance signed off → HIGH
   - Engagement lead reviewed → MODERATE
   - Author only → LOW

**Label = the LOWEST of the three dimensions**

Example: Strong data (HIGH) + 4 assumptions (LOW) + no validation (LOW) = **LOW confidence overall**

### In the deliverable

Every confidence label must have a supporting note:

```
€413,136 annual savings (HIGH CONFIDENCE)

Basis:
- Defect count: 1,247 GL postings missing cost center (measured from DQ rule, current month)
- FTE cost: €1,042/week (from client's own headcount budget; validated)
- Time saved assumption: "If all defects are fixed, reconciliation time drops from 8 hrs to 1.6 hrs/week" (documented; SME-approved)
- Validation: Reviewed by client Finance Controller; accepted

Assumptions that could change the number:
- If only 80% of defects are fixable: €331k (instead of €413k)
- If reconciliation time is 4 hrs (not 8 hrs): €207k (instead of €413k)
```

### Prevention of label inflation

**Don't do this:**
```
€1M annual savings (HIGH CONFIDENCE)
[but the calculation has 7 assumptions and no Finance review]
```

**Do this:**
```
€100k–€1M potential value (DIRECTIONAL)
[if current 5 assumptions could be validated by Finance, HIGH CONFIDENCE could reach €413k]
```

> [!important]
> Confidence labels are about honesty. Label high only if you can defend it. 
> Underestimate, then upsize once you have more data. Never inflate.
