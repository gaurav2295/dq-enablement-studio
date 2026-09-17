---
id: ref-knowledge-base-file-inventory
type: reference
title: Knowledge Base File Inventory
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - parent:ref-architecture-context-and-project-yamls
  - relates:ref-local-deriver
  - relates:ref-rule-name-scorer
  - relates:std-rule-name-heuristics
  - relates:ref-sap-baseline-model
  - relates:ref-value-description-resolution
sources:
  - vault:studio-architecture/Studio — Knowledge Base File Inventory.md
tags: [studio, engine, methodology, sap, knowledge]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

Studio's intelligence lives in the `knowledge/` JSON tree, split three ways — `erp/<erp_id>/`
(per-ERP plug-ins), `methodology/` (ERP-neutral naming, scoring & domain maps), and `sap/` (the
"Pillar B" SAP authority) — with hand-confirmed record counts: 8 ECC domains, 38 joins, 41 PKs, 43
composite keys, 224 registry tables, 103 data domains, 711 business-process entries, 19
heuristics, and a 276-table / 10,644-column ECC baseline.

This is the data side of [[ref-architecture-context-and-project-yamls]]. The engine code that
loads and queries these files is `core/knowledge_engine.py`; the project YAMLs select which ERP
plug-in is active.

## The three-way split

| Tree | Purpose | ERP-specific? |
|---|---|---|
| `knowledge/erp/<erp_id>/` | Per-ERP plug-in: domains, joins, keys, table registry | Yes — `sap_ecc`, `sap_s4hana` |
| `knowledge/methodology/` | Naming conventions, rule-name scoring, domain & business-process maps, AUA org-dimensions | No (ERP-neutral) |
| `knowledge/sap/` | Curated SAP runtime authority — table metadata, column descriptions, value lookups, typed baseline | SAP-wide, "Pillar B" |

Plus three roots outside the split: `knowledge/architecture/` (layered data-flow model),
`knowledge/catalogs/` (the AI rule catalog), and `knowledge/sap_master_tables.json` (header-table
priority for `zDomainSegment`).

## erp/sap_ecc/ — the active plug-in (6-file contract)

Every ERP plug-in honours a fixed 6-file contract. ECC counts (parsed 2026-06-30):

| File | Holds | ECC count | S/4 count |
|---|---|---|---|
| `config.json` | erp_id, display, `custom_table_prefixes ["Z","Y"]` | — | — |
| `domains.json` | business domains (mainTable, keyField, deletionFlags, keywords, orgScopes, inclusionFilters, fieldScopes, fields) | **8** | 7 |
| `joins.json` | source/target/key/cardinality/description | **38** | 16 |
| `primary_keys.json` | table → single join-key-to-parent string | **41** | 24 |
| `composite_keys.json` | table → full row-uniqueness key array | **43** | 23 |
| `table_registry.json` | `{name, description, module, category}` | **224 actual** | 51 |

> [!tip] Implementation status — resolved 2026-07-01 (KNOWN-ISSUES B11/B12)
> `table_registry.json` `_meta.table_count` was corrected from **210** to **224** to match the
> array length, so meta is now authoritative.

The 8 ECC domains: material, customer, vendor, gl_account, asset, purchase_order,
purchasing_info, sales_order. S/4 replaces customer/vendor with `business_partner` (BUT000) and
moves finance onto `ACDOCA` (Universal Journal). See [[ref-sap-baseline-model]].

**Two key files, two semantics** (do not conflate): `primary_keys.json` = the *single* field
linking a table to its parent (e.g. KUNNR for all customer-hierarchy tables); `composite_keys.json`
= the *full* uniqueness key used to build `zConcatenatedKey` and PrfSel drill-through columns.
MANDT is **intentionally excluded** from `composite_keys.json` (single-working-DB → MANDT
constant → key noise).

## methodology/ — ERP-neutral maps

| File | Holds | Count |
|---|---|---|
| `heuristics.json` | rule-name scoring heuristics (regex/pattern + weight) | **19** — see [[std-rule-name-heuristics]] |
| `data_domains.json` | domain → `{ot, bp, cx}` (object type / process / complexity) | **103** |
| `business_processes.json` | subject area → process → object → sub-process → dataset | **711** (19 subject areas, 64 processes, 117 objects) |
| `org_dimensions.json` | per-table org-dimension breakdowns for AUA | 30 tables |
| `view_conventions.json` | OptSel/RptSel defs + `{desc}` keyword-extraction | 2 views |

