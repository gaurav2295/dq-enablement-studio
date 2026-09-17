---
id: qa-bespoke-to-catalog-promotion
type: qa
title: When should a Bespoke rule be promoted to the Catalog?
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
  - relates:prn-catalog-promotion-wraps-instead-of-injecting
  - relates:prc-run-the-bulk-pipeline
---

## Question

What criteria is used when deciding whether a Bespoke rule should be promoted into the Catalog?

## Answer

**A Bespoke rule should be promoted to Catalog when it meets all five criteria below.** Promotion means the rule joins the **Syniti AI Generated Rule Catalog 2025** as a fixed, versioned, peer-reviewed standard that all future engagements can use.

### The Five Promotion Criteria

### 1. Proven Reuse (2+ Engagements, No Modification)

**What it means:**
- The rule has been deployed successfully in at least **two distinct client engagements** (different clients, different industries, or different ERP scenarios)
- Both deployments used the **exact same SQL logic** without client-specific modifications

**Why:**
- One engagement could be a fluke or a client-specific edge case
- Two successful, unmodified deployments prove the rule solves a general problem, not a one-off need

**Evidence:**
- Tracker records showing the rule in 2+ projects with `RuleOrigin = Bespoke`
- Deployment notes / release notes confirming successful closure in both engagements
- No bug reports or escalations between the two uses

**Counterexample:**
- Rule used in Engagement A (SAP ECC) and Engagement B (SAP S/4HANA), but B required vendor-table customization → **Not ready** (two uses, but required adaptation)
- Rule used in Engagement A only → **Not ready** (only one use)

---

### 2. Quality Attestation (Audit Passed, No Defect Escalations)

**What it means:**
- The rule passed all quality gates in both deployments:
  - ✅ Audit Rule Quality checks (syntax, field sections, zSourceSystemID alignment)
  - ✅ Client sign-off (business owner approved the defects flagged)
  - ✅ Production deployment with zero defect escalations or rules-of-origin disputes

**Why:**
- A rule with known defects or unresolved quality findings has no business in the shared Catalog
- The Catalog carries a quality guarantee; promoted rules must have proven pedigree

**Evidence:**
- Audit screen screenshots showing 0 issues at final close
- Client sign-off email / document
- Production deployment log with zero rollback or hotfix requests

**Counterexample:**
- Rule deployed but had to be hotfixed in production for a missing NULL check → **Not ready** (quality issue not caught pre-deployment)
- Rule flagged defects but client never confirmed whether those are real defects or false positives → **Not ready** (unresolved audit findings)

---

### 3. General Applicability (Common Problem, Not One-Off)

**What it means:**
- The rule solves a problem that appears across **multiple client types / industries / ERP scenarios**, not a single client's quirk

**Why:**
- A rule solving a very specific edge case (e.g., "only applies to this client's custom field") belongs in a client codebook, not the shared Catalog
- Catalog rules should be broadly reusable

**Evidence:**
- Rule description and scope are written in general terms ("all materials with no base UoM" not "Client X's materials with their custom UoM field")
- The two engagements came from different industries or ERP scenarios and both needed the same logic
- Business SME or Catalog maintainer confirms the problem is common across Syniti's client base

**Counterexample:**
- Rule applies only to a client's custom data extension with proprietary field mappings → **Not ready** (too specific)
- Rule covers a scenario that only one of the two deployments actually used → **Not ready** (not proven to solve a common problem)

---

### 4. SQL Standards Compliance (Mandatory Rules Followed)

**What it means:**
- The rule's SQL follows **all mandatory standards**:
  - ✅ [[std-cte-rules|CTE Rules]] — every CTE filters on zSourceSystemID; every CTE is used
  - ✅ Five-section output structure (Technical → Basic → Org → Value → Activity)
  - ✅ zIsErrorFlag as INTEGER (1/0), never text or boolean
  - ✅ OptSel + RptSel pair pattern
  - ✅ Joins include zSourceSystemID equality for cross-system safety
  - ✅ Comments explain **why** not **how**

**Why:**
- Catalog rules are templates for derivation and re-use; non-standard SQL causes inheritance of bugs and inconsistencies
- The Catalog is the authority; it must be cleaner than the field

**Evidence:**
- [[ref-ai-static-validator-gate|Static Validator]] report showing zero HIGH or MEDIUM findings on both deployments
- Code review checklist signed off by Catalog maintainer

