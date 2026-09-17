---
id: qa-sql-comments-dq-views-only
type: qa
title: Is the SQL commenting standard applicable only to DQ views?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:qa
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:prn-sql-comments-must-match-local-derive-quality
  - relates:std-sql-comment-standards
---

## Question

Is this commenting standard applicable only to DQ views, or should the same approach be followed for other Syniti-generated SQL objects as well?

## Answer

**The short answer:** The specific commenting standard (section headers, Include/Exclude prefixes, CASE comments structure) applies **only to DQ rule views** (OptSel, RptSel, InfSel, PrfSel, PrfSum).

**However:** The underlying principle — *"a non-SAP reviewer must understand the business meaning of every line"* — applies everywhere in Syniti SQL. Other SQL modules (ETL jobs, data warehouse loads, bridge views, dimension tables) should be well-commented, but they may follow their own architecture-specific standards rather than the DQ rule contract.

**What to do:** When working on non-DQ SQL, check your project's architecture documentation for that module's commenting standards. If none exist, the principle still holds: assume your audience has no SAP background and comment accordingly. The DQ rule format is not a one-size-fits-all solution.

See [[prn-sql-comments-must-match-local-derive-quality|Why SQL Comments Must Match Local-Derive Quality]] for full details — the scope note explicitly states this standard is specific to DQ rule views.