`data_domains.json` example: `"Material Master": {"ot":"Master","bp":"Cross-Process","cx":"H"}`.
(Carries a known typo `"Quality Managemnt"` on QM rows — kept for back-compat.)

## sap/ — the "Pillar B" SAP authority

| File | Holds | Count |
|---|---|---|
| `table_metadata.json` | runtime catalog: module, `deletion_flag`, primary_keys (incl. MANDT), `common_filters` | **85 tables** |
| `column_descriptions.json` | `{COLUMN: plain-English}`, `TABLE.COL` override precedence | **334 columns** |
| `attribute_value_lookups.json` | field → value-description lookup for AUA LEFT JOINs | **236 fields** |
| `sap_ecc_baseline.json` | typed source-neutral SAP-ECC logical model (Erwin XML + DD03L) | **276 tables, 10,644 columns** (487 logical + 10,157 physical) |
| `customer_redactions.txt` | redacted customer-identifier tokens | 18 lines |

`attribute_value_lookups` mechanisms (see [[ref-value-description-resolution]]): `check_table`
(46), `single_lang_text` (6), `domain_fixed_values` (103), `self_describing` (81).
`table_metadata`'s primary_keys **include MANDT** — opposite of `composite_keys.json`, because
it's a different consumer.

> [!tip] Implementation status (B1 — KNA1 deletion flag) — resolved 2026-07-01
> The app now emits **KNA1 & LFA1 = LOEVM** (SAP-standard) consistently across the resolver,
> registry, metadata, and domains; the baseline DD% path is override-only. KNA1 = LOEVM is
> SAP-standard, not customer-specific. Resolution order is baseline DD% (override-only) → domain
> definition → standard registry — see [[ref-deletion-flag-resolver]].

## architecture/ + catalogs/ + root master file

- `architecture/data_flow.json` — 6-layer model (source_systems, snapshots
  `SRECC{system}{batch}`, prep `WRKDQPREP_ALL`, utilities, working `WRKDQ` = the only
  `rule_target`, skp); 4-step promotion path; `supports_multi_source_union_all: false`. Single
  source of topology for [[ref-three-database-architecture]].
- `catalogs/syniti_ai_generated_rule_catalog_2025.json` — **4,828 entries** (Error 2263 / Info
  2565), keyed by `adm_rule_name`, storing both T-SQL and HANA SQL with a `{datastore}`
  placeholder; `op_query_sql` = universe, `report_query_sql` = universe + error WHERE. The
  catalog source of the OptSel/RptSel split — see [[ref-rule-catalog-structure]].
- `sap_master_tables.json` — drives `zDomainSegment` in [[ref-multi-impl-fan-out-engine]];
  **order within each domain is priority**, first table is the `is_header` table carrying the
  classification field (KNA1.KTOKD, LFA1.KTOKK, MARA.MTART). Header wins.

`knowledge/clients/` (per-client `ddic.db` dictionaries, e.g. bacardi/danone) is **gitignored** —
shared via SharePoint under NDA, never the repo.

## Inputs & outputs

- **Consumed by**: [[ref-local-deriver]] (domains/joins/fields/keys), [[ref-sql-generator]] (PKs,
  deletion flags, view patterns), [[ref-rule-name-scorer]] (heuristics),
  [[ref-schema-profiler]] & [[ref-attribute-usage-analysis]] (org-dimensions, value lookups),
  [[ref-catalog-deriver]] (the catalog JSON).
- **Selected by**: the project YAML `erp:` key picks the active `erp/<erp_id>/` plug-in;
  `get_erp_id` defaults to `sap_ecc`.

## Source

- `knowledge-data-config.md` (mining findings, counts confirmed by parsing JSON 2026-06-30)
- `core/knowledge_engine.py:57-146` (loaders: domains, joins, PKs, composite keys, heuristics,
  data-domain map)

## Related

- [[ref-architecture-context-and-project-yamls]]
- [[ref-local-deriver]]
- [[ref-sql-generator]]
- [[ref-rule-name-scorer]]
- [[std-rule-name-heuristics]]
- [[ref-sap-baseline-model]]
- [[ref-value-description-resolution]]
- [[ref-deletion-flag-resolver]]
- [[ref-three-database-architecture]]
- [[ref-rule-catalog-structure]]
- [[ref-multi-impl-fan-out-engine]]
