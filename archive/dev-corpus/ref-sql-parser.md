---
id: ref-sql-parser
type: reference
title: SQL Parser (reverse-engineer specs)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - prereq:ref-sql-generator
  - relates:ref-dqrulespec-data-model
  - relates:ref-sql-comment-and-formatting-standard
  - relates:ref-table-extraction-and-complexity-scoring
  - relates:ref-sql-validator
  - relates:ref-markdown-exporter-and-round-trip-contract
  - relates:gls-round-trip-parse
sources:
  - vault:studio-architecture/Studio — SQL Parser (reverse-engineer specs).md
tags: [studio, engine, sql, sap, methodology]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`core/sql_parser.py` rebuilds a [[ref-dqrulespec-data-model|DQRuleSpec]] from `CREATE VIEW`
SQL using regex — NOT a real SQL parser — because the input is the deterministic format the
Studio's own generator emits; only OptSel blocks produce specs, and RptSel blocks attach to
their OptSel by base-name.

This is the reverse leg of the round-trip: the [[ref-sql-generator|generator]] writes the
view, the parser reads it back. It works ONLY because the generator's header banner,
`-- <Section>` comments, and `/* Include/Exclude: */` predicate comments are load-bearing
data, not decoration (see [[ref-sql-comment-and-formatting-standard]]). Break the format and
the parser stops recognising blocks.

## What it does

1. **Split into view blocks** (`_split_views`, `:163-193`). Finds each block by locating a
   `-- ={10,}` rule line IMMEDIATELY followed (within 200 chars) by a
   `-- DQ Rule | Rule ID | View` metadata line — the
   [[ref-sql-comment-and-formatting-standard|header banner]] IS the delimiter. No headers
   but a `CREATE VIEW` present → the whole text is treated as one block.
2. **Parse the header** (`_parse_header`, `:201-221`) for `-- DQ Rule:`, `-- Rule ID:`, and
   `-- View: (OptSel|RptSel) (<name>)`.
3. **Recover the view name** (`_extract_view_name`, `:224-248`): captures the FINAL
   bracketed identifier in any 1/2/3-part qualified name
   (`CREATE VIEW (?:\[..\].)*\[(name)\] AS`) — handles legacy 3-part and current 2-part
   `[dbo].[name]`.
4. **Route OptSel vs RptSel** (`:100-106`). A block is RptSel if header view-type ==
   `RptSel` OR the view name contains `_RptSel`. RptSel records its source OptSel (via
   `_extract_rptsel_source`, FROM clause), then attaches by base-name (strip `_OptSel`).
   **ONLY OptSel blocks become specs; RptSel SQL is stored on the matching OptSel spec's
   `sql_rptsel`.**
5. **Recover architecture** (`_extract_architecture`, `:310-345`): `working_db` from
   `CREATE VIEW [DB].[dbo]`; `prep_db` from the first non-working-DB
   `FROM/JOIN [DB].[dbo].[table]` qualifier; `source_system` from
   `'<x>' AS [zSourceSystemID]`. `source_db` is NOT recoverable from generated SQL and stays
   empty.
6. **Parse SELECT / JOIN / WHERE** into output fields, joins, logic, and filters (below).
7. **Classify** (`_infer_classification`, `:753-806`).

## Key conventions / algorithm

### Section routing in the SELECT (`_parse_select_fields`, `:411-508`)

Section comments switch `current_section` via `_SECTION_MAP` (`:396-408`), which accepts
BOTH the full labels and the short aliases:

```python
_SECTION_MAP = {
    "syniti technical fields": TECH,   "technical": TECH,   "tech": TECH,
    "basic fields": BASIC,             "basic": BASIC,
    "organizational context": ORG,     "organizational": ORG,  "org": ORG,
    "value context": VALUE,            "value": VALUE,
    "activity context": ACTIVITY,      "activity": ACTIVITY,
}
```

