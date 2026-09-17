---
id: qa-what-is-parity-check
type: qa
title: What is a parity check in DQ rules?
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
  - relates:prc-audit-rule-quality
---

## Question

Could we briefly explain what a parity check is, or link to the relevant module if it's covered elsewhere?

## Answer

A **validation that confirms the SQL matches the specification and the Implication cell**.

Three documents must always agree:

1. **Spec Markdown** — the rule description (Fetch/Check/Return bullets)
2. **SQL view** — the actual OptSel/RptSel code deployed
3. **SKP AssetUpload** — the Implication cell shown to end users

**Parity check** compares these three and asks: *"Do they say the same thing?"*

Example: If the spec says "Limit to finished goods (MTART = 'FERT')" but the SQL has `MTART IN ('FERT', 'HALB')`, that's **parity failure** — a mismatch. The Audit screen flags it with a score (e.g., 0.78 / 1.0 = 78% parity).

**Why it matters:** If spec and SQL diverge, the audit is compromised. Reviewers can't tell *which* document is right, and end users see a promise in SKP that the SQL doesn't keep.

The [[std-sql-comment-standards|SQL Comment Standards]] mandate detailed comments *specifically so parity checks can work* — well-commented SQL is auditable SQL.

## Related

- [[std-sql-comment-standards|SQL Comment Standards]]
- [[prc-audit-rule-quality|Audit Rule Quality]]
