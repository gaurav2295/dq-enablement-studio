---
id: qa-bulk-pipeline-warnings-review-priority
type: qa
title: What should be reviewed first when a rule completes with warnings but does not fail?
domain: studio
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:prc-run-the-bulk-pipeline
created: 2026-09-03
updated: 2026-09-03
links:
  - parent:prc-run-the-bulk-pipeline
  - relates:prc-audit-rule-quality
---

## Question

What should be reviewed first when a rule completes with warnings but does not fail the pipeline?

## Answer

**Review in this priority order:**

1. **The warning message itself** — what is specifically flagged?
   - Stale comment? Missing PK? Unknown table? Validator finding?

2. **The per-rule SQL preview** — does the generated SQL match your intent, even though there's a warning?

3. **The spec** — does the Implication and field sections make sense despite the warning?

4. **Decide:**
   - ✅ **Accept** if the warning is cosmetic (formatting, comment clarity) and the logic is correct
   - ⚠️ **Review carefully** if the warning indicates a potential data-quality issue (missing join, wrong table)
   - ❌ **Fix and re-derive** if the warning suggests the rule won't work as intended

---

### Related

- [[prc-run-the-bulk-pipeline|Run the Bulk Pipeline]]
- [[prc-audit-rule-quality|Audit Rule Quality]]
