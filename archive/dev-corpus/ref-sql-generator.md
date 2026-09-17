---
id: ref-sql-generator
type: reference
title: SQL Generator (OptSel/RptSel skeleton)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - prereq:ref-dqrulespec-data-model
  - implements:prn-optsel-is-the-universe
  - implements:std-optsel-select-structure
  - implements:std-output-field-sections
  - relates:ref-sql-parser
  - relates:ref-generate-sql-dispatcher
  - relates:ref-view-name-token-resolution
  - relates:ref-three-database-architecture
sources:
  - vault:studio-architecture/Studio — SQL Generator (OptSel-RptSel skeleton).md
tags: [studio, engine, sql, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`generate_optsel` builds the MS SQL Server `CREATE VIEW` skeleton — a section-commented
`SELECT` over `WRKDQ` (the one rule repository, never raw source), assembled with JOINs /
WHERE / GROUP BY — and `generate_rptsel` wraps it with the canonical
`SELECT * FROM <OptSel> WHERE [zIsErrorFlag] = 1`.

These two functions are the structural backbone of every Error rule's SQL. They turn a
[[ref-dqrulespec-data-model|DQRuleSpec]] into deployable views; the per-field expressions,
key, flag CASE, and name tokens are produced by collaborator builders (linked below). This
unit covers only the **view skeleton** and the **RptSel wrapper**.

## What it does

`generate_optsel(spec, arch, view_name)` emits:

```sql
-- ============================================================
-- DQ Rule: <rule_name>
-- Rule ID:  <rule_id>
-- View:     Opportunity Report (OptSel) (<view_name>)
-- Generated: <UTC ISO8601>
-- Target: MS SQL Server
-- ============================================================
CREATE VIEW [dbo].[<view_name>] AS
SELECT
    -- Syniti Technical Fields
    '<sys>' AS [zSourceSystemID],
    CONCAT(...) AS [zConcatenatedKey],
    CASE WHEN <error> THEN 1 ELSE 0 END AS [zIsErrorFlag],
    -- Basic Fields
    MARA.MATNR AS [Material Number],
    ...
FROM [WRKDQ].[dbo].[MARA] AS MARA
<JOINs>
<WHERE>
<GROUP BY if any aggregation>
;
```

`generate_rptsel(spec, arch, optsel_name, rptsel_name)` emits the wrapper only:

```sql
CREATE VIEW [dbo].[<RptSel name>] AS
SELECT
    *
FROM [dbo].[<OptSel name>]
WHERE [zIsErrorFlag] = 1
;
```

## Key conventions (do / don't)

- **FROM `WRKDQ`, NEVER raw source.** Rule views are CREATED in AND SELECT FROM `WRKDQ` —
  the one rule repository (a same-DB read, not cross-database). The upstream
  `WRKDQPREP_ALL` prep layer applies relevancy / merge / aggregation / scope and PUSHES its
  output into `WRKDQ`; rules do NOT read it directly. Rules never read raw `SRCECC_DA`. (The
  app now reads Error/Info rule views FROM `WRKDQ` — matching profiling — with
  `WRKDQPREP_ALL` treated as upstream ETL only; KNOWN-ISSUES B4, fixed 2026-07-01.) See
  [[ref-three-database-architecture]].
- **View names are 2-part, base tables are 3-part.** `CREATE VIEW [dbo].[<view>]` (and the
  RptSel `FROM [dbo].[<OptSel>]`) is two-part — `_qualify` deliberately ignores the db
  prefix because SQL Server rejects 3-part `CREATE VIEW` names and the deploy script issues
  `USE <working_db>`. Base SAP tables in OptSel FROM/JOIN keep the db:
  `[WRKDQ].[dbo].[MARA]`. See [[ref-view-vs-table-qualification]].
- **Five SELECT sections, fixed order, each comment-prefixed.**
  `_SECTION_ORDER = [TECH, BASIC, ORG, VALUE, ACTIVITY]` → `-- Syniti Technical Fields`,
  `-- Basic Fields`, `-- Organizational Context`, `-- Value Context`, `-- Activity Context`.
  Empty groups are skipped. These comments are load-bearing — the
  [[ref-sql-parser|SQL parser]] routes on them. See
  [[ref-sql-comment-and-formatting-standard]].
- **The FROM table is aliased to its own uppercased name**
  (`FROM [..].[dbo].[MARA] AS MARA`). Main table = first join's source, else first
  `TABLE.FIELD` in output. No main table → `FROM /* TBD */`; no select parts → bare `*`.
- **GROUP BY only when something aggregates.** Emitted only if any output field has an
  aggregation, grouping by every non-aggregated `table_field`.
- **OptSel = the universe; RptSel = the filtered view.** OptSel returns ALL candidate rows
  with a per-row `zIsErrorFlag`; the error predicate lives in the **CASE, not the WHERE**
  (WHERE is reserved for system filter + deletion exclusions + scope). RptSel never
  re-queries base tables — it `SELECT *`s over the OptSel.
- **`WHERE [zIsErrorFlag] = 1` is Error-only.** The flag filter is emitted only for
  `rule_type == "error"`; other rule types report the whole universe. Integer comparison
  `= 1` — `1` is always the defect. See
  [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]].

