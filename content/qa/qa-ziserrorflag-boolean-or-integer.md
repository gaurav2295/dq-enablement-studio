---
id: qa-ziserrorflag-boolean-or-integer
type: qa
title: Is zIsErrorFlag a Boolean or an Integer?
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:prn-sql-comments-must-match-local-derive-quality
  - relates:std-ziserrorflag-convention
---

## Question

Is zIsErrorFlag a Boolean or an Integer as mentioned here?

## Answer

**Integer** — always `1` (defect) or `0` (pass), never Boolean / TRUE / FALSE / 'Y' / 'N'.

**Why Integer, not Boolean:**

1. **SQL Server compatibility** — Boolean doesn't exist natively in SQL Server; TRUE/FALSE are aliases that resolve to 1/0 anyway
2. **Explicit semantics** — 1 and 0 have clear meaning in DQ context: 1 = error found, 0 = no error
3. **Arithmetic in window functions** — profiling rules (PrfSum) sum and divide `zIsErrorFlag` as numeric; TRUE/FALSE would require type conversion
4. **Cross-system parity** — other databases (Snowflake, Redshift, BigQuery) have different Boolean implementations; integer is universal

**The SQL pattern (canonical):**

```sql
CASE
    /* Material is missing a base unit of measure */
    WHEN MARA.MEINS IS NULL OR MARA.MEINS = ''
        THEN 1      -- error found
    ELSE 0          -- no error
END AS [zIsErrorFlag]
```

**❌ NEVER:**
```sql
CASE WHEN MARA.MEINS IS NULL THEN 'Y' ELSE 'N' END  -- string, not numeric
CASE WHEN MARA.MEINS IS NULL THEN TRUE ELSE FALSE END  -- Boolean alias
CASE WHEN MARA.MEINS IS NULL THEN 1.0 ELSE 0.0 END  -- decimal, not integer
```

**Type declaration in CREATE VIEW:**

```sql
CREATE VIEW [dbo].[DQ_0042_P02_MARA_MEINS_OptSel] AS
SELECT
    ...
    CASE WHEN MARA.MEINS IS NULL OR MARA.MEINS = '' THEN 1 ELSE 0 END AS [zIsErrorFlag],
    ...
FROM ...
```

The CASE expression infers the type as INTEGER from the literal `1` and `0`. No explicit `CAST` is needed.

## Related

- [[std-ziserrorflag-convention|zIsErrorFlag Convention]]
- [[prn-sql-comments-must-match-local-derive-quality|Why SQL Comments Must Match Local-Derive Quality]]
