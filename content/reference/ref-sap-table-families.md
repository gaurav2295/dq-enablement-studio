---
id: ref-sap-table-families
type: reference
title: SAP Table Families
domain: sap
audience: [consultant]
level: foundation
status: review
links:
  - relates:ref-sap-modules
  - relates:ref-sap-key-fields-and-critical-data-elements
  - relates:std-zconcatenatedkey-convention
  - relates:ref-ecc-vs-s-4hana
  - relates:gls-reference-data
sources:
  - vault:sap-knowledge/SAP Table Families.md
tags: [sap, industry-knowledge]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

The most common SAP tables, grouped by entity family. The Studio recognises 224 tables in its ECC
registry; this note documents the ~30 you'll touch most often.

## Material Master (MARA family)

| Table | Grain | Description |
|---|---|---|
| **MARA** | Material | Cross-plant material master — the base record |
| **MAKT** | Material × Language | Material descriptions (one row per language) |
| **MARC** | Material × Plant | Plant-specific material data (MMSTA, MRP, stock indicator) |
| **MARM** | Material × UoM | Alternative units of measure |
| **MBEW** | Material × Plant × Valuation Area | Material valuation (standard cost, moving avg) |
| **MVKE** | Material × Sales Org × Distribution Channel | Sales view |
| **MLAN** | Material × Country | Tax classification per country |

Primary key root: **MATNR**. Composite keys layer additional dimensions (SPRAS, WERKS, VKORG,
etc.).

## Customer Master (KNA1 family)

| Table | Grain | Description |
|---|---|---|
| **KNA1** | Customer | Cross-org customer master — the base record |
| **KNB1** | Customer × Company Code | Company-code-specific (recon account, payment terms) |
| **KNVV** | Customer × Sales Org × Dist Channel × Division | Sales-org-specific (customer group, currency) |
| **KNVP** | Customer × Partner | Partner functions (SP, BP, PY, SH) |
| **KNVI** | Customer × Country | Tax-indicator-per-country |
| **KNB5** | Customer × Company Code | Dunning data |
| **ADRC** | Address ID | Centralised addresses (referenced by KNA1.ADRNR) |

Primary key root: **KUNNR**. Note that KNVP / KNVI carry composite keys with partner counter etc.

## Vendor Master (LFA1 family)

Mirror of the customer family:

| Table | Grain | Equivalent of |
|---|---|---|
| **LFA1** | Vendor | KNA1 |
| **LFB1** | Vendor × Company Code | KNB1 |
| **LFM1** | Vendor × Purchasing Org | KNVV |
| **LFM2** | Vendor × Purchasing Org × WERKS | Plant-specific vendor data |

Primary key root: **LIFNR**.

## Financial Accounting (BKPF / BSEG)

| Table | Grain | Description |
|---|---|---|
| **BKPF** | Document Header | One row per posting document — BUKRS + BELNR + GJAHR |
| **BSEG** | Document Line Item | One row per line — adds BUZEI |
| **BSIK** | Open AP Items | Vendor open items snapshot |
| **BSID** | Open AR Items | Customer open items snapshot |
| **BSAK** | Cleared AP Items | History of cleared vendor items |
| **BSAD** | Cleared AR Items | History of cleared customer items |
| **T001** | Company Code | Reference data — company code master |
| **SKA1 / SKAT** | GL Account / Descriptions | Chart of accounts |

Primary key: **BUKRS + BELNR + GJAHR** (header), add **BUZEI** for line item.

## Purchasing (EKKO / EKPO)

| Table | Grain | Description |
|---|---|---|
| **EKKO** | PO Header | Purchase order header (vendor, currency, doc type) |
| **EKPO** | PO Line Item | One row per PO line (material, qty, plant) |
| **EKBE** | PO History | Goods receipts, invoices per line item |
| **EBAN** | Purchase Requisition | Requisitions before POs are created |

Primary key: **EBELN** (header), **EBELN + EBELP** (line).

## Sales (VBAK / VBAP)

| Table | Grain | Description |
|---|---|---|
| **VBAK** | Sales Doc Header | Sales orders (and quotes / contracts via VBTYP) |
| **VBAP** | Sales Doc Line Item | One row per line (material, qty, customer) |
| **LIKP / LIPS** | Delivery header / line | Same shape as orders, for outbound deliveries |
| **VBRK / VBRP** | Billing header / line | Invoices |
| **VBUK / VBUP** | Doc status (header / item) | Status flags per sales doc |

Primary key: **VBELN** (header), **VBELN + POSNR** (line).

## Controlling (CEPC / CSKS)

| Table | Grain | Description |
|---|---|---|
| **CEPC** | Profit Center | Cross-CO-area profit center master (KOKRS + PRCTR + DATBI) |
| **CEPCT** | Profit Center Description | Per-language (SPRAS) |
| **CSKS** | Cost Center | KOKRS + KOSTL + DATBI |
| **CSKSZ** | Cost Center Description | Per-language |
| **TKA01** | Controlling Area | The CO-area master |

Primary keys are **time-dependent** (DATBI is the end-date) — there's typically one CURRENT
record per entity plus historical ones.

## Configuration tables (T-tables)

Lots of T- prefixed reference tables: T001 (company code), T024 (purchasing group), T077D
(customer account group), T501 (employee subgroup). The Studio's table registry tags these as
`reference` so the deriver knows they're descriptive, not transactional.

## Related

- [[ref-sap-modules|SAP Modules — FI, CO, MM, SD, PP, QM, PM]]
- [[ref-sap-key-fields-and-critical-data-elements|SAP Key Fields and Critical Data Elements]]
- [[std-zconcatenatedkey-convention|zConcatenatedKey Convention]] — uses the primary key recipe
  per table
- [[ref-ecc-vs-s-4hana|ECC vs S/4HANA]] — which of these families change shape on S/4HANA
