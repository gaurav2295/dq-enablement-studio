---
id: gls-field-classification
type: glossary
title: Field Classification
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-output-field-sections
  - relates:ref-sap-key-fields-and-critical-data-elements
  - relates:gls-basic-fields
  - relates:gls-business-friendly-alias
sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/ai_enhance_instructions.md
tags: [sections, sap, catalog]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The per-field `classification` value carried in the SAP field catalog
(`SAP_ECC_Complete.json`), which maps 1:1 onto the four non-technical
[[std-output-field-sections|output field sections]]:

| `classification` | Section | Purpose | Example Fields |
|---|---|---|---|
| `Basic Field` | Basic Fields | **Who/What** — identity, business keys | `MATNR` (material), `KUNNR` (customer), `VBELN` (sales order) |
| `Organizational Field` | Organizational Context | **Where in the org** — scope and hierarchy | `BUKRS` (company code), `WERKS` (plant), `VKORG` (sales org), `KOSTL` (cost center) |
| `Value Field` | Value Context | **How much** — monetary and quantitative | `NETWR` (net value), `STPRS` (price), `WAERS` (currency), `MENGE` (quantity) |
| `Activity Field` | Activity Context | **When** — dates and timestamps | `ERDAT` (creation date), `AEDAT` (change date), `BUDAT` (posting date), `CPUDT` (creation timestamp) |

## Example: Material Master (MARA) Structure

```sql
-- Material rule showing field classifications in output sections
SELECT
  -- Identity Section: Basic Fields
  MARA.MATNR AS MaterialID,
  MARA.MTART AS MaterialType,              -- Basic: classification type
  
  -- Context Section: Organizational Fields
  MARA.WERKS AS Plant,                     -- Organizational: where material is managed
  MARA.BUKRS AS CompanyCode,               -- Organizational: legal entity
  
  -- Value Context Section: Value Fields
  MARA.VERPR AS StandardPrice,             -- Value: monetary amount
  MARA.WAERS AS Currency,                  -- Value: currency code
  MARA.MEINS AS BaseUnitOfMeasure,         -- Value: unit/quantity unit (quantitative)
  
  -- Activity Context Section: Activity Fields
  MARA.ERDAT AS CreatedDate,               -- Activity: when record was created
  MARA.AEDAT AS LastChangedDate,           -- Activity: when last modified
  MARA.LAEDA AS LastReadDate,              -- Activity: when last accessed
  
  -- Technical Fields (system-owned)
  MARA.zSourceSystemID,
  MARA.zConcatenatedKey,
  
  -- Rule outcome
  CASE
    WHEN MARA.MEINS IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM MARA_Stage AS MARA
WHERE MARA.zSourceSystemID = 'SAP';
```

## Usage

This is why section membership is **looked up, not argued about**. Where a consultant's judgement
disagrees with the catalog classification, the catalog wins — it is a lookup, not an argument. For
tables absent from the catalog, classify from domain knowledge using the same four buckets.

### Classification Rules

1. **Identity (Basic Fields)** — Ask: "Who or what is this about?" (The row's subject)
2. **Context (Organizational + Classification)** — Ask: "Where/how is this organized?" (Scope and type)
3. **Value** — Ask: "How much? In what currency?" (Only monetary/quantitative amounts)
4. **Activity** — Ask: "When did this happen?" (Temporal context)
