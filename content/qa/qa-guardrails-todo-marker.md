---
id: qa-guardrails-todo-marker
type: qa
title: What do I do when the Studio emits a TODO marker (literal-1 zIsErrorFlag)?
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

Sometimes the Studio emits a compliant placeholder like `1 AS [zIsErrorFlag]` with a 
`/* TODO */` marker instead of a full CASE expression. What should a user do when they 
see a TODO? Does it block deployment?

## Answer

**No, it doesn't block deployment. A TODO is a yellow flag: "This rule needs a human decision."**

### Why TODOs appear

When the Studio can't extract a clean per-row error condition (e.g., the error is determined 
at GROUP BY level, not row level), it falls back to literal-1:

```sql
SELECT
    src.zSourceSystemID,
    CONCAT(...) AS [zConcatenatedKey],
    1 AS [zIsErrorFlag],  /* TODO: literal 1 — no per-row predicate found */
    src.MATNR,
    src.COUNT_DISTINCT_WERKS
FROM (
    SELECT MATNR, zSourceSystemID, COUNT(DISTINCT WERKS) AS COUNT_DISTINCT_WERKS
    FROM MARA
    GROUP BY MATNR, zSourceSystemID
) AS src
```

### What it means

**Literal-1:** Every row from the OptSel is flagged as an error (defect_count = opportunity_count).

**TODO marker:** "The Studio couldn't figure out the error condition. A human should review and decide."

### How to handle it

**Option 1: The TODO is correct**

If the rule's intent is "return all rows grouped" (not "flag some rows"), then literal-1 is right:

> *"List all materials with their duplicate-plant counts"*

In this case, every group is a "defect" in the sense that it's an opportunity to investigate. 
Remove the TODO comment; the rule is ready.

**Option 2: Refine the error condition**

If you know the threshold (e.g., "count > 1 is an error"):

```sql
CASE WHEN src.COUNT_DISTINCT_WERKS > 1 THEN 1 ELSE 0 END AS [zIsErrorFlag]
```

Replace the literal-1 with this, and the TODO is resolved.

**Option 3: This rule shouldn't exist**

If you realize the rule is ambiguous or not needed, delete it and create a clearer one.

### In the tracker

Rules with TODOs are marked `_review_required` (status) and flagged in the audit report:

```
Rule: DQ_0087
Status: _review_required
Reason: Literal-1 zIsErrorFlag with TODO marker
Action: DBA must decide on the error condition before rule can be deployed
```

The DBA reviews and either:
1. **Approves:** "Literal-1 is correct for this rule" (marks status: `active`)
2. **Edits:** "No, the error should be COUNT > 1" (updates SQL, marks: `active`)
3. **Rejects:** "This rule is unclear; delete it" (marks: `deleted`)

### Prevention

When you author a rule, think about the error condition upfront. If it's ambiguous 
(aggregate vs row-level), clarify it with the SME before submitting.

> [!tip]
> A TODO isn't a failure — it's the Studio saying "I need a human to finalize this decision." 
> Most TODOs get resolved in audit. Plan for that.
