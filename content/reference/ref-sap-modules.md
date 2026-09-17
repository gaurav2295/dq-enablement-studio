---
id: ref-sap-modules
type: reference
title: SAP Modules — FI, CO, MM, SD, PP, QM, PM
domain: sap
audience: [consultant]
level: foundation
status: review
links:
  - relates:ref-sap-table-families
  - relates:ref-sap-key-fields-and-critical-data-elements
  - relates:ref-sap-business-processes
  - relates:ref-sap-data-domains
sources:
  - vault:sap-knowledge/SAP Modules — FI, CO, MM, SD, PP, QM, PM.md
tags: [sap, industry-knowledge]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

The seven core SAP modules our DQ rules typically touch. Knowing which module a table belongs to
is the fastest way to triage a rule into the right domain + remediation team.

| Module | Full name | Owns | Key tables |
|---|---|---|---|
| **FI** | Financial Accounting | The general ledger, AP, AR — the external-facing financials | BKPF, BSEG, BSIK, BSID, T001 |
| **CO** | Controlling | Internal cost accounting — cost centers, profit centers, internal orders | CEPC, CEPCT, CSKS, CSKSZ, COBK, COEP, TKA01 |
| **MM** | Materials Management | Material master, purchasing, inventory | MARA, MAKT, MARC, MARM, MBEW, EKKO, EKPO, EBAN |
| **SD** | Sales and Distribution | Customer master, sales orders, deliveries, billing | KNA1, KNB1, KNVV, VBAK, VBAP, LIKP, LIPS, VBRK |
| **PP** | Production Planning | BOMs, routings, work centers, production orders | MAST, STKO, STPO, PLKO, PLPO, AFKO, AFPO |
| **QM** | Quality Management | Inspection plans, results, quality info records | PLKO (Q-type), QALS, QAVE, QAMR |
| **PM** | Plant Maintenance | Equipment, functional locations, work orders | EQUI, IFLOT, AUFK (PM-orders), VIQMEL |

## Cross-module entities

| Entity | Lives in | Referenced by |
|---|---|---|
| **Customer (KUNNR)** | SD (KNA1) | FI (AR — BSID), CO (PA), SD (orders, deliveries) |
| **Vendor (LIFNR)** | MM (LFA1) | FI (AP — BSIK), MM (EKKO purchase orders) |
| **Material (MATNR)** | MM (MARA) | SD (orders), PP (BOMs), QM (inspection plans), MM (POs, stock) |
| **Company code (BUKRS)** | FI (T001) | All modules — every transactional table |
| **Cost center (KOSTL)** | CO (CSKS) | FI (postings via account-assignment), MM, SD |
| **Profit center (PRCTR)** | CO (CEPC) | Same cross-module reach as cost center |

## Why the module matters

- **Stewardship** — most clients structure their MDM teams by module. Material master defects →
  MM team. Customer master → SD team. Postings reconciliation → FI team.
- **Reference data** — module-specific tables (T001 / KNA1 / MARA) define the universe a rule
  applies to. The Studio tracks each table's module so it picks the right domain automatically
  when deriving a rule.
- **Time-of-day** — overnight batch jobs typically run module-by-module. A DQ rule covering MARA
  shouldn't depend on FI postings being current; they may not be at 3am.

## Module → domain mapping

| Module | Typical [[ref-sap-data-domains|domain]] |
|---|---|
| FI | Finance, Accounting Documents |
| CO | Controlling, Cost Accounting |
| MM | Material Master, Purchasing |
| SD | Customer Master, Sales |
| PP | BOM, Routing, Production |
| QM | Quality Inspection |
| PM | Equipment, Maintenance |

## Related

- [[ref-sap-table-families|SAP Table Families]]
- [[ref-sap-key-fields-and-critical-data-elements|SAP Key Fields and Critical Data Elements]]
- [[ref-sap-business-processes|SAP Business Processes — O2C, P2P, R2R]]
