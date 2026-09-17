---
id: prn-catalog-promotion-wraps-instead-of-injecting
type: principle
title: Why Catalog Promotion Wraps Instead of Injecting
domain: sql-standards
audience: [developer]
level: advanced
status: review
links:
  - prereq:prn-optsel-is-the-universe
  - relates:std-zsourcesystemid-convention
  - relates:std-zconcatenatedkey-convention
  - relates:std-ziserrorflag-convention
  - relates:prn-sql-comments-must-match-local-derive-quality
  - relates:prn-ziserrorflag-is-integer
sources:
  - vault:thought-leadership/Why Catalog Promotion Wraps Instead of Injecting.md
tags: [thought-leadership, methodology, studio, catalog, sap]
created: 2026-08-20
updated: 2026-08-20
---

## The rule

When promotion turns a catalog rule into a deployable Error view, it wraps the catalog SQL
bit-identically as `FROM (<catalog>) AS src` and adds the Syniti tech fields in an outer
`SELECT` — it does **not** inject those columns into the catalog's own `SELECT` list. Injection
reformatted the body and, worse, lifted aggregate predicates out of subquery `HAVING`s into
outer-`SELECT` context where they fail to compile.

The catalog ships **authoritative SQL for ~4,800 Error/Info rules**. Promotion is
**mechanical — no AI** — so it must never re-derive or re-write that SQL. It only adds the
methodology scaffolding (`zSourceSystemID`, `zConcatenatedKey`, `zIsErrorFlag`) around proven
SQL.

## The two strategies

```sql
-- INJECT (earlier versions): edit the catalog's own SELECT list
SELECT
    src_col1, src_col2,
    src.zSourceSystemID AS [zSourceSystemID],   -- inserted into the body
    CASE WHEN ... THEN 1 ELSE 0 END AS [zIsErrorFlag]
FROM ... GROUP BY ... HAVING COUNT(DISTINCT col) > 1   -- gets disturbed

-- WRAP (current): preserve the catalog SQL verbatim as a derived table
SELECT
    -- Syniti Technical Fields
    src.zSourceSystemID AS [zSourceSystemID],
    CONCAT(src.<key>, '|', src.zSourceSystemID) AS [zConcatenatedKey],
    CASE WHEN <error_condition> THEN 1 ELSE 0 END AS [zIsErrorFlag],
    -- Catalog columns (preserved verbatim from op_query_sql)
    src.<col1>, src.<col2>, ...
FROM ( <catalog op_query_sql, verbatim> ) AS src
```

## Worked example: Material duplicate detection rule

Here's a real scenario that shows why wrapping is necessary.

**The catalog rule (MARA duplicates by plant):**

```sql
SELECT MATNR, WERKS, COUNT(DISTINCT PLANT) AS plant_count
FROM MARA
GROUP BY MATNR, WERKS
HAVING COUNT(DISTINCT PLANT) > 1
```

**What injection tried (and failed):**

```sql
SELECT
    MATNR, WERKS, plant_count,
    MARA.zSourceSystemID AS [zSourceSystemID],  -- inserted into body
    CASE WHEN plant_count > 1 THEN 1 ELSE 0 END AS [zIsErrorFlag]
FROM MARA
GROUP BY MATNR, WERKS
HAVING COUNT(DISTINCT PLANT) > 1  -- aggregate in HAVING, but reformatting 
                                   -- dragged it into SELECT context
```

SQL Server rejects this — `COUNT(DISTINCT PLANT)` can't live in the outer SELECT without a GROUP BY at that level.

**What wrap does (and works):**

```sql
SELECT
    src.MATNR, src.WERKS, src.plant_count,
    src.zSourceSystemID AS [zSourceSystemID],
    CONCAT(src.MATNR, '_', src.WERKS, '_', src.zSourceSystemID) AS [zConcatenatedKey],
    CASE WHEN src.plant_count > 1 THEN 1 ELSE 0 END AS [zIsErrorFlag]
FROM (
    SELECT MATNR, WERKS, COUNT(DISTINCT PLANT) AS plant_count, 
           zSourceSystemID
    FROM MARA
    GROUP BY MATNR, WERKS, zSourceSystemID
    HAVING COUNT(DISTINCT PLANT) > 1
) AS src
```

The aggregate stays *inside* the derived table where its GROUP BY/HAVING is valid. The outer SELECT only references columns — no aggregates, so SQL compiles cleanly.

## Why injection broke

Many catalog dup-detection rules express the defect as an **aggregate in a subquery `HAVING`**
— e.g. `... GROUP BY MATNR HAVING COUNT(DISTINCT WERKS) > 1`. Injecting tech columns into the
`SELECT` forced a reformat of the whole statement, which dragged `COUNT(DISTINCT col) > 1` out
of its `HAVING` and up into outer-`SELECT` context. An aggregate function has no group to
aggregate over at that level — SQL Server rejects it. The rule simply doesn't compile.

Wrapping sidesteps this entirely: the aggregate stays *inside* the derived table where its
`GROUP BY`/`HAVING` is still valid. The outer `SELECT` only ever references `src.<col>` — plain
column references, never aggregates.

## What wrapping is allowed to change

The catalog body is preserved **verbatim** with exactly three mutations:

1. **`{datastore}` substitution** — the placeholder is swapped for the resolved prep-layer
   datastore.
2. **Top-level `ORDER BY` stripped** (`_strip_top_level_order_by`) — `ORDER BY` is illegal inside
   a derived table.
3. **System filter appended *inside* the body** (via `_inject_system_filter`) — so the
   per-implementation `zSourceSystemID = '<code>'` scope binds to the catalog's own `FROM`, not
   the wrapper.

Catalog columns are **enumerated** (`src.<col1>, src.<col2>, ...`), not `src.*` — enumeration
avoids emitting a duplicate `zSourceSystemID` column. `src.*` is only the fallback when a column
can't be cleanly named.

## Where the error condition comes from

The `zIsErrorFlag` predicate is the **diff between the report query and the op query** — never
new logic. When the report query is the op universe with one extra `AND`, that remainder *is*
the per-row error condition. See [[prn-optsel-is-the-universe]].

> [!note] Literal-1 fallback
> If the only distinguishing predicate uses an aggregate function (`COUNT|SUM|AVG|MIN|MAX|STDEV|
> STDEVP|VAR|VARP|CHECKSUM_AGG|GROUPING|STRING_AGG`), it can't live in an outer-`SELECT` `CASE`
> — exactly the case wrapping protects. The flag then falls back to `1 AS [zIsErrorFlag]` with a
> `/* TODO */` marker (status: "Best-effort methodology applied (no clean predicate
> extraction)"). Every Error rule still ships its tech fields — the flag is never simply absent.

## Do / Don't

- **Do** wrap proven catalog SQL as `FROM (<catalog>) AS src` and add tech fields in the outer
  `SELECT`.
- **Do** keep aggregates inside the derived table; reference only `src.<col>` in the wrapper.
- **Don't** edit, reformat, or re-derive the catalog body — promotion is mechanical, not
  generative.
- **Don't** lift a subquery `HAVING` aggregate into the outer `SELECT`; fall back to literal-1 +
  TODO instead.

## Related

- ref-catalog-promotion — the engine that implements this.
- [[prn-optsel-is-the-universe]] · ref-catalog-deriver · ref-rule-catalog-structure
- [[prn-sql-comments-must-match-local-derive-quality]] · [[prn-ziserrorflag-is-integer]]
- The three tech fields the wrapper adds: [[std-zsourcesystemid-convention]] ·
  [[std-zconcatenatedkey-convention]] · [[std-ziserrorflag-convention]]
