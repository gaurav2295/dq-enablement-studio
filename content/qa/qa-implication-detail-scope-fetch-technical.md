---
id: qa-implication-detail-scope-fetch-technical
type: qa
title: How Much Detail in Implication Scope/Fetch Before Becoming Too Technical?
domain: rule-design
audience: [consultant, lead]
level: practitioner
status: review
links:
  - parent:prc-format-an-implication
  - relates:gls-implication
  - relates:prn-fetch-check-return
  - relates:std-output-field-sections
sources:
  - coe:changeset-7-dq-studio-workflow-2026-08-31
created: 2026-09-02
updated: 2026-09-02
---

## Question

For rules involving multiple tables and joins, how much detail should be included in the Scope and Fetch sections before the Implication becomes overly technical?

Where's the line between:
- **Helpful detail** ("Checks MARA + MARC join on Material")
- **Too technical** ("JOINs MARA to MARC on MATNR = MATNR WHERE MARA.zSourceSystemID = MARC.zSourceSystemID")

## Context

The Implication section must communicate business impact (for stakeholders) and rule logic (for auditors). Finding the right balance is an art, not a science.

## Why This Matters

- **Readability** — Business stakeholders shouldn't need SQL knowledge to understand rule impact
- **Audit Trail** — Auditors need enough technical detail to verify the rule does what Implication says
- **Rule Clarity** — Ambiguous Implications cause confusion during rule review and enhancement

## Related Concepts

- **Implication** ([[gls-implication]]) — What it costs when rule fails
- **Fetch/Check/Return** ([[prn-fetch-check-return]]) — Rule description structure
- **Output Sections** ([[std-output-field-sections]]) — Context vs Subject

## Expected Answer Should Cover

1. **Sweet Spot** — Recommended detail level with rationale
2. **Examples:**
   - Simple rule (single table): "Checks [field] is not NULL"
   - Join rule (2 tables): "Checks every [table1] has a corresponding [table2] record"
   - Complex join (3+ tables): Guidance on abstraction level
3. **Anti-Patterns:**
   - Too technical: Full SQL written out
   - Too vague: "Checks data integrity" (meaningless)
4. **Testing Question:** How to know if Implication has right detail?
5. **Guidance:** When to split one rule into multiple simpler rules (rather than making Implication complex)

---

**Status:** Awaiting answer  
**Priority:** MEDIUM (Implication quality guidance)  
**Changeset:** 7
