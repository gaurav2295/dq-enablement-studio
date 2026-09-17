---
id: prn-ziserrorflag-is-integer
type: principle
title: Why zIsErrorFlag is Integer
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-ziserrorflag-convention
  - relates:prn-optsel-is-the-universe
  - relates:prn-profiling-has-no-pass-fail
  - relates:con-rule-types
  - relates:gls-adm
sources:
  - vault:thought-leadership/Why zIsErrorFlag is Integer.md
tags: [thought-leadership]
created: 2026-08-20
updated: 2026-08-20
---

## The principle

`zIsErrorFlag` is an integer, `1` or `0` — never `'Y'`/`'N'`, `'Yes'`/`'No'`, or `TRUE`/`FALSE`.

## The variants explicitly rejected

| Variant | Why rejected |
|---|---|
| `'Y'` / `'N'` | Looks like SAP, but SQL Server is case-sensitive on string comparisons by default — `'y' = 'Y'` is FALSE. Bugs. |
| `'Yes'` / `'No'` | Same case-sensitivity issue; also longer to type and easier to typo. |
| `TRUE` / `FALSE` | SQL Server has no native BOOLEAN type. Returns BIT (which is integer underneath). The verbose form is a mirage. |
| `1` / `'0'` (mixed types) | The classic mistake — one side string, the other integer. Comparisons silently coerce, performance suffers, indexing breaks. |

## What we use — integer 1 / 0

```sql
CASE WHEN <error> THEN 1 ELSE 0 END AS [zIsErrorFlag]
```

## Why this wins on five fronts

### 1. Aggregation is trivial

`SUM(zIsErrorFlag)` = total defect count. `AVG(zIsErrorFlag)` = defect rate (0.0–1.0). Both at
the SQL layer, no CASEs in the dashboard.

```sql
SELECT
    COUNT(*) AS Opportunities,
    SUM(zIsErrorFlag) AS Defects,
    AVG(CAST(zIsErrorFlag AS FLOAT)) AS DefectRate
FROM DQ_..._OptSel;
```

With string flags, every aggregation becomes `SUM(CASE WHEN zIsErrorFlag = 'Y' THEN 1 ELSE 0
END)`. More typing, more bugs.

### 2. Filtering is unambiguous

`WHERE zIsErrorFlag = 1` — works on every SQL platform, every collation, every case-sensitivity
setting. No coercion, no fuzz.

### 3. The RptSel pattern is portable

```sql
CREATE VIEW DQ_..._RptSel AS
SELECT * FROM DQ_..._OptSel WHERE [zIsErrorFlag] = 1;
```

Identical syntax on SQL Server, Postgres, Snowflake, BigQuery, anywhere. If Studio output ever
migrates to a different platform, this line doesn't change.

### 4. ADM contract

ADM's defect-counting expects an INTEGER `zIsErrorFlag` column. String flags are silently
dropped from the defect count, which surfaces as "all rules report zero defects" — a
particularly painful failure mode because it looks like success.

### 5. Performance

Integer comparisons and indexing are uniformly faster than string comparisons, especially at the
row volumes WRKDQ sees (millions of records per system × table).

## The "bare 1" anti-pattern

A subtler variant:

```sql
-- ❌ Wrong
SELECT 1 AS zIsErrorFlag
FROM MARA
WHERE LVORM <> 'X' AND MEINS IS NULL;
```

The literal `1` skipped the CASE — instead, the WHERE pre-filters to defects. This makes the
rule:

- Have no opportunities (just defects)
- Return a 100% defect rate trivially
- Break ADM's denominator

Always use the CASE form even if the column appears constant. The CASE makes the contract
explicit: every row in OptSel has a flag value of 1 or 0, depending on whether it's a defect.

## Worked example: Multiple error conditions

When a rule checks multiple conditions, combine them into a single CASE expression:

```sql
-- Rule: "Flag materials if status is bad OR unit of measure is missing"

SELECT
    -- Syniti Technical Fields
    MARA.zSourceSystemID AS [zSourceSystemID],
    CONCAT(MARA.MATNR, '_', MARA.zSourceSystemID) AS [zConcatenatedKey],
    CASE
        WHEN MARA.MMSTA NOT IN ('01','02','03') THEN 1   -- Status is bad
        WHEN MARA.MEINS IS NULL THEN 1                   -- UOM is missing
        ELSE 0
    END AS [zIsErrorFlag],
    
    -- Basic Fields
    MARA.MATNR,
    MARA.PLANT,
    MARA.MMSTA,
    MARA.MEINS
FROM MARA_Stage AS MARA
WHERE MARA.zSourceSystemID = 'SAP'
  AND MARA.LVORM <> 'X'
```

**Single flag, multiple conditions:** If status is bad OR UOM is missing, the row is flagged (1). 
Otherwise, not flagged (0). Downstream scoring sums this one column.

## Profiling doesn't have zIsErrorFlag at all

Profiling means no pass/fail — see [[prn-profiling-has-no-pass-fail|Why Profiling Has No
Pass-Fail]]. PrfSel and PrfSum carry no `zIsErrorFlag`. Adding one to a profiling rule is a
downgrade — it implies check semantics the rule doesn't have.