Within a section the parser recognises: multi-line `CASE … END AS [alias]` → output field
**+** a logic entry; paren-balanced `CONCAT(...) AS [alias]` → output field;
`TABLE.FIELD AS [alias]` → field (aggregations `COUNT/SUM/AVG/MIN/MAX` captured); literal
`'x' AS [alias]`; and `/*…*/` / `NULL` placeholders captured by alias.

- **Key heuristic** (`:537`): a field is flagged `key` when its alias is
  `Material/Customer/Vendor Number` or simply contains "Number".

### JOIN and WHERE recovery

- **JOINs** (`_parse_joins`, `:608-654`): regex for `LEFT/INNER/RIGHT/FULL [OUTER] JOIN` /
  `JOIN`; source table inferred from the first ON condition's left prefix.
- **WHERE** (`_parse_where_clause`, `:662-717`): splits on `AND`, reads the
  `/* Include | Exclude: */` comment to set `filter_type` + description.
  `ISNULL(...) <> 'X'` is decoded back into an EXCLUSION with condition `= 'X'`
  (`_extract_filter_condition`, `:720-746`) — the generator's deletion-flag normalisation is
  reversed here.

### Classification (`_infer_classification`, `:753-806`)

- **Domain**: `KnowledgeEngine.get_domain_by_table` when an engine is supplied; otherwise a
  hardcoded SAP ECC `_FALLBACK_MAP` (MARA → Material Master, KNA1 → Customer Master, LFA1 →
  Vendor Master, EKKO/EKPO → Purchase Order, VBAK/VBAP → Sales Order, …).
- **rule_type is ALWAYS set to ERROR.** The header view-type regex only matches
  `OptSel|RptSel` (`:216`) — InfSel/PrfSel/PrfSum are not header-recognised, so the parser
  is an Error-rule round-trip path.
- **system label** = `engine.get_system_label()` or `"SAP ECC"`.

## Inputs & outputs

| | |
|---|---|
| **Input** | a string of one-or-more generated `CREATE VIEW` blocks; optional `KnowledgeEngine` for domain lookup |
| **Output** | a list of [[ref-dqrulespec-data-model\|DQRuleSpec]]s — one per OptSel; each carries its recovered `sql_rptsel`, output fields, joins, filters, logic, and `ArchitectureContext` |
| **Not recoverable** | `source_db` (informational-only, never in generated SQL); InfSel/Prf views (not header-matched) |

> [!success] Implementation status — resolved 2026-07-01 (KNOWN-ISSUES B10)
> `CLAUDE.md` correctly documents the Studio app shell as **FastAPI + Jinja** (`app.py` +
> `ui/templates/*.html`), not Streamlit — relevant when wiring this parser into a paste-SQL
> upload page. The parser itself is framework-agnostic.

> [!success] Implementation status — resolved 2026-07-01 (KNOWN-ISSUES B2)
> Canonical view naming is `DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}` with
> `{system}` = the PRODUCTION system ID (e.g. PD1). The parser routes on `{id}` and the
> `-- Rule ID:` banner (which must agree), so base-name attachment and id-routing are robust
> to the `{system}` slot. The app uses one canonical view-name pattern: the YAML resolver
> defaults were aligned to the dataclass so `{system}` is consistently present across
> OptSel/RptSel on every build path. See [[ref-view-name-token-resolution]].

## Source

- `core/sql_parser.py:71-345` — block split, header parse, view-name + architecture
  recovery, OptSel/RptSel routing.
- `core/sql_parser.py:396-408` — `_SECTION_MAP` (full-label + short-alias section routing).
- Detail: `knowledge-mining/sql-generation.md` §8.

## Related

[[ref-sql-generator]] · [[ref-generate-sql-dispatcher]] ·
[[ref-sql-comment-and-formatting-standard]] · [[ref-table-extraction-and-complexity-scoring]] ·
[[ref-sql-validator]] · [[ref-view-name-token-resolution]] ·
[[ref-deletion-flag-normalization-in-sql-gen]] · [[ref-output-section-builders]] ·
[[ref-dqrulespec-data-model]] · [[ref-markdown-exporter-and-round-trip-contract]] ·
[[ref-architecture-context-and-project-yamls]]
