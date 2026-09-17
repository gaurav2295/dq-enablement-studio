---
id: gls-activity-context
type: glossary
title: Activity Context
domain: sql-standards
audience: [consultant]
level: foundation
status: review
links:
  - parent:std-output-field-sections
  - relates:gls-field-classification
  - relates:gls-value-context
sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/ai_enhance_instructions.md
tags: [sections, output-fields]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The fifth [[std-output-field-sections|output field section]]: **dates and times only** — creation
date (`ERDAT`, `ERSDA`), change date (`LAEDA`, `AEDAT`), posting and document dates, validity
dates, last-activity timestamps and frequency counters.

## The One Question

*"WHEN did this happen?"* — the temporal context a remediator needs to judge whether a record is stale, dormant or newly broken.

**Never monetary values. Never organisational fields.** A checked date belongs here even though it is the field under check ([[gls-field-classification]], CONFLICT-008). Rules whose *logic* is temporal are a separate matter — see [[con-time-based-filters]].

## Example: Customer Master Record Check

Consider a rule on SAP customer master data checking for missing customer names:

```sql
SELECT
  -- Identity: customer ID + system
  CustomerID,
  zSourceSystemID,
  
  -- Classification: customer type (e.g., Vendor vs. Reseller)
  CustomerType,
  
  -- Context: business location (e.g., APAC vs. EMEA)
  Region,
  
  -- Subject: the data under test
  CustomerName,
  
  -- Activity Context: WHEN did this happen?
  ERDAT AS created_date,      -- Date customer master record was created
  AEDAT AS last_change_date,  -- Most recent modification
  LODAT AS last_order_date,   -- When was last purchase transaction
  INDATE AS inactive_date,    -- If marked inactive, when was that
  
  -- Outcome: did the rule find a defect?
  CASE
    WHEN CustomerName IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM Customers_Stage
WHERE zSourceSystemID = 'SAP';
```

### What Goes IN Activity Context

- Creation / last-modified timestamps: `ERDAT`, `AEDAT`, `LODAT`, `INDATE`
- Posting dates on transactions: `BUDAT` (posting date), `CPUDT` (creation date)
- Frequency counters: `OrderCount`, `InvoiceCount`, `DayssSinceLastActivity`
- Validity windows: `ValidFromDate`, `ValidToDate`

### What Does NOT Go Here

- **Identity / classification fields:** `CustomerType`, `Region`, `Department` → those go in Context
- **Monetary fields:** `TotalSalesAmount`, `OutstandingBalance` → would go in Context or elsewhere, never Activity
- **Business attributes:** `CreditRating`, `PaymentTerm` → Context section
- The checked field itself (Subject): Only if the rule logic is *inherently temporal* (e.g., "dates not in order")
