---
id: qa-sibling-system-post-fanout-generation
type: qa
title: Generating Missing Sibling Rules After New System Added
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - parent:prc-fan-out-a-rule-per-system
  - relates:gls-fan-out
  - relates:gls-system-alias
sources:
  - coe:changeset-7-dq-studio-workflow-2026-08-31
created: 2026-09-02
updated: 2026-09-02
---

## Question

If a sibling system is added to the project after fan-out has already been completed, what is the recommended process for generating the missing sibling rule?

- Can you re-fan-out the lead rule to include the new system?
- Does this create a new sibling with matching SKP_RULE_NNNN?
- Does the existing execution history transfer to the new sibling?
- Are there any risks or special considerations?

## Context

Projects can be extended to include new source systems mid-engagement. Rules must be re-fanned to include the new system. The process should be clear and safe.

## Why This Matters

- **Consistency** — New sibling must match existing siblings (same logic, structure)
- **Traceability** — Audit must show new sibling derived from existing lead
- **Execution History** — New system needs baseline execution data
- **Scope** — Should all rules be re-fanned or just selected ones?

## Related Concepts

- **Fan-Out** ([[gls-fan-out]]) — Splitting rule per system
- **System Alias** ([[gls-system-alias]]) — New system must be configured

## Expected Answer Should Cover

1. **Process:**
   - Re-fan the lead rule? Re-run entire fan-out? Targeted generation?
   - Step-by-step workflow

2. **New Sibling Properties:**
   - SKP_RULE_NNNN: Same as siblings or new?
   - DQOps ID: Generated fresh or allocated from pool?
   - Created timestamp: Today or matched to lead?

3. **Execution History:**
   - New sibling starts with zero history? (Recommended)
   - Or backfilled with synthetic baseline?
   - Impact on defect trending

4. **Validation:**
   - Verification steps before deployment
   - Impact on audit metrics (defect rate not yet trended)

5. **Risk Mitigation:**
   - Potential issues and how to avoid
   - Testing before production deployment

6. **Example:**
   - Project started with P02 (SAP), P01 (LEGACY)
   - Added new system P03 (ORACLE) mid-project
   - Re-fan process to add P03 sibling to all existing rules

---

**Status:** Awaiting answer  
**Priority:** MEDIUM (operational guidance)  
**Changeset:** 7
