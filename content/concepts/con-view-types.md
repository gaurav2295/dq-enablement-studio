---
id: con-view-types
type: concept
title: View Types — OptSel, RptSel, InfSel, PrfSel, PrfSum
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:con-rule-types
  - relates:std-view-naming-patterns
  - relates:std-ziserrorflag-convention
  - relates:prn-optsel-is-the-universe
  - relates:gls-optsel
  - relates:gls-infsel
  - relates:gls-prfsel
  - relates:gls-prfsum
  - relates:gls-rptsel
---

## What they are

Every DQ rule deploys as one or two SQL views in the working database. The view name's suffix
tells you its role.

| Suffix | Role | Used by |
|---|---|---|
| OptSel | Opportunity — the **universe** of records the rule applies to, with `zIsErrorFlag` on each row | Error rules |
| RptSel | Report — the **defects only**, by wrapping OptSel with `WHERE [zIsErrorFlag] = 1` | Error rules |
| InfSel | Info select — same shape as RptSel but for *informational* rather than defect rows | Info rules |
| PrfSel | Profile select — **record-level detail** for a profiling rule | Profiling rules |
| PrfSum | Profile summary — **aggregated** distribution with percentage-within-segment | Profiling rules |

## OptSel ↔ RptSel pair

```sql
CREATE VIEW [dbo].[DQ_0042_P02_MARA_MEINS_OptSel] AS
SELECT
    -- Syniti Technical Fields
    MARA.zSourceSystemID,
    CONCAT(MARA.zSourceSystemID, '_', MARA.MATNR) AS [zConcatenatedKey],
    CASE WHEN MARA.MEINS IS NULL OR MARA.MEINS = '' THEN 1 ELSE 0 END AS [zIsErrorFlag],
    ...
FROM ...
WHERE LVORM <> 'X' AND zSourceSystemID = 'SRCECCZ02100';
GO

CREATE VIEW [dbo].[DQ_0042_P02_MARA_MEINS_RptSel] AS
SELECT * FROM [dbo].[DQ_0042_P02_MARA_MEINS_OptSel]
WHERE [zIsErrorFlag] = 1;
GO
```

The RptSel is **always** that canonical wrapper. It never replicates OptSel logic — it just
filters it.

## PrfSel ↔ PrfSum pair

PrfSel returns the **record grain**: one row per source record, with the segmentation columns
plus the profiled attribute.

PrfSum returns the **aggregated grain**: one row per `(zSourceSystemID, segment, value)` with
COUNT plus percentage-within-segment computed via a window function:

```sql
CAST(100.0 * [Occurrences]
     / NULLIF(SUM([Occurrences]) OVER (PARTITION BY [zSourceSystemID], [Segment]), 0)
     AS DECIMAL(5,1)) AS [Percentage]
```

The `NULLIF(...., 0)` divide-by-zero guard is mandatory — without it, segments where every record
has the same value crash.

### Example — a profiling rule

```sql
-- PrfSel: record-level detail
CREATE VIEW DQ_0001_MARA_MEINS_PrfSel AS
SELECT
    MARA.zSourceSystemID,
    MARA.MATNR,
    MARA.MEINS AS [Value],
    COUNT(*) AS [Occurrences]
FROM MARA
WHERE zSourceSystemID IN ('Z01', 'Z02')
GROUP BY zSourceSystemID, MATNR, MEINS;

-- PrfSum: aggregated distribution
CREATE VIEW DQ_0001_MARA_MEINS_PrfSum AS
SELECT
    [zSourceSystemID],
    [Value],
    COUNT(*) AS [Occurrences],
    CAST(100.0 * COUNT(*)
         / NULLIF(SUM(COUNT(*)) OVER (PARTITION BY [zSourceSystemID]), 0)
         AS DECIMAL(5,1)) AS [Percentage]
FROM DQ_0001_MARA_MEINS_PrfSel
GROUP BY [zSourceSystemID], [Value];
```

Notice: no `zIsErrorFlag`, no filter wrapper. PrfSum shows "10% of materials use EA (each), 85% use KG
(kilogram)", not "X materials fail the rule".

### Example output — what PrfSel and PrfSum look like

**Scenario:** You're profiling base units of measure (MEINS) across materials in two SAP systems (Z01, Z02).

