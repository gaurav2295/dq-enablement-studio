---
id: qa-profiling-consistent-outliers
type: qa
title: If profiling consistently finds the same outliers, what's the next step?
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

If a profiling rule consistently identifies the same outliers across multiple runs, 
what should be the next step? Is that a signal to convert the rule to Error?

## Answer

**Yes, but only if the outliers are *wrong*, not just unusual.**

### The distinction

**Outliers = unusual but not necessarily wrong**
```
Profit Centers by usage frequency:
- PC_1000: 45,000 records (40%)
- PC_2000: 30,000 records (27%)
- PC_9999: 100 records (0.09%)  ← Outlier: rarely used
```

PC_9999 is unusual, but that might be correct — maybe it's a slow-moving cost center.

**Wrong = outliers that violate a business rule**
```
Same profiling rule, but SME says:
"No profit center should be used fewer than 500 times per month.
PC_9999 at 100 is a data quality issue — it should be consolidated."
```

Now PC_9999 is not just an outlier; it violates a policy.

### Decision: Create an Error rule

**When consistent outliers become business rules:**

1. **Document the rule** — what makes PC_9999 wrong?
   - "Profit centers must have at least 500 transactions/month"
   - "Profit centers less than 0.1% of volume should be investigated"

2. **Write an Error rule** — with the outlier as the error condition:
   ```sql
   CASE WHEN COUNT(*) < 500 THEN 1 ELSE 0 END AS [zIsErrorFlag]
   ```

3. **Keep the profiling rule** — for ongoing discovery:
   - Profiling rule: shows distribution of all profit centers
   - Error rule: enforces "minimum 500 transactions" policy

**Result:** You have both discovery (profiling) and enforcement (error).

### When NOT to create an Error rule

**Outlier is normal:**
- Your company truly has slow-moving profit centers
- The profiling rule is sufficient for tracking them
- No action needed; don't over-regulate

**Outlier is data quality, but solving it is out of scope:**
- You discovered that PC_9999 should be consolidated into PC_1000
- But consolidation is a master-data cleanup, not a DQ rule
- Document the finding; don't create an Error rule

### The monthly check

If profiling consistently finds the same 3–5 outliers month after month:

1. **Interview the SME** — "Are these normal or wrong?"
2. **If wrong:** Create an Error rule (even if it's just for monitoring)
3. **If normal:** Accept them and focus profiling on other dimensions

> [!tip]
> Profiling is discovery. If discovery reveals a pattern you want to enforce, 
> write an Error rule. Don't confuse "unusual" with "defective."
