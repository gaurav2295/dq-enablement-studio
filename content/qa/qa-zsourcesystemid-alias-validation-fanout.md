---
id: qa-zsourcesystemid-alias-validation-fanout
type: qa
title: Validating zSourceSystemID Matches Alias Mapping Before Deployment
domain: rule-design
audience: [developer]
level: practitioner
status: review
links:
  - parent:prc-fan-out-a-rule-per-system
  - relates:gls-zsourcesystemid
  - relates:gls-system-alias
  - relates:gls-fan-out
sources:
  - coe:changeset-7-dq-studio-workflow-2026-08-31
created: 2026-09-02
updated: 2026-09-02
---

## Question

Does the Studio perform any validation to confirm that the generated zSourceSystemID filter matches the correct alias mapping before deployment?

For example:
- If alias says "P02 = SAP", does Studio verify the rule filter says `WHERE zSourceSystemID = 'SAP'`?
- What happens if there's a mismatch (P02 alias but filter has LEGACY code)?
- Is this validation automatic or manual?
- At what stage does validation occur (derivation, pre-deploy, deploy-time)?

## Context

Fan-out generates per-system implementations with zSourceSystemID filters. These filters must match the project's system alias configuration, or defect counts will silently include wrong systems.

## Why This Matters

- **Data Integrity** — Mismatched filters cause silent cross-system contamination
- **Audit Safety** — Validator must catch alias mismatches before rules deploy
- **Configuration Drift** — Project config (aliases) and rule filters can diverge
- **Error Prevention** — Critical issue; should be caught early

## Related Concepts

- **zSourceSystemID** ([[gls-zsourcesystemid]]) — System identifier in every row
- **System Alias** ([[gls-system-alias]]) — Project's system code mapping
- **Fan-Out** ([[gls-fan-out]]) — Per-system rule generation

## Expected Answer Should Cover

1. **Validation Timing:**
   - At rule derivation?
   - Pre-deployment check?
   - Deploy-time validation?

2. **Validation Mechanism:**
   - Automatic (built into system)?
   - Manual review required?
   - User warning if mismatch detected?

3. **Mismatch Handling:**
   - Blocks deployment? (safest)
   - Allows override with warning?
   - Silently accepts (dangerous)?

4. **Scope of Validation:**
   - Just zSourceSystemID?
   - Also validate view names match aliases (P02 in view name = P02 system)?
   - Validate across entire fan-out group?

5. **Example:**
   - Alias config: P02 = SAP, P01 = LEGACY
   - Lead rule: WHERE zSourceSystemID = 'SAP'
   - Fan-out generates: P02 version with zSourceSystemID = 'SAP', P01 version with... what?
   - Validation: Checks P01 version has zSourceSystemID = 'LEGACY'?

---

**Status:** Awaiting answer  
**Priority:** HIGH (data integrity critical)  
**Changeset:** 7
