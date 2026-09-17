---
id: std-optsel-select-structure
type: standard
title: OptSel SELECT Structure
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - vault:templates/OptSel SELECT Structure.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
  - dq-studio:knowledge/methodology/view_conventions.json
tags: [template, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - implements:gls-optsel
  - relates:prn-optsel-is-the-universe
  - relates:std-output-field-sections
  - relates:std-sql-comment-standards
  - relates:std-zsourcesystemid-convention
  - relates:std-zconcatenatedkey-convention
  - relates:std-ziserrorflag-convention
  - relates:con-view-types
  - relates:gls-organizational-context
---

## What it is

The canonical skeleton for an Error or Info rule's OptSel view. Drop-in template; substitute
placeholders for the rule's specifics.

## The two-view contract

Each Error rule generates **exactly two views** — no more, no fewer:

| View | Suffix | Purpose | Reads from |
|---|---|---|---|
| Opportunity View | `_OptSel` | Defines the complete population under analysis and identifies defective records within it | The SAP tables directly |
| Report View | `_RptSel` | Displays only defective records | The Opportunity View only |

Every Opportunity View must carry `zConcatenatedKey` and `zIsErrorFlag`, and must read directly
from source tables — an OptSel that selects from another DQ view is not an opportunity view, it is
a second report.

The generator's own contract restates this: OptSel `selects_from: source_tables`, contains joins,
filters and a logic `CASE`, and always includes the error flag, the concat key and the source
system ID; RptSel `selects_from: optsel_view`, selects all columns, filters errors only. Both are
created in the working database.

## The skeleton

```sql
-- ============================================================
-- DQ Rule: <Rule name>
-- Rule ID: <NNNN>
-- View:    Opportunity Report (OptSel) (<view_name>)
-- Generated: <timestamp>
-- Target: MS SQL Server
-- ============================================================

CREATE VIEW [dbo].[<view_name>] AS
SELECT
    -- Syniti Technical Fields
    <PrimaryAlias>.zSourceSystemID AS [zSourceSystemID],
    CONCAT(<PrimaryAlias>.zSourceSystemID, '_', <PrimaryAlias>.<PK1>, '_', <PrimaryAlias>.<PK2>, ...) AS [zConcatenatedKey],
    CASE
        /* <Error condition explanation> */
        WHEN <error_condition>
            THEN 1
        ELSE 0
    END AS [zIsErrorFlag],
    <PrimaryAlias>.zDomainSegment AS [zDomainSegment],

    -- Basic Fields
    <PrimaryAlias>.<PK> AS [<Business Label>],
    <DescriptionAlias>.<DescField> AS [<Business Label>],

    -- Organizational Context
    <OrgAlias>.<OrgField> AS [<Business Label>],

    -- Value Context
    <ValueAlias>.<AmountOrCurrencyField> AS [<Business Label>],

    -- Activity Context
    <PrimaryAlias>.ERSDA AS [Created On],
    <PrimaryAlias>.LAEDA AS [Last Changed]

FROM [WRKDQ].[dbo].[<PrimaryTable>] AS <PrimaryAlias>

LEFT OUTER JOIN [WRKDQ].[dbo].[<DescriptionTable>] AS <DescAlias>
    ON <DescAlias>.<key> = <PrimaryAlias>.<key>
    AND <DescAlias>.SPRAS = 'E'
    AND <DescAlias>.zSourceSystemID = <PrimaryAlias>.zSourceSystemID
    /* English description for output readability */

LEFT OUTER JOIN <OrgTable> AS <OrgAlias>
    ON <OrgAlias>.<key> = <PrimaryAlias>.<key>
    AND <OrgAlias>.zSourceSystemID = <PrimaryAlias>.zSourceSystemID
    /* Organizational context for the row */

WHERE
    /* Exclude: records flagged for deletion */
    <PrimaryAlias>.LVORM <> 'X'

    AND /* Include: Limit to source system <alias> */
    <PrimaryAlias>.zSourceSystemID = '<system_code>'

    AND /* Include: <additional scope constraint> */
    <additional_filter>
;

GO
```

## A concrete example — material UoM rule, P02 implementation

```sql
-- ============================================================
-- DQ Rule: A material must have a valid base unit of measure
-- Rule ID: 0042
-- View:    Opportunity Report (OptSel) (DQ_0042_P02_MARA_MEINS_OptSel)
-- Generated: 2026-06-05T10:00:00
-- Target: MS SQL Server
-- ============================================================

CREATE VIEW [dbo].[DQ_0042_P02_MARA_MEINS_OptSel] AS
SELECT
    -- Syniti Technical Fields
    MARA.zSourceSystemID AS [zSourceSystemID],
    CONCAT(MARA.zSourceSystemID, '_', MARA.MATNR) AS [zConcatenatedKey],
    CASE
        /* Material missing a base unit of measure (required for all FERT
           materials so planning + costing modules can compute). */
        WHEN MARA.MEINS IS NULL OR MARA.MEINS = ''
            THEN 1
        ELSE 0
    END AS [zIsErrorFlag],
    MARA.zDomainSegment AS [zDomainSegment],

    -- Basic Fields
    MARA.MATNR AS [Material Number],
    MAKT.MAKTX AS [Material Description],
    MARA.MTART AS [Material Type],
    MARA.MEINS AS [Base UoM],

    -- Organizational Context

    -- Value Context

    -- Activity Context
    MARA.ERSDA AS [Created On],
    MARA.LAEDA AS [Last Changed]

FROM [WRKDQ].[dbo].[MARA] AS MARA

LEFT OUTER JOIN [WRKDQ].[dbo].[MAKT] AS MAKT
    ON MAKT.MATNR = MARA.MATNR
    AND MAKT.SPRAS = 'E'
    AND MAKT.zSourceSystemID = MARA.zSourceSystemID
    /* English description for the report */

WHERE
    /* Exclude: records flagged for deletion */
    MARA.LVORM <> 'X'

    AND /* Include: Limit to source system P02 */
    MARA.zSourceSystemID = 'SRCECCZ02100'

    AND /* Include: Limit to finished + semi-finished + raw materials */
    MARA.MTART IN ('FERT', 'HALB', 'ROH')
;

GO
```

> [!note] The checked field does not live in Value Context
> `MEINS` (Base UoM) is the field under check, yet it appears in **Basic Fields**, not Value Context. 
> This is correct: section placement is determined by what type of field it is (identifier, money, date, 
> organizational), never by whether the rule happens to be checking it. A base unit of measure 
> identifies a material record, so it belongs in Basic Fields. Empty sections (Organizational Context 
> and Value Context here) carry comment headers anyway — "reviewed, none applicable" rather than 
> "forgot to think about it". See [[std-output-field-sections]] for the classification rules.

## The companion RptSel

```sql
CREATE VIEW [dbo].[DQ_0042_P02_MARA_MEINS_RptSel] AS
SELECT *
FROM [dbo].[DQ_0042_P02_MARA_MEINS_OptSel]
WHERE [zIsErrorFlag] = 1
;

GO
```

That's it. RptSel is always this exact wrapper — no logic, no formatting changes, just
`SELECT * FROM OptSel WHERE [zIsErrorFlag] = 1`.

Two rules make the wrapper enforceable:

- **It must read only from the Opportunity View** — never directly from SAP tables. A RptSel that
  re-reads source tables can drift out of step with its OptSel and produce a defect count that no
  longer reconciles to the opportunity count.
- **`WHERE zIsErrorFlag = 1` is the only permitted filter.** Any additional predicate on RptSel
  silently shrinks the defect set relative to the flag the OptSel published, so the two views stop
  agreeing.

Both are checked by the Studio at export.

## Questions from consultants

- [[qa-optsel-rptsel-automated-validation|Which OptSel/RptSel requirements are validated automatically?]]
- [[qa-second-report-definition|What is meant by "second report"?]]

## Related

- [[std-output-field-sections|Output Field Sections]]
- [[std-sql-comment-standards|SQL Comment Standards]]
- [[std-zsourcesystemid-convention|zSourceSystemID Convention]]
- [[std-zconcatenatedkey-convention|zConcatenatedKey Convention]]
- [[std-ziserrorflag-convention|zIsErrorFlag Convention]]
- [[con-view-types|View Types — OptSel RptSel InfSel PrfSel PrfSum]]
