---
id: ref-sap-business-processes
type: reference
title: SAP Business Processes — O2C, P2P, R2R
domain: sap
audience: [consultant]
level: foundation
status: review
links:
  - relates:ref-sap-modules
  - relates:ref-sap-data-domains
  - relates:ref-local-deriver
sources:
  - vault:sap-knowledge/SAP Business Processes — O2C, P2P, R2R.md
tags: [sap, industry-knowledge]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

Three top-level end-to-end processes that recur in every SAP engagement. Knowing which one a rule
sits inside drives stakeholder alignment, remediation prioritisation, and the SKP Category
column.

## Order-to-Cash (O2C)

The revenue-side flow: from customer order to cash collected.

```
Customer master → Sales order → Delivery → Billing → AR posting → Cash receipt
   (KNA1)         (VBAK/VBAP)   (LIKP/LIPS)  (VBRK/VBRP)  (BKPF/BSEG-BSID)  (BSAD)
```

**Modules involved:** SD (primary), FI (AR), MM (inventory consumption from delivery), CO (margin
reporting)

**Typical DQ rules:**

- Customer has valid VAT registration / EU country
- Customer has consistent currency between KNA1, KNB1, KNVV
- Sales order references an active material
- Delivery exists for every released sales order line
- Billing document has a valid GL account assignment

## Procure-to-Pay (P2P)

The supply-side flow: from purchase requisition to vendor paid.

```
Vendor master → Purchase requisition → PO → Goods receipt → Invoice → AP posting → Payment
   (LFA1)         (EBAN)              (EKKO/EKPO) (MSEG)   (RBKP/RSEG)  (BKPF/BSEG-BSIK)  (BSAK)
```

**Modules involved:** MM (primary), FI (AP), CO (cost accounting when GR posts), QM (inspection
on receipt)

**Typical DQ rules:**

- Vendor has valid bank account (IBAN)
- Vendor has tax registration appropriate for country
- PO references a deletion-flagged material (defect)
- Invoice three-way match (PO + GR + Invoice) reconciles
- GR posted but invoice missing > 30 days

## Record-to-Report (R2R)

The financial close + reporting flow.

```
Sub-ledger postings → GL postings → Period close → Trial balance → Reports / disclosures
                       (BKPF/BSEG)      (T009Y)
```

**Modules involved:** FI (primary), CO (cost allocations), all modules feed in

**Typical DQ rules:**

- Posting in a closed period (FI gate violation)
- GL account in BSEG doesn't exist in SKA1
- Company code in BKPF doesn't exist in T001
- Tax balance reconciles to ledger
- Inter-company postings have matching counterparties

## Why three processes, not more

Most SAP DQ initiatives map naturally to one of these three at the top level. Sub-processes
(e.g. "Master Data Governance", "Logistics") are flows *within* one of these three rather than
separate top-level processes.

## In rule metadata

The spec's `business_process` field carries one of these three values. The Studio's
[[ref-local-deriver|local deriver]] picks it via keyword heuristics:

- Keywords like *order*, *customer*, *sales*, *delivery*, *billing*, *revenue* → O2C
- Keywords like *vendor*, *purchase*, *PO*, *goods receipt*, *invoice*, *payment* → P2P
- Keywords like *GL*, *journal*, *close*, *reconcile*, *trial balance*, *posting* → R2R

Manual override always allowed.

## Related

- [[ref-sap-modules|SAP Modules — FI, CO, MM, SD, PP, QM, PM]]
- [[ref-sap-data-domains|SAP Data Domains]]
- [[con-cleanse-action-categorization|Cleanse Action Categorization]]
- [[ref-local-deriver|Local Deriver]]
