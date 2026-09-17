---
id: gls-value-context
type: glossary
title: Value Context
domain: sql-standards
audience: [consultant]
level: foundation
status: review
links:
  - parent:std-output-field-sections
  - relates:gls-field-classification
  - relates:gls-activity-context
  - relates:gls-organizational-context
sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/ai_enhance_instructions.md
tags: [sections, output-fields]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The fourth [[std-output-field-sections|output field section]]: **money only** — amounts
(`NETWR`, `STPRS`, `VERPR`, `DMBTR`), prices, costs, rates, percentages and currencies (`WAERS`).

## The One Question

*"HOW MUCH is this worth?"* — the section exists so the remediator can prioritise by exposure.

**Never dates. Never organisational fields.** An earlier reading of the standard put "the field
under check" here, which sent unit-of-measure and date rules into Value Context; that reading is
superseded — the section is decided by the field's own
[[gls-field-classification|classification]] (CONFLICT-008).

## Example: Sales Order Line Item Rule

Consider a rule on SAP sales order lines checking for missing unit prices:

```sql
SELECT
  -- Identity: order + line + system
  SalesOrderID,
  LineItemNumber,
  zSourceSystemID,
  
  -- Classification: document type, order category
  DocumentType,
  OrderCategory,
  
  -- Context: customer, material, plant
  CustomerID,
  MaterialID,
  Plant,
  
  -- Activity Context: when did this happen?
  ERDAT AS created_date,
  AEDAT AS last_change_date,
  
  -- Subject: the data under test
  UnitPrice,
  
  -- Value Context: HOW MUCH?
  NETWR AS net_amount,        -- Net value of line item
  STPRS AS standard_price,    -- Standard cost price
  VERPR AS proposed_price,    -- Proposed selling price
  WAERS AS currency_code,     -- Currency (e.g., USD, EUR)
  ExchangeRate,               -- Conversion rate if multi-currency
  PercentageDiscount,         -- Discount percentage
  
  -- Outcome: did the rule find a defect?
  CASE
    WHEN UnitPrice IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM SalesOrders_Stage
WHERE zSourceSystemID = 'SAP';
```

### What Goes IN Value Context

- Monetary amounts: `NETWR`, `STPRS`, `VERPR`, `DMBTR`, `AUFWV` (order value)
- Prices: `MMEPR` (minimum price), `PREIS` (price), discounts as amounts
- Costs: material cost, freight, duty
- Rates and percentages when tied to amounts: `ExchangeRate`, `TaxRate`, `DiscountPercent`
- Currency codes: `WAERS`, `FOREX` 

### What Does NOT Go Here

- **Classification:** `DocumentType`, `OrderCategory` → Context section
- **Dates:** `ERDAT`, `AEDAT`, `BUDAT` → Activity Context
- **Identity/Organizational:** `Plant`, `SalesOrg`, `CompanyCode` → Context section
- **Pure count/percentage:** `OrderLineCount`, `Percentage` (unrelated to amount) → Organization Context or elsewhere

> [!note]
> Value Context is a *SQL section*, not a valuation. No SQL the Studio emits ever produces a
> currency figure — see [[prn-value-discipline]].
