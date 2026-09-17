---
id: gls-consistency
type: glossary
title: Consistency
domain: dq-fundamentals
audience: [consultant, lead, instructor]
level: foundation
status: review
links:
  - relates:con-dq-dimensions
  - relates:gls-conformity
sources:
  - coe:seven-dimension model per CONFLICT-001
  - vault:dq-methodology/DQ Dimensions.md
tags: [dimensions, foundations]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**Do related values agree with each other across records and systems?** Consistency is a
comparison dimension — it needs two or more places the same fact is stored and checks they say
the same thing. Unlike [[gls-conformity]], which validates one field against a fixed standard,
Consistency validates one field against another live value, so the rule is only as good as the
join between the two sources.

## Example rule

A customer's currency matches between the sales-area view (`KNA1`/`KNVV`) and the company-code
view (`KNB1`). The same customer master can carry two different currency codes if the records
were maintained by different teams at different times — the rule catches the drift.

## Cost of a defect

A currency mismatch between sales and finance views causes wrong currency conversion on billing,
reconciliation breaks between SD and FI, and manual correction before period close. Consistency
defects are expensive precisely because each side of the comparison looks individually correct —
the record passes every single-field check and only fails when checked against its counterpart,
which is why Consistency and Conformity are usually run as a paired check: format first, then
agreement.
