---
id: qa-3tier-view-alternatives
type: qa
title: Can you view which tier descriptions were rejected and why?
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

When the profiler resolves a field description using the three-tier model, is there a way 
to see which alternatives were available? For example, if Tier 1 provided "Material ID" 
but Tier 2 had "Product Number", can a reviewer see both options and understand why Tier 1 
was selected?

## Answer

**Yes, through the profiler's metadata audit panel.** The profiler dashboard includes a 
**description-resolution detail view** that shows what was considered and what won.

### What you can see

For each (table, column):

- **Selected description** — the one rendered in the dashboard (winner)
- **Source tier** — which tier provided it (Tier 1 / 2 / 3)
- **Alternatives** — descriptions from lower-priority tiers (if any)
- **Match confidence** — was it an exact match, partial match, or fallback?

### How to access it

1. Open the **Profiler Dashboard**
2. Click on a column's label (the human-readable text)
3. **"Description origin"** detail panel opens, showing:
   ```
   Selected:    "Material ID" (Tier 1: snapshot)
   Alternative: "Product Number" (Tier 2: client, 6 weeks old)
   Alternative: "MATNR" (Tier 3: internal SAP)
   ```

### Engagement-level audit

At the engagement level, you can run a **metadata audit report** that lists:
- All fields with multiple-tier alternatives
- Which tier won each time
- Fields where Tier 2 or Tier 3 won (and why Tier 1 had no match)

**Example output:**
```
Field: MARA.MATNR
  ✓ Tier 1 (snapshot): "Material ID" — selected
  — Tier 2 (client): "Product Number"
  — Tier 3 (internal): "MATNR"
  
Field: MARA.MTART
  ✗ Tier 1 (snapshot): (blank — not in DD% at profile time)
  ✓ Tier 2 (client): "Material Type" — selected (fallback)
  — Tier 3 (internal): "MTART"
```

### For DBA audit

If a reviewer disagrees with a selected label:

1. **Check the profiler detail view** — confirm which tier won and why
2. **If Tier 1 is wrong:** Escalate to the client's Basis team. The DD% contains the label; 
   if it's incorrect, the DD% needs to be corrected.
3. **If Tier 2 was used:** Tier 1 was blank. Plan a re-snapshot to refresh Tier 1 for the next run.

> [!tip]
> The resolution is deterministic and auditable. You can always see why a tier was chosen 
> and what alternatives existed. No "hidden" selections.
