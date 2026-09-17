---
id: prn-profiling-has-no-pass-fail
type: principle
title: Why Profiling Has No Pass-Fail
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - prereq:con-rule-types
  - prereq:con-profiling-concepts
  - relates:std-rule-description-template-profiling
  - relates:prn-ziserrorflag-is-integer
  - relates:std-ziserrorflag-convention
  - relates:prn-fetch-check-return
  - relates:prn-optsel-is-the-universe
sources:
  - vault:thought-leadership/Why Profiling Has No Pass-Fail.md
tags: [thought-leadership, profiling]
created: 2026-08-20
updated: 2026-08-20
---

## The principle

The category split between Error/Info rules (pass/fail) and Profiling rules (distributions) is
intentional and load-bearing. Conflating them is one of the easiest mistakes to make — including
for an AI generating the rule.

## What profiling actually produces

A distribution, not a verdict. For "Profile of Profit Center usage by Controlling Area":

| Controlling Area | Profit Center | Count | % |
|---|---|---|---|
| 1000 | PC_1010 | 15,432 | 38.4 |
| 1000 | PC_1020 | 11,002 | 27.4 |
| 1000 | PC_1030 | 8,761 | 21.8 |
| 1000 | (NULL) | 5,003 | 12.4 |

There is no record-level pass/fail in that output. It is not "PC_1010 is correct" and "PC_1020
is wrong" — every row is part of the description, and the human reader looks at the shape and
decides what to do.

## Why the mistake is easy to make

Pre-trained models default to Error-rule vocabulary because most DQ rules ARE Error rules.
Without an explicit profiling prompt variant, the natural failure mode is to:

- Add a `zIsErrorFlag` CASE to the PrfSel view, returning every row as flag = 0 because there is
  no error
- Mention "defects" and "validation" in the Implication
- Wrap PrfSel in a `WHERE [zIsErrorFlag] = 1` filter, which returns zero rows

These are not just stylistic slips — they break the contract:

- A PrfSel with `zIsErrorFlag` always 0 looks defective when ADM tries to count opportunities
- A profiling Implication saying "validates that…" misleads the SME reader about what the rule
  does
- A `WHERE zIsErrorFlag = 1` filter returns an empty PrfSum, which renders as a blank report

## How the Studio enforces the split

AI Review branches by rule type:

- Profiling → a profiling-specific prompt that explicitly forbids `zIsErrorFlag` suggestions
- Error / Info → the original Error-rule prompt

## When a profiling rule "could" be made an Error rule

Sometimes a profiling rule looks like it has a natural pass/fail interpretation:

> [!tip]
> "Profile of Profit Center usage" — values that occur less than 0.1% of the time are probably
> typos.

The temptation is to turn it into an Error rule with `CASE WHEN occurrence_count < threshold
THEN 1`. Resist it: profiling is a **discovery** activity, Error is an **enforcement** activity,
and they're consumed differently — a profiling rule's output goes to a steward who decides
what's worth fixing, while an Error rule's output goes to ADM, which auto-counts defects and
reports defect rates.

If the < 0.1% rule is right, write it as a SECOND, separate Error rule. Keep the profiling rule
for the discovery view.

## From discovery to enforcement: A worked example

Here's a real progression showing how profiling leads to enforcement.

**Week 1: Create a Profiling rule**

Rule: `Profile of Material Status (MMSTA) distribution`

```sql
CREATE VIEW [dbo].[DQ_0045_SAP_MARA_StatusDistribution_PrfSel] AS

SELECT
  MMSTA AS MaterialStatus,
  COUNT(*) AS RecordCount,
  ROUND(100.0 * COUNT(*) / (SELECT COUNT(*) FROM MARA_Stage), 2) AS Percent,
  MIN(MATNR) AS FirstMaterial,
  MAX(MATNR) AS LastMaterial
FROM MARA_Stage
WHERE zSourceSystemID = 'SAP'
GROUP BY MMSTA
ORDER BY RecordCount DESC;
```

Output shows the distribution:

| MMSTA | RecordCount | Percent |
|-------|-------------|---------|
| 01    | 45,231      | 87.4%   |
| 02    | 3,567       | 6.9%    |
| XX    | 1,243       | 2.4%    |
| (null)| 459         | 0.9%    |

**SME observation:** "Why are 2.4% of materials marked XX (retired)? Those shouldn't be active."

**Week 3: Decide and create Error rule**

Engagement lead decides: **2% retired materials is a defect. Write an Error rule.**

New rule: `MARA: Retired materials in active dataset`

```sql
CREATE VIEW [dbo].[DQ_0046_SAP_MARA_RetiredStatus_OptSel] AS

SELECT
  -- Syniti Technical Fields
  MARA.zSourceSystemID AS [zSourceSystemID],
  CONCAT(MARA.MATNR, '_', MARA.zSourceSystemID) AS [zConcatenatedKey],
  CASE WHEN MARA.MMSTA = 'XX' THEN 1 ELSE 0 END AS [zIsErrorFlag],
  
  -- Basic Fields
  MARA.MATNR AS MaterialID,
  MARA.MMSTA AS MaterialStatus

FROM MARA_Stage AS MARA
WHERE MARA.zSourceSystemID = 'SAP'
;
```

Create the RptSel wrapper:

```sql
CREATE VIEW [dbo].[DQ_0046_SAP_MARA_RetiredStatus_RptSel] AS
SELECT * FROM [DQ_0046_SAP_MARA_RetiredStatus_OptSel]
WHERE [zIsErrorFlag] = 1
;
```

**Result:**
- **Profiling rule (DQ_0045)** stays active — continues to show all status values and percentages
- **Error rule (DQ_0046)** is new — enforces "no retired materials" and counts defects
- Both rules coexist; they answer different questions

The profiling rule **discovered** a problem; the Error rule **enforces** a policy.

## The vocabulary discipline

Use the right verbs:

| Activity | Profiling | Error |
|---|---|---|
| Acquire data | Fetch | Fetch |
| Operate on data | **Profile** (group by, count, percent) | **Check** (CASE-WHEN error) |
| Emit results | **Surface** (distribution) | **Return** (defect rows + flag) |

The verbs are the contract. A description that says "validates that profit centers are correct"
smells wrong on a profiling rule — it imports Error-rule vocabulary into a context where there
is no notion of "correct."

## Profiling rule review checklist

When reviewing a profiling rule before deployment:

- [ ] **Distribution visible?** Does the output show counts and percentages per group?
- [ ] **No zIsErrorFlag column?** Profiling rules should NOT have a flag; check it's absent
- [ ] **[Implication] or context column present?** Does it explain what each row means?
- [ ] **Segmentation clear?** Can a reader understand how rows are grouped? (e.g., "by plant", "by status")
- [ ] **Completeness achievable?** Can all rows be included, or is there an artificial WHERE filter?
- [ ] **Terminology correct?** Description uses "profile", "surface", "distribution" (not "defects", "validate")
- [ ] **No pass/fail logic?** No CASE statements checking business rules or thresholds

**If any check fails:** Mark `_review_required` and send back for revision.
