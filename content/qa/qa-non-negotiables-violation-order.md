---
id: qa-non-negotiables-violation-order
type: qa
title: If multiple non-negotiables are violated, what order are they reported?
domain: studio
audience: [developer]
level: advanced
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

If a generated rule violates more than one non-negotiable at the same time 
(e.g., zIsErrorFlag is VARCHAR AND it's in the WHERE clause), 
is there a defined order in which violations are identified and reported?

## Answer

**Yes. The Studio validates in order and stops at the first critical violation.**

### Validation order (priority)

1. **Shape violations (structure)** — stop immediately
   - Missing zSourceSystemID column
   - Missing zConcatenatedKey column
   - Missing zIsErrorFlag column
   
2. **Type violations (data type)** — stop if found
   - zIsErrorFlag is not INTEGER (e.g., VARCHAR, BOOLEAN)
   
3. **Logic violations (semantics)** — warn but don't stop
   - Error condition is in WHERE (not CASE)
   - zIsErrorFlag is a pre-filtered 1 (not per-row check)
   - Deletion flag in both WHERE and CASE

### Example: Multiple violations

Rule output:
```sql
SELECT
    CONCAT(...) AS [zConcatenatedKey],
    -- zSourceSystemID missing ← STOP HERE (critical, #1)
    CASE WHEN status = 'X' THEN 'ERROR' ELSE 'OK' END AS [zIsErrorFlag]  -- Not INTEGER
FROM ...
WHERE status = 'X'  -- Error condition in WHERE
```

**Validator output:**
```
❌ CRITICAL: zSourceSystemID column is missing (violation #1)
   Stop validation. Rule is un-deployable.

[Other violations not reported because validation stopped]
```

User fixes the zSourceSystemID, then re-validates:

```
❌ CRITICAL: zIsErrorFlag is VARCHAR, not INTEGER (violation #2)

[Other violations still not checked]
```

User fixes the type, then re-validates:

```
⚠ WARNING: Error condition found in WHERE clause, not CASE
   Fix: Move the condition into the CASE expression
```

### Why stop-at-first?

**Early feedback loop:** Users fix one violation, retest, find the next. 
This iterative approach is faster than reporting all violations at once and overwhelming the user.

### Full diagnostic (if requested)

Some tools provide a `--full-audit` flag that reports all violations:

```
--full-audit report:
  ❌ zSourceSystemID missing (critical)
  ❌ zIsErrorFlag is VARCHAR (critical)
  ⚠ Error condition in WHERE (warning)
  ⚠ Deletion flag in both WHERE and CASE (warning)
```

But this is opt-in; default behavior stops at the first critical.

> [!tip]
> If you see one violation, fix it and re-validate. The next one will appear. 
> This is intentional: focus on one problem at a time.
