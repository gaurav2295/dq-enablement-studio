---
id: ref-multi-impl-fan-out-engine
type: reference
title: Multi-Impl Fan-out Engine
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:ref-bulk-processor-and-dqops-id-invariants
  - relates:ref-architecture-context-and-project-yamls
  - relates:ref-view-name-token-resolution
  - relates:ref-catalog-deriver
  - relates:ref-output-section-builders
  - relates:ref-local-deriver
  - relates:con-multi-implementation-model
  - relates:std-studio-config-shape
  - relates:ref-profiling-view-generation
sources:
  - vault:studio-architecture/Studio — Multi-Impl Fan-out Engine.md
  - dq-studio:.claude/skills_canonical/studio-multi-impl.md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`core/multi_impl.py` is the engine room for the Studio's fan-out model — ONE conceptual rule
becomes N per-system implementations for Error/Info, and exactly ONE implementation for Profiling
(a single spec carrying two SQL views) — supplying three reusable helpers that operate on a
fully-built [[ref-dqrulespec-data-model|DQRuleSpec]]: the `zSourceSystemID` system filter
(Profiling-exempt), the gap-filling zero-padded `SKP_RULE_<n>` id generator, and the
`zDomainSegment` source-table picker ("rule name wins, earliest offset").

Each implementation gets its own DQOps `rule_id`, one SQL view, and one tracker row; siblings
share `skp_rule_id` + `parent_rule_key` so the tracker / UI can group them. The bulk fan-out *loop*
lives in `pipeline/bulk_processor.py` (see [[ref-bulk-processor-and-dqops-id-invariants|Bulk
Processor & DQOps ID Invariants]]); this module owns the small spec-mutating helpers it calls.

## The hierarchy — load this first

- **Rule** — conceptual. No DQOps ID. Identified by `skp_rule_id`.
- **Implementation** — deployable. Owns one `rule_id` (DQOps ID), one SQL view, one tracker row,
  one SKP enforcement entity.
- One rule fans out to N implementations **for Error/Info only**.
- **Profiling: one rule = one spec carrying TWO SQL views** (PrfSel in `sql_optsel`, PrfSum in
  `sql_rptsel`) under ONE DQOps ID. `view_type` stays an empty string — labelling the spec as one
  of the two views would be ambiguous. **No fan-out for profiling.**

| Field | Cardinality | Source |
|---|---|---|
| `skp_rule_id` (`SKP_RULE_<n>`) | shared across siblings | bulk page "Starting SKP_Rule_ID" + per-batch counter |
| `rule_id` (DQOps ID, e.g. `0042`) | unique per implementation | bulk page "Starting DQOps ID" + per-batch counter |
| `parent_rule_key` | links siblings | defaults to `skp_rule_id` |

A user-supplied `skp_rule_id` on a row is **preserved verbatim**; the auto-counter walks past
collisions rather than overwriting. For a profiling row with an `SKP_RULE_<n>` but no `rule_id`,
the DQOps ID is locked to the SKP's numeric portion and then claimed through the batch counter —
that keeps the SKP↔DQOps join stable across re-imports while guaranteeing it cannot collide with
an auto-assigned id elsewhere in the batch.

## Fan-out resolution (Error/Info only)

Three-tier precedence in `pipeline/bulk_processor.py::_expand_implementations`:

1. The row's `systems` CSV column wins outright.
2. A caller-supplied `default_systems` kwarg — a test escape hatch. The public API does not expose
   it; the bulk page used to and it was removed in favour of project-level scope.
3. The project's fan-out scope from the YAML (silent fallback).

If all three are empty → `[""]`: one implementation, no system filter. `excluded_systems` then
subtracts codes that are configured but not yet ready to deploy.

Tier 3 is the `system_aliases` **keys**: they are the authoritative `zSourceSystemID` values, they
drive the per-impl `WHERE zSourceSystemID = '<code>'` filter, and the alias **value** is only the
cosmetic [[ref-view-name-token-resolution|view-name]] slot — so filter value and view-name suffix
can never drift apart. `source_systems` is the legacy fallback; if both are set and disagree,
aliases win with a one-time warning.

> [!warning] Which YAML key supplies tier 3 — CONFLICT-005
> Current code reads `system_aliases` keys, falling back to `source_systems`
> (`architecture.py:200-231`); the dq-studio `studio-multi-impl` skill states the reverse
> precedence. Either way, the **display alias values never participate in fan-out** — that
> independence is the tested invariant. See [[std-studio-config-shape]].

