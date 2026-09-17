---
id: ref-catalog-deriver
type: reference
title: Catalog Deriver
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - contrast:ref-local-deriver
  - relates:ref-catalog-promotion
  - relates:ref-dqrulespec-data-model
  - relates:ref-sql-parser
  - relates:ref-rule-catalog-structure
  - implements:prn-catalog-promotion-wraps-instead-of-injecting
  - implements:prn-optsel-is-the-universe
sources:
  - vault:studio-architecture/Studio — Catalog Deriver.md
tags: [studio, engine, catalog, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`derive_spec_from_catalog()` builds a [[ref-dqrulespec-data-model|DQRuleSpec]] from a catalog entry
by treating the catalog SQL as the source of truth — it never regenerates SQL. It wraps the catalog
body in a Studio CREATE VIEW, reverse-engineers `output_fields`/`joins`/`filters` back out of that
SQL, resolves table aliases to real SAP names, injects the per-implementation system filter, and
applies methodology restructuring to native Error catalogs too.

The catalog ships **authoritative SQL for ~4,800 Error/Info rules** (Profiling is never in the
catalog). Where the [[ref-local-deriver]] *generates* SQL from a knowledge base, the catalog path
*preserves* hand-authored SQL and only re-derives the spec metadata around it. This is the
opposite-direction engine: SQL → spec, not spec → SQL.

## What it does

`derive_spec_from_catalog(catalog_entry, rule_id, architecture, rule_name_override="",
system_filter="", requested_rule_type="", promote_info_to_error=True) -> DQRuleSpec`

1. **Validate** — raise `ValueError` if both `op_query_sql` and `report_query_sql` are empty (bulk
   processor surfaces it as a row error).
2. **Read catalog rule type** — `ERROR` if `rule_type.lower()=="error"`, else `INFO`. Final type:
   explicit `requested_rule_type` wins, then promotion (→Error), then the catalog tag.
3. **Decide restructuring** — `should_attempt = promote_info_to_error AND (native Error OR
   user-requested Error)`. **Native Error catalogs are ALSO restructured**, not just Info→Error. Raw
   Error catalog SQL lacked `zIsErrorFlag`, which broke the canonical RptSel filter, so every Error
   rule now goes through the methodology shape.
4. **Resolve view names** via the project naming pattern (OptSel/InfSel by type; RptSel for Error).
   `{system}` token resolved through `resolve_system_alias`; `{table}`/`{field}` are best-effort
   hints from `catalog_entry.tables[0]` + first SELECT column — wrong guesses only affect view-name
   aesthetics, never the SQL.
5. **Substitute `{datastore}`** — canonical target is `WRKDQ`: rule views are created in AND read
   FROM `WRKDQ` (one repository, same-DB read), downstream of the `WRKDQPREP_ALL` prep layer whose
   consolidated output is pushed into `WRKDQ`. The app reads Error/Info rule views FROM `WRKDQ`,
   matching profiling; `WRKDQPREP_ALL` is upstream ETL only.
6. **Wrap in CREATE VIEW** — Error rules call `catalog_promotion.promote_info_to_error` (WRAP, never
   inject); Info rules wrap `op_sql or rpt_sql` directly. See [[ref-catalog-promotion]].
7. **Inject the per-impl system filter** (non-Error here; Error rules already got it inside the
   promoted body — doing it twice would double-filter).
8. **Reverse-engineer the spec** from `op_sql or rpt_sql` (the universe): `_extract_output_fields`,
   `_extract_joins`, `_extract_filters`. Append the promoted error condition as a `LogicEntry`
   (element=`zIsErrorFlag`, operator=`CASE`, value=`1`).
9. **Prepend tech fields** (Error only), **build the 3-part description**, assemble the spec
   (`business_impact="Medium"`, `rule_source="Catalog"`), attach transients, run the fail-soft
   [[ref-ai-static-validator-gate|validator gate]].

## Key conventions (do / don't)

- **SQL is source of truth — never regenerated.** The deriver wraps, it does not rebuild. The
  catalog's own `report_query_sql` is preserved on `_catalog_report_query_sql_original` for
  reference but is **never deployed** — RptSel is ALWAYS the canonical wrapper
  `SELECT * FROM [dbo].[<OptSel>] WHERE [zIsErrorFlag] = 1`.
- **OptSel = the universe.** The error predicate lives in the `CASE`, not the WHERE. WHERE is
  reserved for system filter + deletion exclusions + scope. Catalog WHERE predicates default to
  **EXCLUSION** `FilterEntry` — the error predicate is deliberately NOT among them (the promoter
  lifted it into the CASE).
- **Resolve aliases to real SAP tables.** `_extract_alias_map` builds `{alias_upper: table_upper}`
  so `M.MATNR` resolves to `MARA.MATNR` (not `M`). Without this, `spec.main_table` would return
  `"M"`/`"T1"`/`"ska1"` and the rule-name scorer would reject the spec. Joins record both `source`
  and `target` as real SAP names with ON-predicate aliases rewritten.
- **Read `src.zSourceSystemID`, never hardcode the literal.** The injected select column reads the
  actual column so source-system drift surfaces immediately (multiple values in output) instead of
  masquerading as success. The generator likewise reads `src.zSourceSystemID`.
- **System-filter injection is paren-aware.** When a top-level WHERE exists it wraps the existing
  predicate in parens and ANDs the inclusion — catalog WHEREs often use OR chains, and a naked `AND`
  append would bind to the last OR branch and silently widen the result. Always qualified by the
  FROM-table alias.
- **Comment- and paren-aware scanning.** `_find_top_level` / `_comment_spans` skip keyword matches
  inside `--` / `/* */` banners and inside subquery parens, so a banner saying "WHERE" or a
  subquery's `GROUP BY` is never mistaken for the outer clause.
- **`zIsErrorFlag` always exists.** When no clean predicate can be extracted, emit literal `1 AS
  [zIsErrorFlag]` with a TODO marker (status: "Best-effort methodology applied"). No Error rule
  ships without its Syniti technical fields.

## Inputs & outputs

- **In:** a `CatalogEntry` (`adm_rule_name`, `rule_type`, `op_query_sql`, `report_query_sql`,
  `tables`, `implication`...), a `rule_id`, an
  [[ref-architecture-context-and-project-yamls|ArchitectureContext]], plus optional
  name/system/type overrides.
- **Out:** one `DQRuleSpec` with `sql_optsel`/`sql_rptsel` = wrapped catalog SQL, reverse-engineered
  `output_fields`/`logic`/`joins`/`filters`, the banked Fetch/Check/Return
  [[ref-ai-derive-and-enhance-internals|description]], and transients `_catalog_id`,
  `_catalog_op_query_sql_original`, `_promotion_attempted/_applied/_status`, `_warnings`,
  `_validator_findings`.

## Description template

`_build_catalog_description` emits the banked 3-part shape: **1. Functional/Business Description**
(from `implication`), **2. Specific Relevancy Criteria/Scope** (rule text + tables), **3. DQ Checks**
with `Fetch` / `Check` / `Return` bullets using `<br />` for in-cell breaks (renders cleanly in
markdown tables + Excel paste).

> [!note] Implementation status
> Every known open item on this path is closed in the shipped snapshot: the single canonical
> view-name pattern set is the project-YAML resolver, and its defaults were aligned to the dataclass
> so `{system}` is present (production system ID / agreed alias, e.g. PD1 — never the interim QA
> system) for Error/Info views; profiling views omit it. `zConcatenatedKey` uses one separator (`_`)
> on BOTH paths: the catalog/promotion path's `'|'` was changed to `'_'`, CONCAT is NULL-safe, and
> the keyless fallback emits `''` not NULL — identical across both paths. The app creates AND reads
> Error/Info rule views FROM **WRKDQ** (one repository, same-DB read), matching profiling;
> `WRKDQPREP_ALL` is upstream ETL only (relevancy/merge/aggregate/scope) whose output is pushed into
> `WRKDQ`.

## Source

- `core/catalog_deriver.py:49-468` — `derive_spec_from_catalog` (full mapping).
- `core/catalog_deriver.py:823-991` — `_from_alias`, comment/paren-aware scanners,
  `_inject_system_filter`.
- `core/catalog_deriver.py:1124-1312` (per mining doc) — `_inject_zsource_systemid_select_column`
  (read-not-hardcode), `_build_catalog_description`.
- Promotion mechanics: `core/catalog_promotion.py`. Detail: `knowledge-mining/derivation-spec.md` §7.

## Related

[[ref-catalog-promotion]] · [[prn-catalog-promotion-wraps-instead-of-injecting]] ·
[[ref-sql-parser]] · [[ref-local-deriver]] · [[ref-view-name-token-resolution]] ·
[[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] ·
[[ref-datastore-substitution-and-erp-compat-check]] · [[ref-rule-catalog-structure]]
