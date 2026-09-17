---
id: qa-attribute-source-verification
type: qa
title: If both spec and profile results exist, how do you verify which was used?
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

When both a spec file and profile-results upload provide attribute selections, how can a user verify 
which attributes were ultimately included in the generated SQL?

## Answer

**Priority order is documented and visible in the manifest. You can verify which source won per attribute.**

### The priority order

When both sources exist, spec file wins:

```
Tier 1 (highest priority): Spec file (xlsx) attributes
Tier 2 (fallback): Profile results attributes
Result: Combined, spec first, then profile fills gaps
```

### How to verify

**In the manifest file** (generated after attribute analysis runs):

```json
{
  "table": "MARA",
  "attributes": [
    {
      "name": "MATNR",
      "source": "spec_file",
      "reason": "Explicitly listed in spec"
    },
    {
      "name": "PLANT",
      "source": "spec_file",
      "reason": "Explicitly listed in spec"
    },
    {
      "name": "MEINS",
      "source": "profile_results",
      "reason": "Not in spec; filled from profile (low-cardinality, 7 distinct values)"
    },
    {
      "name": "MMSTA",
      "source": "profile_results",
      "reason": "Not in spec; filled from profile (low-cardinality, 6 distinct values)"
    }
  ]
}
```

**Key fields:**
- `source`: Which source provided this attribute (spec_file or profile_results)
- `reason`: Why it was included or excluded

### What if there's a conflict?

**Scenario:** Spec says to INCLUDE MEINS, but profile results are missing MEINS.
- **Result:** Spec wins. MEINS is included (spec declared it; profile absence doesn't block it)

**Scenario:** Spec says EXCLUDE MEINS, but profile results have MEINS.
- **Result:** Spec wins. MEINS is excluded (spec is explicit; profile is ignored)

### Auditing the decisions

**Step 1:** Open the manifest
**Step 2:** Review each attribute's "source" field
**Step 3:** If you disagree, edit the spec file or re-run profiling
**Step 4:** Re-run attribute analysis
**Step 5:** Verify the new manifest

### When to use each source

| Scenario | Use |
|----------|-----|
| You know exactly which attributes you need | Spec file (explicit) |
| You want data-driven selection (use low-cardinality from profile) | Profile results (discovery) |
| You want a mix (explicit + data-driven gaps) | Both (spec for known, profile for gaps) |

> [!tip]
> The manifest is your audit trail. Always check it before using the generated SQL. 
> If something looks wrong, you can trace it back to spec vs profile and fix the source.