## Profiling exception — the correction that keeps getting re-litigated

**One profiling row → one `DQRuleSpec`.** Both SQL slots populated, `view_type` blank,
`system_filter` blank.

- **Don't** produce two sibling specs distinguished by `view_type`. That was the OLD model. Code or
  tests asserting `len(profiling_specs) == 2` are stale — the assertion is `== 1` with both SQL
  slots populated.
- **Don't** treat profiling rules as system-fanned-out. Profiling is cross-system by design. A
  `systems` value on a profiling row becomes `WHERE zSourceSystemID IN (...)` **inside** the single
  view, not a fan-out trigger.
- **Don't** add `{system}` to profiling view-name patterns. See [[std-view-naming-patterns]].

One tracker row per profiling spec, with the ViewType column rendered as the paired literal
`"PrfSel + PrfSum"` rather than a single value. Tracker rows sort by `skp_rule_id` then `rule_id`
so siblings group visually.

## 1. `apply_system_filter(spec)` — per-impl zSourceSystemID inclusion

Appends `<main_table>.zSourceSystemID = '<code>'` as a FilterEntry INCLUSION. Mutates in place,
returns the same instance for chaining. Concrete rules:

- **Profiling-exempt** — if `spec.rule_type == RuleType.PROFILING`, returns unchanged. Profiling
  keeps cross-system `IN (...)` semantics (Plan §C4); `system_filter` on a profiling impl is used
  only for the view name.
- **No-op guards** — empty `system_filter` → skip; empty `main_table` → skip silently rather than
  emit a bogus unqualified filter.
