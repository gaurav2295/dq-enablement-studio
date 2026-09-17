---
id: ref-deletion-flag-resolver
type: reference
title: Deletion Flag Resolver (3-tier)
domain: sap
audience: [developer]
level: advanced
status: review
links:
  - prereq:ref-sap-baseline-model
  - relates:ref-sap-deletion-flags-vs-status-fields
  - relates:ref-local-deriver
sources:
  - vault:sap-knowledge/Deletion Flag Resolver (3-tier).md
tags: [studio, engine, sap, agent, course]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

The Studio automatically determines which column marks a row as logically deleted on a given SAP
table, rather than requiring you to look it up or guess it per rule.

This is the SAP-side knowledge behind the methodology rule in
[[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]] and the catalogue in
[[ref-sap-deletion-flags-vs-status-fields|SAP Deletion Flags vs Status Fields]].

## What it does

Resolves the single column that flags a row as logically deleted — one of `LVORM`, `LOEVM`, or
`LOEKZ`, depending on the table and the customer's ECC build. The Studio uses the answer to emit an
**exclusion** filter (deleted rows are excluded from the rule's universe), never an error condition
— see [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]].

## How it resolves the flag

The Studio checks, in order:

1. **The customer's own SAP dictionary extract**, when one has been loaded for that table — this
   confirms which of the known column names actually exists on the customer's system.
2. **Curated domain knowledge** maintained for the relevant business domain.
3. **A standard SAP fallback list** covering the common table families (below), used as a last
   resort when neither of the above has an answer.

> [!note] Customer metadata confirms, it isn't the source of the standard
> The customer-dictionary check doesn't *invent* the flag — it confirms which of the known column
> names the customer's own system actually has. The standard SAP registry is the source of truth;
> customer metadata confirms or overrides it.

When a table physically carries more than one deletion-flag column (rare), the Studio prefers
`LVORM` over `LOEVM` over `LOEKZ` — `LVORM` is the most common on master-data headers.

## Standard flag by table family

| Family | Tables → flag |
|---|---|
| Master-data headers | KNA1 → LOEVM, LFA1 → LOEVM (SAP-standard), MARA → LVORM |
| Customer/vendor views | KNB1, KNVV, KNVP, LFB1, LFM1 → LOEVM |
| Material views | MARC, MARD, MVKE → LVORM |
| Inspection plan family | PLKO, PLAS, PLPO → LOEKZ |
| Purchasing | EKKO, EKPO, EBAN, EINA, EINE → LOEKZ |
| Sales | VBAK, VBAP, LIKP, LIPS have no master-data deletion flag — no exclusion filter applies. A time-based scope is available instead, see [[con-time-based-filters|Time-Based Filters]] |

Convention: mostly `LVORM` on master headers, `LOEVM` on view tables, `LOEKZ` on transactional
plan/order tables.

## KNA1 and LFA1

`KNA1` and `LFA1` use `LOEVM` as their deletion flag — this is treated as the SAP standard for
these two tables, not something that varies by customer.

## If no flag is found

An empty result means "no deletion flag for this table — skip the exclusion filter," not an error.

## Related

- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]] — the methodology rule
  (exclusion filter vs error logic)
- [[ref-sap-deletion-flags-vs-status-fields|SAP Deletion Flags vs Status Fields]] — the full SAP
  column catalogue + status codes
- [[ref-sap-baseline-model|SAP Baseline Model (logical vs physical)]] — the logical/physical
  distinction this resolver depends on
- Deletion Flag Normalization in SQL Gen — how the
  resolved flag becomes a WHERE clause
- SAP Metadata Validators (Pillars A & B)
- [[con-time-based-filters|Time-Based Filters]]
- [[ref-local-deriver|Local Deriver]]
- [[ref-value-description-resolution|Value-Description Resolution (4 mechanisms)]]
- Knowledge Base File Inventory
