---
id: con-rule-types
type: concept
title: Rule Types — Error, Info, Profiling
domain: rule-design
audience: [consultant]
level: foundation
status: review
sources:
  - vault:dq-methodology/Rule Types — Error, Info, Profiling.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:con-view-types
  - relates:std-ziserrorflag-convention
  - relates:con-multi-implementation-model
  - relates:prn-profiling-has-no-pass-fail
  - relates:gls-optsel
---

## The three types

Every Syniti DQ rule is one of three types. The type determines what views are produced, how
SQL is shaped, and how results flow into SKP. (See [[con-view-types|View Types — OptSel, RptSel, InfSel, PrfSel, PrfSum]] for detailed explanations and SQL examples of each view type.)

## View and Flag Terminology

Every rule type produces SQL **views** with standardized suffixes that tell you their role. You'll also see the `zIsErrorFlag` column used throughout Error and Info rules:

| Term | What it is | What it contains |
|------|-----------|-----------------|
| **OptSel** | Opportunity select | All candidate records that the rule evaluates, plus a computed `zIsErrorFlag` column (0 or 1) indicating whether each record is defective |
| **RptSel** | Report select | Only the defective records (where `zIsErrorFlag = 1`), filtered from OptSel — the defect list that needs remediation |
| **InfSel** | Info select | For Info rules: records of interest, without a pass/fail flag — same shape as RptSel but semantically different (not "defects", just "noteworthy rows") |
| **PrfSel** | Profile select | For Profiling rules: record-level detail showing each record's value in the profiled attribute, plus segment columns |
| **PrfSum** | Profile summary | For Profiling rules: aggregated distribution (one row per segment/value) with counts and percentages — no flag, no pass/fail |
| **zIsErrorFlag** | Error flag column | An integer (0 or 1) computed in OptSel/InfSel that marks whether a record violates the rule condition. 0 = passes; 1 = defective. Profiling rules don't use this column. |

**Key insight:** The suffix tells you the contract — OptSel/RptSel pairs come with a flag for Error rules; PrfSel/PrfSum pairs come without a flag for Profiling rules; InfSel stands alone for Info rules. See [[con-view-types|View Types]] for detailed examples of each.

## Error

A pass/fail rule that flags records violating a business constraint.

- Emits **OptSel** (universe of candidates + `zIsErrorFlag`) and **RptSel**
  (`WHERE [zIsErrorFlag] = 1`).
- Defects (zIsErrorFlag = 1) need remediation before downstream use.
- Example: *"A material must have a valid base unit of measure."*

**What is "universe"?** The universe (or scope) is the set of records the rule evaluates — not *all* data, but the records that *should* have this rule applied. For example:
- A rule checking "finished goods must have a costing method" has a universe of **only finished-goods materials** (MARA.MTART = 'FERT'), not all material types.
- A rule checking "active customer credit limits must be <= €1M" has a universe of **only active customers** (KNVP.STATAG ≠ 'X'), not deleted or test records.
- A rule checking "purchase order line items must have a delivery date" applies to **all PO line items in a date range**, not historical archives.

The universe is defined in the rule's OptSel view via a `WHERE` clause that filters to "records in scope". Everything outside that WHERE is implicitly out of scope — the rule doesn't evaluate it. See [[prn-optsel-is-the-universe|Why OptSel Is the Universe and RptSel Is the Wrapper]] for the technical details.

## Info

Same structural shape as Error — flags records — but the surfaced rows aren't *defects*; they're
records worth attention. No remediation contract.

- Same OptSel + RptSel pair, with the same zIsErrorFlag mechanics.
- Surfaces things like high-value customers, recently-changed master records, or "look here"
  cases.
- Example: *"A customer with credit limit > €1M should be flagged for review."*

## Profiling

No pass/fail — produces a distribution of values across segments.

- Emits **PrfSel** (record-level detail) and **PrfSum** (aggregated summary with percentages).
- No `zIsErrorFlag`. No CASE-WHEN-error logic.
- Cross-system by design — does NOT fan out per system; segments by `zSourceSystemID`.
- Example: *"Profile of Profit Center usage by Controlling Area."*

## Why three types and not two

Profiling could be implemented as "an Info rule with no error condition", but the **vocabulary
differs sharply**:
- Error/Info → talks about *defects*, *check conditions*, *remediation*
- Profiling → talks about *distributions*, *segmentation*, *percentage windows*

Mashing them into one shape produces SQL where profiling rules awkwardly carry a
`WHERE [zIsErrorFlag] = 1` line that filters everything out, OR Error rules awkwardly carry
GROUP BY clauses that don't belong. Keeping them separate keeps each idiom clean.

## OptSel and RptSel — what they mean (with example)

Error and Info rules always produce two views: **OptSel** and **RptSel** (for Info rules, it's OptSel and **InfSel**). Here's what each does:

**OptSel** (Opportunity Select)
- Contains **all candidate records** the rule evaluates
- Each row has a computed `zIsErrorFlag` column (0 or 1)
- 0 means the record passes the rule; 1 means it fails (defective)
- Used by remediation teams to understand the full scope of records they're working with

**RptSel** (Report Select)
- Contains **only the defective records** (where `zIsErrorFlag = 1`)
- It's simply: `SELECT * FROM OptSel WHERE zIsErrorFlag = 1`
- Used by stakeholders to see the defect list that needs fixing
- The RptSel count ÷ OptSel count = defect rate

### Example: MARA materials rule

Rule: *"Active material must have valid base unit of measure"*

**OptSel output (all active materials in scope):**

```
MATNR      | MEINS | zIsErrorFlag
-----------|-------|-------------
M000001    | KG    | 0
M000002    | EA    | 0
M000003    | NULL  | 1  ← defective
M000004    | KG    | 0
M000005    | NULL  | 1  ← defective
M000006    | EA    | 0
... (137,494 more records)
-----------|-------|-------------
Total OptSel rows: 137,500 (the universe)
Defects (zIsErrorFlag = 1): 8,200
```

**RptSel output (defects only):**

```
MATNR      | MEINS | zIsErrorFlag
-----------|-------|-------------
M000003    | NULL  | 1
M000005    | NULL  | 1
... (8,198 more defective records)
-----------|-------|-------------
Total RptSel rows: 8,200 (the defects)
```

**The calculation:**

```
Defect rate = RptSel count / OptSel count
            = 8,200 / 137,500
            = 5.97%
```

**Why both views?** Because downstream reporting and remediation need both numbers at once:
- OptSel row count = the denominator (eligible records)
- RptSel row count = the numerator (failed records)
- Defect rate = failures ÷ eligible (the ratio that matters to stakeholders)

If OptSel pre-filtered to defects only, every rule would report 100% defect rate (meaningless). If RptSel returned everything unfiltered, you couldn't tell which records are defective. The split is strict on both sides.

For **Profiling rules**, the pattern is different: they produce **PrfSel** (record-level detail) and **PrfSum** (aggregated summary with percentages), without a flag or binary pass/fail.

## Related

- [[con-view-types|View Types — OptSel RptSel InfSel PrfSel PrfSum]]
- [[std-ziserrorflag-convention|zIsErrorFlag Convention]]
- [[con-multi-implementation-model|Multi-Implementation Model]]
- [[prn-profiling-has-no-pass-fail|Why Profiling Has No Pass-Fail]]
