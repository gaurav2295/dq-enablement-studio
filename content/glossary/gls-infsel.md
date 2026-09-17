---
id: gls-infsel
type: glossary
title: InfSel (Info Selection view)
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:con-view-types
  - relates:con-rule-types
  - relates:std-view-naming-patterns
  - relates:gls-syniti-technical-fields
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [views, infsel]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **Info Selection view** — the single view an **Info** rule deploys. Same shape as a
[[gls-rptsel|RptSel]], but the rows it returns are *informational* rather than defects: an Info
rule surfaces a population worth looking at, it does not assert that those records are wrong.

## Example: End-of-Life Materials

An Info rule highlighting materials past their last-reorder date (potential candidates for archival):

```sql
CREATE VIEW [dbo].[DQ_0205_SAP_MARA_EOL_InfSel] AS

SELECT
  -- Identity
  MARA.MaterialID,
  MARA.zSourceSystemID,
  
  -- Context
  MARA.Plant,
  MARA.MaterialType,
  
  -- Subject: last time ordered
  MARA.LastReorderDate,
  MARA.CurrentDate,
  DATEDIFF(DAY, MARA.LastReorderDate, MARA.CurrentDate) AS DaysSinceLastReorder,
  
  -- Implication: explain why this row matters
  'Material has not been reordered in ' 
    + CAST(DATEDIFF(YEAR, MARA.LastReorderDate, MARA.CurrentDate) AS VARCHAR)
    + ' years. Consider archival or remedial action.'
    AS [Implication]
  
  -- No zIsErrorFlag — this is informational, not a defect
  
FROM MARA_Stage AS MARA
WHERE MARA.zSourceSystemID = 'SAP'
  AND DATEDIFF(DAY, MARA.LastReorderDate, MARA.CurrentDate) > 730  -- Longer than 2 years
ORDER BY DATEDIFF(DAY, MARA.LastReorderDate, MARA.CurrentDate) DESC;
```

Notice: No `zIsErrorFlag`, but the `[Implication]` column explains what the remediator should do.

## Usage

An Info rule carries no `zIsErrorFlag` — instead it carries an `[Implication]` column saying why
the row matters — so there is no OptSel to wrap and no defect count to reconcile. One rule, one
view.

| Rule type | Views | Flag | Outcome |
|---|---|---|---|
| Error | OptSel + RptSel | `zIsErrorFlag` | Defect count reconciles |
| Info | InfSel | None | `[Implication]` explains action |
| Profiling | PrfSel + PrfSum | None | Distribution statistics |

**Promotion path:** An Info rule can later be **promoted** to Error, at which point it gains an OptSel/RptSel pair and a `zIsErrorFlag` — see [[prn-catalog-promotion-wraps-instead-of-injecting]].

## When to choose Info vs Error

Not every finding is a defect. The difference comes down to intent:

| Question | If Yes → | If No → |
|----------|----------|---------|
| Is this record *wrong*, or just *worth looking at*? | **Info** (observation) | **Error** (violation) |
| Is there a business policy/threshold for this? | **Error** (enforce it) | **Info** (discovery) |
| Will ADM auto-count it as a defect? | **Error** (affects metrics) | **Info** (doesn't escalate) |

**Example contrast:**

| Scenario | Type | Why |
|----------|------|-----|
| Profit Centers appearing < 0.5% of time | **Info** (profiling: is this a typo?) | Discovery question; no policy yet |
| "All GL postings must have a profit center" | **Error** | Business policy; defect if missing |
| Materials without a reorder date in 2 years | **Info** (archival candidates) | Worth flagging, not inherently wrong |
| "All active materials must have reorder date" | **Error** | Business rule; defect if missing |

## Second example: Stale master data

An **Info rule** highlighting supplier master records not updated in 12 months:

```sql
CREATE VIEW [dbo].[DQ_0042_SAP_LFA1_StaleSupplier_InfSel] AS

SELECT
  -- Identity
  Lifnr AS SupplierID,
  zSourceSystemID,
  
  -- Context
  Name1 AS SupplierName,
  Land1 AS SupplierCountry,
  Erdat AS CreatedDate,
  Laerd AS LastModifiedDate,
  DATEDIFF(DAY, Laerd, GETDATE()) AS DaysSinceUpdate,
  
  -- Implication: why this matters
  'Supplier master has not been reviewed in ' 
    + CAST(DATEDIFF(MONTH, Laerd, GETDATE()) AS VARCHAR)
    + ' months. Recommend annual verification of contact details and payment terms.'
    AS [Implication]

FROM LFA1_Stage
WHERE zSourceSystemID = 'SAP'
  AND DATEDIFF(DAY, Laerd, GETDATE()) > 365
ORDER BY DaysSinceUpdate DESC;
```

**Why Info, not Error?** The business has no rule saying "suppliers must be updated within X days." This is a *stewardship observation* — the data owner decides if stale is acceptable. If they decide stale is unacceptable, they write a separate Error rule with the same predicate, and both rules coexist.
