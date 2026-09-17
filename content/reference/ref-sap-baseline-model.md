---
id: ref-sap-baseline-model
type: reference
title: SAP Baseline Model (logical vs physical)
domain: sap
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-sap-dd-dictionary-tables
  - relates:ref-deletion-flag-resolver
  - relates:ref-sap-deletion-flags-vs-status-fields
sources:
  - vault:sap-knowledge/SAP Baseline Model (logical vs physical).md
tags: [sap, engine, methodology]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

The Studio keeps one internal reference of SAP table structure — tables, primary keys, foreign
keys, and columns — built from multiple sources, so every rule-generation path agrees on the same
facts about a table's shape.

## Logical vs. physical names

SAP metadata can describe a table's columns in two ways:

- **Logical** — a business-English name (e.g. "Customer Number"), coming from a baseline data
  model.
- **Physical** — the actual SAP database column name (e.g. `KUNNR`), confirmed from the customer's
  own SAP dictionary extract.

Column-existence checks only trust **physical** names — a logical name alone isn't enough to
confirm a specific column like `LVORM` actually exists on a table. Until a customer's own
dictionary extract has been loaded for a table, that table's column list is treated as unconfirmed
for this purpose.

### Three contributing sources

| Source | Contributes | Name kind |
|---|---|---|
| A baseline SAP data model | standard ECC structure: tables + keys + business-key attributes | logical (English names) |
| The customer's own SAP dictionary extract | confirmed **physical** column names — e.g. `KUNNR`, `MATNR`, `LVORM` | physical |
| Project overrides | custom Z/Y tables and per-customer extensions, declared per project | either |

## Who relies on this

- **[[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]]** — only trusts a table's
  deletion-flag column once physical confirmation is available for that table; logical names alone
  can't confirm a specific column like `LVORM`/`LOEVM`/`LOEKZ`.
- **SAP Metadata Validators (Pillars A & B)** — cross-checks
  curated SAP reference data against this baseline, catching cases where the two disagree.
- **Table Validator & Autocomplete**,
  Studio — DQRuleSpec Data Model, and the SQL generators that need
  real physical column names.

> [!tip] KNA1 and LFA1 deletion flag
> `KNA1` and `LFA1` use `LOEVM` as their deletion flag — this is treated as the SAP standard for
> these two tables (not something that varies by customer), even though a customer's own dictionary
> extract can confirm or override it for a genuinely custom build.

## Related

- [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]]
- [[ref-sap-deletion-flags-vs-status-fields|SAP Deletion Flags vs Status Fields]]
- SAP Metadata Validators (Pillars A & B)
- Table Validator & Autocomplete
- Schema Ingestion (DDL-DBML-CSV)
- [[ref-sap-dd-dictionary-tables|SAP DD% Dictionary Tables]]
- [[ref-building-a-per-client-dd-dictionary|Building a Per-Client DD% Dictionary]]
