---
id: qa-who-decides-universe-scope
type: qa
title: Who decides which records belong in the opportunity universe?
domain: rule-design
audience: [consultant, lead]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-04
created: 2026-09-07
updated: 2026-09-07
---

## Question

A rule's opportunity universe is defined by the `WHERE` clause filters (system scope, deletion 
flags, status filters, business scope). But **who on the engagement decides what those filters 
should be?** Is it the SME? The DBA? The engagement lead?

## Answer

**The SME (subject matter expert) decides; the DBA implements.** Here's the decision workflow:

### The SME decides the scope

The SME owns the business definition of "what records are in play for this rule." They answer:

- **Should deleted records be included?** → "No, we only care about active materials"
- **Should test data be included?** → "No, exclude MTART = 'TEST'"
- **Should inactive records be included?** → "No, only materials with status 01, 02, 03"
- **Should records from all plants be included?** → "No, only Plants 1000 and 1100"

These answers become the universe scope. They are **not technical decisions**; they are 
**business decisions about what matters**.

### The DBA implements the scope

Once the SME has decided, the DBA translates it into WHERE-clause filters:

- "active materials only" → `LVORM <> 'X'` (delete flag field)
- "exclude test data" → `MTART NOT IN ('TEST', 'SAMPLE')`
- "status 01, 02, 03" → `MMSTA IN ('01', '02', '03')`
- "plants 1000, 1100" → `WERKS IN ('1000', '1100')`

The DBA may negotiate with the SME ("which status codes count as active?") but the 
DBA is not deciding — the SME is.

### During rule authoring

In the Studio:

1. **Consultant (with SME) writes the rule description** — this includes the scope 
   ("Find active materials missing unit of measure")
2. **Consultant derives the rule** → fills in the `WHERE` clause based on the scope
3. **DBA reviews in audit** → confirms the WHERE filters match the business intent

### When scope is unclear

If the SME hasn't decided yet, the rule is marked `_review_required` and sent back. 
The Studio does not guess the scope.

> [!tip]
> **The universe is a business decision, not a technical detail.** If the SME can't articulate 
> which records are "in play," the rule isn't ready to author.
