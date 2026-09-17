---
id: ref-catalog-promotion
type: reference
title: Catalog Promotion (wrap not inject)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - parent:ref-catalog-deriver
  - implements:prn-catalog-promotion-wraps-instead-of-injecting
  - relates:ref-sql-validator
  - relates:ref-zconcatenatedkey-and-ziserrorflag-sql-emission
  - relates:ref-rule-catalog-structure
  - relates:ref-local-deriver
  - contrast:std-zconcatenatedkey-convention
  - relates:gls-catalog-promoter
  - relates:gls-distinguishing-predicate
sources:
  - vault:studio-architecture/Studio — Catalog Promotion (wrap not inject).md
  - dq-studio:docs/Studio_Overview.md
tags: [studio, engine, catalog, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`promote_info_to_error()` turns a catalog op/report query pair into a deployable Error OptSel by
wrapping the catalog universe SQL bit-identically as `FROM (<catalog>) AS src`, computing the
per-row error condition as the *diff* between the report and op WHERE/HAVING clauses, and emitting
the Syniti technical fields in an outer SELECT — it never re-derives or re-formats the catalog SQL.

This is the methodology engine behind the [[ref-catalog-deriver]]'s Error path. The catalog ships
**authoritative SQL for ~4,800 Error/Info rules**; promotion is **mechanical (no AI)** — it lifts
the existing report-vs-op predicate into a `zIsErrorFlag` CASE rather than writing new logic. See
[[prn-catalog-promotion-wraps-instead-of-injecting]] for the rationale.

## Why wrap, not inject

Earlier versions *field-injected* the Syniti tech columns into the catalog's own SELECT list. That
reformatted the body and — worse — **lifted aggregate predicates (`COUNT(DISTINCT col) > 1`) out of
subquery `HAVING`s into outer-SELECT context, where they fail to compile.** The wrap approach
preserves the catalog SQL **verbatim** as a derived table and adds the tech fields *around* it:

```sql
SELECT
    -- Syniti Technical Fields
    src.zSourceSystemID AS [zSourceSystemID],
    CONCAT(src.<key>, '_', src.zSourceSystemID) AS [zConcatenatedKey],
    CASE WHEN <error_condition> THEN 1 ELSE 0 END AS [zIsErrorFlag],
    -- Catalog columns (preserved verbatim from op_query_sql)
    src.<col1>, src.<col2>, ...
FROM ( <catalog op_query_sql, verbatim> ) AS src
```

The only mutations allowed on the catalog body: `{datastore}` substitution; **top-level `ORDER BY`
stripped** (`_strip_top_level_order_by` — illegal inside a derived table); and the per-impl system
filter appended *inside* the body via `_inject_system_filter`. Catalog columns are **enumerated** as
`src.<col>` (not `src.*`) to avoid a duplicate `zSourceSystemID` column; `src.*` is only the
fallback when a column can't be cleanly named.

## Eligibility — `info_to_error_eligible` (`:47-100`)

Returns `(eligible, reason)`. A catalog entry can be promoted only when **all** hold:

- **Both `op_query_sql` AND `report_query_sql` are non-empty.**
- **The FROM/JOIN skeletons are equal** — `_sql_skeleton` is the normalised text between `FROM` and
  the first `WHERE`/`GROUP BY`/`ORDER BY`/`HAVING`/`UNION`. Same skeleton means the report query is
  the universe filtered down, so the difference *is* the defect.
- **A distinguishing predicate exists**: a top-level `WHERE` the report adds, OR a `HAVING` the
  report adds, OR a subquery-`HAVING` the report has that op doesn't.

Notes: the catalog `rule_type` label **no longer gates eligibility** — native Error catalogs whose
op/rpt pair fits the methodology shape are restructured too (raw Error SQL lacked `zIsErrorFlag`,
breaking the canonical RptSel filter). Aggregation queries are eligible when the report adds a
`HAVING` op lacks — that `HAVING` becomes the per-group flag.

## The error condition — `_extract_error_condition` (`:493-554`)

The error predicate driving the CASE is the **report-vs-op diff**, resolved by skeleton:

- **Same skeleton (the common case):** prefer the **top-level WHERE diff** — if the report WHERE
  starts with `op_where + " AND "`, return the remainder. Then try the **top-level HAVING diff**,
  then the **subquery HAVING** (trusted only when structures match).
- **Different skeleton** (report adds JOINs / wraps subqueries — dup-detection rules): **skip the
  WHERE diff entirely** — it's usually a universe filter, not the error predicate, and lifting it
  would produce a semantically-wrong CASE. Only a `HAVING` diff is returned. When nothing usable
  remains → empty.

> [!note] Literal-1 fallback
> When no clean predicate can be extracted — or the predicate uses an aggregate function
> (`_AGGREGATE_FN_RE` = COUNT|SUM|AVG|MIN|MAX|STDEV|STDEVP|VAR|VARP|CHECKSUM_AGG|GROUPING|STRING_AGG)
> that can't live in an outer-SELECT CASE — the flag falls back to `1 AS [zIsErrorFlag]` with a `/*
> TODO: literal 1 ... */` marker. The [[ref-sql-validator|validator]] flags this
> (`literal-flag-fallback`, Medium); status string: "Best-effort methodology applied (no clean
> predicate extraction)". **Every Error rule still ships with its tech fields** — the flag is never
> simply absent.

## The promotion decision tree (and its three banners)

For an Error rule sourced from the Syniti rule catalog, the deriver walks one decision tree. The
branch it takes is recorded as a **banner comment in the emitted SQL**, which is what makes the
promoter's behaviour auditable after deployment:

```text
catalog_entry (op_query_sql + report_query_sql)
  │
  ├─ structure-eligible?   (op + rpt skeleton match, distinguishing predicate)
  │     │
  │     ├─ YES → promoter extracts the per-row error condition:
  │     │         • top-level WHERE diff             → predicate
  │     │         • top-level HAVING diff            → group-aggregate predicate
  │     │         • subquery HAVING (structures match) → dup-detection predicate
  │     │       Banner: "Promoted from Info catalog entry" or
  │     │               "Restructured native Error catalog entry"
  │     │
  │     └─ NO  → best-effort path:
  │               literal `1 AS [zIsErrorFlag]` + `/* TODO */` marker
  │               Banner: "Best-effort methodology applied"
```

The three banner strings are therefore a closed set — *Promoted from Info catalog entry*,
*Restructured native Error catalog entry*, *Best-effort methodology applied* — and the same
vocabulary appears in `Batch_Summary.xlsx`'s reconciliation sheet as the per-row promoter status
(plus a fourth, `Catalog entry not auto-restructurable`, for rows the deriver declined).

> [!important] The bypass check is the tripwire
> The audit's `catalog-methodology-bypass` check fires when a catalog-sourced view ships carrying
> **none** of the three banners. That means the view skipped the promoter entirely and went out as
> raw catalog SQL — the exact bug shape that existed before this engine was introduced. See
> std-req-sql-catalog-methodology-bypass and prn-adr-040.

## Inputs & outputs

- **In:** `op_query_sql` + `report_query_sql` (both MS SQL), the resolved key field, system filter /
  `zSourceSystemID` code, optional `zdomain_table`.
- **Out:** `(optsel_body, error_condition)` — the wrapped OptSel CREATE-VIEW body and the lifted
  predicate. The [[ref-catalog-deriver]] then appends the error condition as a `LogicEntry`
  (element=`zIsErrorFlag`, operator=`CASE`) and the RptSel is **always** the canonical wrapper
  `SELECT * FROM [dbo].[<OptSel>] WHERE [zIsErrorFlag] = 1` — the catalog's own report query is
  preserved on `_catalog_report_query_sql_original` but never deployed.
- **Key field:** `_pick_key_field` — first `key="Yes"` field's `table_field`, else first non-empty,
  else `<table>.ID` placeholder. The generator **reads `src.zSourceSystemID`** rather than
  hardcoding the literal so source-system drift surfaces (see
  [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]]).

> [!note] Implementation status — separator and NULL-safety are canonical
> `zConcatenatedKey` separator is now `_` on **both** paths. Promotion emits **NULL-safe
> `CONCAT(src.<key>, '_', src.zSourceSystemID)`** (catalog `'|'`→`'_'`), matching
> [[ref-local-deriver|local-derive]]; CONCAT is NULL-safe and the keyless fallback emits `''`
> (never NULL). One separator (`_` underscore, no space — ADM), NULL-safe, **never NULL**, on both
> the local-derive and catalog/promotion paths — the previously-audited NULL `zConcatenatedKey` in
> 137/321 rules no longer occurs.

> [!warning] Argument order is the one remaining divergence — CONFLICT-007
> What is *not* yet canonical is the order of the CONCAT arguments. This path emits key first —
> `CONCAT(src.<key>, '_', src.zSourceSystemID)` (`core/catalog_promotion.py:262`, `:796`) — while
> [[std-zconcatenatedkey-convention|the standard]] and the local-derive path put `zSourceSystemID`
> first (`core/sql_generator.py::_collect_concat_key_fields`: "zSourceSystemID always goes first").
> The same record therefore gets two different keys depending on which route derived it. Logged as
> CONFLICT-007.

## Source

- `core/catalog_promotion.py:47-100` — `info_to_error_eligible` (skeleton equality + distinguishing
  predicate) and `_sql_skeleton`.
- `core/catalog_promotion.py:108-307` — `promote_info_to_error` (wrap strategy, body mutations,
  outer SELECT, aggregate→literal-1 fallback, `_strip_top_level_order_by`).
- `core/catalog_promotion.py:493-554` — `_extract_error_condition` (WHERE/HAVING/subquery-HAVING
  diff resolution).
- `core/catalog_promotion.py:757-814` — `_build_tech_block`; `:259, 789-791` — the `CONCAT('_')` key.
  Detail: `knowledge-mining/derivation-spec.md` §8.

## Related

[[ref-catalog-deriver]] · [[prn-catalog-promotion-wraps-instead-of-injecting]] ·
[[ref-rule-catalog-structure]] · [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] ·
[[ref-sql-generator]] · [[ref-sql-parser]] · [[ref-sql-validator]] ·
[[ref-deletion-flag-normalization-in-sql-gen]] · [[ref-local-deriver]] ·
[[prn-sql-comments-must-match-local-derive-quality]]
