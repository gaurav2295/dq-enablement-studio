---
id: ref-bulk-processor-and-dqops-id-invariants
type: reference
title: Bulk Processor & DQOps ID Invariants
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - parent:ref-bulk-pipeline
  - relates:ref-catalog-deriver
  - relates:ref-local-deriver
  - relates:ref-multi-impl-fan-out-engine
  - relates:ref-architecture-context-and-project-yamls
  - relates:ref-skp-assetupload-and-tracker-flow
  - relates:gls-dqops-id
sources:
  - vault:studio-architecture/Studio — Bulk Processor & DQOps ID Invariants.md
tags: [studio, engine, pipeline, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`BulkProcessor` is the Excel-driven orchestrator that turns one import row into N deployable
implementations — import → catalog/local derive → per-system fan-out → (optional) AI enhance →
export — and it owns the two non-negotiable id invariants: DQOps ids are counter-owned never
row-owned for Error/Info, and Profiling keeps its SKP→DQOps lock but routes the locked id through
the shared counter so it can never collide.

The orchestrator (`pipeline/bulk_processor.py`, `BulkProcessor` + `BulkResult`) is constructed per
project and loads config / ERP / [[ref-architecture-context-and-project-yamls|architecture]] /
[[ref-knowledge-base-file-inventory|knowledge engine]] **once** (`bulk_processor.py:119-127`). It is
the page behind [[ref-bulk-pipeline]].

## What it does — the data flow

1. **Import** — xlsx / csv / json. Columns: `rule_id, rule_name, rule_type, catalog_id, systems,
   skp_rule_id, data_domain, extra_info` plus profiling columns. `_parse_excel_sheet` accepts column
   aliases; the workbook is parsed across **ALL sheets** so Error/Info and Profiling rules can sit on
   separate tabs (`bulk_processor.py:808-997`).
2. **Derive** — per row: when a `catalog_id` is present, the [[ref-catalog-deriver]] wraps the
   authoritative catalog SQL (Info→Error rows go through the [[ref-catalog-promotion|promoter]]);
   otherwise the [[ref-local-deriver]] generates the spec from the knowledge base.
3. **Fan-out** (`_expand_implementations`, `bulk_processor.py:435-658`) — see below.
4. **AI Enhance** (optional, client-side, 2nd pass) — Step 1 rule-name enhance (one Sonnet call per
   parent group; siblings inherit via textual swap), Step 2 local re-derive (skipped for catalog
   rules), Step 3 AI SQL review (opt-in, **OFF by default** — the [[ref-audit-engine|Audit page]] is
   the structural gate). See [[ref-ai-derive-and-enhance-internals]].
5. **Export** — `DQ_Rule_Deploy.sql`, per-rule `sql/`, `markdown/`, `specs/` JSON,
   `DQ_Report_Tracker.xlsx`, `Batch_Summary.xlsx` (Reconciliation + Failed Rules sheets), per-rule
   unit tests, all bundled in `DQ_Rule_Package.zip`. See [[ref-exporters]].

Per-rule single pipeline (`_process_single_rule`, `bulk_processor.py:1038-1135`): score → derive
(type-aware) → apply overrides → attach architecture → **attach multi-impl metadata BEFORE SQL
gen** (so [[ref-view-name-token-resolution|view-name resolution]] and the WHERE builder see
`system_filter`) → generate SQL.

## Fan-out rules

- **Error / Info = one impl per source system.** Precedence: row `systems` CSV → caller
  `default_systems` (test escape hatch) → project `system_aliases` keys → `source_systems` legacy →
  `[""]` (single impl, no filter). Each impl draws **its own DQOps id**.
- **Profiling = always exactly 2 impls** (PrfSel + PrfSum) sharing **ONE** rule_id; it does **not**
  fan out by system — `systems` becomes an `IN (...)` filter. See [[ref-profiling-view-generation]].
- **`system_aliases` KEYS are authoritative.** The keys are the real `zSourceSystemID` column values
  AND drive the per-impl WHERE filter; the VALUE is only the cosmetic view-name slot — so filter
  value and view-name suffix can never drift. `source_systems` is the legacy fallback; if both are
  set and codes disagree, **aliases win with a one-time WARNING** (`architecture.py:203-229`). The
  generator reads `src.zSourceSystemID` rather than hardcoding the literal, so source-system drift
  surfaces instead of masquerading as success.

## DQOps id invariants (the load-bearing decisions)

> [!important] D-1 — DQOps ids are counter-owned, never row-owned for Error/Info
> The batch counter is the single source of truth. `_next_dqops()` hands out strictly incremental
> ids from the user-supplied start and tracks every issued id in a `used_dqops` set so an id can
> **never be reissued**; zero-padded 4 digits (`f"{n:04d}"`). A row-supplied `rule_id` is **NOT
> honoured** in Error/Info fan-out — sibling impls each need a distinct id
> (`bulk_processor.py:265-291,612-625`).

> [!important] D-2 — Profiling keeps its SKP→DQOps lock, made collision-safe
> Profiling deliberately retains a **1 SKP = 1 DQOps** lock (so re-import joins line up: 1 DQOps →
> 1 tracker → 1 enforcement). The locked id is still routed through `next_dqops()` so it is
> **claimed in the shared `used_dqops` set** and cannot collide with a counter-issued Error/Info id
> (`bulk_processor.py:480-503`).

**SKP_RULE id auto-gen** (`next_skp_rule_id(existing, start=1)`, `multi_impl.py:103-139`): returns
`SKP_RULE_<n>` zero-padded to 4 digits → `SKP_RULE_0001`. Walks **forward** from `start` until it
finds an integer not in `existing` (gap-filling), `start` clamped to ≥1. Ignores any id not matching
`SKP_RULE_<digits>` — so an explicit high-number id (`SKP_RULE_9999`) does **not** push the
auto-counter past it; the counter keeps handing out sequential ids around the user's `start`.
Row-supplied SKP ids are honoured verbatim and never reissued.

> Worth internalising: the **DQOps id is per-impl** (each per-system sibling gets its own), but the
> **SKP_RULE id is shared** across all siblings of one conceptual rule (the grouping key the
> [[ref-skp-assetupload-and-tracker-flow|AssetUpload]] exporter collapses on).

## Per-row warnings (surfaced as badges)

- Alias VALUE → KEY auto-translation: a friendly alias in a row (e.g. `P02` → `SRCECCZ02100`) is
  translated for the WHERE filter; a `_systems_warning` is attached
  (`bulk_processor.py:534-544,647-655`).
- Unknown per-row codes get a `_systems_warning` ("likely returns zero rows") shown as a yellow
  badge (`bulk_processor.py:633-641`).
- `excluded_systems` = subset opting out of the default fan-out (per-row `systems` still overrides).

## Inputs & outputs

- **In:** an import workbook/CSV/JSON, a project id, a start DQOps id, a start SKP id.
- **Out:** a list of `BulkResult` impls (each with its own DQOps id, view names, `system_filter`,
  spec, SQL, `_systems_warning`), bundled by the exporters into `DQ_Rule_Package.zip`.

> [!note] Implementation status
> The app is documented as **FastAPI + Jinja** (`app.py` + `ui/templates/*.html`), not Streamlit.
> There is one canonical view-name pattern set: the project-YAML resolver defaults were aligned to
> the dataclass so `{system}` is always present. Error/Info view names carry `{system}` = production
> system ID / agreed alias (e.g. PD1), never the interim QA system; profiling views omit `{system}`
> by default.

## Source

- `pipeline/bulk_processor.py:435-658` — `_expand_implementations` (fan-out + id assignment).
- `pipeline/bulk_processor.py:265-291,612-625` — `_next_dqops` / `used_dqops`; `:480-503` —
  Profiling SKP→DQOps lock; `:1038-1135` — `_process_single_rule`.
- `core/multi_impl.py:103-139` — `next_skp_rule_id`; `architecture.py:203-229` — alias resolution.
- Detail: `knowledge-mining/app-arch-ops.md` §5, `scoring-profiling.md` §2.3.

## Related

[[ref-multi-impl-fan-out-engine]] · [[ref-catalog-deriver]] · [[ref-local-deriver]] ·
[[ref-profiling-view-generation]] · [[ref-view-name-token-resolution]] ·
[[ref-architecture-context-and-project-yamls]] · [[ref-skp-assetupload-and-tracker-flow]] ·
[[ref-exporters]]
