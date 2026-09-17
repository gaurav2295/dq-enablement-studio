---
id: gls-adm
type: glossary
title: ADM
domain: platform
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:prn-ziserrorflag-is-integer
  - relates:prn-optsel-is-the-universe
  - relates:gls-defect-rate
  - relates:gls-adm-rule-name
sources:
  - dq-studio:docs/DQ_RULE_STANDARDS.md
  - bob-dq:CLAUDE.md
tags: [platform, downstream]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The Syniti platform environment that consumes deployed DQ rule views, counts defects against
opportunities, and reports the results. An engagement's instance is referred to as its **ADM-M
environment**, and it is where rule execution actually happens — the design tooling never touches
client systems.

## Usage

Several conventions in this corpus are ADM contracts rather than preferences:

- [[gls-ziserrorflag|zIsErrorFlag]] must be an **integer** — ADM counts defects arithmetically.
- The OptSel/RptSel pair must reconcile — ADM computes `defects / opportunities` from both.
- [[gls-zconcatenatedkey|zConcatenatedKey]] carries **no space** in its alias.
- Rule names are capped at 100 characters.

> [!note]
> The sources use "ADM" unexpanded throughout; no expansion is recorded in the material this
> corpus is built from, so none is asserted here.
