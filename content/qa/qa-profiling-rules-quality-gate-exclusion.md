---
id: qa-profiling-rules-quality-gate-exclusion
type: qa
title: Why are profiling rules excluded from the AI SQL Quality Gate?
domain: ai-enhancement
audience: [consultant, developer]
level: practitioner
status: approved
sources:
  - coe:ref-ai-static-validator-gate and prn-profiling-has-no-pass-fail
created: 2026-09-02
updated: 2026-09-02
links:
  - parent:ref-ai-static-validator-gate
  - relates:prn-profiling-has-no-pass-fail
  - relates:gls-prfsel
  - relates:gls-prfsum
  - relates:prc-audit-rule-quality
---

## Question

Why are profiling rules excluded entirely from the quality gate rather than having a reduced set of profiling-specific checks applied to them?

## Answer

**Profiling rules skip the quality gate because they operate on fundamentally different principles than Error rules.** The gate's checks are shaped for Error rules and would only produce noise on profiling rules.

### The Structural Difference

**Error Rules (Gate applies):**
- ✅ Expect `zIsErrorFlag` column (1 = error, 0 = valid)
- ✅ Expect OptSel + RptSel pair
- ✅ Filter WHERE for universe, CASE for logic
- ✅ Gate checks all of these

**Profiling Rules (Gate doesn't apply):**
- ❌ No `zIsErrorFlag` — profiling has no pass/fail
- ❌ No OptSel + RptSel pair — only PrfSel (detail) + PrfSum (summary)
- ❌ No error condition in CASE — only GROUP BY aggregations
- ❌ Gate's checks would flag all of the above as errors (false positives)

### Why a "Profiling-Specific Gate" Wouldn't Help

**It would be more complex, not simpler:**

1. **Most checks wouldn't apply** — e.g., "is zIsErrorFlag present?" is meaningless for profiling
2. **Profiling validity is different** — the real question is "are COUNT and COUNT DISTINCT correct?", not "is the error flag right?"
3. **Profiling is audit-heavy, not gate-heavy** — profiling rules are reviewed manually for accuracy, not auto-gated for syntax

**Better to skip it entirely and rely on the heavier [[prc-audit-rule-quality|Audit Rule Quality]] process,** which handles both Error and Profiling rules correctly.

---

### What Profiling Rules Get Instead

**Profiling rules still have guardrails, just different ones:**

1. **Manual audit only** — no automated gate, but Audit Rule Quality covers them comprehensively
2. **Sample data review** — AI Enhance generates sample data showing a few rows from PrfSel and PrfSum so you can verify the aggregation is sensible
3. **Format checking** — basic SQL syntax is still checked, just not the Error-specific structure

---

### The Trade-Off

| Approach | Pro | Con |
|---|---|---|
| **Separate profiling-specific gate** | Could catch profiling-unique bugs | Complex; most checks irrelevant; adds maintenance burden |
| **Skip gate entirely (current)** | Simple; no false positives; lets audit handle it | Relies on manual review; less automated safety net |

**Current choice:** Skip the gate. Profiling rules are validated during the [[prc-audit-rule-quality|Audit]] phase, not the quality gate phase.

---

### Related

- [[ref-ai-static-validator-gate|The AI SQL Quality Gate]]
- [[prn-profiling-has-no-pass-fail|Why Profiling Has No Pass/Fail]]
- [[prc-audit-rule-quality|Audit Rule Quality]]
