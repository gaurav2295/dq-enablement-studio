---
id: gls-optsel
type: glossary
title: OptSel (Opportunity Selection view)
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: approved
links:
  - relates:con-dq-dimensions
  - relates:prn-optsel-is-the-universe
sources:
  - vault:dq-methodology/View Types.md
  - dq-studio:knowledge/methodology/view_conventions.json
tags: [views, optsel]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **Opportunity Selection view** — the primary SQL view of a DQ rule. It selects the full
population of records the rule applies to (the *universe*) and computes `zIsErrorFlag`
(`1` = error, `0` = clean) for every record in it. Naming pattern:
`DQ_{id}_{table}_{field}_{description}_OptSel`.

## Usage

Every Error rule ships as an OptSel plus a wrapping RptSel; the OptSel is where all logic
lives. The mandatory technical fields (`zDQOpsID`, `zRuleName`, `zSourceSystemID`,
`zConcatenatedKey`, `zIsErrorFlag`) appear first, in that order.

> [!tip]
> If you find rule logic in a RptSel, that is a standards violation — the RptSel is a wrapper,
> never a second brain. See [[prn-optsel-is-the-universe]].