## Collaborators (skeleton calls into)

The skeleton delegates the hard parts; it just assembles them in order.

| Piece | Builder | Note |
|---|---|---|
| View name tokens | `_resolve_system_token` + `resolve_view_name` | [[ref-view-name-token-resolution]] |
| SELECT field exprs | `_build_select_parts` / `_build_field_expr` (`:1284-1345`) | [[ref-output-section-builders]] |
| zConcatenatedKey | `_build_concat_key_expr` | [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] |
| zIsErrorFlag CASE | `_build_logic_case` / `_parse_logic_case` | [[ref-logic-case-predicate-templates]] |
| JOINs | `_build_joins` | (same skeleton module) |
| WHERE | `_build_where` | [[ref-deletion-flag-normalization-in-sql-gen]] |
| Dispatch by rule-type | `generate_sql` → `(primary, secondary)` | [[ref-generate-sql-dispatcher]] |

`_build_select_parts` (`:1284-1308`) is where the section comments are interleaved with
field expressions and where the `zIsErrorFlag` element gets its CASE swapped in (alias
rewritten to `AS [zIsErrorFlag]` via regex).

## Inputs & outputs

| | |
|---|---|
| **Input** | a `DQRuleSpec` (output_fields grouped by section, logic, joins, filters) + an [[ref-architecture-context-and-project-yamls\|ArchitectureContext]] (supplies `prep_db`, `working_db`, system aliases, view-name patterns) + the resolved view name(s) |
| **Output** | two SQL strings — OptSel (primary → `spec.sql_optsel`) and RptSel (secondary → `spec.sql_rptsel`). Info/Profiling rules take different branches via the [[ref-generate-sql-dispatcher]] (InfSel; PrfSel/PrfSum) |

> [!success] Implementation status — resolved 2026-07-01 (KNOWN-ISSUES B1–B15)
> The shipped skeleton implements the canonical behaviour on every item below (all
> KNOWN-ISSUES items B1–B15 shipped 2026-07-01):
> - **B2** — Error/Info view names now include `{system}` (the production system alias,
>   e.g. PD1 — never the interim QA system). The YAML resolver defaults were aligned to the
>   dataclass so there is one canonical view-name pattern set with `{system}` present on
>   OptSel/RptSel/InfSel.
> - **B4** — canonical FROM is **`WRKDQ`** (the one rule repository; rules are created in
>   AND read from it as a same-DB read). The app now reads Error/Info rule views FROM/JOIN
>   `WRKDQ` — matching profiling — with `WRKDQPREP_ALL` treated as upstream ETL only that
>   pushes its output INTO `WRKDQ`, never the rule SELECT-FROM target. The architecture
>   diagram remains the single source of truth for the layer topology.
> - **B6** — the `{desc}` token (Title_Case slug, ≤50 chars) is now part of the canonical
>   view-name pattern: `DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}`, so it reaches
>   the assembled name.

## Source

- `core/sql_generator.py:169-251` — `generate_optsel` (skeleton) + `generate_rptsel`
  (canonical wrapper).
- `core/sql_generator.py:1284-1308` — `_build_select_parts` (section comments + field exprs
  + zIsErrorFlag CASE swap).
- Supporting: `_sql_header` (`:1260`), `_qualify` / `_qualified_table` (`:2110-2135`),
  `_build_group_by` (`:1513`), `generate_sql` dispatcher (`:132-166`).
- Detail: `knowledge-mining/sql-generation.md` §2, §5.1, §6, §14.

## Related

[[ref-generate-sql-dispatcher]] · [[ref-view-name-token-resolution]] ·
[[ref-logic-case-predicate-templates]] · [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] ·
[[ref-output-section-builders]] · [[ref-view-vs-table-qualification]] ·
[[ref-sql-comment-and-formatting-standard]] · [[ref-profiling-view-generation]] ·
[[ref-local-deriver]] · [[ref-catalog-promotion]] · [[prn-catalog-promotion-wraps-instead-of-injecting]]
