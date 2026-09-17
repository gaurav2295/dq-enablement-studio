---
id: qa-accuracy-vs-conformity-impossible-values
type: qa
title: How do we distinguish between Accuracy and Conformity when a value is technically valid but not realistically possible?
domain: dq-fundamentals
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:qa
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:con-dq-dimensions
---

## Question

How do we distinguish between Accuracy and Conformity when a value is technically valid but not realistically possible? For example, if a material creation year is 1905, would that be classified as an Accuracy issue or a Conformity issue?

## Answer

**The distinction depends on the real-world context:**

- **If the material genuinely was created in 1905** → it is **Accurate** (matches reality), but likely **Non-Conforming** (fails your system's standard range, e.g., "materials must be created after 1950")
  - *Remediation:* Code review. Clarify with the business whether 1905 is valid for this domain. If materials from that era are genuinely part of the master data, update the conformity standard. If it's a data entry error, update the record.

- **If the material was NOT created in 1905** (e.g., it's a modern material, but the year was entered wrong) → it is **Inaccurate** (doesn't match reality) and likely also **Non-Conforming**
  - *Remediation:* Data cleanup. Research the correct creation year and update the record.

**How to tell which is which:**

1. **Check the real-world source.** Was this material actually created in 1905? Contact the source system owner or business steward.
2. **If YES** → Accuracy is fine; Conformity failed (system's range rule is the issue).
3. **If NO** → Accuracy failed; you need to find the correct value.

**Why it matters:** An accurate value that fails conformity needs a *system decision* (adjust the range? Yes or no?). An inaccurate value needs *data research and cleanup* (what's the real value?). Confusing them leads to wrong remediation.

See [[con-dq-dimensions|The Seven DQ Dimensions]] for the full explanation of when Accuracy and Conformity diverge.
