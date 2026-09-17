---
id: qa-bulk-pipeline-reprocess-failed-rules
type: qa
title: Can failed rules be reprocessed individually or must the entire batch be run again?
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
  - relates:prc-derive-a-dq-rule
---

## Question

If some rules succeed and others fail during a bulk run, can the failed rules be reprocessed individually, or must the entire batch be run again?

## Answer

**You can reprocess failed rules individually in the single-rule designer.** There is no need to re-run the entire batch.

**Process:**
1. Open the failed rule in **Space 1 — DQ Rules** (the single-rule designer)
2. Fix the issue (e.g., set missing API key, improve rule name, select table manually)
3. Click **Derive** again or **AI Enhance**
4. Verify it succeeds
5. Stage it in the workspace

The successful rules from the previous bulk run remain in the workspace. Only the rules you fix are re-processed.

---

### Related

- [[prc-run-the-bulk-pipeline|Run the Bulk Pipeline]]
- [[prc-derive-a-dq-rule|Derive a DQ Rule (single rule)]]
