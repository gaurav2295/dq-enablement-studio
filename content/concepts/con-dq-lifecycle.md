---
id: con-dq-lifecycle
type: concept
title: The DQ Lifecycle
domain: dq-fundamentals
audience: [consultant, lead, instructor]
level: foundation
status: review
sources:
  - academy:landing.html#lifecycle
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:con-what-is-data-quality
  - relates:con-profiling-concepts
---

## What it is

Data quality is not a one-time activity. It follows a continuous cycle: **Profile → Rule →
Remediate → Recheck**.

## Cycle detail

### 1. Profile

You run a schema profile on your master data to understand:

- How many records exist
- What fields are null, empty, or unusual
- What values appear most often (low vs high cardinality)
- What distributions look abnormal

### 2. Rule

Based on profiling findings and business requirements, you define rules that codify what "bad"
means. Each rule has:

- A **name** (concise, business-friendly)
- A **description** (what is being checked and why)
- A **logic** (the error condition in SQL)
- A **scope** (inclusions and exclusions)

### 3. Remediate

Once rules flag bad records, someone fixes them. This might be:

- **Automated** — recalculate a field, fill a null with a default, merge duplicates
- **Manual** — domain expert reviews and corrects the record
- **Process** — fix the upstream system that's creating bad data

### 4. Recheck

You run the rule again to verify the fix worked. This confirms:

- The flagged records now pass
- No new errors were introduced
- The data is now fit for business purpose

## Example: A real material data lifecycle

**Scenario:** You're validating a SAP materials master (MARA) for a manufacturing company.

**Initial State:**
- Total materials in system: 142,000
- Active materials (LVORM ≠ 'X', not deleted): 137,500
- Materials missing base unit of measure (MEINS is null or blank): 8,200

**1. Profile** — You run a schema profile and discover:
- 8,200 materials (5.98% of active materials) are missing MEINS
- UoM distribution across the 129,300 complete records is skewed: 85% use KG, 10% use EA, 5% use other
- Root cause analysis reveals three categories:
  - **New materials (3,200):** Recent uploads without UoM assigned — should have defaults
  - **Migrated materials (4,500):** From a legacy system merge — many are obsolete or dormant
  - **High-value materials (500):** Critical SKUs that need manual review and domain judgment

**2. Rule** — Based on these findings and business input, you define:
- **Name:** *"Active material must have valid base UoM"*
- **Scope:** All materials where LVORM ≠ 'X' (active, not deleted) AND zSourceSystemID = 'Z01'
- **Logic:** MEINS is not null and not blank
- **Impact:** Planning and costing modules require a valid UoM to calculate quantities and costs; missing UoM blocks demand planning.

**3. Remediate** — The data team executes a three-pronged fix:

| Action | Count | Details |
|--------|-------|---------|
| **Auto-assign default UoM** | 3,200 | New materials get KG (the most common UoM) assigned via a batch process. Reasoning: new materials without explicit requirements default to the dominant UoM for safety. |
| **Mark obsolete materials as deleted** | 4,500 | These are migrated legacy materials no longer in use. They're marked LVORM = 'X' (deleted flag) in MARA. After this, they fall *out of scope* for the rule (WHERE LVORM ≠ 'X' excludes them). |
| **Manual domain review** | 500 | High-value, exception SKUs reviewed by the materials steward: 450 receive proper UoM assignment (e.g., "KG" for bulk chemicals, "EA" for individual parts). 50 are flagged as custom internal-use materials and excluded from the rule scope via a special material type filter. |
| **Data entry errors introduced** | 3 | During remediation, the batch process writes 3 records with typos (e.g., "KGG" instead of "KG") — caught by the recheck. |

**4. Recheck** — You run the rule again on the updated data:

| Metric | Before Remediation | After Remediation | Change |
|--------|-------------------|-------------------|--------|
| **Universe (Active materials)** | 137,500 | 133,000 | 4,500 deleted, 50 excluded by type |
| **Defects (Missing MEINS)** | 8,200 | 3 | 3,200 auto-fixed + 450 manual-fixed + 4,500 out-of-scope = 8,197 resolved |
| **Defect rate** | 5.98% | 0.002% | ✅ Acceptable (< 0.01% threshold) |
| **Remediation success** | — | 8,197 of 8,200 (99.96%) | Only 3 data errors remain |

**Result:** The materials master is now fit for purpose — the planning module can proceed safely. The 3 remaining defects are flagged for immediate correction in the next refresh cycle, but the defect rate is below the business threshold (0.01% tolerance).

> [!important]
> This cycle repeats. DQ is continuous improvement, not a one-off project.

## Questions from consultants

- [[qa-profiling-vs-rule-execution|What is the difference between profiling and rule execution?]]
- [[qa-fit-for-purpose-definition|How do we determine that data is fit for purpose?]]
