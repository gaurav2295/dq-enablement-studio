---
id: qa-why-prfsel-not-optsel
type: qa
title: Why are profiling rules implemented using PrfSel and PrfSum instead of OptSel and RptSel?
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

Why are profiling rules implemented using PrfSel and PrfSum instead of OptSel and RptSel?

## Answer

**The core reason:** OptSel/RptSel embody an **error rule contract** (binary pass/fail with a flag), while profiling rules have a **fundamentally different contract** (distribution without error semantics).

**Error rules (OptSel ↔ RptSel):**
- OptSel holds the complete universe with a `zIsErrorFlag` (`1` = error, `0` = pass)
- RptSel wraps OptSel with `WHERE zIsErrorFlag = 1` to show defects only
- Downstream reporting needs *both* counts: universe size (OptSel) and defect count (RptSel) to compute defect rate

**Profiling rules (PrfSel ↔ PrfSum):**
- PrfSel returns record-level detail (one row per source record with profiled attribute)
- PrfSum returns aggregated distribution (one row per segment + value with count and percentage)
- There is no `zIsErrorFlag` — profiling has no concept of "error"
- No binary pass/fail; instead shows "X% of materials use unit EA, Y% use KG"

**Why different names matter:** The suffix signals the contract to downstream tooling:
- `RptSel` always means "defects only" (error rule output)
- `PrfSel` / `PrfSum` means "distribution detail/summary" (no error model)

Using `OptSel/RptSel` for profiling would mislead reviewers (they'd expect a flag) and break tooling that routes views by suffix. Different suffixes ensure clarity and prevent confusion.

See [[con-view-types|View Types — OptSel, RptSel, InfSel, PrfSel, PrfSum]] for the full structure and examples.
