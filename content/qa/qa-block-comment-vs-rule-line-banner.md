---
id: qa-block-comment-vs-rule-line-banner
type: qa
title: What's the difference between block comment and rule-line banner formats?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-sql-comment-standards
---

## Question

I'm finding it difficult to understand the relationship between the block comment vs rule-line banner formats and the fields they contain. Could this be explained more clearly?

## Answer

Two **equivalent** ways to express the same four mandatory facts. Use one or the other, not both.

| Aspect | Block Comment Form | Rule-Line Banner Form |
|--------|-------------------|----------------------|
| **Format** | `/* --- ... --- */` at the top | `-- ====` lines with inline fields |
| **Fields** | Rule Name, Author, Creation Date, View Type | Rule Name, Rule ID, View Type, Generated, Target |
| **When** | Hand-authored rules | Studio-generated rules |
| **Parser** | Generic; any SQL tool can read it | Studio-specific; used for round-trip |
| **Which to use** | On consultant-written rules | On all Studio-generated output |

**Block form (hand-authored):**
```sql
/* ---------------------------------------------------------
Rule Name: A material must have a valid base unit of measure
Author: Jane Consultant
Creation Date: 2026-06-01
View Type: Opportunity Report (OptSel)
--------------------------------------------------------- */
```

**Rule-line banner (Studio-generated):**
```sql
-- ============================================================
-- DQ Rule: A material must have a valid base unit of measure
-- Rule ID: 0042
-- View:    Opportunity Report (OptSel) (DQ_0042_P02_MARA_MEINS_OptSel)
-- Generated: 2026-06-01T13:21:56
-- Target: MS SQL Server
-- ============================================================
```

**Key insight:** The banner is where the Studio's round-trip parser **finds the boundaries** of a rule's SQL block. If you hand-author a rule, you can use the block form; if Studio generated it, keep the rule-line banner — don't convert between them on a live rule (it breaks the parser).

**All four facts must be present in whichever form you choose:**
1. Rule name (verbatim from tracker)
2. Author or Rule ID (to trace who made it)
3. Creation date (for audit trail)
4. View type (OptSel, RptSel, InfSel, etc.)

## Related

- [[std-sql-comment-standards|SQL Comment Standards]]
