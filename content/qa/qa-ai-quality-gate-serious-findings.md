---
id: qa-ai-quality-gate-serious-findings
type: qa
title: What types of findings trigger the AI to retry?
domain: ai-enhancement
audience: [consultant, developer]
level: practitioner
status: approved
sources:
  - coe:ref-ai-static-validator-gate
created: 2026-09-02
updated: 2026-09-02
links:
  - parent:ref-ai-static-validator-gate
  - relates:prc-audit-rule-quality
  - relates:gls-rule-fulfilment-review
---

## Question

Are there specific types of findings considered "serious" enough to trigger the single retry?

## Answer

**Yes.** The AI SQL Quality Gate retries on **"serious" findings** — issues that will cause the SQL to fail or produce incorrect results.

### Serious Findings (Trigger One Retry)

**Findings that cause a retry:**

| Finding Type | Example | Why Serious |
|---|---|---|
| **SQL won't compile** | Missing closing parenthesis, invalid column name, syntax error | Rule cannot be deployed |
| **Critical logic flaw** | zIsErrorFlag inverted (returns 0 on errors, 1 on valid records) | Wrong defects flagged |
| **Missing required field** | zSourceSystemID missing from SELECT or WHERE | Rule won't align across systems |
| **Wrong join condition** | Join missing ON clause, or joining wrong tables | Data integrity broken |
| **Hardcoded values in logic** | `WHERE zSourceSystemID = 'Z01'` instead of column reference | Rule won't fan-out to other systems |

### What Happens on Retry

1. The AI receives the exact error/finding from the quality gate
2. The AI is told: "You produced this error. Fix it."
3. The AI rewrites the SQL to resolve the issue
4. The rewritten version is **always shown to you** with findings attached, regardless of whether the second attempt succeeded

**Result:**
- ✅ If fixed → You see clean SQL with zero serious findings
- ⚠️ If not fixed → You see the SQL with findings still recorded; you must manually review and fix

### Lesser Findings (No Retry, Just Warning)

**Findings that do NOT trigger a retry:**

| Finding Type | Example | Action |
|---|---|---|
| **Code style** | Inconsistent naming, extra line breaks | Recorded as warning; you can ignore or manually fix |
| **Performance hints** | Suboptimal index usage, missing covering columns | Recorded as warning; optimize if time allows |
| **Comment quality** | Comments don't explain the join logic | Recorded as warning; update comments manually |
| **Unused fields** | A field in SELECT not used in CASE logic | Recorded as warning; remove if unnecessary |

---

### The Retry is Exactly One

There is **no loop**. The process is:

1. AI produces SQL
2. Quality gate checks it
3. If serious findings → AI retries once (exactly once)
4. Whatever comes back is shown to you with findings attached

**Example:**
- Attempt 1: Missing zSourceSystemID → Serious → Triggers retry
- Attempt 2: Still missing zSourceSystemID → No retry → Findings shown, you fix manually

---

### Where Findings Are Recorded

Once you save/export:
- **Accepted AI enhancements:** Findings appear on the **Reconciliation** sheet in the bulk export
- **Rules that failed save:** Findings appear on the **Failed Rules** sheet
- **During review in Studio:** Findings display as inline warnings and a summary banner

---

### Related

- [[ref-ai-static-validator-gate|The AI SQL Quality Gate]]
- [[prc-audit-rule-quality|Audit Rule Quality]]
- [[prc-run-the-bulk-pipeline|Run the Bulk Pipeline]]