- **Idempotent** — scans existing filters and bails if an INCLUSION on `zsourcesystemid` with the
  same code already exists (so re-running bulk fan-out on a saved spec doesn't double-add).
- **Human label** — description reads `Limit to source system <alias> (<code>)` when an alias
  resolves (via `spec.system_alias`, else `resolve_system_alias(arch, code)`), else just the code.
  This threads through to the markdown Filters cell.
- The emitted filter feeds the existing `_build_where` / `_parse_filter` chain in
  [[ref-sql-generator|core.sql_generator]].

> The generator READS `src.zSourceSystemID` rather than hardcoding the literal, so source-system
> drift (multiple system values in output) surfaces instead of masquerading as success.

## 2. `next_skp_rule_id(existing, start=1)` — gap-filling id allocator

Returns the next `SKP_RULE_<n>`, **zero-padded to 4 digits** (`SKP_RULE_0001`).

- Parses `existing`, keeping only strings matching `SKP_RULE_<digits>`; everything else
  (non-strings, malformed) is ignored.
- Walks forward from `max(start, 1)` to the first integer **not** already seen — so a
  manually-assigned outlier (e.g. `SKP_RULE_9999`) does NOT push the auto-counter past it; ids stay
  sequential around the user's `start`. `start` is clamped to ≥1 (`SKP_RULE_0000` is not valid).

## 3. `select_domain_segment_source(spec)` — "rule name wins"

Picks the master table to qualify `zDomainSegment` from (e.g. `"KNA1"`), or `""` when the rule
shouldn't carry the column. `append_domain_segment_field(spec)` then appends a TECH
[[ref-output-section-builders|OutputField]] `zDomainSegment` = `<table>.zDomainSegment` only when
the picker returns non-empty (idempotent; **NOT** part of
[[ref-zconcatenatedkey-and-ziserrorflag-sql-emission|zConcatenatedKey]] — it's a classification,
not an identifier; positioned `max(position)+1`, renders last within the TECH section).

Decision flow:

1. Collect every referenced table (`main_table`, left side of each `output_fields[*].table_field`,
   both ends of each join).
2. Group those against `DOMAIN_SEGMENT_TABLES` (customer / vendor / material).
3. **0 groups** → `""` (not a CVM rule).
4. **1 group** → highest-priority referenced table in that group.
5. **2+ groups** → disambiguate, in order:
   - **rule name** — keyword `customer`/`vendor`/`material` at the **earliest offset** wins (e.g.
     *"Material types must align with customer pricing"* → `material` at offset 0 beats `customer`
     at offset 30 → MARA group);
   - then `spec.data_domain` (itself rule-name-derived), same earliest-offset rule;
   - then `spec.main_table` membership in a group;
   - final fallback: deterministic pick by sorted domain name (keeps generation stable).

> The "rule name wins" semantics are an explicit user decision: a Customer rule that joins to MARA
> gets `KNA1.zDomainSegment`, **not** `MARA.zDomainSegment`.

### `DOMAIN_SEGMENT_TABLES` — three layers, priority-ordered lists

Loaded once at import (`_load_domain_segment_tables`). Within each list, **order = priority**; the
header table comes first because it carries the underlying classification field (KNA1→KTOKD,
LFA1→KTOKK, MARA→MTART).

| domain | priority order (header first) |
|---|---|
| customer | KNA1, KNB1, KNVV, KNVI, KNVP, KNVK, KNVA, KNVD, KNVS, KNAS, KNB5, KNBK |
| vendor | LFA1, LFB1, LFM1, LFM2, LFAS, LFB5, LFBK, LFBW, LFC1, LFC3 |
| material | MARA, MARC, MARD, MAKT, MBEW, MVKE, MARM, MEAN, MLAN, MLGN, MLGT |

- **Authoritative source:** `knowledge/sap_master_tables.json` (edit + restart to update without
  code changes; the Pipeline app reads it too). **Embedded fallback:** the dict literal above —
  used when the JSON is missing / malformed / empty (a `[multi_impl] WARNING` prints to stdout but
  Studio keeps running). Domains absent from the JSON inherit from the fallback, so removing (say)
  `vendor` from the YAML can't silently delete that detection branch.

## 4. `populate_implementation_metadata(spec, …)` — sibling-metadata setter

Convenience setter; empty values are skipped (incremental-safe). Key fallbacks:

- `parent_rule_key` defaults to `skp_rule_id` when blank (the common "siblings share the parent"
  case).
- `system_alias` auto-resolves from `system_filter` via `resolve_system_alias` when not passed
  (falls through to the code itself when no alias is configured).

## Inputs & outputs

| | |
|---|---|
| **Input** | a fully-built `DQRuleSpec` + per-impl values (`system_filter`, `system_alias`, `skp_rule_id`, …) |
| **Output** | the same `DQRuleSpec` mutated in place: + system-filter FilterEntry, + `zDomainSegment` OutputField, + sibling metadata; `next_skp_rule_id` returns a `SKP_RULE_NNNN` string |
| **Callers** | `pipeline/bulk_processor.py` fan-out, single-rule editor, [[ref-catalog-deriver|Catalog Deriver]] (`_zdomain_table_for_spec` delegates to `select_domain_segment_source`) |

## Settled — push back on these

This model has been corrected by the user more than once; the current shape is final until they
reopen it. Push back on a change that would:

- Reintroduce the two-spec profiling model.
- Conflate fan-out scope with `system_aliases` display values.
- Add `{system}` back to profiling view names.
- Make profiling rules fan out per system.
- Drop `SKP_Rule_ID` as redundant — it is not; it is the parent identifier.

## Verification

```bash
# 250 profiling rows must produce exactly 250 specs (this was 500 once):
python3 -m pytest tests/test_multi_impl.py::TestBulkFanOut::test_profiling_row_produces_one_spec_with_paired_views -v

# An Error/Info row with N systems must produce N specs sharing one skp_rule_id:
python3 -m pytest tests/test_multi_impl.py::TestBulkFanOut::test_error_row_with_systems_csv_produces_one_impl_per_system -v

# Excel upload threads start_id + start_skp_id through the Form() params:
python3 -m pytest tests/test_multi_impl.py::TestStartSkpId::test_excel_upload_endpoint_threads_starting_numbers -v
```

## Source

- `core/multi_impl.py:34-100` — `apply_system_filter` (Profiling-exempt, idempotent, alias label)
- `core/multi_impl.py:103-139` — `next_skp_rule_id` (gap-filling, 4-digit zero-pad)
- `core/multi_impl.py:142-352` — `DOMAIN_SEGMENT_TABLES` loader + `select_domain_segment_source`
  ("rule name wins, earliest offset")
- `core/multi_impl.py:355-406` — `append_domain_segment_field` (TECH field, not a key)
- `core/multi_impl.py:409-451` — `populate_implementation_metadata`

## Related

[[ref-bulk-processor-and-dqops-id-invariants]] · [[ref-dqrulespec-data-model]] ·
[[ref-architecture-context-and-project-yamls]] · [[ref-view-name-token-resolution]] ·
[[ref-sql-generator]] · [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] ·
[[ref-output-section-builders]] · [[ref-catalog-deriver]] · [[ref-profiling-view-generation]] ·
[[ref-local-deriver]] · [[ref-skp-assetupload-and-tracker-flow]]
