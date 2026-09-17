---
id: qa-attribute-low-cardinality-criteria
type: qa
title: What makes an attribute "low-cardinality" for attribute gap filling?
domain: studio
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

When profile results are used to fill attribute gaps, the procedure mentions filtering for "low-cardinality" attributes. 
What specifically qualifies as low-cardinality, and what threshold is used?

## Answer

**Low-cardinality = columns with a small, bounded set of distinct values.**

### The threshold

**Default threshold: ≤ 20 distinct values**

A column with 20 or fewer unique values is considered low-cardinality and eligible for attribute gap-filling.
If it has 21+, it's considered high-cardinality and skipped (not useful as a dimension attribute).

### Why the threshold?

**Organizational dimensions (low-cardinality examples):**
- Plant (WERKS): ~5–10 values (Plant 1000, 1100, 1200, etc.)
- Company (BUKRS): ~3–8 values (company codes)
- Cost Center (KOSTL): ~30–50 values (departments)
- Status codes (MMSTA): 5–10 values (01=active, 02=blocked, etc.)

**Non-dimensions (high-cardinality examples):**
- Material ID (MATNR): 50,000+ values
- Customer ID (KUNNR): 100,000+ values
- Invoice amount: millions of distinct values

### How to verify in profile results

Profile output shows:

```
Column: WERKS
  Distinct values: 7
  Most common values: (1000: 45%), (1100: 38%), (1200: 12%), ...
  ✓ Low-cardinality (qualifies as dimension)

Column: MATNR
  Distinct values: 87,432
  Most common values: (SKU001: 0.2%), (SKU002: 0.15%), ...
  ✗ High-cardinality (does not qualify)
```

### Adjusting the threshold

**You can override** the default ≤ 20 threshold in the procedure configuration:

```yaml
attribute_usage:
  low_cardinality_threshold: 30  # Change from default 20 to 30
```

**When to adjust:**
- **Lower (e.g., 10):** Stricter; only the most clear-cut dimensions are included
- **Higher (e.g., 30):** Relaxed; more attributes included (may be noisy)

### The decision

If a column has:
- **≤ threshold distinct values** → Include in attribute gap-fill
- **> threshold distinct values** → Exclude (not a dimension)

> [!tip]
> Low-cardinality isn't just a number — it's about usability. 
> A column with 50 values might be technically usable but hard to report on. 
> Use the threshold as a starting point; adjust based on profiling results.
