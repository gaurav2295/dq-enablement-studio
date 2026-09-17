---
id: ref-three-database-architecture
type: reference
title: Three-Database Architecture (resolution)
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - relates:ref-dqrulespec-data-model
  - relates:ref-architecture-context-and-project-yamls
  - relates:ref-sql-generator
  - relates:ref-view-vs-table-qualification
  - relates:ref-layer-2-layer-4-datastore-views
  - relates:ref-three-repo-ecosystem
  - relates:ref-catalog-deriver
  - relates:std-studio-config-shape

  - relates:gls-prep-db
  - relates:gls-working-db
sources:
  - vault:studio-architecture/Studio — Three-Database Architecture (resolution).md
  - dq-studio:.claude/skills_canonical/studio-architecture.md
tags: [studio, engine, methodology, architecture, sap]
created: 2026-08-20
updated: 2026-08-20
---

> [!note] A third numbering scheme
> The three databases here (`source_db` / `prep_db` / `working_db`) are yet another numbering —
> distinct from the four layers in [[con-data-architecture-layers]] and from the Layer 2/Layer 4
> datastore views in [[ref-layer-2-layer-4-datastore-views]]. Don't map any of the three onto
> each other.

## Summary

Every generated DQ rule is CREATEd in AND SELECTs FROM `working_db` (`WRKDQ`) — one
repository, a same-database read. `prep_db` (`WRKDQPREP_ALL`) is the UPSTREAM prep layer
whose output is pushed into `WRKDQ`; rules do NOT read it directly. `source_db` is
informational only, and `filter_db` is a back-compat property that just aliases `prep_db`.

The three databases are fields on the embedded `ArchitectureContext` (see
[[ref-dqrulespec-data-model]] and [[ref-architecture-context-and-project-yamls]]). They are
resolved once from the project YAML by `resolve_architecture` and then carried inside every
spec, so the [[ref-sql-generator|SQL generator]] never has to re-read config. This unit
documents the canonical wiring, which the code now implements end-to-end (Error/Info rules
read `WRKDQ`, matching profiling — KNOWN-ISSUES B4, fixed 2026-07-01).

## The three roles (canonical)

| Field | Canonical value | Role in a generated view |
|---|---|---|
| `source_db` | `SRCECC_DA` | **Informational only.** Tells the user/markdown where the raw ERP snapshot lives. Rules do **NOT** execute against it any more — data is consolidated upstream by the separate DQ Data Pipeline app (see [[ref-three-repo-ecosystem]]). |
| `prep_db` | `WRKDQPREP_ALL` | **Upstream prep layer (NOT the rule source).** Applies relevancy criteria, merges sources, performs logical aggregation, and applies scope for one or many source systems. Its output is **pushed into `WRKDQ`**; rules do **NOT** SELECT FROM it directly. |
| `working_db` | `WRKDQ` | **The one repository — CREATE-VIEW target AND SELECT-FROM target.** Both the view definition object and the tables its body reads live here, so the rule read is same-database (not cross-DB). |

So a rule view is `CREATE VIEW [WRKDQ].[dbo].[DQ_...] AS SELECT ... FROM [WRKDQ].[dbo].[<table>] ...` — created in and reading from the same `WRKDQ` repository.
Within the broader topology (`source → SRCECC_DA → WRKDQPREP_ALL (prep) → WRKDQ (rules
created + read here)`, see [[ref-layer-2-layer-4-datastore-views]] and
[[ref-profiling-view-generation]]) the prep layer's output is pushed into `WRKDQ`, and
rules then read entirely within `WRKDQ`.

## `filter_db` — the back-compat alias (do / don't)

`filter_db` is a **read-only `@property` that returns `prep_db`** — not a fourth database.

- **Why it exists:** the Studio used to split a per-system filter-view layer (where Layer-2
  `{system}_{table}_FILT` views lived) from the upstream prep layer. Both collapsed into
  `prep_db` once the DQ Pipeline app took over data prep.
- **DO** read `prep_db` directly in new code.
- **DON'T** treat `filter_db` as separately configurable — `view_generator` and tests still
  reference `arch.filter_db`, and `from_dict` soft-migrates a legacy serialized `filter_db`
  key → `prep_db`.

## Resolution (where the values come from)

`resolve_architecture(config)` builds the context from the project YAML's `databases:`
block with a three-level fall-through (`core/architecture.py:191-195`):

```text
prep_db = databases.prep  OR  databases.filter  OR  databases.source
```

`prep` is the new canonical key; `filter` is the legacy key kept working by the same
fall-through. `source_db` and `working_db` map straight from `databases.source` /
`databases.working`. Legacy YAMLs still load unchanged; new YAMLs should write `databases.prep`
exclusively. **Don't remove the fall-through** — it is the only thing keeping partially-migrated
projects building.

```yaml
# Current canonical shape:
databases:
  source: SRCECC_DA
  prep:   WRKDQPREP_ALL
  working: WRKDQ
```

## The hard rules

These are settled. A change request that breaks one of them needs an explicit decision, not a
patch.

