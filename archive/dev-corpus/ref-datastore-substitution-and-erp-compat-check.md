---
id: ref-datastore-substitution-and-erp-compat-check
type: reference
title: "{datastore} Substitution & ERP-Compat Check"
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - parent:ref-catalog-deriver
  - relates:ref-catalog-promotion
  - relates:ref-rule-catalog-structure
  - relates:ref-table-extraction-and-complexity-scoring
  - relates:ref-three-database-architecture
sources:
  - vault:studio-architecture/Studio — {datastore} Substitution & ERP-Compat Check.md
tags: [studio, engine, catalog, sap]
created: 2026-08-20
updated: 2026-08-20
---

Catalog SQL ships with a `{datastore}` placeholder that the deriver swaps for the project's
prep database (`[<db>].[dbo]`), and on the same pass it scans the body for S/4HANA-only
Business-Partner tables (BUT0xx) — when found while the Studio targets ECC it raises a
compatibility warning that rides on both the SQL banner and `spec._warnings`. Both are small,
late steps inside the [[ref-catalog-deriver|Catalog Deriver]], run before the CREATE VIEW wrap.

## {datastore} substitution

The catalog authors SQL against an abstract placeholder so one body works on any project
(`substitute_datastore`, `rule_catalog.py:244-263`):

```sql
FROM {datastore}.CSKA AS cska   -- becomes →   FROM [WRKDQ].[dbo].CSKA AS cska
```

- Replacement value is **bracket-qualified**: `[<db>].[dbo]` (SQL Server two-part qualifier).
- Empty `db` (defensive) → the `{datastore}.` prefix is **stripped** entirely so the SQL still
  parses (a DBA can prepend the DB at deploy).
- Canonically, rule views are created in AND read from the **single repository `WRKDQ`**
  (`[WRKDQ].[dbo]`) — a same-database read. `WRKDQPREP_ALL` is the **upstream prep layer**
  (relevancy / source-merge / aggregation / scope) whose output is pushed into `WRKDQ`; it is
  **not** the rule SELECT-FROM target. Error/Info and Profiling views agree: all read from
  `WRKDQ`; `WRKDQPREP_ALL` is upstream ETL only (KNOWN-ISSUES B4, fixed 2026-07-01).
- `get_entry(catalog_id)` returns the entry with `{datastore}` **still present** —
  substitution is the caller's job because the target DB is per-project context.

## ERP-compatibility check

`_detect_erp_compatibility_issues` (`catalog_deriver.py:1372-1406`):

```python
_S4_BP_TABLES = {"BUT000", "BUT020", "BUT021", "BUT050", "BUT051"}
```

- Extracts tables from the promoted body via `extract_tables_from_sql` (see
  [[ref-table-extraction-and-complexity-scoring|Table Extraction]]), intersects with
  `_S4_BP_TABLES`. Empty intersection → no-op.
- The set is **deliberately conservative** — only the highest-confidence S/4-only tables,
  because false positives cost reviewer trust.
- When hit, returns a 4-line warning naming the tables, stating they are empty/missing on an
  ECC source, giving the ECC equivalent chain (KNA1 → KNVK → ADRC for customers, LFA1 → ADRC
  for vendors), and pointing to the ECC ↔ S/4HANA catalog-translation backlog item.
- Surfaced two ways: a `-- !! WARNING !!` block prepended to the CREATE VIEW banner by
  `_wrap_create_view` (`:471-512`), AND assigned to `spec._warnings` (`:430-431`) so the bulk
  UI / Tracker / markdown render it.

## Key conventions

- **DO** substitute `{datastore}` exactly once, against the rule repository `WRKDQ`; never
  deploy a view that still contains `{datastore}`.
- **DON'T** treat the ERP warning as a hard gate — it is **fail-soft** (the table extractor is
  wrapped in `try/except → []`); it never blocks generation, it only annotates.
- **DON'T** widen `_S4_BP_TABLES` speculatively — the conservative set is intentional.
- The flag means "won't resolve on ECC", not "wrong rule" — the rule is correct for an S/4HANA
  source; it needs the ECC equivalent chain when the project is ECC.

## Inputs & outputs

| Direction | What |
|---|---|
| In | catalog `op_query_sql` / `report_query_sql` (containing `{datastore}`), `architecture.prep_db`/`source_db`, the promoted SQL body |
| Out | datastore-qualified SQL ready to wrap; `erp_warnings: list[str]` → SQL banner block + `spec._warnings` |

## Source pointers

- `core/rule_catalog.py:244-263` — `substitute_datastore` (placeholder → `[<db>].[dbo]`).
- `core/catalog_deriver.py:226-234` — DB choice + op/rpt substitution (targets `WRKDQ`).
- `core/catalog_deriver.py:1372-1406` — `_detect_erp_compatibility_issues` + `_S4_BP_TABLES`.
- `core/catalog_deriver.py:471-512`, `:430-431` — warning block on banner + `spec._warnings`.
