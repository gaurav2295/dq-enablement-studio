---
id: qa-zdomainsegment-example-impact
type: qa
title: What is zDomainSegment with an example and impact?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:gls-zdomainsegment
created: 2026-09-03
updated: 2026-09-03
links:
  - parent:gls-zdomainsegment
  - relates:std-output-field-sections
  - relates:gls-syniti-technical-fields
---

## Question

From the definition, it looks like the account group or material type fields are being referenced but the explanation and significance is not very clear. Can we get an example along with the impact?

## Answer

**zDomainSegment is a classification column** that categorizes master records (Customers, Vendors, Materials) by their business type/group for segmentation in your DQ rule output.

### What It Is

zDomainSegment captures the **classification field** from SAP master tables:

| Master Domain | Table | Classification Field | zDomainSegment Captures |
|---|---|---|---|
| **Customer** | KNA1 | KTOKD (Customer Account Group) | "01" = Regular customer, "02" = One-time customer, etc. |
| **Vendor** | LFA1 | KTOKK (Vendor Account Group) | "01" = Supplier, "02" = Employee, etc. |
| **Material** | MARA | MTART (Material Type) | "FERT" = Finished good, "HALB" = Semi-finished, "RAWM" = Raw material |

### Example with Impact

**Scenario:** You're creating a rule to check **Customer address completeness**.

```sql
-- Your DQ Rule
SELECT
  kna1.zSourceSystemID,
  kna1.zConcatenatedKey,
  kna1.zDomainSegment,  -- ← Added by Studio
  kna1.KUNNR AS customer_id,
  kna1.KTOKD AS account_group,
  CASE
    WHEN kna1.ORT01 IS NULL OR LTRIM(kna1.ORT01) = '' THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM MARA AS kna1
WHERE kna1.zSourceSystemID = 'SRCECC02100'
```

**Impact of zDomainSegment:**

When you audit this rule, zDomainSegment lets you **segment defects by customer type**:

```
CUSTOMER COMPLETENESS AUDIT RESULTS
────────────────────────────────────
zDomainSegment | Defect Count | Impact
─────────────────────────────────────
01 (Regular)   |     45       | High — affects order fulfillment
02 (One-time)  |      3       | Low — no recurring impact
03 (Internal)  |      1       | None — internal testing accounts
```

**Why it matters:**
- You can **prioritize fixes** (fix Regular customers first)
- You can **skip irrelevant segments** (ignore Internal for production)
- You can **calculate business impact** ("45 regular customers missing address = $X in delayed shipments")

### How It's Used in Rules

**Rules using zDomainSegment:**
1. Always include it in the **Technical Fields section** of the output
2. It's a **plain table reference** — no JOIN, no CASE logic
3. It's **never part of the error condition** (error flag logic) — it just classifies which records have defects

**Example usage:**
```sql
-- ✅ CORRECT — Just reference the column
SELECT
  ...,
  kna1.zDomainSegment,  -- Classification, not error logic
  ...
FROM kna1
```

```sql
-- ❌ WRONG — Never CASE on it or JOIN to look it up
SELECT
  ...,
  CASE WHEN kna1.KTOKD = '01' THEN 'Regular' ELSE 'Other' END AS zDomainSegment
FROM kna1
```

### Real-World Impact Example

**Before zDomainSegment:** "We found 500 customer defects"  
→ Ambiguous priority, need to manually sort

**With zDomainSegment:** 
- 400 Regular customers (urgent, revenue impact)
- 90 One-time customers (low priority, no recurring impact)
- 10 Internal customers (skip, test data)  
→ Clear prioritization: fix the 400 first

---

### Related

- [[gls-zdomainsegment|zDomainSegment]]
- [[gls-syniti-technical-fields|Syniti Technical Fields]]
- [[std-output-field-sections|Output Field Sections]]
