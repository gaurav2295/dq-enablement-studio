---
id: ref-view-vs-table-qualification
type: reference
title: View vs Table Qualification
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-sql-generator
  - relates:ref-generate-sql-dispatcher
  - relates:ref-view-name-token-resolution
  - relates:ref-three-database-architecture
  - relates:ref-sql-parser
  - relates:ref-catalog-promotion
sources:
  - vault:studio-architecture/Studio — View vs Table Qualification.md
tags: [studio, engine, sql, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

Generated VIEW names are always 2-part `[dbo].[<name>]` (SQL Server rejects 3-part `CREATE VIEW`
names — DB context is implicit, set by a `USE` at deploy time), while base TABLE references carry
their 3-part `[<db>].[dbo].[<table>]` form. Canonically the DB is `WRKDQ`: rule views are created
in AND read FROM `WRKDQ` (one repository, a same-DB read).

This is one rule with two helpers in `core/sql_generator.py`. Get it wrong and either the `CREATE
VIEW` fails to compile (3-part view name) or the rule reads from the wrong database (2-part table
ref).

## What it does

Two sibling helpers, called everywhere the generator emits an identifier:

- **`_qualify(view_name, db_prefix)`** (`:2117-2135`) — ALWAYS returns `[dbo].[<view_name>]`, a
  two-part name. The `db_prefix` arg is accepted for API symmetry but is deliberately ignored.
  Used for the `CREATE VIEW` target and for the RptSel `FROM [dbo].[<OptSel>]` (view-on-view).
- **`_qualified_table(table, db_prefix)`** (`:2110-2114`) — returns `[<db>].[dbo].[<table>]`, a
  three-part name that keeps the DB. Used for the OptSel/InfSel/Prf FROM and JOIN targets that hit
  physical tables. Canonically `<db>` is `WRKDQ` — the same repository the view is created in.

So in one generated OptSel you see both forms side by side:

```sql
CREATE VIEW [dbo].[DQ_0042_P06_KNA1_KTOKD_OptSel] AS   -- 2-part: the view we create
SELECT ...
FROM [WRKDQ].[dbo].[KNA1] AS KNA1                       -- 3-part: same-DB base table read (WRKDQ)
;
```

…and the RptSel wraps the OptSel as a view-on-view, also 2-part:

```sql
CREATE VIEW [dbo].[DQ_0042_P06_KNA1_KTOKD_RptSel] AS
SELECT *
FROM [dbo].[DQ_0042_P06_KNA1_KTOKD_OptSel]             -- 2-part: same-DB view ref
WHERE [zIsErrorFlag] = 1
;
```

## Key conventions (do / don't)

- **DO** emit `CREATE VIEW [dbo].[<name>]` — never `[db].[dbo].[name]`. SQL Server rejects 3-part
  `CREATE VIEW` names; the database context is implicit and the deploy script sets it with
  `USE <working_db>` before running the batch.
- **DON'T** 3-part-qualify a view-to-view `FROM` either. RptSel reads OptSel in the same DB, so
  `FROM [dbo].[<OptSel>]` — a 3-part name there would be redundant.
- **DO** keep the DB on base table refs: `[<db>].[dbo].[<table>]`. Canonically that DB is `WRKDQ`
  — rule views are created in AND read FROM `WRKDQ` (one repository, a same-DB read), so the
  prefix names the same DB the view lives in. See [[ref-three-database-architecture]].
- Canonically the FROM/JOIN `db` is `WRKDQ` (the one repository rule views are created in and read
  from). `WRKDQPREP_ALL` is the upstream prep layer whose output is pushed INTO `WRKDQ` — it is
  not the rule FROM target; raw `SRCECC_DA` is never the FROM target either. See
  [[ref-sql-generator]].
- The schema is always `dbo` in both forms — Studio does not emit non-`dbo` schemas.

> [!note] Implementation status — resolved 2026-07-01 — B4 (rule FROM target)
> The app now reads Error/Info rule views FROM/JOIN the working DB `WRKDQ` — one repository,
> matching profiling — and treats `WRKDQPREP_ALL` as upstream ETL only. The former cross-DB read
> FROM `arch.prep_db or arch.source_db` is resolved.

> One-liner to remember: the view name is 2-part (DB-local, implicit); the base table is 3-part
> but names the same DB (`WRKDQ`) — the 3-part form is a fully-qualified same-DB read, not a
> cross-DB read.

## Why it matters (round-trip)

The asymmetry is also why the [[ref-sql-parser|SQL parser]] tolerates both shapes:
`_extract_view_name` (`:224-248`) captures the final bracketed identifier in any 1/2/3-part name
(`CREATE VIEW (?:\[..\].)*\[(name)\] AS`), so it round-trips both current 2-part views and legacy
3-part views; and `_extract_architecture` reads `working_db` from a `CREATE VIEW [DB].[dbo]`
prefix when present (legacy) and the base-table FROM prefix (canonically `WRKDQ`, the repository
the rule view both lives in and reads from).

## Inputs & outputs

- **In:** a bare view name / table name plus an (ignored, for views) db prefix.
- **Out:** the qualified identifier string spliced into the generated SQL.

## Source

- `core/sql_generator.py:2110-2135` — `_qualified_table` (3-part, keeps DB) and `_qualify`
  (2-part, drops DB; docstring carries the SQL-Server rationale).
- `core/sql_generator.py:169-251` — `generate_optsel` / `generate_rptsel` use both helpers (CREATE
  VIEW + FROM).

## Related

- [[ref-sql-generator]]
- [[ref-generate-sql-dispatcher]]
- [[ref-view-name-token-resolution]]
- [[ref-three-database-architecture]]
- [[ref-architecture-context-and-project-yamls]]
- [[ref-layer-2-layer-4-datastore-views]]
- [[ref-sql-parser]]
- [[ref-sql-comment-and-formatting-standard]]
- [[ref-catalog-promotion]]
