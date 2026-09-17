---
id: ref-get-table-last-refresh-date
type: reference
title: Get Table Last Refresh Date (DPaaS)
domain: platform
audience: [consultant]
level: foundation
status: deprecated
links:
  - relates:ref-sap-dd-dictionary-tables
  - relates:ref-building-a-per-client-dd-dictionary
sources:
  - vault:syniti-platform/Get Table Last Refresh Date (DPaaS).md
tags: [reference, syniti-platform, dpaas, collect, sql]
created: 2026-08-20
updated: 2026-08-20
---

## Goal

Retrieve the last date a table was refreshed by Collect, using the user-defined scalar function
`[dbo].[GetTableLastRefreshDate]`.

> [!note]
> This function exists in the `[ddDPaaS]` database and returns information specific to **DPaaS**
> (Data Profiling as a Service). It is not available in standard ADM databases.

## Syntax

```sql
[dbo].[GetTableLastRefreshDate] ( table )
```

## Arguments

| Argument | Description |
|---|---|
| `table` | The table for which you want the last refresh date. |

## Return

- **Type:** `datetime`
- **Value:** the date on which the table was last refreshed by Collect.

## Example

```sql
SELECT [dbo].[GetTableLastRefreshDate]('MARA') AS LastRefresh;
```

## Related

[[ref-sap-dd-dictionary-tables]] · [[ref-building-a-per-client-dd-dictionary]]
