---
id: qa-bulk-pipeline-reprocess-failed-individually
type: qa
title: Reprocessing Failed Rules After Bulk Pipeline Run
domain: studio
audience: [consultant, developer]
level: practitioner
status: review
links:
  - parent:prc-run-the-bulk-pipeline
  - relates:prc-derive-a-dq-rule
sources:
  - coe:changeset-7-dq-studio-workflow-2026-08-31
created: 2026-09-02
updated: 2026-09-02
---

## Question

If some rules succeed and others fail during a bulk run, can the failed rules be reprocessed individually, or must the entire batch be run again?

- How are failed rules marked/tracked?
- Can you select just the failed rules and re-run them?
- Do successful rules need to be re-derived if you run the batch again?
- How long until success/failure is final (or can you retry failed rules indefinitely)?

## Context

Bulk derivation processes many rules at once. Inevitably, some fail (missing metadata, ambiguous names, AI derivation issues). Users need a workflow to fix and retry without re-processing everything.

## Why This Matters

- **Efficiency** — Reprocessing 1,000 rules because 10 failed is wasteful
- **Iteration** — Consultant adds missing metadata, re-runs just failed rules
- **Audit Trail** — Must track which rules were re-derived and why
- **Time to Complete** — Clear retry workflow accelerates project completion

## Related Concepts

- **Bulk Pipeline** ([[prc-run-the-bulk-pipeline]]) — Batch derivation
- **Derive a Rule** ([[prc-derive-a-dq-rule]]) — Individual rule process
- **Project Spec** ([[gls-project-spec]]) — Input to bulk processor

## Expected Answer Should Cover

1. **Failed Rule Tracking:**
   - How are failures logged?
   - Where to view failure reasons?
   - Downloadable failure report?

2. **Retry Options:**
   - Re-run entire batch?
   - Re-run only failed rules?
   - Re-run specific subset?
   - How to select which rules to retry?

3. **Retry Process:**
   - Steps to prepare failed rules for retry
   - Does consultant edit spec between runs?
   - Validation before retry?

4. **Re-Derivation Idempotency:**
   - If successful rule is re-derived, does it overwrite?
   - Can user preserve manual edits from first run?
   - Version tracking of derivations?

5. **Limits & Best Practices:**
   - How many times can a rule be retried?
   - When to give up and escalate?
   - Recommended retry strategy

6. **Example Scenario:**
   - Bulk run: 1,000 rules, 950 succeed, 50 fail
   - Consultant reviews failures, adds missing domain mappings
   - Retry: Re-run 50 failed rules
   - Result: All pass, bulk pipeline complete

---

**Status:** Awaiting answer  
**Priority:** HIGH (workflow efficiency)  
**Changeset:** 7
