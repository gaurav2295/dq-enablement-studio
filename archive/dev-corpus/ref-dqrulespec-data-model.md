---
id: ref-dqrulespec-data-model
type: reference
title: DQRuleSpec Data Model
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-local-deriver
  - relates:ref-catalog-deriver
  - relates:ref-sql-generator
  - relates:ref-multi-impl-fan-out-engine
  - relates:ref-markdown-exporter-and-round-trip-contract
  - relates:con-rule-types
  - implements:prn-ziserrorflag-is-integer
  - implements:std-output-field-sections
  - relates:gls-logicentry
sources:
  - vault:studio-architecture/Studio — DQRuleSpec Data Model.md
tags: [studio, engine, methodology, sap, datamodel]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`DQRuleSpec` is the one canonical, serializable interchange object every Studio path produces
and consumes — carrying identity + multi-implementation + classification fields, the four body
lists (`output_fields` / `logic` / `joins` / `filters`) plus the embedded `ArchitectureContext`,
governed by the `RuleType` / `FieldCategory` / `FilterType` enums, with `_deletion_is_error` as
the single transient that survives a round-trip.

Whether a rule comes from [[ref-local-deriver|the Local Deriver]], [[ref-catalog-deriver|the
Catalog Deriver]], [[ref-sql-parser|the SQL parser]], or
[[ref-ai-derive-and-enhance-internals|AI derive]], it lands in *this* shape.
[[ref-sql-generator|The SQL generator]] reads only this object; [[ref-markdown-exporter-and-round-trip-contract|the markdown exporter]]
round-trips it. One concept, one model.

## The enums (verbatim)

| Enum | Members | Notes |
|---|---|---|
| `RuleType` | `ERROR="Error"`, `INFO="Info"`, `PROFILING="Profiling"` | `str, Enum` so `.value` round-trips in JSON. This is the canonical type — **not** the 6 business categories the [[ref-rule-type-detection]] detector produces. |
| `FieldCategory` | `TECH`, `BASIC`, `ORG`, `VALUE`, `ACTIVITY` | The **5 output sections**; drives both the [[ref-output-section-builders]] and SQL section comments. |
| `FilterType` | `INCLUSION`, `EXCLUSION` | Inclusion = scope restriction; Exclusion = record removal (e.g. deletion flag). The error predicate is **never** a filter. |
| `ObjectType` | `MASTER`, `TRANSACTIONAL` | Enum exists but `object_type` is stored as a **plain `str`** (`"Master"`, `"Unknown"`, `""`) — treat the field as free text. |

## The body lists (one row = one methodology element)

- **`output_fields: list[OutputField]`** — `section` (`FieldCategory`), `element` (display name),
  `table_field` (`"MARA.MATNR"`, `""` for calculated, `"*"` for COUNT), `value`
  (`"Calculated"`, `"BIT (1/0)"`), `aggregation`, `instruction` (free text or a CASE/CONCAT
  recipe), `position: int`, `key` (`"Yes"`/`""`).
- **`logic: list[LogicEntry]`** — the per-row error-detection condition: `element`, `operator`,
  `table_field`, `value`, `instruction`. `value` encodes the flag mapping as text, e.g.
  `"1 - If ...\n0 - If ..."`. Empty for Info/Profiling.
- **`joins: list[JoinEntry]`** — `element`, `source` (table on LEFT), `target` (table on RIGHT),
  `join_type` (default `"LEFT JOIN"`), `join_key` (ON predicate), `cardinality` (`"N:1"`).
- **`filters: list[FilterEntry]`** — `filter_type` (default INCLUSION), `description`,
  `operator`, `table`, `field`, `condition`. `condition` uses the methodology micro-DSL the SQL
  generator's `_parse_filter` reads, e.g. `"IF MARA.LVORM = 'X' THEN Exclude"`.

## Identity, multi-impl & classification

- **Identity:** `rule_id` (DQOps ID, per-implementation), `rule_name`, `rule_name_score: float`.
- **Multi-implementation:** one conceptual rule fans out to N per-system or 2 profiling-view
  implementations. Siblings share `skp_rule_id` (`SKP_RULE_<n>`) + `parent_rule_key`; each
  carries its own `system_filter` (the per-impl zSourceSystemID value), `system_alias`,
  `view_type` (`OptSel/RptSel/InfSel/PrfSel/PrfSum`), and `rule_source` (`"Bespoke"` default /
  `"Catalog"`). See [[ref-multi-impl-fan-out-engine]].
- **Classification:** `data_domain`, `object_type`, `business_process`, `business_impact`,
  `rule_type: RuleType = ERROR`, `system: str = "SAP ECC"`.
