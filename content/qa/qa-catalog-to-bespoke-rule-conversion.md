---
id: qa-catalog-to-bespoke-rule-conversion
type: qa
title: Can a Catalog rule be converted to a Bespoke rule if client-specific modifications are required?
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: approved
sources:
  - coe:con-catalog-vs-bespoke-rules
created: 2026-09-02
updated: 2026-09-02
links:
  - parent:con-catalog-vs-bespoke-rules
  - relates:std-skp-rule-identifier-convention
  - relates:prc-audit-rule-quality
  - relates:prc-run-the-bulk-pipeline
---

## Question

Can a Catalog rule be converted into a Bespoke rule if client-specific modifications are required, and if yes, how should the Rule Origin be maintained?

## Answer

**Yes — Catalog rules can be adapted as Bespoke rules** when the Catalog rule matches the business intent but requires client-specific modifications (different tables, additional filters, custom logic, or data model variations).

### When to Adapt a Catalog Rule

Adapt (rather than derive fresh) when:

- **The Catalog rule's intent matches** — e.g., "material must have a valid UoM" is exactly what the client wants
- **But the data model differs** — e.g., the client uses a custom materials extension table instead of MARA
- **Or scope is client-specific** — e.g., the rule applies to finished goods only, not all material types
- **Or business logic needs a tweak** — e.g., the tolerance for a price variance check is ±40% instead of ±50%

### The Conversion Process

1. **Get the Catalog rule's SQL** — open it in the Catalog space or spec sheet
2. **Modify for the client** — adapt tables, filters, CTEs, or conditions as needed
3. **Mark as Bespoke in RuleOrigin** — set `RuleOrigin = "Bespoke"` in the tracker
4. **Document the lineage** — in the spec's Description block, add a note like:
   - "Based on Catalog rule `DQ_0042`, adapted for custom vendor table (`ZVEND_CUSTOM`)"
   - "Based on Catalog rule `DQ_0028`, restricted to finished goods (FERT only) per client scope"
   - "Based on Catalog rule `DQ_0156`, modified tolerance from ±50% to ±40% per client SLA"
5. **Let the bulk pipeline assign new IDs** — the adapted rule gets its own DQOps ID and SKP_RULE_NNNN

### Why Bespoke (Not Catalog)

Once you modify a Catalog rule, it's no longer the **authoritative Syniti version**. Therefore:

| Aspect | Catalog | Adapted (Bespoke) |
|--------|---------|-------------------|
| **Parity guarantee** | Rule SQL matches Catalog exactly; auditable against master | Rule is client-specific; needs client-specific validation evidence |
| **Update path** | Future Catalog updates apply automatically | Adapted rules don't inherit Catalog updates; client owns the modified version |
| **Reuse across engagements** | Yes — same rule, same SQL, same parity | Client-specific; can be promoted if useful elsewhere |

### Example: Adapting a Price Variance Rule

**Catalog Rule (DQ_0142):**
```markdown
**RuleOrigin:** Catalog
**Catalog ID:** DQ_0142

**1. Functional/Business Description**
Order line prices must not deviate more than ±50% from the material master price.
This prevents data-entry errors and pricing mistakes that could affect margins.

**2. Specific Relevancy Criteria/Scope**
Applies to all sales order line items created in the last 90 days across all sales organizations.

**3. DQ Checks (Conditions)**
- **Fetch** <br /> Retrieve all records from VBAP, joined with MARA for material master price.
- **Check** <br /> Mark any record where: order price is outside ±50% of material standard price.
- **Return** <br /> Error records are sales orders at pricing risk due to variance from standard.

***SKP_RULE_ID: SKP_RULE_0142***
```

**Client Adaptation (Bespoke):**
```markdown
**RuleOrigin:** Bespoke
**Adapted from:** Catalog rule DQ_0142

**1. Functional/Business Description**
Order line prices must not deviate more than ±40% from the material master price.
This client's SLA requires tighter margin protection than the catalog standard.

**2. Specific Relevancy Criteria/Scope**
Applies to all sales order line items created in the last 90 days, scoped to Key Accounts 
(SOLSA = 'KAM') per client governance policy.

**3. DQ Checks (Conditions)**
- **Fetch** <br /> Retrieve all records from VBAP, joined with MARA for material master price and KNA1 for account type.
- **Check** <br /> Mark any record where: order price is outside ±40% of material standard price AND customer segment is Key Account.
- **Return** <br /> Error records are key account orders at tighter pricing risk; requires escalation review.

***SKP_RULE_ID: SKP_RULE_[auto-assigned]***
```

**Changes made:**
- Tolerance changed from ±50% to ±40%
- Scope restricted to Key Accounts only
- Join added to KNA1 for account-type filtering
- Description reflects client SLA and governance

**Result:** This adapted rule gets its own DQOps ID and SKP_RULE_NNNN, marked as Bespoke. The lineage is clear for auditing and future promotion.

### Does the Adapted Rule Inherit Future Catalog Updates?

**No — once adapted, the Bespoke rule is disconnected from the Catalog rule's lifecycle.** If the Catalog maintainers later improve `DQ_0142` (e.g., fix a bug or add a field), your adapted Bespoke version does **not** automatically inherit that fix.

**Why:** The adaptation already diverged from the authoritative SQL — there's no way to distinguish "the Catalog's fix" from "your client-specific change" at the SQL level without a proper diff/merge process the Studio doesn't automate.

**What to do if the Catalog rule you adapted from gets updated:**
1. Check the Catalog's release notes periodically for rules you've adapted
2. If a fix is relevant to your adaptation, manually re-apply it to your Bespoke version
3. Document in your spec: "Re-synced with DQ_0142 v1.2 fix on [date]"

### Promotion Path

If an adapted rule proves valuable across multiple client engagements:

1. **Document the variation** — collect feedback on what clients needed
2. **Propose to Catalog maintainers** — "DQ_0142_variant: Tighter tolerance for key-account pricing"
3. **Promote into Catalog** — becomes a new standard variant that future engagements can use
4. **Update RuleOrigin to Catalog** — once it's in the master catalog

This keeps the Catalog fresh and responsive to real client needs while preserving audit trails.

---

### Related

- [[con-catalog-vs-bespoke-rules|Catalog vs Bespoke Rules]]
- [[std-skp-rule-identifier-convention|SKP Rule Identifier Convention]]
- [[prc-run-the-bulk-pipeline|Run the Bulk Pipeline]]
