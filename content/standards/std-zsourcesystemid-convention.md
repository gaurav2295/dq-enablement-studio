---
id: std-zsourcesystemid-convention
type: standard
title: zSourceSystemID Convention
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
sources:
  - vault:dq-methodology/zSourceSystemID Convention.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:con-multi-implementation-model
  - relates:ref-system-aliases-map
  - relates:std-zconcatenatedkey-convention
  - relates:std-ziserrorflag-convention
  - relates:gls-zsourcesystemid
  - relates:std-cte-rules
---

## What it is

The **system discriminator column**. Present on every consolidated staging table in
`WRKDQPREP_ALL`, and carried verbatim into every DQ rule view.

## Format

- Column name: `zSourceSystemID` — exact casing.
- Value: the source system code (e.g. `SRCECCZ02100`, `SRCS4SG2100`, `P01` for Bacardi).
- Type: NVARCHAR (typically `NVARCHAR(50)`).

## How rules use it

### Error / Info rules → filter

Each per-system implementation adds an **inclusion filter** restricting to one system:

```sql
WHERE
    /* Include: Limit to source system P02 */
    MARA.zSourceSystemID = 'SRCECCZ02100'
```

This filter is appended automatically. The comment label uses the friendly alias from
`system_aliases`; the literal uses the actual `zSourceSystemID` value stored in the data.

### Profiling rules → segment

Profiling rules do NOT filter by system — they **segment by it**, so a single profiling view
returns one row per `(system, segment, value)` tuple:

```sql
SELECT
    zSourceSystemID,
    [Segmentation Field],
    [Profiled Value],
    COUNT(*) AS Occurrences,
    100.0 * COUNT(*) / SUM(COUNT(*)) OVER (PARTITION BY zSourceSystemID, [Segment]) AS Percentage
FROM ...
GROUP BY zSourceSystemID, [Segmentation Field], [Profiled Value]
```

`zSourceSystemID` is a **mandatory segmentation dimension** on every profiling view — always in
the SELECT, always in the GROUP BY.

## Format for other z-prefixed columns

While `zSourceSystemID` is the primary system discriminator, other Syniti-added columns follow the same naming convention. When working with these columns, use the exact casing and spelling:

| Column | Type | Purpose | Example |
|--------|------|---------|---------|
| `zSourceSystemID` | NVARCHAR(50) | Source system identifier | `'SRCECCZ02100'`, `'P02'` |
| `zConcatenatedKey` | NVARCHAR(255) | Composite key (no space in name) | `'Z01_M000001'`, `'Z02_12345_67890'` |
| `zIsErrorFlag` | INTEGER | Defect flag: 0 = pass, 1 = error | `1`, `0` |
| `zDomainSegment` | NVARCHAR(50) | Domain classification (Material/Customer/Vendor) | `'Material'`, `'Customer'` |

**Critical:** The names carry **no spaces** and use **exact casing** — `zConcatenatedKey` (not `z Concatenated Key` or `ZCONCATENATEDKEY`). These columns are added by the Studio and carried verbatim through all generated views. Mismatch in naming breaks round-trip parsing and audit validation.

## Why the z prefix

Syniti convention — `z`-prefixed columns are Syniti-added metadata, not source-SAP data.
Reviewers reading a query can tell at a glance which columns came from the source versus which
the Studio injected.

Other `z`-prefixed columns you'll see:

- [[std-zconcatenatedkey-convention|zConcatenatedKey]] — composite-key column
- [[std-ziserrorflag-convention|zIsErrorFlag]] — defect flag (Error rules)
- `zDomainSegment` — coarse domain tag (Material / Customer / Vendor / etc.)

## Common mistakes

> [!warning] Casing and naming
> `ZSourceSystemID`, `ZSOURCESYSTEMID`, `zSourceSystemId` — casing matters. `zSourceSystem`
> (missing the trailing `ID`) is also wrong.

- Putting it in the SELECT but forgetting the GROUP BY for profiling rules.

## Questions from consultants

- [[qa-consolidated-staging-table|What is a consolidated staging table?]]
- [[qa-why-casing-important-zsourcesystemid|Why is casing important for zSourceSystemID?]]

## Related

- [[con-multi-implementation-model|Multi-Implementation Model]]
- [[ref-system-aliases-map|System Aliases Map]]
- [[std-zconcatenatedkey-convention|zConcatenatedKey Convention]]
- [[std-ziserrorflag-convention|zIsErrorFlag Convention]]
- [[std-cte-rules|CTE Rules]] — every CTE must filter and output `zSourceSystemID` too
