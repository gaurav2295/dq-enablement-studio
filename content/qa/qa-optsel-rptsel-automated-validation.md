---
id: qa-optsel-rptsel-automated-validation
type: qa
title: Which OptSel/RptSel requirements are validated automatically by Studio?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-optsel-select-structure
  - relates:prc-audit-rule-quality
---

## Question

Which OptSel/RptSel requirements are validated automatically by Studio, and which remain the developer's responsibility?

## Answer

The Studio's **export validator** checks structural requirements; consultants remain responsible for **business logic**.

**Automatically validated by the Studio:**

| Requirement | Check | Fails if |
|---|---|---|
| **OptSel reads from source tables** | Scans FROM clause | FROM references another DQ view (e.g., `FROM DQ_0041_OptSel`) |
| **RptSel reads from OptSel only** | Scans FROM clause | FROM references source tables or a different OptSel |
| **RptSel has exactly one filter** | Parses WHERE | WHERE contains conditions other than `zIsErrorFlag = 1` |
| **zConcatenatedKey exists** | Searches SELECT | CASE or computation instead of column reference |
| **zIsErrorFlag is numeric 1/0** | Type checks CASE | Returns string `'Y'`, Boolean TRUE, or non-integer |
| **Column names match exactly** | Validates spelling | `zSourceSystem` (missing ID), `ZCONCATENATEDKEY` (wrong case) |
| **Three-part qualified names** | Checks database prefix | `FROM MARA` (bare), `FROM [SRCECC].[dbo].[MARA]` (source system) |

**Developer responsibility (manual review):**

| Aspect | Why manual |
|---|---|
| **Correct business logic in the CASE** | Studio can't verify semantics — "is NULL" vs "= 'X'" is your choice |
| **Correct joins** | Studio validates syntax; you validate the relationship is right |
| **Right fields in each section** | Studio checks comments exist; you verify field placement (Basic vs Org vs Value) |
| **WHERE conditions match the universe** | Studio can't know if "FERT only" is the right scope |
| **Comments match the SQL** | Studio checks comments exist; you verify they're accurate |

**The result:** You can't deploy SQL that **structurally violates the standard** (wrong view names, missing flag, literal zSourceSystemID). But you can deploy SQL that's **structurally correct but semantically wrong** (comments that lie, logic that misses edge cases).

That's why code review and audit are required after the Studio passes it.

## Related

- [[std-optsel-select-structure|OptSel SELECT Structure]]
- [[prc-audit-rule-quality|Audit Rule Quality]]