**PrfSel output (record-level detail):**

```
zSourceSystemID | MATNR    | Value | Occurrences
----------------|----------|-------|-------------
Z01             | M000001  | KG    | 1
Z01             | M000002  | EA    | 1
Z01             | M000003  | KG    | 1
Z01             | M000004  | KG    | 1
Z01             | M000005  | EA    | 1
Z02             | M010001  | KG    | 1
Z02             | M010002  | L     | 1
Z02             | M010003  | KG    | 1
... (137,493 more rows)
```

**PrfSum output (aggregated summary with percentages):**

```
zSourceSystemID | Value | Occurrences | Percentage
----------------|-------|-------------|------------
Z01             | KG    | 85,200      | 85.2%
Z01             | EA    | 10,000      | 10.0%
Z01             | L     | 4,800       | 4.8%
Z02             | KG    | 32,100      | 89.5%
Z02             | EA    | 2,600       | 7.2%
Z02             | L     | 1,300       | 3.3%
```

**What you're seeing:**

- **PrfSel:** One row per material, showing its UoM value. If you're a data steward troubleshooting "why is Z01 system showing so many L (liter) values?", you'd query PrfSel to see which materials use L.
- **PrfSum:** One row per (system, UoM value) pair, showing the aggregate count and percentage. If executives ask "what's the distribution of UoMs across our systems?", you'd show them PrfSum — it tells the story in 6 rows instead of 137,500.

**Why both?** PrfSum is the dashboard view (executives, stakeholders); PrfSel is the drill-down (data stewards investigating anomalies). Together they answer "what's the shape of this data?" at two different levels of detail.

## Why different suffixes for different rule types

**Error rules (OptSel ↔ RptSel):** Error rules produce a **binary pass/fail** on each record via
`zIsErrorFlag`. OptSel holds all candidates with the flag; RptSel filters to failures only. This
pair structure is mandatory because downstream reporting (ADM, SKP) needs *both* the universe count
(denominator) and the defect count (numerator) to compute defect rate.

**Info rules (InfSel):** Info rules don't produce pass/fail — they produce **counts and distributions**.
A rule that counts "sales orders per material" returns one row per unique value, not one row per
material with a flag. InfSel (not RptSel) reflects this: it's a "selection of informational results",
not "reports of defects". No flag, no binary distinction.

**Profiling rules (PrfSel ↔ PrfSum):** Profiling rules also don't pass/fail — they distribute values
across records and aggregates. PrfSel is record-grain detail; PrfSum is the rolled-up distribution.
Neither carries `zIsErrorFlag` because profiling has no notion of "error". The different suffix names
(Prf vs Opt/Rpt) signal that the contract is fundamentally different.

### Why this naming convention

- **Two-letter / four-letter suffix** makes the role visible in any list of view names — you can
  scan a deployment script and know immediately which views are reports, which are universes, which
  are profiling.
- **Pair semantics** (OptSel + RptSel for Error, PrfSel + PrfSum for Profiling) lets SKP route views
  automatically into the right query columns.
- **Different suffix families** (Opt/Rpt vs InfSel vs PrfSel/PrfSum) prevent confusion: "RptSel" always
  means "defects", never "profiling output" or "informational results".

## Questions from consultants

**Q: Why are profiling rules implemented using PrfSel and PrfSum instead of OptSel and RptSel?**

A: See [[qa-why-prfsel-not-optsel|Why are profiling rules implemented using PrfSel and PrfSum instead of OptSel and RptSel?]] — the key is that OptSel/RptSel embody an error-rule contract (binary pass/fail), while profiling rules have no error model (they show distributions).

**Q: If a rule is informational rather than error-based, why is InfSel used instead of RptSel?**

A: See [[qa-why-infsel-not-rptsel|If a rule is informational rather than error-based, why is InfSel used instead of RptSel?]] — RptSel means "defects only", while InfSel means "informational results" (counts and distributions with no pass/fail semantics).

## Related

- [[con-rule-types|Rule Types — Error, Info, Profiling]]
- [[std-view-naming-patterns|View Naming Patterns]]
- [[std-ziserrorflag-convention|zIsErrorFlag Convention]]
- [[prn-optsel-is-the-universe|Why OptSel is the Universe and RptSel is the Wrapper]]
