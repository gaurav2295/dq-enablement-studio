---
id: ref-ecc-vs-s-4hana
type: reference
title: ECC vs S/4HANA
domain: sap
audience: [consultant]
level: foundation
status: review
links:
  - relates:ref-sap-table-families
  - relates:ref-sap-key-fields-and-critical-data-elements
sources:
  - vault:sap-knowledge/ECC vs S-4HANA.md
tags: [sap, industry-knowledge]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

What's different, what's the same — practical implications for DQ rule authoring across both
platforms.

## What carries over (most of it)

Most SAP tables and field names are **identical** between ECC and S/4HANA:

- MARA, KNA1, LFA1, BKPF, BSEG, EKKO, VBAK — all carry over with the same PKs
- Customer / vendor / material concepts unchanged
- Most DQ rules written for ECC work as-is on S/4HANA

The Studio has separate knowledge files (`knowledge/erp/sap_ecc/` and
`knowledge/erp/sap_s4hana/`) but the contents are ~85% overlapping.

## Where S/4HANA differs

### Customer + Vendor → Business Partner

S/4HANA merges customer and vendor into a unified **Business Partner** model:

| ECC | S/4HANA |
|---|---|
| KNA1 (customer) + LFA1 (vendor) | **BUT000** (business partner) |
| KNVV (customer-sales view) | BUT0CC (BP role + assignment) |
| LFM1 (vendor-purchasing) | BUT0CC + BUT_HIER |

Old KNA1 / LFA1 still exist as *compatibility views* in S/4HANA — your rules continue to work —
but the underlying truth lives in BUT000+. For new rules on S/4, target BUT000 directly when the
rule cares about cross-role BP attributes.

### Financial postings — Universal Journal (ACDOCA)

S/4HANA collapses BKPF + BSEG + CO postings (COEP) + asset postings (ANEK/ANEP) + material
postings (MLDOC) into one table: **ACDOCA** ("Universal Journal").

| ECC | S/4HANA |
|---|---|
| BKPF + BSEG (FI) | **ACDOCA** |
| COEP (CO) | ACDOCA |
| MLDOC (material ledger) | ACDOCA |
| Reconciliation between sub-ledgers | Eliminated |

For DQ rules:

- Old BKPF/BSEG queries still work on S/4 via compatibility views
- New rules targeting cost / margin / profit reporting should hit ACDOCA directly
- Reconciliation rules (FI ↔ CO) become trivial on S/4 — they're the same row

### Material number (MATNR) length

- **ECC**: MATNR is `CHAR(18)` — max 18 characters
- **S/4HANA**: MATNR extended to `CHAR(40)` — max 40 characters

For rules with hardcoded MATNR comparisons, the length difference matters in two places:

- WHERE-clause IN-lists — long MATNRs from S/4 won't fit ECC's 18-char column
- View output column widths — declare NVARCHAR(40) for cross-platform views

### MMSTA, status fields

Same fields, same codes — but the customising (T141) may differ between platforms. Always check
the active T-table for the actual codes in use.

## Customising tables, the same on both

- T001 (company code), T024 (purchasing group), T141 (material status), T077D (customer account
  group) — same across both platforms
- ECC + S/4 share the same data element + domain catalogue, so DD04T descriptions are stable

## What's S/4HANA-only

- **Embedded analytics** — CDS views, Fiori KPIs — these aren't tables in the traditional sense;
  DQ on them happens at the CDS view layer, not the underlying base table
- **In-memory side-effects** — some long-running batch jobs on ECC don't exist on S/4 because the
  same logic runs at query time in HANA; their absence doesn't mean a defect

## Project YAML — which to load

```yaml
erp: sap_ecc       # → Studio loads knowledge/erp/sap_ecc/
erp: sap_s4hana    # → Studio loads knowledge/erp/sap_s4hana/
```

The Studio's knowledge engine respects this — same code paths, different reference data. See
Studio — Architecture Context & Project YAMLs.

## Related

- [[ref-sap-table-families|SAP Table Families]]
- [[ref-sap-key-fields-and-critical-data-elements|SAP Key Fields and Critical Data Elements (CDEs)]]
- Studio — Architecture Context & Project YAMLs