- **Status:** `status` ∈ `Draft | Reviewed | Approved | SQL Generated`.
- **Generated artifacts:** `sql_optsel`, `sql_rptsel`, `sample_data`.
- **Embedded:** `architecture: ArchitectureContext` (3-DB wiring + view patterns + fan-out
  config) — see [[ref-architecture-context-and-project-yamls]] and
  [[ref-three-database-architecture]].

## Computed properties

- `.inclusions` / `.exclusions` — `filters` split by `filter_type`.
- `.fields_by_section(section)` — output fields in one section.
- `.main_table` — first output field with a dotted `table_field`, part before the dot. (This is
  *why* the catalog deriver resolves SQL aliases → real SAP table names: otherwise `.main_table`
  returns `"M"`, not `"MARA"`.)
- `.key_field` — first `key="Yes"` field's `table_field`.

## Serialization & the one round-tripped transient

`to_dict` / `from_dict` are the JSON contract. **Underscore-prefixed transients are stripped from
golden specs — except `_deletion_is_error`, which is explicitly written and restored** so a
manual edit → regenerate cycle preserves deletion-*detection* intent (the deletion flag stays the
error CASE, not a WHERE exclusion). `from_dict` also soft-migrates legacy `filter_db` →
`prep_db`. All other transients (`_catalog_id`, `_domain_confidence`, `_fields_matched`,
`_domain_unknown`, `_review_required`, `_warnings`, `_validator_findings`, `_profiling_input`, …)
are attached dynamically by the derivers and not persisted.

## Key conventions (do / don't)

- **`zIsErrorFlag` is INTEGER `1`/`0`** via `CASE WHEN <error> THEN 1 ELSE 0 END`; `1` is ALWAYS
  the defect. The `LogicEntry.value` text encodes this mapping. Never strings, never
  CAST-to-decimal. See [[prn-ziserrorflag-is-integer]].
- **The error predicate lives in `logic` (→ the CASE), never in `filters`.** `filters` is system
  scope + deletion exclusions only.
- **`zConcatenatedKey` separator is `_`** (no space, ADM requirement), must be NULL-safe and
  identical across paths — see status below.
- **`object_type` is free-text**, not the `ObjectType` enum — read it defensively.

> [!tip] Implementation status — resolved 2026-07-01
> - **B3 — zConcatenatedKey separator.** Canonical: one separator (`_`), NULL-safe (a NULL key
>   column must not null the whole expression), never NULL, **identical** across local-derive and
>   catalog/promotion. The app now uses `_` on BOTH paths (catalog's `|` was changed to `_`), the
>   CONCAT is NULL-safe, and the keyless fallback emits `''` rather than NULL. See
>   [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]].
> - **B4 — rule FROM target.** Canonical: it is ONE repository — rule views are CREATED in AND
>   SELECT FROM `WRKDQ` (a same-DB read). `WRKDQPREP_ALL` is the UPSTREAM prep layer (relevancy /
>   merge / aggregate / scope across one or many source systems) whose output is PUSHED INTO
>   `WRKDQ`; rules do NOT read it directly. Topology stays `source → SRCECC_DA →
>   WRKDQPREP_ALL (prep) → WRKDQ (rules created + read here)`. The app now reads Error/Info rule
>   views FROM/JOIN `WRKDQ` — one repository, matching profiling — and treats `WRKDQPREP_ALL` as
>   upstream ETL only. See [[ref-three-database-architecture]].

## Source

- `knowledge-mining/derivation-spec.md` §1 — the derivation spec detail behind this model.
- `core/spec_model.py:14-36` — `RuleType` / `ObjectType` / `FieldCategory` / `FilterType` enums.
- `core/spec_model.py:177-238` — `DQRuleSpec` fields (identity, multi-impl, classification, body
  lists, status, artifacts).
- `core/spec_model.py:352-358` — `_deletion_is_error` round-trip in `to_dict` (restored
  ~`:461-463` in `from_dict`).
- Also: `OutputField` (`:38-49`), `LogicEntry` (`:52-60`), `JoinEntry` (`:63-73`), `FilterEntry`
  (`:75-84`), `ArchitectureContext` (`:87-174`), computed properties (`:240-265`).

## Related

- [[ref-local-deriver]]
- [[ref-catalog-deriver]]
- [[ref-sql-parser]]
- [[ref-ai-derive-and-enhance-internals]]
- [[ref-multi-impl-fan-out-engine]]
- [[ref-output-section-builders]]
- [[ref-logic-builder-templates]]
- [[ref-sql-generator]]
- [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]]
- [[ref-architecture-context-and-project-yamls]]
- [[ref-markdown-exporter-and-round-trip-contract]]
