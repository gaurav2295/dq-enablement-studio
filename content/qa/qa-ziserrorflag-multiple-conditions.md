---
id: qa-ziserrorflag-multiple-conditions
type: qa
title: If a rule has multiple error conditions, should they be combined into one zIsErrorFlag?
domain: sql-standards
audience: [developer]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

If a rule checks multiple error conditions (e.g., "Status is bad OR cost center is missing"), 
should all conditions be combined into a single zIsErrorFlag CASE expression, or should 
each condition be evaluated separately before deriving the final flag?

## Answer

**Combine them into a single CASE expression using OR/AND logic.**

### The pattern

```sql
CASE 
    WHEN MMSTA NOT IN ('01','02','03') THEN 1      -- Error: bad status
    WHEN COST_CENTER IS NULL THEN 1                  -- Error: missing cost center
    WHEN CURRENCY_CODE = 'XXX' THEN 1               -- Error: invalid currency
    ELSE 0
END AS [zIsErrorFlag]
```

**Single flag, multiple conditions.** If ANY condition is true, flag = 1.

### Why one CASE, not separate flags

**Don't do this:**
```sql
CASE WHEN MMSTA NOT IN ('01','02','03') THEN 1 ELSE 0 END AS [status_error],
CASE WHEN COST_CENTER IS NULL THEN 1 ELSE 0 END AS [cc_error],
CASE WHEN CURRENCY_CODE = 'XXX' THEN 1 ELSE 0 END AS [currency_error]
```

**Problems:**
- Three separate columns confuse the counting logic (which column is THE error flag?)
- Downstream scoring can't sum them correctly
- Violates guardrail #2: one zIsErrorFlag per rule

### When you truly need separate columns

If the business wants to track "which condition was violated" for each defect:

```sql
CASE 
    WHEN MMSTA NOT IN ('01','02','03') THEN 1 ELSE 0
END AS [zIsErrorFlag],

CASE WHEN MMSTA NOT IN ('01','02','03') THEN 'status_bad' ELSE NULL END AS [error_category_1],
CASE WHEN COST_CENTER IS NULL THEN 'cc_missing' ELSE NULL END AS [error_category_2],
CASE WHEN CURRENCY_CODE = 'XXX' THEN 'currency_invalid' ELSE NULL END AS [error_category_3]
```

**But:**
- Still one zIsErrorFlag (for counting)
- Additional category columns (for diagnostics; optional)

**Better approach:** Use a comment in the SQL to document which conditions are included:

```sql
-- zIsErrorFlag: 1 if Status is bad OR Cost Center is missing OR Currency is invalid
CASE 
    WHEN MMSTA NOT IN ('01','02','03') THEN 1
    WHEN COST_CENTER IS NULL THEN 1
    WHEN CURRENCY_CODE = 'XXX' THEN 1
    ELSE 0
END AS [zIsErrorFlag]
```

### OR vs AND logic

**OR logic (most common):** Flag = 1 if ANY condition fails
```sql
CASE 
    WHEN condition_A = true OR condition_B = true THEN 1
    ELSE 0
END
```
Result: All defects grouped together; details in separate columns if needed.

**AND logic (rare):** Flag = 1 only if ALL conditions fail
```sql
CASE 
    WHEN condition_A = true AND condition_B = true THEN 1
    ELSE 0
END
```
Use only if the error is the intersection of multiple problems.

### Example: OR vs AND

```sql
-- OR: Flag if status is bad OR cost center is missing (both matter)
CASE 
    WHEN MMSTA NOT IN ('01','02','03') THEN 1
    WHEN COST_CENTER IS NULL THEN 1
    ELSE 0
END AS [zIsErrorFlag]

-- AND: Flag only if BOTH status is bad AND cost center is missing (rare)
CASE 
    WHEN MMSTA NOT IN ('01','02','03') AND COST_CENTER IS NULL THEN 1
    ELSE 0
END AS [zIsErrorFlag]
```

> [!tip]
> One rule = one zIsErrorFlag. Multiple conditions combine into that single flag using 
> OR/AND logic. If you're tempted to create multiple flags, create multiple rules instead.
