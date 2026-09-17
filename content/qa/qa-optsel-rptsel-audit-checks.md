---
id: qa-optsel-rptsel-audit-checks
type: qa
title: What audit checks verify OptSel and RptSel integrity?
domain: studio
audience: [developer, lead]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-04
created: 2026-09-07
updated: 2026-09-07
---

## Question

OptSel and RptSel are critical — they define the universe and the defect rows. What audit 
checks verify they're correct? Are there automated validations, or does a DBA review them?

## Answer

**Multiple layers:** automated validations + DBA audit. Here's what catches problems:

### Automated checks (in the Studio / tracker)

1. **OptSel/RptSel shape check**
   - OptSel must have: zSourceSystemID, zConcatenatedKey, zIsErrorFlag
   - RptSel must be: `SELECT * FROM OptSel WHERE zIsErrorFlag = 1`
   - Missing columns or wrong filter → **validator fails, rule is un-deployable**

2. **zIsErrorFlag data type check**
   - Must be INTEGER (1 or 0), not VARCHAR/CHAR
   - Validator checks SQL DDL → rejects if wrong type → **rule un-deployable**

3. **Duplicate predicate check**
   - Scans for the same condition in both WHERE and CASE
   - Example: `WHERE LVORM <> 'X'` AND `CASE WHEN LVORM = 'X' THEN 1` → **red flag, rule marked _review_required**

4. **Dead code detection**
   - If same deletion flag appears twice (WHERE + CASE), audit flags it
   - Grep check: `"LVORM" appears N times in WHERE, N times in CASE`

5. **Defect rate sanity check**
   - If defect_count > opportunity_count → impossible; signals RptSel returned more rows than OptSel
   - Tracker alerts and blocks publication

### DBA review (post-generation)

In the audit phase ([[prc-audit-rule-quality]]):

1. **WHERE clause audit**
   - Does the WHERE match the documented scope?
   - Are deletion flags correct for this table? (LVORM for MARA? LOEKZ for VBAK?)
   - Does it exclude test/inactive records as promised?

2. **CASE logic audit**
   - Is the error condition correct?
   - Does it match the rule description?
   - Are all edge cases handled?

3. **Opportunity count audit**
   - Run the OptSel. Is the row count reasonable?
   - Does it align with known population sizes? (e.g., "we have ~50k active materials")
   - If count is 0 or 99%+, investigate why

4. **Defect rate audit**
   - Run RptSel. Defect count = what?
   - Rate = defect_count / opportunity_count. Does it make sense?
   - If rate is 0%, 100%, or > 50%, investigate

### When something fails

**Automated checks fail** → Rule is marked un-deployable; cannot be published until fixed.

**DBA audit finds issues** → Rule is marked `_review_required`; assigned back to the author 
with comments. Cannot deploy until DBA approves.

> [!tip]
> The automated checks catch syntax/schema problems. The DBA audit catches logic/scope problems. 
> Both must pass before a rule is production-ready.
