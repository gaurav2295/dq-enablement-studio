---
id: qa-metadata-quality-validation
type: qa
title: How is metadata quality validated?
domain: sap
audience: [consultant, lead]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-04
created: 2026-09-07
updated: 2026-09-07
---

## Question

The [[ref-sap-deletion-flags-vs-status-fields|deletion-flag catalogue]] lists which columns 
are deletion flags for which tables (LVORM for MARA, LOEKZ for EKKO, etc.). But how do we 
know these mappings are correct and current? What if a client has custom fields? What if 
an SAP patch changes things?

## Answer

**Three validation layers:** pre-engagement audit, per-engagement verification, and ongoing monitoring.

### 1. Pre-engagement metadata audit

Before the engagement starts:

- **SAP version check** — confirm the client's SAP release (ECC 6.0, S/4HANA 2021, etc.)
  Deletion flags are remarkably stable, but confirm with the client's Basis team
  
- **Client customizing check** — query the client's T141 (MMSTA codes), T077Y/T077X (PSTAT codes)
  to see if they have custom status fields (Z_AKTIV, STATUS_FLAG, etc.)
  
- **Table discovery** — run SE11 queries against the client's DD03L to verify field names
  Example: "Does MARA have LVORM?" → `SELECT * FROM DD03L WHERE TABNAME = 'MARA' AND FIELDNAME = 'LVORM'`
  
Result: **engagement-specific metadata snapshot** is captured in the Studio project config.

### 2. Per-engagement verification

During rule authoring and audit:

- **Profiler discovery** — When the profiler runs, it samples 100+ rows from each table
  and checks: "Does this field actually have the expected values?" 
  Example: LVORM on MARA should contain only `'X'` or `' '`. If you see `'Y'`, `'1'`, `NULL`, 
  something is wrong.
  
- **DBA spot-check** — During rule audit, the DBA runs a quick sanity check:
  ```sql
  SELECT DISTINCT LVORM FROM MARA_Stage;
  -- Should return: 'X', ' ' (and maybe NULL)
  -- If returns: 'X', 'Y', '1', 'UNKNOWN' → escalate
  ```
  
- **Validation script** — Before rules deploy, a metadata-validator script confirms:
  - "This table uses LVORM for deletion" ✓
  - "Values are only 'X' or blank" ✓
  - "No nulls in the deletion flag" ✓
  
  If validation fails, the rule is marked `_review_required`.

### 3. Ongoing monitoring

After deployment:

- **Defect rate drift** — If a rule's defect rate suddenly jumps 10x (from 2% to 20%), 
  it may signal that the deletion flag stopped working as expected. Investigate.
  
- **Client notification** — If the client installs a major SAP patch, ask the Basis team:
  "Did deletion flags change?" Update metadata as needed.
  
- **Annual refresh** — Once a year (or after a client upgrade), re-run the pre-engagement 
  metadata audit to catch drift.

### When metadata is uncertain

If you cannot verify a deletion flag:

- **Don't guess** — if LVORM is missing from MARA in the client's DD03L, 
  do not assume it's called Z_DELETION or STATUS_FLAG. Ask.
  
- **Use `no_filter`** — Tell the Studio to skip the deletion-flag exclusion for that table
  in the rule's `where_filters` config. The rule will still work; it just won't exclude 
  deleted records (which you can note in the rule description: "includes deleted records").
  
- **Document the gap** — Add a comment: `/* TODO: verify LVORM with client Basis team */`
  Rule marked `_review_required` until confirmed.

> [!tip]
> **Metadata is only as good as the engagement's SAP version and customizing.** Verify once, 
> monitor continuously, update on major changes. Don't assume stale; always ask.
