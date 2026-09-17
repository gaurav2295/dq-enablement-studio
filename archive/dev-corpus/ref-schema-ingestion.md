---
id: ref-schema-ingestion
type: reference
title: Schema Ingestion (DDL/DBML/CSV)
domain: sap
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-sap-baseline-model
  - relates:ref-table-validator-and-autocomplete
  - relates:ref-dqrulespec-data-model
  - relates:ref-deletion-flag-resolver
  - relates:ref-sap-dd-dictionary-tables
  - relates:ref-knowledge-base-file-inventory
sources:
  - vault:sap-knowledge/Schema Ingestion (DDL-DBML-CSV).md
tags: [studio, engine, sap, agent, course]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

`parse_schema_file(path)` ingests an SAP schema from files only — never a live DB — auto-detecting
DDL/DBML/CSV by suffix, parsing DDL column bodies by manual paren-depth counting, mapping CSV
headers flexibly (with SAP's `X` accepted as a PK-true token), and exposing case-insensitive
`validate_field_ref` / `validate_spec_fields` that collect every `TABLE.FIELD` reference across
all spec sections.

This is the file-based front door for schema knowledge. There are **no live DB connections**
anywhere in the studio — a customer hands over a `.sql`/`.ddl`/`.dbml`/`.csv` extract and this
module turns it into a `SchemaModel` that the deriver and validator query. It feeds
[[ref-sap-baseline-model|SAP Baseline Model (logical vs physical)]] and backs
[[ref-table-validator-and-autocomplete|Table Validator & Autocomplete]].

## What it does

`parse_schema_file(path)` reads the file as text and **auto-detects format by suffix**, then
attaches `source_file` for provenance (`schema_parser.py:269-308`):

| Suffix | Parser |
|---|---|
| `.dbml` | `parse_dbml` |
| `.csv` | `parse_csv_schema` |
| `.sql` / `.ddl` | `parse_ddl` |
| anything else | DDL if text contains `CREATE TABLE` (upper-cased check), else CSV |

Missing file raises `FileNotFoundError`. Table & field names are **upper-cased on ingest** across
every parser (SAP physical-name convention); data types are upper-cased too.

## DDL parser — paren-depth, not naive split

(`parse_ddl`, `:316-430`)

- **Header regex** tolerates optional `[schema].`, `[dbo].`, and bracketed names:
  `CREATE TABLE [dbo].[KNA1] (` all parse (`:327-334`).
- **Column body extracted by manual parenthesis-depth counting**
  (`_extract_balanced_parens`, `_split_column_defs`, `:336-348, 433-473`) so a column like
  `KUNNR NVARCHAR(40)` survives — a regex `split(",")` would break inside `(40)`.
- Table-level constraints are skipped, but `PRIMARY KEY (...)` columns and
  `FOREIGN KEY (...) REFERENCES ...` are extracted into `references` (`:352-370`).
- Per-column regex `[name] TYPE[(length)] [modifiers]`: `nullable = "NOT NULL" not in modifiers`,
  `is_pk = "PRIMARY KEY" in modifiers`, length parsed from `(\d+)` (`:372-405`).
- Standalone `ALTER TABLE ... ADD [CONSTRAINT ...] FOREIGN KEY (...) REFERENCES ...` is also
  parsed into references (`:416-428`).

## DBML parser

(`parse_dbml`, `:481-552`)

- `Table name { ... }` blocks; per line `field type [settings]`. `is_pk = "pk" in settings`;
  `nullable = "not null" not in settings and not is_pk`; description pulled from `note: '...'`.
- `Ref: t1.f > t2.f` (any of `<`, `>`, `-`) → a reference. Lines starting `//` or `Note` are
  skipped.

## CSV parser — flexible headers, `X` = PK-true

(`parse_csv_schema`, `:560-633`)

- Opened with **`utf-8-sig`** encoding (strips a BOM) and **delimiter auto-detect**: tab if the
  4 KB sample's tab-count exceeds its comma-count, else comma (`:573-580`).
- `_map_csv_columns` maps semantic roles to whatever the header actually says (case-insensitive),
  so customer spreadsheets don't need renaming (`:618-633`):

| Role | Accepted headers |
|---|---|
| table | `table_name`, `table`, `tablename` |
| field | `field_name`, `field`, `column`, `column_name`, `fieldname` |
| type | `data_type`, `type`, `datatype`, `column_type` |
| description | `description`, `desc`, `comment`, `note` |
| pk | `primary_key`, `pk`, `key`, `is_pk`, `is_key` |

- **PK truthy tokens**: `pk_flag in ("Y", "X", "YES", "1", "TRUE", "PK")`, case-insensitive
  (`:603`). Note **`X`** is accepted — it's the SAP boolean-true literal (the same `X` that means
  "deleted" in a `LVORM` cell and "true" in a checkbox field). Rows with no table or field are
  skipped.

