---
id: ref-logic-case-predicate-templates
type: reference
title: Logic-CASE Predicate Templates
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - prereq:ref-logic-builder-templates
  - implements:prn-ziserrorflag-is-integer
  - relates:ref-zconcatenatedkey-and-ziserrorflag-sql-emission
  - relates:ref-generate-sql-dispatcher
  - relates:ref-sql-validator
  - relates:ref-output-section-builders
sources:
  - vault:studio-architecture/Studio — Logic-CASE Predicate Templates.md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`_parse_logic_case` maps one `LogicEntry`'s free-text `value` to ONE of ~13 ordered,
first-match-wins SQL predicate templates (completeness null/empty, three LEN variants, numeric
range, `=`/`<>`, LIKE/NOT LIKE, cross-field, plus generic and last-resort fallbacks) — and every
branch wraps that predicate as `CASE WHEN <error> THEN 1 ELSE 0 END AS [<alias>]`. This is the
function that turns [[ref-logic-builder-templates|Logic Builder Templates]]'s `"1 - If …"` text
into the `zIsErrorFlag` CASE.

A direct port of the HTML app's `parseLCase()`. It runs per logic entry;
[[ref-zconcatenatedkey-and-ziserrorflag-sql-emission|zConcatenatedKey & zIsErrorFlag SQL
Emission]]'s `_build_logic_case` picks the **first** entry with a `table_field` that parses to a
non-`None` CASE (alias default `"DQ_Check"`).

## What it does

Given a `LogicEntry` it reads `value` (the `1 - If …` flag text) and `instruction`, derives
`field = lr.table_field` and `alias = lr.element or "DQ_Check"`, then walks the branches **top to
bottom and returns on the first match**. Order is load-bearing: e.g. the completeness branch must
beat the generic null fallback. If `table_field` is empty it returns `None` (the caller then falls
through to the next logic entry, or emits a `NULL` `zIsErrorFlag` placeholder).

## The templates (branch order — first match wins)

Every branch emits the same skeleton. Only the WHEN predicate changes:

```sql
CASE
        WHEN <error_condition>
        THEN 1
        ELSE 0
    END AS [<alias>]
```

`THEN 1 ELSE 0` are INTEGER literals in EVERY branch — `1` is always the defect.

| # | Branch | Triggers on (`value`) | Emitted error predicate |
|---|---|---|---|
| 1 | Complex multi-table | `1 - If(<cond>)` whose `<cond>` contains a `TBL.FIELD` ref | the embedded `<cond>` verbatim (IS NULL / AND / OR normalized) |
| 2 | Completeness null/empty | `1 - if … null\|empty\|''\|'0'` AND no `AND TBL.` cross-table clause | `<field> IS NULL OR LTRIM(RTRIM(<field>)) = '' OR <field> = '0'` |
| 3 | Length `> N` | `LEN(…) > N`, "more than/over/exceed N char", "length greater than N" | `<field> IS NULL OR LEN(LTRIM(RTRIM(<field>))) > N` |
| 4 | Length `< N` | `LEN(…) < N`, "less/fewer/under N char" | `<field> IS NULL OR LEN(LTRIM(RTRIM(<field>))) < N` |
| 5 | Length within / max N | "within/at most/max/maximum/<= N char" | `<field> IS NULL OR LEN(LTRIM(RTRIM(<field>))) > N` (same as `>`) |
| 6 | Numeric range | "between/from N and/to M" | `<field> IS NULL OR CAST(<field> AS FLOAT) < N OR CAST(<field> AS FLOAT) > M` |
| 7 | Equals literal | `= 'value'` | `<field> = 'value'` |
| 8 | Not-equals literal | `<> 'value'` | `<field> <> 'value'` |
| 9 | NOT LIKE | `NOT LIKE 'x'` | `<field> NOT LIKE 'x'` |
| 10 | LIKE | `LIKE 'x'` | `<field> NOT LIKE 'x'` — error = value does NOT match the expected pattern |
| 11 | Cross-field | `A.X <> B.Y` (two `TBL.FIELD` refs) | `A.X <> B.Y OR A.X IS NULL OR B.Y IS NULL` |
| 12 | Generic null/empty | keyword `empty\|null\|blank\|missing\|not populated` in `value`+`instruction` | `<field> IS NULL OR LTRIM(RTRIM(<field>)) = ''` |
| 13 | Last resort (safe) | nothing matched | `/* Logic: <alias> - <value> */ CASE WHEN 1=0 THEN 1 ELSE 0 END AS [<alias>]` — flags NOTHING |

Notes that surprise:

- **Branch 5 (within/max N) emits `LEN(…) > N`** — same predicate as the `> N` branch (an
  at-most-N rule flags rows that exceed N).
- **Branch 10 (LIKE) emits `NOT LIKE`** — the rule says "value should match pattern X", so the
  *error* is a non-match. Authoring a positive `LIKE` predicate and expecting positive matching is
  wrong here.
- **Branch 13 is deliberately inert** (`WHEN 1=0`): when nothing parses, the generator flags zero
  rows rather than guessing — and leaves a `/* Logic: … */` comment the reviewer can find.

## Key conventions (do / don't)

- **DO trust order.** Put the most-specific phrasing in the `LogicEntry.value` so it lands on the
  intended branch; the completeness branch (#2) explicitly excludes `AND TBL.` clauses so
  cross-table conditions fall to #1/#11 instead.
- **DON'T author `= NULL`.** Use the completeness/null branches — the validator's
  `null-compared-with-eq` check rejects `= NULL` / `<> NULL`.
- **The error predicate belongs ONLY in this CASE, never the WHERE.** `OptSel` returns the universe
  with the per-row flag; `RptSel = SELECT * FROM <OptSel> WHERE [zIsErrorFlag] = 1`.
- **`zIsErrorFlag` is INTEGER `1`/`0`** — never strings, never CAST-to-decimal; `1` is always the
  defect. Every template hard-codes `THEN 1 ELSE 0`.

## Inputs & outputs

- **In:** a single `LogicEntry` (`element`, `table_field`, `value`, `instruction`).
- **Out:** a CASE-expression string aliased `AS [<alias>]`, or `None` when `table_field` is empty.
- **Downstream:** `_build_logic_case` selects the first non-`None` result; `_build_select_parts`
  rewrites its trailing alias to `AS [zIsErrorFlag]`
  (`re.sub(r"AS \[[^\]]+\]$", "AS [zIsErrorFlag]", …)`). No logic at all →
  `/* zIsErrorFlag: define logic condition */ NULL AS [zIsErrorFlag]`.

## Source

- `core/sql_generator.py:1539-1682` — `_parse_logic_case` (the ~13 ordered branches)
- `core/sql_generator.py:1537-1549` — `_build_logic_case` (first-non-None selection, alias default
  `DQ_Check`)
- Upstream `value` text produced by `core/local_deriver.py::_build_logic` — see
  [[ref-logic-builder-templates|Logic Builder Templates]]

## Related

[[ref-logic-builder-templates]] · [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] ·
[[ref-sql-generator]] · [[ref-generate-sql-dispatcher]] · [[ref-deletion-flag-normalization-in-sql-gen]] ·
[[ref-sql-validator]] · [[ref-output-section-builders]] · [[ref-dqrulespec-data-model]]
