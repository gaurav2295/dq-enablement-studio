---
id: gls-rptsel
type: glossary
title: RptSel (Report Selection view)
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
links:
  - prereq:gls-optsel
  - relates:con-view-types
  - relates:prn-optsel-is-the-universe
sources:
  - vault:dq-methodology/View Types — OptSel RptSel InfSel PrfSel PrfSum.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [views, rptsel]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **Report Selection view** — the second view of an Error rule. It is a thin wrapper over the
rule's [[gls-optsel|OptSel]] that returns **the defects only**:

```sql
CREATE VIEW [dbo].[DQ_0042_P02_MARA_MEINS_RptSel] AS
SELECT * FROM [dbo].[DQ_0042_P02_MARA_MEINS_OptSel]
WHERE [zIsErrorFlag] = 1;
```

## Usage

Every Error rule ships an OptSel/RptSel **pair**; the pair is what lets SKP populate its
Opportunity Query and Error Query columns from one rule. The RptSel is always that canonical
wrapper — it references its OptSel partner and filters `[zIsErrorFlag] = 1`.

> [!warning]
> Rule logic in a RptSel is a standards violation. Replicating or re-stating the OptSel's
> `CASE` there is how the two drift and the defect rate stops reconciling — see
> [[prn-optsel-is-the-universe]].
