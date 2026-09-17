---
id: ref-sap-key-fields-and-critical-data-elements
type: reference
title: SAP Key Fields and Critical Data Elements (CDEs)
domain: sap
audience: [consultant]
level: foundation
status: review
links:
  - relates:ref-sap-table-families
  - relates:std-zconcatenatedkey-convention
  - relates:ref-sap-modules
  - relates:ref-sap-deletion-flags-vs-status-fields
  - relates:gls-criticality
  - relates:gls-field-classification
sources:
  - vault:sap-knowledge/SAP Key Fields and Critical Data Elements.md
tags: [sap, industry-knowledge, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

The high-value fields every DQ practitioner should recognise at sight. These drive primary keys,
foreign-key checks, and the "Critical Data Element" weighting in rule criticality scoring.

## Master-data identifiers

| Field | Domain | What it identifies |
|---|---|---|
| **MATNR** | Material | Material number — PK of MARA family |
| **KUNNR** | Customer | Customer number — PK of KNA1 family |
| **LIFNR** | Vendor | Vendor number — PK of LFA1 family |
| **PERNR** | HR | Personnel number (HR module) |
| **EQUNR** | Equipment | Equipment number (PM module) |
| **OBJNR** | Object | Generic CO object number (cost element, internal order) |
| **PRCTR** | Profit Center | Profit center code (CO) |
| **KOSTL** | Cost Center | Cost center code (CO) |

## Organizational

| Field | Description |
|---|---|
| **BUKRS** | Company Code — the legal entity |
| **WERKS** | Plant — physical / logical inventory location |
| **VKORG** | Sales Organization |
| **VTWEG** | Distribution Channel |
| **SPART** | Division |
| **KOKRS** | Controlling Area |
| **GSBER** | Business Area |
| **EKORG** | Purchasing Organization |
| **LGORT** | Storage Location |
| **WAERS** | Currency Key (always 3-char ISO) |

## Financial

| Field | Description |
|---|---|
| **BELNR** | Document number (BKPF / BSEG) |
| **GJAHR** | Fiscal year |
| **BUZEI** | Line item number within a document |
| **SAKNR** | GL Account number |
| **HKONT** | GL Account (BSEG) — different code than SAKNR for historical reasons |
| **DMBTR** | Amount in local currency |
| **WRBTR** | Amount in document currency |
| **BUDAT** | Posting date |
| **BLDAT** | Document date |

## Tax + compliance

| Field | Description |
|---|---|
| **STCEG** | VAT Registration Number (often used for cross-border matching) |
| **STCD1 / STCD2** | Tax numbers 1 + 2 (country-specific format) |
| **IBAN** | International bank account number |

## Status + deletion

| Field | Role | See |
|---|---|---|
| **LVORM** | Deletion flag (master data — MARA, KNA1, LFA1) | [[con-deletion-flags-vs-status-fields\|Deletion Flags vs Status Fields]] |
| **LOEKZ** | Deletion flag (transactional — EKKO, PLKO) | [[con-deletion-flags-vs-status-fields\|Deletion Flags vs Status Fields]] |
| **LOEVM** | Deletion flag (extensions — KNB1, KNVV) | [[con-deletion-flags-vs-status-fields\|Deletion Flags vs Status Fields]] |
| **MMSTA** | Material status at plant level | [[con-deletion-flags-vs-status-fields\|Deletion Flags vs Status Fields]] |
| **PSTAT** | Customer / vendor account status | [[con-deletion-flags-vs-status-fields\|Deletion Flags vs Status Fields]] |

## Time-dependent keys

Many SAP master tables carry **DATBI** (date-to / end of validity) as part of the primary key:

| Table | Composite PK |
|---|---|
| CEPC (Profit Center) | KOKRS + PRCTR + DATBI |
| CSKS (Cost Center) | KOKRS + KOSTL + DATBI |
| CEPC_BUKRS | KOKRS + PRCTR + DATBI + BUKRS |

For "current" records, DATBI = 99991231. Older snapshots have earlier DATBIs. Rules that need
only the current record filter `WHERE DATBI = '99991231'` (date is stored as YYYYMMDD CHAR(8) in
SAP).

## Critical Data Elements (CDEs)

A subset of fields the practice classifies as **Critical Data Elements** — fields whose quality
has outsized impact on regulatory, financial, or operational outcomes. The Studio's
rule-criticality scorer weights these heavily:

```
MATNR, KUNNR, LIFNR, SAKNR, BUKRS,
STCEG, IBAN, WAERS, BUDAT, LOEVM
```

A rule that checks a CDE scores +1 per CDE in the rule's SQL (capped at +3) on the criticality
heuristic — see Studio — Rule-Name Scorer (engine).

## Related

- [[ref-sap-table-families|SAP Table Families]]
- [[std-zconcatenatedkey-convention|zConcatenatedKey Convention]]
- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]]
- [[ref-sap-deletion-flags-vs-status-fields|SAP Deletion Flags vs Status Fields]] — which flag
  sits on which table family, and the status-code catalogue
- [[ref-sap-modules|SAP Modules — FI, CO, MM, SD, PP, QM, PM]]
