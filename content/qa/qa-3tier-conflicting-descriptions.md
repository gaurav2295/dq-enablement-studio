---
id: qa-3tier-conflicting-descriptions
type: qa
title: What happens when different tiers have conflicting descriptions?
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

The three-tier description resolution model prioritizes snapshot > client > internal. 
But what if Tier 1 (snapshot) returns "Material ID" and Tier 2 (client) returns "Product Number"? 
How do we decide which one is correct?

## Answer

**Tier 1 wins. Always.** The priority is not about "correctness"; it's about **freshness**.

### Why Tier 1 is authoritative

Tier 1 (snapshot) is built from the **current profile run's DD% extract**. It represents 
what the client's data dictionary *looks like right now*. If Tier 1 has a label, it's 
the most current available and should be used — even if it conflicts with Tier 2 or Tier 3.

| Tier | Freshness | Authority |
|------|-----------|-----------|
| Tier 1 (snapshot) | Current (from this profile run) | Use this |
| Tier 2 (client) | Stale (weeks/months old) | Don't use if Tier 1 available |
| Tier 3 (internal) | Generic (SAP standard) | Use only as fallback |

### The conflict scenario

**Example:**
- Tier 1 (snapshot from DD03L): "Material ID" (populated from table MARA, field MATNR)
- Tier 2 (client dict, 6 weeks old): "Product Number" (old label, never updated)
- Studio chooses: **"Material ID"** (Tier 1 wins)

**Why?** If Tier 1 has the label, the client's DD% was available and current at profile time. 
That label is fresher than a client dictionary built 6 weeks ago.

### When Tier 2 would have won

If Tier 1 is **blank** (e.g., DD% was inaccessible, or the field didn't exist in DD% when extracted):
- Tier 1: (blank)
- Tier 2: "Product Number"
- Tier 3: (generic SAP label)
- Studio chooses: **"Product Number"** (Tier 2 now wins)

### What this means for engagement review

As a reviewer, if you see a label that looks wrong:

1. **Check the provenance badge** — which tier provided it?
2. **If it's Tier 1:** The label is fresh. If it looks odd, investigate why the DD% contains that label 
   (maybe the client renamed the field recently; confirm with them).
3. **If it's Tier 2 or Tier 3:** The label is stale or generic. Plan a re-snapshot to refresh Tier 1.

> [!tip]
> Conflicts are resolved by hierarchy, not by "correctness." Tier 1 is always preferred because 
> it's current. If you disagree with a Tier 1 label, the issue is with the client's DD%, not the 
> resolution logic.
