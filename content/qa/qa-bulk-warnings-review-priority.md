---
id: qa-bulk-warnings-review-priority
type: qa
title: Review Priority for Rules Completed with Warnings
domain: studio
audience: [consultant]
level: practitioner
status: review
links:
  - parent:prc-run-the-bulk-pipeline
  - relates:prc-audit-rule-quality
sources:
  - coe:changeset-7-dq-studio-workflow-2026-08-31
created: 2026-09-02
updated: 2026-09-02
---

## Question

What should be reviewed first when a rule completes with warnings but does not fail the pipeline?

- What categories of warnings exist?
- Are all warnings equal priority or are some more critical?
- Is manual review mandatory for any warnings?
- Can a rule be deployed if it has warnings?

## Context

The bulk pipeline passes rules with warnings (not failures). Distinguishing "review-able" warnings from "acceptable" warnings helps prioritize consultant effort.

## Why This Matters

- **Quality Gate** — Some warnings may block deployment; others are informational
- **Efficiency** — Prioritize review time on high-risk warnings
- **Confidence** — Know when a warning is safe to ignore vs. must be fixed
- **Audit Trail** — Document why warnings were accepted or escalated

## Related Concepts

- **Audit Quality** ([[prc-audit-rule-quality]]) — Post-execution validation
- **Bulk Pipeline** ([[prc-run-the-bulk-pipeline]]) — Batch operation
- **Rule Fulfillment** ([[gls-rule-fulfilment-review]]) — Semantic validation

## Expected Answer Should Cover

1. **Warning Categories:**
   - Performance warnings (correlated subqueries, inefficient joins)
   - Confidence warnings (AI low-confidence on table/field matching)
   - Semantic warnings (rule name ≠ logic, slight mismatch)
   - Metadata warnings (missing description, sources)
   - [Other?]

2. **Priority Levels:**
   - Critical: Always review, may block deployment
   - High: Review strongly recommended
   - Medium: Consider reviewing if time allows
   - Low: Safe to ignore if quality acceptable

3. **Deployment Readiness:**
   - Can rule deploy with warnings?
   - Which warning categories block deployment?
   - Override mechanism?

4. **Review Checklist:**
   - For each warning type, what to check
   - Acceptance criteria

5. **Example:**
   - Rule A: Completes with "correlated subquery" warning (performance) — Review priority?
   - Rule B: Completes with "AI confidence 60%" warning (semantic) — Review priority?
   - Rule C: Completes with "missing description" warning (metadata) — Block deployment?

---

**Status:** Awaiting answer  
**Priority:** HIGH (deployment gate)  
**Changeset:** 7
