---
id: qa-3tier-unmapped-fields-reporting
type: qa
title: How are unmapped fields (with no descriptions) reported?
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

If a field goes through all three tiers and gets no description from any of them, 
the profiler displays the technical name (e.g., "MATNR" instead "Material ID"). 
But how does a reviewer find these unmapped fields so they can be manually labeled?

## Answer

**Three reporting mechanisms:** profiler badge, unmapped-fields report, and audit checklist.

### 1. Profiler provenance badge (immediate visibility)

The profiler dashboard's **provenance badge** tells you:
```
Descriptions: 96% snapshot · 3% client · 1% internal · 0% unmapped
```

If unmapped% > 0, fields have no labels from any tier.

**Click on "0% unmapped"** → see the list of fields with no description.

### 2. Unmapped fields report (detailed audit)

Run the **metadata audit report**. It produces a section listing:

```
UNMAPPED FIELDS (fell through all three tiers)
================================================

Table: MARA
  - ZXYZ01 (Tier 1 blank, Tier 2 blank, Tier 3 blank)
  - ZXYZ02 (custom field, no Z-documentation)

Table: MARC
  - ZSPEED (not in DD03L snapshot; not in client dict)

Total unmapped: 3 fields
Recommendation: Review with client; add Z-field documentation or extend Tier 2
```

### 3. DBA audit checklist (manual review)

During the audit phase, the DBA checks:

- [ ] Unmapped fields exist? ✓ (ZXYZ01, ZXYZ02, ZSPEED)
- [ ] Are they custom/Z fields? (decide: label manually or skip)
- [ ] Should they be documented in the client dictionary? (escalate to Basis if yes)
- [ ] Acceptable to show technical name? (OK for internal use; not OK for client-facing dashboards)

### How to resolve unmapped fields

**Option 1: Add to the client dictionary** (Tier 2)
- Contact the client's MDM/Basis team
- Add Z-field labels to the SAP data dictionary (via SE11)
- Rebuild the client dictionary (next engagement phase)

**Option 2: Manual mapping** (one-off)
- For known unmapped fields, create a local **field-label mapping** in the project config
- Example: `ZXYZ01 → "Custom Material Flag"`
- Profiler uses this mapping as a "Tier 2.5" (custom client override)

**Option 3: Accept technical name** (if internal-only)
- If the profiler/dashboard is for DBAs only, the technical name is acceptable
- Document why the field is unmapped (e.g., "custom Z field; no business label available")

### Prevention: Regular refreshes

To minimize unmapped fields:

1. **Monthly snapshot runs** — catch new Z fields as soon as they appear
2. **Quarterly client dict rebuild** — incorporate new fields into Tier 2
3. **Annual DD% audit** — ask Basis: "Are there unlabeled Z fields we should document?"

> [!tip]
> Unmapped fields are expected on engagements with custom Z tables. The profiler makes them 
> visible so you can decide how to handle each one. Don't ignore them; decide consciously 
> whether to label, skip, or accept the technical name.
