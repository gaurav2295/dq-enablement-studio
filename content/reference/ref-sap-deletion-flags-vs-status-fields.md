---
id: ref-sap-deletion-flags-vs-status-fields
type: reference
title: SAP Deletion-Flag & Status-Field Catalogue
domain: sap
audience: [consultant]
level: practitioner
status: review
links:
  - relates:con-filter-presets
  - relates:ref-deletion-flag-resolver
  - relates:prn-deletion-flags-belong-in-where
  - relates:gls-loevm
  - relates:gls-lvorm
sources:
  - vault:sap-knowledge/SAP Deletion Flags vs Status Fields.md
tags: [sap, industry-knowledge]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

SAP-side lookup data only — for the WHERE-vs-CASE rule itself, see
[[con-deletion-flags-vs-status-fields]] and [[prn-deletion-flags-belong-in-where]].

## Deletion flag catalogue

| Table family | Flag column | Values |
|---|---|---|
| **MARA family** (MARA, MAKT, MARC, MARM, MBEW, MVKE) | **LVORM** | `'X'` = flagged for deletion, `' '` = active |
| **MARC** *(also)* | also has plant-specific deletion via MMSTA codes | see status section |
| **KNA1 family** (KNA1, KNB1, KNVV, KNVP, KNVI) | **LOEVM** | `'X'` = flagged for deletion. KNA1 = **LOEVM** is SAP-standard — not LVORM. |
| **LFA1 family** (LFA1, LFB1, LFM1, LFM2) | **LOEVM** | `'X'` = flagged for deletion. LFA1 = **LOEVM** is SAP-standard (central deletion flag). |
| **EKKO / EKPO** | **LOEKZ** | `'X'` = flagged for deletion, `'L'` = blocked, `'S'` = locked |
| **PLKO / PLPO** (Routings, Plans) | **LOEKZ** | `'X'` = flagged for deletion |
| **VBAK / VBAP** (sales docs) | **No master-data deletion flag** | Use ABGRU (Reason for Rejection) + status, or a **time-based filter** (see [[con-time-based-filters|Time-Based Filters]]). VBAK/VBAP/LIKP/LIPS have no fallback deletion flag — the Studio skips the deletion-flag exclusion for these tables rather than mis-filtering. |
| **BKPF** | **STBLG** (reverse document) + STJAH | A document is "reversed" if STBLG is populated |
| **LIKP / LIPS** (Deliveries) | **No standard deletion flag** | Use status fields |

## Why three different deletion-flag column names

SAP's history. LVORM dates from R/3's master data (`L`öschvor`m`erkung — "deletion notice").
LOEKZ came later for transactional documents (`L`ösch`k`ennzeichen — "deletion indicator").
LOEVM is the customer/vendor extension variant. The column names differ; the semantics are
identical: `'X'` = flagged.

## Status code references

### MMSTA (MARC) — Plant-Specific Material Status

| Code | Meaning | Typical impact |
|---|---|---|
| `' '` (blank) | Active, no restriction | Normal |
| `01` | Blocked for procurement | Cannot raise POs |
| `02` | Blocked for sales | Cannot sell |
| `03` | Blocked for production | Cannot run BOMs |
| `04` | Blocked for usage | Material cannot be used in any process |
| `05` | Plant-specific block (config) | Per-client meaning |

Codes 01-05 are SAP-delivered defaults; specific clients add custom Z-codes via customising (T141
/ T141T). Always check the client's `T141` table for the actual code list in use.

### MSTAE (MARA) — Cross-Plant Material Status

Same structure as MMSTA but applies cross-plant. Configured via T141 too. If MSTAE is populated,
the material is blocked everywhere (regardless of MMSTA per plant).

### PSTAT — Account Status (KNA1, LFA1)

Per-block status indicator. Values are tenant-specific (T077Y / T077X for customer/vendor account
groups). A non-blank PSTAT typically means an account is in setup, under approval, or
partially-extended (e.g. exists at KNA1 level but missing KNVV records).

## How to discover deletion + status fields for an unfamiliar table

1. **Studio metadata** — `knowledge/sap/table_metadata.json` carries the deletion flag for 87
   known tables
2. **DD03L lookup** — query DD03L for the table where FIELDNAME matches LVORM / LOEKZ / LOEVM /
   `?STA?`
3. **SE11 / DD03L domain check** — the data element's domain often hints (DOM_DELFLAG, etc.)

> [!tip]
> When a Z*/Y* customer table has no obvious deletion flag, default to `no_filter` and ask the
> client's MDM team — they often have a custom flag (`Z_AKTIV`, `STATUS_FLAG`, etc.).

## Related

- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]] — the methodology rule
- [[con-filter-presets|Filter Presets]] — `auto_active` uses these
- Studio — Schema Profiler (engine)
- [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]]
