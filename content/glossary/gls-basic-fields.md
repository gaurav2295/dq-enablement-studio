---
id: gls-basic-fields
type: glossary
title: Basic Fields
domain: sql-standards
audience: [consultant]
level: foundation
status: review
links:
  - parent:std-output-field-sections
  - relates:gls-field-classification
  - relates:gls-business-friendly-alias
  - relates:gls-syniti-technical-fields
sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/ai_enhance_instructions.md
tags: [sections, output-fields]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The second [[std-output-field-sections|output field section]]: the record's **identification and
descriptive** columns — primary key plus the names, descriptions and type fields that say *which*
record this row is about.

## The One Question

*"WHAT is this record?"* — material number and material description, customer id and customer name, order number and order type.

## Example: Materials by Plant

| SAP Table | Basic Field | Question | Answer |
|---|---|---|---|
| MARA | `MATNR` | "What material?" | "MX-2024-001" |
| MARA | `MAKTX` | "What's its name?" | "Aluminum Bracket" |
| MARA | `MTART` | "What type?" | "Raw material" |
| MARC | `WERKS` | "Which plant?" | "P02_Hamburg" |
| MARC | `LGORT` | "Which storage?" | "01" (Production floor) |
| KNA1 | `KUNNR` | "What customer?" | "CUS-99456" |
| KNA1 | `NAME1` | "What name?" | "ABC Trading GmbH" |

```sql
-- Material master rule with Basic Fields section
SELECT
  -- Basic Fields (Identity + Description)
  MARA.MATNR AS MaterialID,              -- Who/what am I?
  MARA.MAKTX AS MaterialDescription,     -- What am I called?
  MARA.MTART AS MaterialType,            -- What category am I?
  
  -- Classification Fields
  MARA.SPART AS DivisionCode,            -- Which business unit?
  
  -- Organizational Context Fields
  MARC.WERKS AS Plant,                   -- Which plant?
  MARC.LGORT AS StorageLocation,         -- Which storage area?
  
  -- Activity Context Fields
  MARA.ERDAT AS CreatedDate,             -- When was I created?
  MARA.AEDAT AS LastChangedDate,         -- When last modified?
  
  -- Value Context Fields
  MARA.VERPR AS StandardPrice,           -- What's my cost?
  MARA.MEINS AS BaseUnitOfMeasure,       -- What unit?
  
  -- Rule Outcome
  CASE
    WHEN MARA.MAKTX IS NULL OR MARA.MTART IS NULL THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM MARA_Stage AS MARA
LEFT JOIN MARC_Stage AS MARC
  ON MARA.MATNR = MARC.MATNR
  AND MARA.zSourceSystemID = MARC.zSourceSystemID
WHERE MARA.zSourceSystemID = 'SAP';
```

## Usage

The one-question test is *"WHAT is this record?"* — material number and material description,
customer id and customer name, order number and order type.

Membership is a **lookup, not a judgement**: a real SAP column classified `Basic Field` in the
field catalog belongs here ([[gls-field-classification]]). Note the consequence — a checked
material type lands in Basic Fields even though it is the field under check; the section is
decided by what kind of field it is, never by the rule's interest in it (CONFLICT-008).
