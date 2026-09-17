---
id: ref-zconcatenatedkey-and-ziserrorflag-sql-emission
type: reference
title: zConcatenatedKey & zIsErrorFlag SQL Emission
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-output-section-builders
  - relates:ref-logic-case-predicate-templates
  - relates:ref-sql-generator
  - relates:ref-deletion-flag-normalization-in-sql-gen
  - implements:std-zconcatenatedkey-convention
  - implements:std-ziserrorflag-convention
  - relates:std-zsourcesystemid-convention
  - implements:prn-ziserrorflag-is-integer
  - contrast:prn-catalog-promotion-wraps-instead-of-injecting
sources:
  - vault:studio-architecture/Studio — zConcatenatedKey & zIsErrorFlag SQL Emission.md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

The SQL generator emits the two computed Syniti tech columns deterministically:
`zConcatenatedKey` is a `CONCAT(...)` of `zSourceSystemID` plus every key field joined by `'_'`
(no per-field CAST), and `zIsErrorFlag` is always a `CASE WHEN <error> THEN 1 ELSE 0 END`
(INTEGER 1 = defect, 0 = pass) — never strings, never CAST-to-decimal.

These two columns are the heart of an OptSel: `zConcatenatedKey` is the row identity SKP joins on,
and `zIsErrorFlag` is the per-row defect verdict that [[ref-sql-generator|RptSel]] filters on.
They are built by the Tech-section emitters in `sql_generator.py`, downstream of the rows that
[[ref-output-section-builders]] mark `key="Yes"`.

## zConcatenatedKey

`_build_concat_key_expr` / `_collect_concat_key_fields`:

- **Field set**: `zSourceSystemID` is ALWAYS first (inserted at index 0), then every output field
  with `key in ("X","Yes")`.
- **Form**: `CONCAT(<f1>, '_', <f2>, '_', …) AS [zConcatenatedKey]` — underscore separator,
  interleaved by `_interleave`.
- **NO per-field CAST** (design decision): inside SQL Server `CONCAT()` every arg auto-converts to
  NVARCHAR and NULL is treated as empty string, so a CAST is noise for string-typed SAP SE11 key
  fields. A DBA can add a targeted CAST only for a numeric-stored key.
- **Alias** is the literal `zConcatenatedKey` — no space (ADM requirement).
- **Fallbacks**: parse a `CONCAT(...)` formula, or a `Concatenate: X.A + '_' + Y.B` instruction;
  ultimate fallback emits `/* zConcatenatedKey: define key fields */ NULL AS [zConcatenatedKey]`.
- **Profiling variant**: PrfSel concat uses the Unicode literal `N'_'` (vs OptSel's `'_'`); same
  NULL-safe CONCAT shape.

```sql
CONCAT(MARA.zSourceSystemID, '_', MARA.MATNR, '_', MARC.WERKS) AS [zConcatenatedKey]
```

> [!note] Implementation status — resolved 2026-07-01 — B3 (zConcatenatedKey separator)
> Canonical rule: separator is `_` (underscore), NULL-safe, never NULL, and identical across
> local-derive and catalog/promotion. The app now emits `_` on both paths — the
> catalog/promotion path's `|` was converged to `_` (catalog `"|"` → `"_"`), CONCAT remains
> NULL-safe, and the keyless fallback emits `''` rather than `NULL`. Both `_build_tech_block` /
> `promote_info_to_error` and local-derive now produce identical `_`-separated keys.

## zIsErrorFlag

`_build_select_parts`: when an output field's element is `zIsErrorFlag`, the logic CASE (from
`_build_logic_case`) is inserted, and its trailing alias is rewritten to `AS [zIsErrorFlag]` via
`re.sub(r"AS \[[^\]]+\]$", "AS [zIsErrorFlag]", …)`. With no logic:
`/* zIsErrorFlag: define logic condition */ NULL AS [zIsErrorFlag]`.

Every branch of `_parse_logic_case` emits the same integer shape — always `THEN 1 ELSE 0`:

```sql
CASE
    WHEN <error_condition>
    THEN 1
    ELSE 0
END AS [zIsErrorFlag]
```

Do / don't:

- **DO** keep `1` = defect, `0` = pass, as INTEGER literals. Never `'Yes'`/`'No'`, `'Y'`/`'N'`,
  never CAST-to-decimal. See [[prn-ziserrorflag-is-integer]].
- **DO** put the error predicate in the CASE — OptSel returns the full candidate universe with a
  per-row flag. The WHERE is reserved for system filter, scope, and deletion exclusions.
- **DON'T** emit `zIsErrorFlag` for Info/Profiling rules. Info/Tech-info builds the two key fields
  only; profiling has no error detection.
- RptSel wraps OptSel: `SELECT * FROM <OptSel> WHERE [zIsErrorFlag] = 1` (integer compare, Error
  rules only).
- Last-resort placeholder `CASE WHEN 1=0 THEN 1 ELSE 0 END` flags nothing (deliberately safe).
  Catalog promotion's literal-`1`-with-TODO is a different fallback (no clean predicate
  extracted) — see [[prn-catalog-promotion-wraps-instead-of-injecting]].

The validator backstops both columns: `missing-tech-columns` (High) requires all three Syniti
tech fields (skips `zIsErrorFlag` for non-Error), and `null-unsafe-key-concat` (Low) flags any
`+ '|' + … AS [zConcatenatedKey]` (use CONCAT).

## Inputs & outputs

| | |
|---|---|
| **Inputs** | spec `output_fields` (the `key="Yes"` rows + the `zIsErrorFlag` element), the logic CASE from `_build_logic_case`, `zSourceSystemID` read from `src`/main-table (not hardcoded) |
| **Outputs** | two SELECT-list expressions: `CONCAT(...) AS [zConcatenatedKey]` and `CASE … THEN 1 ELSE 0 END AS [zIsErrorFlag]` |

## Source

- `core/sql_generator.py:1348-1394` — `_build_concat_key_expr` (CONCAT, `'_'`, no CAST);
  `:1854-1869` `_collect_concat_key_fields`; `:2155-2165` `_interleave`
- `core/sql_generator.py:1296-1308` — `_build_select_parts` (zIsErrorFlag placement + alias
  rewrite); `:1552-1695` `_parse_logic_case` (always `THEN 1 ELSE 0`)
- `core/catalog_promotion.py:257-259` — promotion tech block
  (`CONCAT(src.<key>, '_', src.zSourceSystemID)` — separator converged to `_` per B3, fixed
  2026-07-01; literal-1 + TODO fallback)

## Related

- [[ref-output-section-builders]]
- [[ref-logic-case-predicate-templates]]
- [[ref-sql-generator]]
- [[ref-catalog-promotion]]
- [[ref-deletion-flag-normalization-in-sql-gen]]
- [[ref-profiling-view-generation]]
- [[ref-sql-validator]]
- [[std-zconcatenatedkey-convention]]
- [[std-ziserrorflag-convention]]
- [[std-zsourcesystemid-convention]]
- [[prn-ziserrorflag-is-integer]]
- [[prn-catalog-promotion-wraps-instead-of-injecting]]
