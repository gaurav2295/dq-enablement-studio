---
id: gls-rule-fulfilment-review
type: glossary
title: Rule-Fulfilment Review
domain: ai-enhancement
audience: [consultant, developer]
level: practitioner
status: review
links:
  - parent:gls-ai-enhance
  - relates:std-ai-enhance-scope
  - relates:ref-ai-derive-and-enhance-internals
  - relates:gls-ai-additions
sources:
  - dq-studio:docs/ai_enhance_instructions.md
tags: [ai, review]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The AI call that asks one question first — **does this SQL actually check what the rule name says
it checks?** — and one question second: fix it where it does not.

This is the defect class AI review exists to catch: a rule can be syntactically perfect, pass every
structural check, and still test the wrong condition.

## The Core Questions

1. **Does the SQL fulfil the rule name?** (semantic match)
2. **If not, what's missing?** (gap analysis)
3. **Fix it** (corrected SQL)

## Example: Rule Fulfillment Review

### INPUT: A Rule with a Gap

**Rule Name:** `DQ_0042_SAP_KNA1_CustomerMaster_MissingCurrencyCode`

**Rule Description:** "Flag customers missing a valid currency code"

**Provided SQL (BEFORE):**
```sql
SELECT
  KUNNR AS CustomerID,
  zSourceSystemID,
  LAND1 AS CountryCode,      -- ❌ Wrong field!
  CASE
    WHEN LAND1 IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM KNA1_Stage
WHERE zSourceSystemID = 'SAP';
```

**The Problem:** The rule checks `LAND1` (country code) but the rule name says it should check currency code.

---

### RULE FULFILLMENT REVIEW OUTPUT

```
====== RULE FULFILLMENT REVIEW ======

RULE FULFILLMENT:
  Rule Name: "CustomerMaster_MissingCurrencyCode"
  Intent: Check for missing customer currency codes
  
  Current SQL checks: LAND1 (Country Code) ❌ MISMATCH
  Should check: WAERS (Currency Code per customer) ✅
  
  Finding: Rule name and SQL do not align.
  Severity: HIGH (wrong field entirely, not just edge case)

SQL REVIEW:
  ✅ Syntax: Valid, no errors
  ✅ Structure: Proper OptSel structure (all rows, zIsErrorFlag)
  ✅ Technical fields: zSourceSystemID included
  ❌ Semantic: Checks country, not currency
  ❌ Field match: LAND1 ≠ currency code concept
  
  Issue: Customer master (KNA1) doesn't have WAERS as base field.
  Root cause: Confusion with KNVV (sales view), which has WAERS.
  
  Recommendation: Join KNA1 → KNVV to check WAERS, OR
                   Use centralized currency from TCURR if per-customer currency is expected.

CORRECTED SQL:
```sql
-- Option A: Join to sales view (KNVV) if customer currency is org-dependent
SELECT
  k1.KUNNR AS CustomerID,
  k1.zSourceSystemID,
  kv.VKORG AS SalesOrg,
  kv.WAERS AS CurrencyCode,
  CASE
    WHEN kv.WAERS IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM KNA1_Stage AS k1
LEFT JOIN KNVV_Stage AS kv
  ON k1.KUNNR = kv.KUNNR
  AND k1.zSourceSystemID = kv.zSourceSystemID
WHERE k1.zSourceSystemID = 'SAP'
  AND kv.VKORG = 'SALES_ORG_1';  -- Specify org scope

-- Option B: Use company code currency from company master (T001)
SELECT
  k.KUNNR AS CustomerID,
  k.zSourceSystemID,
  t.WAERS AS CompanyCodeCurrency,
  CASE
    WHEN t.WAERS IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM KNA1_Stage AS k
LEFT JOIN T001_Stage AS t
  ON k.BUKRS = t.BUKRS
  AND k.zSourceSystemID = t.zSourceSystemID
WHERE k.zSourceSystemID = 'SAP';
```

AI ADDITIONS:
  → Consider adding BUKRS (company code) to context section for audit trail
  → Profile WAERS distribution to detect unexpect currency codes
  → Add validation: WAERS must be in valid currency list (TCURC)
  → Document business rule: Is currency per customer or per org?

NOTES:
  • The rule name indicates a specific semantic intent that wasn't realized in SQL
  • Pre-AI structural checks would pass (syntax OK, fields exist, OptSel shape correct)
  • Only semantic review (fulfillment check) catches this mismatch
  • Severity elevated because wrong field could mask real currency issues
  • Recommend clarifying customer currency hierarchy before re-deriving

STRUCTURED METADATA:
  fulfillment_match: FALSE
  semantic_gap: "Checks country, should check currency"
  severity: HIGH
  fix_applied: TRUE
  corrected_sql_count: 2 (two valid options provided)
  requires_clarification: business rule definition (currency scope)
  ai_confidence: HIGH (clear field name mismatch)
```

---

## Response Structure (Fixed Sections)

Every rule fulfillment review response contains these sections in this order:

| Section | Purpose | Example |
|---|---|---|
| **RULE FULFILLMENT** | Semantic match analysis | "Checks LAND1, should check WAERS → MISMATCH" |
| **SQL REVIEW** | Syntax + semantic checks | ✅/❌ marks for syntax, structure, field match |
| **CORRECTED SQL** | Fixed SQL (if needed) | One or more corrected versions |
| [[gls-ai-additions\|**AI ADDITIONS**]] | Enhancement suggestions | Profile, validation, context additions |
| **NOTES** | Context & decisions | Why the gap exists, recommendations |
| **STRUCTURED METADATA** | Machine-readable summary | fulfillment_match, severity, confidence |

**Rule:** Anything outside these sections is dropped, not surfaced.

## Usage

This is the defect class [[gls-ai-enhance|AI review]] exists to catch: a rule can be syntactically perfect, pass every
structural check, and still test the wrong condition. Everything the model touches beyond that is
scope creep, and scope creep is diffed and reported.

### When Fulfillment Mismatches Occur

- **Ambiguous rule name** → "Customer data incomplete" could mean many things
- **Wrong table joined** → Checked KNVV instead of KNA1
- **Wrong field selected** → LAND1 (country) vs WAERS (currency)
- **Wrong condition logic** → IS NOT NULL instead of NOT IN (domain list)
- **Scope misunderstood** → Thought customer-level, but it's org-level
