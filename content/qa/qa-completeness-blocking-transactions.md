---
id: qa-completeness-blocking-transactions
type: qa
title: Why are Completeness gaps considered more tolerable than Accuracy or Integrity issues? Are there examples where a Completeness issue can also block a transaction?
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

Why are Completeness gaps considered more tolerable than Accuracy or Integrity issues? Are there examples where a Completeness issue can also block a transaction?

## Answer

Completeness gaps are **NOT always more tolerable** than Accuracy or Integrity. The tolerance depends on *which* value is missing and whether it blocks a critical business process.

**Completeness is MORE tolerable when:**
- The system can auto-populate a sensible default (e.g., default tax ID to a placeholder)
- Downstream processes can continue with partial data
- The gap is in a secondary (non-critical) field

**Completeness is LESS tolerable (blocking) when:**
- The missing value is a primary key or natural key
- The missing value is a blocking prerequisite for a downstream process
- The business process cannot proceed without it

**Examples of Completeness gaps that DO block transactions:**

1. **Customer missing a credit limit** (required for credit approval)
   - Process: Dunning/credit check before fulfillment
   - Impact: Order cannot be released until credit limit is set
   - Blocking: YES — transaction halts

2. **Material missing a base unit of measure (UoM)**
   - Process: Planning and costing require UoM to calculate demand and inventory value
   - Impact: Cannot reserve inventory, cannot cost goods sold
   - Blocking: YES — transaction halts

3. **Purchase order missing a ship-to address**
   - Process: Logistics cannot fulfill order without destination
   - Impact: Order cannot be confirmed or shipped
   - Blocking: YES — transaction halts

4. **Vendor missing a payment method**
   - Process: Accounts Payable cannot process invoice payment
   - Impact: Supplier is not paid; relationship at risk
   - Blocking: YES — transaction halts

**The misconception:** Completeness is not "always tolerable." The difference is:
- **Tolerable Completeness gaps:** missing optional comments, secondary descriptions, non-blocking fields
- **Intolerable Completeness gaps:** missing required values like keys, credit limits, ship-to addresses, payment methods — these block transactions just like Accuracy or Integrity defects

**The real pattern:** Dimension priority depends on business impact, not on the dimension itself. Ask the business which missing values block their critical processes.

See [[con-dq-dimensions|The Seven DQ Dimensions]] and [[qa-dimension-priority-business-dependent|Are Accuracy and Integrity always higher priority?]] for how business context shapes dimension criticality.
