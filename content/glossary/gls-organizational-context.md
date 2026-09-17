---
id: gls-organizational-context
type: glossary
title: Organizational Context
domain: sql-standards
audience: [consultant]
level: foundation
status: review
links:
  - parent:std-output-field-sections
  - relates:gls-field-classification
  - relates:gls-value-context
  - relates:gls-org-vs-central
sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/ai_enhance_instructions.md
tags: [sections, output-fields]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The third [[std-output-field-sections|output field section]]: the **structural and hierarchical**
columns that scope a record — company code (`BUKRS`), plant (`WERKS`), cost centre (`KOSTL`),
division (`SPART`), sales organisation, purchasing organisation, business area.

## The One Question

*"WHERE in the org does this record belong?"* — the organizational boundaries that define which remediator has authority over this record.

> [!warning]
> Putting an organisational field in [[gls-value-context|Value Context]] is the single most common
> miscategorisation. A plant, a company code and a sales org are *where*, never *how much*.

## Example: Material Master Rule

Consider a rule on SAP materials checking for missing base units of measure:

```sql
SELECT
  -- Identity: material + system
  MaterialID,
  zSourceSystemID,
  
  -- Classification: material type, category
  MaterialType,
  MaterialCategory,
  
  -- Organizational Context: WHERE in the org?
  Plant,                    -- Physical location of material
  CompanyCode,              -- Legal entity owning the material
  SalesOrganization,        -- Sales org responsible for distribution
  PurchasingOrganization,   -- Procurement org responsible
  DivisionCode,             -- Strategic division (product line)
  CostCenter,               -- Cost allocation center
  
  -- Activity Context: when did this happen?
  ERDAT AS created_date,
  AEDAT AS last_change_date,
  
  -- Subject: the data under test
  BaseUnitOfMeasure,
  
  -- Value Context: monetary values if any
  StandardPrice,
  Currency,
  
  -- Outcome: did the rule find a defect?
  CASE
    WHEN BaseUnitOfMeasure IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM Materials_Stage
WHERE zSourceSystemID = 'SAP';
```

### What Goes IN Organizational Context

- **SAP Organizational Units:** `BUKRS` (company code), `WERKS` (plant), `LGORT` (storage location)
- **Sales & Distribution:** `VKORG` (sales org), `VTWEG` (distribution channel), `SPART` (division)
- **Procurement:** `EKORG` (purchasing org), `EKGRP` (buyer group)
- **Accounting:** `KOSTL` (cost center), `PRCTR` (profit center)
- **Hierarchies:** `DivisionCode`, `RegionCode`, `BusinessUnit`

### What Does NOT Go Here

- **Monetary:** `StandardPrice`, `Amount` → Value Context
- **Temporal:** `CreatedDate`, `LastChangeDate` → Activity Context
- **Classification/Type:** `MaterialType`, `MaterialCategory` → Classification section
- **Identity:** `MaterialID`, `CustomerID` → Identity section
