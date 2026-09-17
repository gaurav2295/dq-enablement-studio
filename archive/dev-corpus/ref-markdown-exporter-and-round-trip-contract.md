---
id: ref-markdown-exporter-and-round-trip-contract
type: reference
title: Markdown Exporter & Round-Trip Contract
domain: studio
audience: [developer, consultant]
level: practitioner
status: review
links:
  - parent:ref-single-rule-designer
  - relates:ref-dqrulespec-data-model
  - relates:ref-output-section-builders
  - relates:ref-profiling-view-generation
  - relates:ref-three-database-architecture
  - relates:ref-exporters
sources:
  - vault:studio-architecture/Studio — Markdown Exporter & Round-Trip Contract.md
tags: [studio, engine, methodology, both]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

Markdown is the human-editable face of a DQ rule: export writes the spec to a canonical `.md`
file, but import parses the spec back and deliberately does NOT reconstruct the SQL — the next
derive/regenerate rebuilds it from the parsed spec.

This is the interchange layer that lets a human hand-edit a rule's *intent* (name, fields, joins,
filters, logic, description) in plain Markdown and re-import it, while guaranteeing the generated
SQL always matches the current spec rather than a possibly-stale hand-edit. It sits behind the
[[ref-single-rule-designer|Single Rule Designer]] export/import buttons and feeds the bulk
`markdown/` output folder.

## What it does

- **Export** — `POST /api/export-markdown` (`routes.py:434`) serialises a
  [[ref-dqrulespec-data-model|DQRuleSpec]] to a canonical Markdown document: rule identity, the
  [[ref-output-section-builders|5 output sections]] (Tech / Basic / Org / Value / Activity), joins,
  filters, the Logic / Check Conditions, and the Fetch / Check / Return description.
- **Import** — `POST /api/import-markdown` (`routes.py:392`) parses that Markdown back into a spec.
  **SQL is NOT reconstructed from the Markdown** — `import-markdown` rebuilds only the *spec*; the
  next `/api/derive` or `/api/generate-sql` rebuilds the OptSel/RptSel from it (`routes.py:392-402`).
- **CLI** — `studio.py derive --format markdown` and `studio.py bulk --format markdown` emit the
  same documents. Filename pattern: `DQ_{rule_id}_{safe_name}.md`, where `safe_name` is the rule
  name truncated to 40 chars with spaces → underscores (`studio.py:198-199,335-336`).
- **Bulk** — the pipeline writes a `markdown/` folder of one `.md` per rule into
  `DQ_Rule_Package.zip` alongside `specs/` JSON and per-rule `sql/` (`routes.py:1740-1879`). md
  import/export lives in `pipeline/`.

## The round-trip contract (the load-bearing rule)

> [!important] Import parses the spec, NOT the SQL
> Markdown is the source of truth for **intent**; generated SQL is a **derived artifact**.
> Importing a hand-edited `.md` rebuilds the spec only — the SQL is regenerated on the next derive
> so it can never drift from the spec. Do/don't:
> - **Do** edit the rule name, output fields, joins, filters, or logic in Markdown, then re-import
>   and re-derive.
> - **Don't** hand-edit SQL in the Markdown and expect it to survive import — it won't be parsed
>   back; the regenerator overwrites it.

- The Markdown carries the spec; the `to_dict`/`from_dict` JSON path (`spec_model.py:267-358` /
  `:360-465`) is the parallel machine interchange. Both are spec-only by the same principle.
- `_deletion_is_error` is the **only** transient (underscore-prefixed) attribute round-tripped
  through serialization (`spec_model.py:352-357`, restored `:461-463`) so a manual edit → regen
  preserves deletion-detection intent.
- `from_dict` soft-migrates legacy `filter_db` → `prep_db` (`spec_model.py:441-443`) so older
  exports still load.

## Profiling is built from `_profiling_input`, not output_fields

For profiling rules the Markdown **Output Structure** section is built from
`spec._profiling_input` + `metric_type` verbatim (`local_deriver.py:2115-2127`), NOT from
`output_fields` — which for profiling hold only the two tech fields (zSourceSystemID,
zConcatenatedKey). The segment / profiled / COUNT columns live in the profiling input, so the
exporter reads them there. See [[ref-profiling-view-generation|Profiling View Generation
(PrfSel-PrfSum)]].

## Inputs & outputs

- **In (export):** a derived `DQRuleSpec`. **Out:** a canonical `DQ_{rule_id}_{safe_name}.md`
  document.
- **In (import):** a Markdown rule document. **Out:** a parsed `DQRuleSpec` with **no SQL** —
  `sql_optsel`/`sql_rptsel` stay empty until the next derive/regenerate.

> [!note] Implementation status — resolved 2026-07-01
> **B10** — the exporter is served by **FastAPI + Jinja** (`app.py` + `ui/templates/*.html`),
> **NOT** Streamlit. `CLAUDE.md` now correctly says FastAPI + Jinja, matching README/HANDOFF/INSTALL
> (KNOWN-ISSUES B10, fixed 2026-07-01).
> **B4** — canonical FROM = **WRKDQ** (one repository): DQ rule views are created in AND read FROM
> `WRKDQ` (a same-database read). **WRKDQPREP_ALL** is the upstream prep layer — it applies
> relevancy criteria, merges sources, performs logical aggregation, and applies scope for one or
> many source systems, then **pushes its output into WRKDQ**; rules do NOT read it directly. The app
> now reads Error/Info rule views FROM/JOIN `WRKDQ` (the working repository), matching profiling —
> one repository, no cross-DB read of the prep layer (KNOWN-ISSUES B4, fixed 2026-07-01). The
> topology in [[ref-three-database-architecture|Three-Database Architecture (resolution)]] is the
> single source of truth.

## Source

- `api/routes.py:392-402` (import-markdown), `:434` (export-markdown), `:1740-1879` (bulk package).
- `studio.py:198-199,335-336` (CLI markdown filenames).
- `core/spec_model.py:267-358`/`:360-465` (serialization), `:352-357`/`:461-463`
  (`_deletion_is_error`).
- `core/local_deriver.py:2115-2127` (profiling Output Structure from `_profiling_input`).
- Detail: `knowledge-mining/app-arch-ops.md` §3, §17.12; `derivation-spec.md`.

## Related

[[ref-single-rule-designer]] · [[ref-dqrulespec-data-model]] · [[ref-output-section-builders]] ·
[[ref-generate-sql-dispatcher]] · [[ref-sql-generator]] · [[ref-profiling-view-generation]] ·
[[ref-exporters]] · [[ref-bulk-processor-and-dqops-id-invariants]] · [[ref-sql-parser]]
