---
id: qa-dimension-priority-business-dependent
type: qa
title: Are Accuracy and Integrity always higher priority than other dimensions, or does the priority depend on business process and client requirements?
domain: dq-fundamentals
audience: [consultant, lead]
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

Are Accuracy and Integrity always higher priority than other dimensions, or does the priority depend on the business process and client requirements?

## Answer

Priority is **NOT fixed** — it depends entirely on business context and client requirements. Accuracy and Integrity are *often* high priority because they typically block transactions or disrupt reporting, but this is context-dependent.

**Accuracy priority depends on:**
- **Which field?** A customer's phone number (Accuracy) might be critical for contact delivery but not for financial posting. A payment amount (Accuracy) might be blocking for revenue recognition.
- **Which process?** Shipping depends on accurate addresses. Costing depends on accurate prices. Neither is universally "higher priority."
- **Which business?** A healthcare provider prioritizes Accuracy in patient allergies (safety-critical). A logistics company prioritizes Accuracy in delivery locations.

**Integrity priority depends on:**
- **Which reference?** A broken customer → sales order link blocks order fulfillment. A broken material → BOM link might only affect planning or costing.
- **How often does it occur?** One orphaned record might have low impact. Millions of orphaned records block system initialization.

**Completeness is also context-dependent:**
- Completeness gaps (missing required values) can block transactions — a customer without a credit limit blocks credit approval.
- Completeness gaps in optional fields might have low business impact.

**The real rule:** Always ask the business to confirm criticality. Don't assume Accuracy or Integrity = always-critical. Completeness gaps in required fields might block transactions just as much as Accuracy defects. Dimension priority ranking is a business decision, not a methodology rule.

See [[con-dq-dimensions|The Seven DQ Dimensions]] for how to approach criticality assessment — the "Why dimensions matter operationally" section explains how dimension priority depends on business context.
