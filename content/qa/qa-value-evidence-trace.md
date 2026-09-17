---
id: qa-value-evidence-trace
type: qa
title: What information is included in an evidence trace for a currency figure?
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

The principle says "Every figure carries an evidence trace." What exactly goes into an evidence 
trace for a value figure like "€413,136 annual savings"? How can a reviewer validate it?

## Answer

**An evidence trace is a complete audit trail from the rule finding to the final number.**

### Components of an evidence trace

**1. Source rule**
```
Rule: DQ_0087 "FI: GL posting missing cost center"
Defect count: 1,247 GL postings (November 2026)
Opportunity count: 50,000 total GL postings
Defect rate: 2.5%
```

**2. Addressable population**
```
Which defects can actually be fixed?
- Of 1,247 missing cost centers, 1,100 can be auto-corrected (88%)
- 147 are ambiguous and require manual review
Addressable: 1,100 defects × 12 months = 13,200 annually
```

**3. Value lever mapping**
```
Which lever applies this rule?
Lever: "Finance Reconciliation → Reduce Manual Reconciliation (FTE)"
FTE cost basis: €50,000/year (from client's org chart, grade FI-3)
```

**4. Impact calculation**
```
What does fixing these defects save?
Current state: 1 FTE spends 8 hrs/week on cost-center matching
If 1,100 defects fixed monthly: Saves ~1.6 hrs/week per month
Annual: 1.6 hrs × 52 weeks = 83.2 hrs/year = 0.04 FTE
Annual cost avoidance: 0.04 FTE × €50k/year = €2,000
```

**5. Assumptions documented**
```
- "8 hrs/week spent on cost-center matching" (source: FI Controller interview, 2026-09-01)
- "1.6 hrs/week saved if defects fixed" (based on 80% of defects being auto-correctable)
- "€50k/year FTE cost" (from client's FI salary band; verified against GL)
```

**6. Validation checkpoints**
```
- Finance Controller signed off on FTE cost: ✓
- Rule author confirmed defect count: ✓
- Client Basis team confirmed all 1,100 defects are auto-correctable: ✓ (with notes)
- Assumptions audited by engagement lead: ✓
```

**7. Confidence level**
```
HIGH CONFIDENCE because:
- Defect count is measured (from DQ rule)
- FTE cost is from actual client data
- Only 1 major assumption (1.6 hrs savings)
- All assumptions reviewed and signed off
```

### What makes a trace "complete"?

**Verifiable:** Every step can be traced back to a source document or person
- "€50k/year" → GL extract or org chart
- "8 hrs/week" → Interview notes with FI Controller
- "1,247 defects" → DQ rule output

**Reversible:** If an assumption changes, the number recalculates
- "If actually 4 hrs/week (not 8 hrs): recalculate to €1,000 (not €2,000)"
- "If 60% auto-correctable (not 80%): recalculate to €1,200"

**Auditable:** An external auditor (Finance, internal audit) can walk through it and confirm

### How reviewers validate the trace

1. **Read the summary** — see the final number and confidence label
2. **Spot-check the assumptions** — pick 2–3 and verify sources
3. **Recalculate** — plug the numbers into the formula yourself
4. **Challenge the addressability** — "Can you really fix all 1,100 defects?"
5. **Sign off** — "Trace is sound" or "Revise this assumption"

### In the deliverable

An evidence trace is included as a footnote or appendix:

```
€413,136 annual savings
[See Appendix B: Evidence trace for FI reconciliation lever]
```

Appendix B includes all 7 components above, making the number fully traceable and defensible.

> [!tip]
> A strong evidence trace turns opinion into fact. If you can't write a trace, 
> you don't have enough evidence for the number. Go back and collect more data.
