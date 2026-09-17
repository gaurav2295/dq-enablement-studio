---
id: ref-sql-comment-and-formatting-standard
type: reference
title: SQL Comment & Formatting Standard (as implemented)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - implements:prn-sql-comments-must-match-local-derive-quality
  - implements:std-sql-comment-standards
  - relates:ref-catalog-promotion
  - relates:ref-sql-generator
  - relates:ref-sql-parser
  - relates:ref-sql-validator
  - relates:ref-deletion-flag-normalization-in-sql-gen
  - relates:ref-dqrulespec-data-model
  - contrast:std-output-field-sections
sources:
  - vault:studio-architecture/Studio — SQL Comment & Formatting Standard (as implemented).md
tags: [studio, engine, sql, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

Every generated view carries a fixed `=== ` header block (which the SQL parser routes on),
`-- <Section>` comments before each SELECT group, `/* Include: */` and `/* Exclude: */`
comments before every WHERE predicate, JOIN/CASE comments, and commas placed AFTER field lines
only — the formatting is load-bearing, not cosmetic.

These conventions exist so AI-derived SQL reads exactly like locally-derived SQL (see
[[prn-sql-comments-must-match-local-derive-quality]]) AND so the round-trip [[ref-sql-parser]]
can reverse a generated view back into a [[ref-dqrulespec-data-model]]. Break the format and the
parser stops recognising blocks.

## What it does

The generator emits comments at five levels of the view. Target dialect is MS SQL Server
throughout.

### Header block (parser-load-bearing)

`_sql_header` emits a fixed six-line banner wrapped in 60-char `=` rules:

```sql
-- ============================================================
-- DQ Rule: <rule_name>
-- Rule ID: <rule_id>
-- View:    <label> (<view_name>)
-- Generated: <UTC ISO8601, %Y-%m-%dT%H:%M:%S>
-- Target: MS SQL Server
-- ============================================================
```

`<label>` is the human view-type tag (`_VIEW_TYPE_LABELS`): OptSel → `Opportunity Report
(OptSel)`, RptSel → `Defects Report (RptSel)`, InfSel → `Information Report (InfSel)`, PrfSel →
`Profiling Report — Detail (PrfSel)`, PrfSum → `Profiling Report — Summary (PrfSum)`.

> [!important] Why the banner format is rigid
> `_split_views` detects view blocks by finding a `-- ={10,}` rule line IMMEDIATELY followed
> (within 200 chars) by a `-- DQ Rule | Rule ID | View` metadata line. The header IS the block
> delimiter. The validator also routes on it: `view-name-rule-id-mismatch` (High) checks that
> `DQ_NNNN_` in the view name equals the `-- Rule ID: NNNN` banner.

### Section comments (SELECT)

Each SELECT field group is prefixed with `-- <Section Label>`, emitted in the fixed order
`[TECH, BASIC, ORG, VALUE, ACTIVITY]`:

```sql
-- Syniti Technical Fields
-- Basic Fields
-- Organizational Context
-- Value Context
-- Activity Context
```

Empty groups are skipped. The parser switches `current_section` on these comments, so they are
mandatory.

### WHERE comments (Include / Exclude)

`_build_where` precedes EVERY predicate with an inline block comment on its own line:

```sql
WHERE
    /* Include: only the QA system */
    src.zSourceSystemID = 'P06'
    /* Exclude: drop records marked for deletion */
    AND ISNULL(MARA.LVORM, '') <> 'X'
```

- Connector is `AND` by default, `OR` when `filter.operator == "OR"`.
- The comment text is the filter description; `Include` for inclusions (scope), `Exclude` for
  exclusions (deletion flags, record removals).
- Dedup key: `<filter_type>:<table>.<field>:<condition>` (uppercased).
- The parser reads the `/* Include | Exclude: */` comment to set `filter_type` + description on
  round-trip — so the comment is data, not decoration.

### JOIN and CASE comments

- `_build_joins`: a join with no key emits `-- TODO: Join key needed for SRC -> TGT` then `ON /*
  TBD */`. Multi-condition ON clauses split on `AND` across lines. (Layer-2/4 views add inline
  `/* TBL → SEG */` join comments.)
- Logic-CASE fallback paths emit `/* Logic: <alias> - <value> */`. The
  [[ref-catalog-promotion|catalog promoter]]'s literal-1 fallback leaves a
  `/* TODO: literal 1 ... */` marker the validator detects (`literal-flag-fallback`, Medium).

### Comma placement (after fields only)

`_join_select_parts` puts commas AFTER field lines, NEVER after section-comment lines, and never
after the last item:

```sql
SELECT
    -- Syniti Technical Fields
    '<sys>' AS [zSourceSystemID],
    CONCAT(...) AS [zConcatenatedKey],
    CASE WHEN <error> THEN 1 ELSE 0 END AS [zIsErrorFlag],
    -- Basic Fields
    MARA.MATNR AS [Material Number]
FROM ...
```

This is the rule that prevents the `trailing-comma-before-from` bug class (regex
`,\s*\n\s*FROM`) the [[ref-sql-validator]] guards as a High-severity syntax check — package #21
once shipped 8 trailing-comma defects before this check existed.

## Inputs & outputs

- **In:** a `DQRuleSpec` (rule_name, rule_id, output_fields grouped by section, joins, filters) +
  resolved view name + view-type.
- **Out:** comment strings interleaved into the OptSel/RptSel/InfSel/PrfSel/PrfSum SQL by the
  [[ref-sql-generator]] skeleton. Layer-2/Layer-4 datastore views use a fuller header style
  (Table / Source(s) / Database / Inclusions / Exclusions / Dependencies; date format `%B %d,
  %Y`).

## Source

- `core/sql_generator.py:1251-1272` — `_VIEW_TYPE_LABELS` + `_sql_header` (header block).
- `core/sql_generator.py:1468-1510` — `_build_where` (Include/Exclude predicate comments).
- `core/sql_generator.py:2138-2152` — `_join_select_parts` (after-field-only comma placement).
- Supporting: `_build_joins` (`:1397-1426`), section comments in `_build_select_parts`
  (`:1284-1287`), parser block detection `_split_views` / `_parse_header`
  (`sql_parser.py:163-221`).
- Detail: `knowledge-mining/sql-generation.md` §7, §2.1, §2.5, §8.

## Related

[[ref-sql-generator]] · [[ref-sql-parser]] · [[ref-sql-validator]] ·
[[ref-output-section-builders]] · [[ref-deletion-flag-normalization-in-sql-gen]] ·
[[ref-logic-case-predicate-templates]] · [[ref-layer-2-layer-4-datastore-views]] ·
[[ref-markdown-exporter-and-round-trip-contract]] ·
[[prn-sql-comments-must-match-local-derive-quality]] · [[ref-dqrulespec-data-model]] ·
[[std-sql-comment-standards]] · [[ref-catalog-promotion]]
