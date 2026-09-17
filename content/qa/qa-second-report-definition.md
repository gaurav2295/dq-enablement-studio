---
id: qa-second-report-definition
type: qa
title: What is meant by "second report" in OptSel/RptSel?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-optsel-select-structure
  - relates:prn-optsel-is-the-universe
---

## Question

What is meant by 'second report' in this context? Does it refer to a second Report view built under the same Opportunity view? or is it any view that derives its data from an existing DQ view rather than directly from source tables?

## Answer

**Any view that derives from a DQ rule view rather than directly from source tables.**

**Examples:**

| Pattern | Name | Allowed? |
|---|---|---|
| OptSel → RptSel | Standard pair | ✅ Yes, canonical |
| OptSel → Custom filter view | "Second report" | ❌ No, violates standard |
| RptSel → Another view (e.g., aggregation) | Chained derivation | ❌ No, violates standard |
| Source table → OptSel → RptSel | Canonical chain | ✅ Yes, correct |
| Source table → OptSel → Custom aggregate | Chained derivation | ❌ No, second report violation |

**Why it's forbidden:**

Once you've derived an OptSel from sources, any further derivation must stop. Creating a view that reads from OptSel and adds additional filters, aggregations, or transformations is a "second report" and breaks the contract:

- OptSel is the **definitive universe** — all candidates, fully auditable
- RptSel is the **definitive defect list** — errors only, filtered from OptSel
- Any view built on top of these is adding **unauthorized filtering or aggregation**

**Real scenario:**

```sql
-- CORRECT: OptSel + RptSel pair
CREATE VIEW DQ_0042_OptSel AS
SELECT * FROM MARA WHERE zSourceSystemID = 'Z01' ...;

CREATE VIEW DQ_0042_RptSel AS
SELECT * FROM DQ_0042_OptSel WHERE zIsErrorFlag = 1;

-- WRONG: "second report" — deriving from RptSel
CREATE VIEW DQ_0042_High_Value_Errors AS
SELECT * FROM DQ_0042_RptSel 
WHERE MARA.NETWR > 10000;  -- unauthorized secondary filter
```

The "High_Value_Errors" view is a second report — it re-filters the defects, making the defect count no longer reconcile to the OptSel. Audit breaks.

**The rule:** One rule = one OptSel, one RptSel, no more. If you need aggregations or secondary filters, create a new rule.

## Related

- [[std-optsel-select-structure|OptSel SELECT Structure]]
- [[prn-optsel-is-the-universe|Why OptSel Is the Universe and RptSel Is the Wrapper]]