**Counterexample:**
- Rule has a join to a lookup table without zSourceSystemID alignment → **Not ready** (cross-system safety issue)
- Rule logic is embedded in a deeply nested CASE instead of broken into CTEs → **Not ready** (readability/maintainability issue)

---

### 5. Stable Logic (Intent Hasn't Drifted Between Uses)

**What it means:**
- The rule's **core logic and intent** remained the same between the two engagements
- If variations were needed, they were documented and stable (not ad-hoc changes)

**Why:**
- A rule that changes meaning each time it's used isn't stable enough to be canonical
- Stable logic is auditable and predictable

**Evidence:**
- Rule description (Implication) is identical or nearly identical in both deployments
- If variations exist, they're documented as deliberate "variants" (e.g., "DQ_0042_strict_tolerance" vs. "DQ_0042_standard_tolerance"), not changes

**Counterexample:**
- Rule used for "material must have UoM" in Engagement A, but reinterpreted as "material group must have UoM" in Engagement B → **Not ready** (intent drifted)
- Rule tuned for different thresholds (40% tolerance vs. 50%) without documented variants → **Not ready** (unstable logic)

---

### The Promotion Decision

| Criterion | Met? | Blocker? |
|-----------|------|----------|
| Proven reuse (2+ engagements) | ✅ or ❌ | ✅ Yes — if only 1 use, cannot promote |
| Quality attestation (audit passed) | ✅ or ❌ | ✅ Yes — if defects unresolved, cannot promote |
| General applicability | ✅ or ❌ | ✅ Yes — if too specific, cannot promote |
| SQL standards compliance | ✅ or ❌ | ✅ Yes — if non-compliant, cannot promote |
| Stable logic | ✅ or ❌ | ✅ Yes — if intent drifted, cannot promote |

**Outcome:**
- **All 5 criteria met** → Promote to Catalog; assign Catalog ID (DQ_XXXX); increment Catalog version
- **Any criterion missing** → Do not promote; rule stays Bespoke; revisit after next successful engagement

---

### The Promotion Workflow

Once a Bespoke rule is approved for promotion:

1. **Catalog maintainers** review the rule and documentation
2. **Assign a Catalog ID** (DQ_0001 through DQ_9999; must be unique)
3. **Version the rule** in the Catalog (v1.0)
4. **Update RuleOrigin** in existing deployments to `Catalog` (optional; depends on versioning policy)
5. **Document in release notes** — "Added DQ_XXXX: [rule name]"
6. **Future engagements** can import DQ_XXXX directly as a Catalog rule

---

### Real-World Example: Promotion Success

**Bespoke rule created in Engagement A (2025-Q2):**
- Client: European Bank
- Rule: "GL Account must have a posting period"
- Deployed successfully, no defects, client signed off

**Used again in Engagement B (2025-Q4):**
- Client: Asian Insurance
- Different industry, same SAP ECC
- Rule logic unchanged, deployed successfully, zero issues

**Promotion decision (2025-Q4):**
- ✅ Proven reuse: 2 engagements, 6 months apart, exact same SQL
- ✅ Quality: Both passed Audit, no escalations
- ✅ General applicability: GL posting periods are a universal SAP concept across industries
- ✅ SQL compliance: Follows all standards, CTE-based, zSourceSystemID aligned
- ✅ Stable logic: Description identical in both deployments

**Result:** Promoted to Catalog as **DQ_0047: GL Account Posting Period Validation** (v1.0)

---

### Real-World Example: Promotion Rejection

**Bespoke rule created in Engagement C (2025-Q1):**
- Client: Tech Company (SAP S/4HANA)
- Rule: "Cost Center must exist in this client's custom ZCOSTCTR extension table"
- Used successfully, no defects

**Considered for promotion (2025-Q2):**
- ❌ Proven reuse: Only 1 engagement to date (not yet 2)
- ✅ Quality: Passed Audit, client approved
- ❌ General applicability: Rule hardcodes ZCOSTCTR table; not reusable for clients without this extension
- ✅ SQL compliance: Standards-compliant
- ✅ Stable logic: Intent stable within the one use

**Result:** **Not promoted.** Recommendation: "Revisit after second engagement uses this rule. If another client with ZCOSTCTR needs it, and it requires no modification, then promote as a variant: DQ_XXXX_s4hana_zcostctr."

---

### Related

- [[con-catalog-vs-bespoke-rules|Catalog vs Bespoke Rules]]
- [[std-skp-rule-identifier-convention|SKP Rule Identifier Convention]]
- [[qa-catalog-to-bespoke-rule-conversion|Can a Catalog rule be converted to Bespoke?]]
