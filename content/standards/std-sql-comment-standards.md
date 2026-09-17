---
id: std-sql-comment-standards
type: standard
title: SQL Comment Standards
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: approved
sources:
  - vault:templates/SQL Comment Standards.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
  - dq-studio:.claude/skills_canonical/studio-sql-quality.md
tags: [template, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:std-output-field-sections
  - relates:std-ziserrorflag-convention
  - relates:std-implication-template
  - relates:std-optsel-select-structure

  - relates:prn-deletion-flags-belong-in-where
  - relates:std-view-naming-patterns
  - relates:gls-business-friendly-alias
---

## What it is

What every DQ rule's SQL must explain — in comments — so a reviewer with no SAP background can
understand the rule by reading the SQL alone.

## The mandatory comment layers

### 1. Banner header

Every CREATE VIEW starts with this block:

```sql
-- ============================================================
-- DQ Rule: <Rule name verbatim — exactly as it appears on the tracker>
-- Rule ID: <NNNN>
-- View:    <Role description> (<View name>)
-- Generated: <ISO timestamp>
-- Target: MS SQL Server
-- ============================================================
```

Example:

```sql
-- ============================================================
-- DQ Rule: A material must have a valid base unit of measure
-- Rule ID: 0042
-- View:    Opportunity Report (OptSel) (DQ_0042_P02_MARA_MEINS_OptSel)
-- Generated: 2026-06-01T13:21:56
-- Target: MS SQL Server
-- ============================================================
```

**The four facts the header must carry.** Whatever the banner's visual form, four facts are
mandatory on **every generated view** — the DQ Rule Standards state this as a block comment
opening the file:

```sql
/* ---------------------------------------------------------
Rule Name:
Author:
Creation Date:
View Type:
--------------------------------------------------------- */
```

| Field | What goes in it |
|---|---|
| **Rule Name** | The rule name verbatim, exactly as it appears on the tracker |
| **Author** | Who authored the rule — a person, or the generating tool |
| **Creation Date** | When the view was generated |
| **View Type** | `OptSel` / `RptSel` (or `InfSel` / `PrfSel` / `PrfSum`) |

The Studio checks that exactly these four are present.

> [!note] Two banner forms — block comment vs rule-line banner
> The standards doc specifies the `/* --- ... --- */` block above; the Studio generator emits the
> `-- ====` rule-line banner shown earlier, which additionally carries **Rule ID** and **Target**
> and which the round-trip parser uses as its view-block delimiter. The generator form is a
> superset — Rule Name, Creation Date (as `Generated`) and View Type (inside `View:`) are all
> present, with Author implied by the generating tool. Keep the generator form on Studio-produced
> SQL; the block form is acceptable on hand-authored rules provided all four facts appear.

### 2. Section headers in the SELECT

The 5-section structure from [[std-output-field-sections|Output Field Sections]] — each section
commented even if empty:

```sql
SELECT
    -- Syniti Technical Fields
    MARA.zSourceSystemID, ...

    -- Basic Fields
    MARA.MATNR AS [Material Number],

    -- Organizational Context

    -- Value Context
    MARA.MEINS AS [Base UoM],

    -- Activity Context
    MARA.ERSDA AS [Created On]
FROM ...
```

### 3. JOIN comments

Each JOIN gets a brief description of WHY it's there:

```sql
LEFT OUTER JOIN MAKT
    ON MAKT.MATNR = MARA.MATNR
    AND MAKT.SPRAS = 'E'
    /* English description from MAKT — keeps the report human-readable */
```

For multi-table joins, comment the COMPLETE join structure (a single comment over the JOIN
keyword usually suffices unless the join keys aren't self-evident).

### 4. WHERE-clause filter comments

**Every WHERE condition** gets an inline `/* … */` explanation of WHAT it does AND WHY:

```sql
WHERE
    /* Exclude: records flagged for deletion at MARA level */
    MARA.LVORM <> 'X'

    AND /* Include: Limit to source system P02 */
    MARA.zSourceSystemID = 'SRCECCZ02100'

    AND /* Include: Limit to finished + semi-finished materials */
    MARA.MTART IN ('FERT', 'HALB')
```

Two distinct comment prefixes:

- `/* Exclude: … */` — for filters that remove records from the universe
- `/* Include: … */` — for filters that restrict the universe to a subset

The Studio's exporters auto-emit these via the `filter_type` (INCLUSION / EXCLUSION) on the spec.

### 5. CASE-WHEN comments (Error rules)

The `zIsErrorFlag` CASE carries the rule's defect logic — comment what fails and what passes:

```sql
CASE
    /* Material is missing a base unit of measure — required for all FERT/HALB
       materials so planning + costing modules can compute correctly. */
    WHEN MARA.MEINS IS NULL OR MARA.MEINS = ''
        THEN 1
    ELSE 0
END AS [zIsErrorFlag]
```

For multi-condition CASEs, comment each WHEN branch:

```sql
CASE
    /* Plant-level deletion flag set */
    WHEN MARC.LVORM = 'X' THEN 1
    /* Plant material status blocked (codes 01-03) */
    WHEN MARC.MMSTA IN ('01', '02', '03') THEN 1
    ELSE 0
END AS [zIsErrorFlag]
```

## Field aliases — readable, not technical

Every output column should be aliased with a **business-readable label** in square brackets:

```sql
MARA.MATNR AS [Material Number],
MARA.MEINS AS [Base UoM],
MAKT.MAKTX AS [Material Description],
T001W.NAME1 AS [Plant Name]
```

NOT:

```sql
MARA.MATNR AS [MATNR],
MARA.MEINS AS [MEINS]
```

The technical name is right there on the left of the AS — the alias gives the human label.
Reviewers should be able to read the output without an SAP dictionary at hand.

## The rest of the house style

Comments carry the meaning, but a reviewer's eye also depends on the mechanical conventions being
uniform across every generated view.

### Table aliases and quoting

- Table aliases **match the table name verbatim** — `KNA1 AS KNA1`. Never shorten to `k`. A
  reviewer reading a 40-line SELECT should never have to scroll back to the FROM to decode an
  alias.
- Column aliases use `[Bracketed Title Case]` — `KNA1.KUNNR AS [Customer]`.
- String literals use **single** quotes: `'Z02'`. Double quotes are an *identifier* delimiter in
  SQL Server, so `"Z02"` is a different thing entirely.
- Comments: `--` for a line, `/* */` inline. Don't cross the quoting styles — `'value'` for data,
  `[name]` for identifiers.

### Database qualification — always three-part and bracketed

```sql
[WRKDQ].[dbo].[KNA1] AS KNA1                       -- FROM / JOIN
[WRKDQ].[dbo].[DQ_0042_P02_KNA1_KTOKD_OptSel]      -- CREATE VIEW
```

Both the FROM/JOIN qualifier and the CREATE VIEW qualifier are `working_db` — rules are created in
and read from the one repository. Schema is always `[dbo]`. A bare `FROM KNA1` is a defect, and so
is `FROM [SRCECC_DA].[dbo].[KNA1]` — rules never touch the source ERP database. See
[[qa-rules-never-touch-source-erp|Rules never touch the source ERP system]].

### Rule name constraints (ADM)

- Hard limit **100 characters**; target **85**.
- Preserve SAP acronyms uppercase: PIR, BOM, MRP, PO, SO, GL, AP, AR, UoM, CoA, FI.

## Deletion flags vs status fields — the most common comment-level defect

**Deletion flags** belong in the **WHERE clause as an exclusion**, and nowhere else. **Status fields** are what drives the `zIsErrorFlag` CASE for active/inactive checks. Confusing the two produces dead code.

### Typical deletion indicators by master-data table

| Table | Deletion Flag | Purpose |
|---|---|---|
| MARA | `LVORM` | Material is marked for deletion at plant level |
| KNA1 | `LOEVM` | Customer is marked for deletion |
| LFA1 | `LOEVM` | Vendor is marked for deletion |
| KONP | `LOEKZ` | Condition record is marked for deletion |

All deletion flags should be excluded in the WHERE clause and never checked in the error-condition CASE.

### Examples of correct vs. incorrect patterns

```sql
WHERE ISNULL(MARA.LVORM, '') <> 'X'
CASE
    WHEN MARA.LVORM = 'X' THEN 1   -- DEAD: the WHERE already excluded these rows
    ...
END
```

The CASE branch can never fire, and the comment on it describes a condition the view cannot
produce — which is worse than no comment. Do not duplicate a WHERE condition into the CASE. See
[[prn-deletion-flags-belong-in-where]] and
[[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]].

## Comment defects to check for in review

- A missing section comment, or the five in the wrong order.
- A WHERE condition with no `/* Include: */` or `/* Exclude: */` explanation.
- A JOIN with no relationship comment.
- A `zIsErrorFlag` CASE branch a reviewer cannot map to a business condition — the test is whether
  they can answer *"what counts as an error here?"* without leaving the SQL.
- The same condition in both WHERE and CASE (deletion-flag duplication is the usual offender).
- A bare table name with no database qualifier, or the source DB as the qualifier.
- **`TODO` comments in generated SQL.** The generator must fail loudly rather than emit a
  placeholder; a TODO that reaches a deployed view is a defect that was invited in.
- Commented-out code left in the output.
- Profiling SQL wearing the five-section Error/Info layout — profiling has its own structure and
  the section comments do not apply to it.

## Why this matters

DQ rule SQL is **read by humans during defect remediation** — not by engineers. A defect lands on
a steward's desk with the OptSel row attached; they need to understand *why this is wrong*
without context-switching to a separate documentation tool.

Well-commented SQL also passes the **audit + parity check** with high scores. Sparse-comment
rules drop audit confidence and trigger reconciliation warnings.

## Questions from consultants

- [[qa-what-is-parity-check|What is a parity check?]]
- [[qa-block-comment-vs-rule-line-banner|What's the difference between block comment and rule-line banner?]]
- [[qa-rules-never-touch-source-erp|What does "Rules never touch the source ERP system" mean?]]

## Related

- [[std-output-field-sections|Output Field Sections]]
- [[std-ziserrorflag-convention|zIsErrorFlag Convention]]
- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]]
- [[std-implication-template|Implication Template]]
- Three-Database Architecture
- [[prn-deletion-flags-belong-in-where|Why Deletion Flags Belong in WHERE]]