## Validation against the parsed schema

`SchemaModel.has_table` / `get_table` / `has_field` / `get_field` are all **case-insensitive**
(`:45-88`).

- **`validate_field_ref("TABLE.FIELD")`** → `FieldValidation(valid, reason, data_type,
  description, suggestions)` (`:90-141`). No `.` → "No table prefix". Missing table → suggests
  similar table names (`_suggest_tables`: candidate must share the **first 2 chars**, then ranked
  by edit distance). Missing field → suggests similar fields in that table (`_suggest_fields`:
  pure edit distance).
- **`validate_spec_fields(spec)`** collects every `TABLE.FIELD` across the whole
  [[ref-dqrulespec-data-model|DQRuleSpec]], de-dupes into a set, and validates each (`:143-176`):
  - `output_fields` → `f.table_field`
  - `logic` → `l.table_field`
  - `joins` → regex `(\w+\.\w+)` over `join_key` (a join can name two refs)
  - `filters` → `f"{filt.table}.{filt.field}"`

> [!note] Three independent fuzzy-suggest implementations
> Don't assume one shared utility. `table_validator.suggest` scores
> `edit_distance − 0.5·prefix + 0.3·len_diff`; `schema_parser._suggest_tables` requires a
> first-2-char match *then* edit distance; `schema_parser._suggest_fields` is pure edit distance.
> See [[ref-table-validator-and-autocomplete|Table Validator & Autocomplete]].

## Inputs & outputs

- **In:** a single `.sql`/`.ddl`/`.dbml`/`.csv` file (path). For validation: a `TABLE.FIELD`
  string or a `DQRuleSpec`.
- **Out:** a `SchemaModel` (`tables` → `SchemaTable` → `SchemaField`, plus `references` and
  `source_file`); `FieldValidation` objects carrying suggestions for the fix-it UI.

## Source

`core/schema_parser.py:90-633` — `parse_schema_file` (`:269`), `parse_ddl` (`:316`),
`_extract_balanced_parens`/`_split_column_defs` (`:433`), `parse_dbml` (`:481`),
`parse_csv_schema` (`:560`), `_map_csv_columns` (`:618`), `validate_field_ref` (`:90`),
`validate_spec_fields` (`:143`).

## See also

- [[ref-sap-baseline-model|SAP Baseline Model (logical vs physical)]] — where the ingested schema
  becomes baseline columns with `name_kind`
- [[ref-table-validator-and-autocomplete|Table Validator & Autocomplete]] — the other
  (differently-scored) suggest path, used in the table-name UI
- [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]] — defers to physical columns that
  this ingest provides
- [[ref-sap-dd-dictionary-tables|SAP DD% Dictionary Tables]] — the DD03L/DD04T sources a CSV/DDL
  extract typically comes from
- [[ref-dqrulespec-data-model|Studio — DQRuleSpec Data Model]]
- [[ref-knowledge-base-file-inventory|Studio — Knowledge Base File Inventory]]
- [[ref-building-a-per-client-dd-dictionary|Building a Per-Client DD% Dictionary]]