- **Every FROM/JOIN qualifier in generated rule SQL is `working_db`** — never `source_db`. The
  generator expression is `arch.working_db or arch.source_db`; the soft fallback to `source_db`
  exists only so a partially-migrated ArchitectureContext still builds, and should never fire in
  a configured project.
- **The CREATE VIEW header is `working_db`** (`WRKDQ`) for every rule type.
- **`working_db` and `prep_db` must stay different values.** They are separate by design — view
  definitions and prep output are different concerns, and collapsing them removes the boundary
  the DQ Pipeline app hands off across.
- **`source_db` and `prep_db` stay separate fields even when one is blank.** Never infer one from
  the other.
- **Catalog `{datastore}` substitution targets `prep_db`, not `source_db`** —
  `core/catalog_deriver.py:232`, `datastore_db = architecture.prep_db or architecture.source_db`.
  This is a genuine asymmetry with methodology-generated SQL (which targets `working_db`), because
  catalog SQL ships verbatim from the catalog rather than being built by the generator. See
  [[ref-catalog-deriver]] and [[prn-catalog-promotion-wraps-instead-of-injecting]].
- **The view body contains no `SRCECC_DA` reference** in any FROM/JOIN. Comment lines may name it
  for provenance — that is what it is for.

> [!warning] Conflicting guidance in the wild — CONFLICT-004
> The dq-studio `studio-architecture` skill file states the rule FROM target is `prep_db`
> (`WRKDQPREP_ALL`). That captured the pre-B4 state; the current generator targets `working_db`
> (`core/sql_generator.py:188-195`, `:281-283`, `:1416-1418`). The half of the skill rule that
> still holds — **never `source_db`** — is preserved above. Recorded as CONFLICT-004.

## Bugs this wiring exists to prevent

- Using `arch.source_db` as the FROM qualifier anywhere in `core/sql_generator.py`.
- Reintroducing `filter_db` as a separate configurable concept (it is a back-compat property — see
  the section above).
- Having a rule query a source ERP database in any way — the architectural flaw the prep-layer
  consolidation removed.
- Making `working_db` and `prep_db` the same value "for simplicity".

## Charter boundary — what the Studio does not do

The Studio is **only** the rule design + generation layer. It does **not** ingest data from source
ERPs, populate `WRKDQPREP_ALL`, schedule rule execution, or push results to SKP cloud. Those
belong to the separate DQ Data Pipeline app and the SKP integration layer (see
[[ref-three-repo-ecosystem]]). A feature request that would have the Studio touch source databases
or move data is outside its charter — raise it with the Pipeline team rather than re-implementing
prep work inside the Studio.

## Implementation status — B4 (rule FROM target)

> [!success] Implementation status — resolved 2026-07-01 (KNOWN-ISSUES B4)
> **Canonical FROM = `WRKDQ` (one repository).** Rules are CREATEd in AND SELECT FROM
> `WRKDQ` — a same-database read. `WRKDQPREP_ALL` is the upstream prep layer whose output is
> pushed into `WRKDQ`; rules do NOT read it directly. `source_db` stays informational.
>
> **The app now implements this.** Error/Info rule views read FROM/JOIN `working_db`
> (`WRKDQ`) — one repository, matching profiling, which already read `WRKDQ` correctly.
> `WRKDQPREP_ALL` is upstream ETL only; rules no longer read the prep layer.

## Inputs & outputs

- **In:** `databases:` block of `config/projects/<id>.yaml` (`source` / `prep` /
  `working`; legacy `filter`).
- **Out:** `ArchitectureContext.source_db` / `.prep_db` / `.working_db` (+ `.filter_db`
  property), embedded on the spec and consumed by the SQL generator and
  [[ref-view-vs-table-qualification|table-qualification]] logic.

## Source

- `core/spec_model.py:91-105` — `source_db` / `prep_db` / `working_db` field comments
  stating the three roles verbatim.
- `core/spec_model.py:161-174` — `filter_db` `@property` returning `prep_db` (back-compat
  docstring).
- `core/architecture.py:191-195` — `prep_db = prep OR filter OR source` fall-through.
- `knowledge/architecture/syniti_dq_data_flow.md` + `data_flow.json` — topology (`prep`
  default_db `WRKDQPREP_ALL`, `working` default_db `WRKDQ`, `rule_target` on `working`).
- Detail: `knowledge-mining/knowledge-data-config.md` §2.3, §3.
- `core/catalog_deriver.py:232` — `{datastore}` substitution resolving to `prep_db`.

## Verification

```bash
# Generated SQL points FROM the rule repository, not the source DB:
python3 -m pytest tests/test_sql_generator.py::TestSQLGeneration::test_optsel_has_correct_database -v

# Catalog datastore substitution uses prep_db:
python3 -m pytest tests/test_rule_catalog.py::TestCatalogDeriver::test_datastore_placeholder_substituted -v
```

## Related

[[ref-dqrulespec-data-model]] · [[ref-architecture-context-and-project-yamls]] ·
[[ref-knowledge-base-file-inventory]] · [[ref-sql-generator]] ·
[[ref-view-vs-table-qualification]] · [[ref-layer-2-layer-4-datastore-views]]
