---
id: qa-non-negotiables-intent-mismatch
type: qa
title: What if a rule passes all checks but doesn't match the business intent?
domain: studio
audience: [lead, consultant]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

A rule technically passes all enforcement checks (no missing fields, correct data types, 
proper structure), but when a reviewer reads the SQL, it seems to be checking something 
different from what the business description says. How is that handled?

## Answer

**The automated checks enforce syntax and structure, not semantics. This gap is caught in DBA audit.**

### The scenario

Rule description says:
> "Flag materials where status is inactive (MMSTA NOT IN ('01', '02', '03'))"

But the SQL does:
```sql
CASE WHEN MMSTA IS NULL THEN 1 ELSE 0 END AS [zIsErrorFlag]
```

**Automated validation:** ✅ All checks pass (shape, type, structure OK)

**But:** The SQL is checking for NULL status, not for inactive status. Mismatch.

### How it's caught

**In [[prc-audit-rule-quality|DBA audit phase]]:**

Checklist item:
- [ ] Does the CASE expression match the business description?

If not:
```
❌ AUDIT FINDING: Logic-Intent Mismatch

Rule description: "Flag materials where status is inactive..."
Actual SQL: CASE WHEN MMSTA IS NULL THEN 1 ELSE 0 END
             ↑ Checks for NULL, not for inactive statuses

Fix: Either rephrase the description or update the SQL condition
```

Rule is marked `_review_required` and sent back to the author.

### Why this isn't caught automatically

The automated checks don't understand business intent — they can't parse English 
descriptions and match them to SQL logic. They catch:
- Syntax errors ✓
- Data type errors ✓
- Missing structural requirements ✓

But they can't catch:
- Logic doesn't match intent ✗
- Edge cases not considered ✗
- Scope misunderstands ✗

### Prevention

**During rule authoring:**

1. **Write description first** — "What error condition am I detecting?"
2. **Write the CASE logic** — "What is the SQL expression for that condition?"
3. **Cross-check:** Do they match? If not, revise before submitting.

**During audit:**

The DBA spot-checks every rule: description vs SQL. This is manual, so it catches 
what automation misses.

> [!important]
> Automation ensures technical compliance. Humans ensure business correctness. 
> Both are required.
