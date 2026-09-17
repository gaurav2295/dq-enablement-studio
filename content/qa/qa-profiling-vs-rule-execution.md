---
id: qa-profiling-vs-rule-execution
type: qa
title: What is the difference between profiling and rule execution?
domain: dq-fundamentals
audience: [consultant]
level: foundation
status: review
sources:
  - coe:changeset-5-sql-fundamentals
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:con-dq-lifecycle
  - relates:con-rule-types
---

## Question

What is the difference between profiling and rule execution? Aren't both activities looking for data issues?

## Answer

These are fundamentally different activities, despite both involving data analysis:

**Profiling** is *exploratory discovery*:
- Goal: Understand the data — what values exist, how they're distributed, what patterns emerge
- Activity: Run a schema profile, see what's nullable, empty, unusual, cardinality, distributions
- Output: A distribution report (PrfSel + PrfSum) — "10% of materials use EA, 85% use KG"
- Pass/Fail: **None** — profiling has no error conditions; it just shows what is
- Timing: Usually upfront, before rules exist

**Rule Execution** is *enforcement against constraints*:
- Goal: Validate that data meets business standards — find violations, flag defects
- Activity: Apply business rules (Error, Info, or Profiling rules), compute `zIsErrorFlag`, filter to violations
- Output: A defect report (RptSel) or distribution summary (PrfSum) — "423 materials are missing a base UoM"
- Pass/Fail: **Yes** (for Error/Info rules) / **No** (for Profiling rules, which follow their own naming convention — PrfSel/PrfSum)
- Timing: Continuous — rules run on every refresh to catch new defects

**The overlap:** Both can examine the same data. But profiling answers "what do we have?"; rules answer "what's broken?" (or for profiling rules, "how is it distributed across the business?").

**One-line summary:** Profiling says *"here's what the data looks like"*; rule execution says *"here's what should be fixed"* (or for profiling rules, *"here's how it's distributed across the business"*).

## Related

- [[con-dq-lifecycle|The DQ Lifecycle]]
- [[con-rule-types|Rule Types — Error, Info, Profiling]]
- [[prn-profiling-has-no-pass-fail|Why Profiling Has No Pass-Fail]]
