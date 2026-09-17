---
id: qa-why-infsel-not-rptsel
type: qa
title: If a rule is informational rather than error-based, why is InfSel used instead of RptSel?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:qa
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:con-view-types
  - relates:prn-fetch-check-return
---

## Question

If a rule is informational rather than error-based, why is InfSel used instead of RptSel?

## Answer

**The core reason:** `RptSel` implies "reports of defects" (binary pass/fail), while `InfSel` means "selection of informational results" (no error model).

**Error rules use RptSel:**
- RptSel filters OptSel to `WHERE zIsErrorFlag = 1` (defects only)
- The name signals: this view shows records that *failed* the rule
- Example: "Customer missing a country code" — failure is the point

**Info rules use InfSel:**
- Info rules don't produce pass/fail — they produce *counts and distributions*
- A rule like "Count of sales orders per material" returns one row per unique value, not one row per material with a pass/fail flag
- InfSel reflects this: it's a "selection of informational results", not "reports of defects"
- Example: "10 finished goods use unit EA, 45 use KG, 12 use LTR" — no error semantics, just observation

**Why the distinction matters:**
- **Naming clarity:** `RptSel` always means "binary failure report"; `InfSel` always means "informational observation"
- **Downstream routing:** Tools that consume DQ views route by suffix. A tool expecting pass/fail logic would misinterpret `InfSel` if it carried the `RptSel` name
- **Domain language:** Info rules answer "what does the data look like?" not "what's wrong with it?"

**The naming pattern:**
- Error rules: OptSel (universe) + RptSel (defects)
- Info rules: InfSel (distribution of values — no paired universe view)
- Profiling rules: PrfSel (record detail) + PrfSum (aggregated distribution)

See [[con-view-types|View Types — OptSel, RptSel, InfSel, PrfSel, PrfSum]] for the full structure and examples of each rule type.
