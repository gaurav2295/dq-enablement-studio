---
id: ref-sap-data-domains
type: reference
title: SAP Data Domains
domain: sap
audience: [consultant]
level: foundation
status: review
links:
  - relates:ref-sap-business-processes
  - relates:ref-sap-modules
  - relates:ref-sap-table-families
  - relates:ref-local-deriver
sources:
  - vault:sap-knowledge/SAP Data Domains.md
tags: [sap, industry-knowledge]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

A finer-grained classification than [[ref-sap-business-processes|SAP Business Processes —
O2C, P2P, R2R]] — 103 domains in the Studio's `knowledge/methodology/data_domains.json`. Used to
bucket a rule into the right knowledge subset during derivation.

## The top-level domains

| Domain | Typical scope | Anchor tables |
|---|---|---|
| **Material Master** | Cross-plant material data | MARA, MAKT, MARC, MARM, MBEW, MVKE |
| **Customer Master** | Customer data across org levels | KNA1, KNB1, KNVV, KNVP, ADRC |
| **Vendor Master** | Vendor data across org levels | LFA1, LFB1, LFM1, LFM2 |
| **GL Master** | Chart of accounts, GL configuration | SKA1, SKAT, SKB1 |
| **Cost Center Master** | Cost centers + descriptions | CSKS, CSKSZ |
| **Profit Center Master** | Profit centers + descriptions | CEPC, CEPCT |
| **Accounting Documents** | FI postings (header + line) | BKPF, BSEG, BSIK, BSID |
| **Sales Documents** | Orders, quotes, contracts | VBAK, VBAP, VBUK, VBUP |
| **Purchasing Documents** | POs, requisitions, contracts | EKKO, EKPO, EBAN |
| **Goods Movements** | Inventory transactions | MSEG, MKPF |
| **Inspection Plans** | QM plans + operations | PLKO, PLPO (Q-type) |
| **BOMs** | Bills of material | MAST, STKO, STPO |
| **Routings** | Production routings | PLKO, PLPO (N-type) |
| **Equipment Master** | PM equipment | EQUI, IFLOT |
| **Configuration / Reference** | T-tables | T001, T024, T141, T077D, … |

## Sub-domains

Inside Material Master, for example, you have sub-domains for:

- Material Numbers (anchor: MARA.MATNR)
- Material Descriptions (anchor: MAKT)
- Material Valuation (anchor: MBEW)
- Plant-Specific Data (anchor: MARC)
- Units of Measure (anchor: MARM)

The Studio's [[ref-local-deriver|local deriver]] matches rule names to specific sub-domains via
keyword scoring, then picks the right anchor table from there.

## Why a domain taxonomy

Two reasons:

1. **Deriver disambiguation** — *"A customer must have a valid country"* could land on
   KNA1.LAND1 OR KNB1.LAND1; the domain (Customer Master) anchors it to KNA1 by default
2. **Stewardship routing** — clients organise data stewards by domain. A defect in Material
   Valuation goes to a different team than one in Customer Master

## In the Studio

`knowledge/methodology/data_domains.json` carries:

```json
{
  "Material Master": {
    "module": "MM",
    "keywords": ["material", "MATNR", "MARA", "product"],
    "anchor_tables": ["MARA", "MAKT", "MARC"],
    "stewardship": "Material Master Team"
  },
  …
}
```

The deriver scores a rule name against each domain's keyword list, picks the highest-scoring
match, and sets `spec.data_domain = "Material Master"`.

## Related

- [[ref-sap-modules|SAP Modules — FI, CO, MM, SD, PP, QM, PM]]
- [[ref-sap-business-processes|SAP Business Processes — O2C, P2P, R2R]]
- [[ref-sap-table-families|SAP Table Families]]
- [[ref-local-deriver|Local Deriver]]
