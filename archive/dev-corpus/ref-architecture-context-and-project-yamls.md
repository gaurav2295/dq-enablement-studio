---
id: ref-architecture-context-and-project-yamls
type: reference
title: Architecture Context & Project YAMLs
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - relates:ref-sql-generator
  - relates:ref-knowledge-base-file-inventory
  - relates:ref-dqrulespec-data-model
  - relates:ref-three-database-architecture
  - relates:ref-config-editor
  - relates:ref-multi-impl-fan-out-engine
  - relates:std-view-naming-patterns
  - relates:std-studio-config-shape
  - relates:prn-studio-design-principles
sources:
  - vault:studio-architecture/Studio — Architecture Context & Project YAMLs.md
  - dq-studio:.claude/skills_canonical/studio-architecture.md
  - dq-studio:.claude/skills_canonical/studio-config-shape.md
tags: [studio, engine, methodology, sap, config]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`config/projects/<id>.yaml` is the production config that `core/architecture.py::resolve_architecture`
turns into an `ArchitectureContext` — the embedded object every rule carries that wires the three
databases (`source`/`prep`/`working`), decides the per-system fan-out scope (`system_aliases` keys
win over `source_systems`), and supplies the view-name patterns and profiling sources the
[[ref-sql-generator|SQL generator]] reads.

Two project YAMLs ship — `sap_ecc.yaml` and `sap_s4hana.yaml`. The `erp:` key selects the
[[ref-knowledge-base-file-inventory|knowledge plug-in]]; the rest of the YAML resolves into the
`ArchitectureContext` that gets stamped onto the [[ref-dqrulespec-data-model|DQRuleSpec]]. See
[[ref-three-database-architecture]] for the DB-key fall-through in depth and [[ref-config-editor]]
for the UI that edits these files.

## What it does

Reads a project YAML, normalises and validates its keys, and resolves them into a typed
`ArchitectureContext` (`core/spec_model.py:87-174`). Also writes config back through a save
whitelist. Entry points (`architecture.py`):

- `load_project_config(id)` — reads `config/projects/{id}.yaml`.
- `resolve_architecture(config)` → `ArchitectureContext` (`architecture.py:178-278`).
- `save_project_config(...)` — whitelisted write-back (`architecture.py:44-95`).
- `resolve_system_alias`, `resolve_view_name`, `get_erp_id`, `get_profiling_sources` /
  `resolve_profiling_sources` (`architecture.py:281-384`).

## Project YAML keys

| Key | Meaning |
|---|---|
| `project_name`, `erp` | label + ERP plug-in selector (`sap_ecc` / `sap_s4hana`) |
| `databases` | `{source, prep, working}` — the three-DB wiring (see below) |
| `source_system` | single canonical system, e.g. `ECCP00100_DQ` |
| `source_systems` | list of fan-out codes — **legacy fallback** |
| `system_aliases` | dict `code → friendly`, e.g. `SRCECCZ02100 → P02`; **keys are the authoritative fan-out scope** |
| `excluded_systems` | per-system fan-out opt-out (subset of alias keys) |
| `profiling_sources` | list of `{source_db, source_system, system_name}` |
| `naming` | view-name patterns |
| `layer_strategy`, `skp`, `profiling` | downstream + optional config |

## Key conventions

**Three-DB key fall-through.** `prep_db = databases.prep OR databases.filter OR databases.source`
(`architecture.py:191-195`). `prep` is the canonical key; `filter` is the legacy name. `source_db`
is informational only — **rules never execute against it**. `working_db` (`WRKDQ`) is the single
rule repository: rule views are **created in AND read FROM `WRKDQ`** (a same-DB read —
`CREATE VIEW [WRKDQ].[dbo].[DQ_…] AS SELECT … FROM [WRKDQ].[dbo].[<table>]`). `prep_db`
(`WRKDQPREP_ALL`) is the **upstream prep layer** (relevancy criteria, source merge, logical
aggregation, per-system scope) whose output is **pushed into `WRKDQ`** — it is **not** the rule
SELECT-FROM target.

**Fan-out precedence — aliases win.** If `system_aliases` is populated, `src_sys =
list(aliases.keys())` and `source_systems` is **ignored**; a one-time WARNING logs only if both are
set and their code-sets disagree (`architecture.py:219-231`). The alias *keys* drive both the
per-impl `WHERE zSourceSystemID = ...` filter and are the authoritative `zSourceSystemID` values;
the alias *value* is the cosmetic view-name `{system}` slot only — so filter value and view-name
suffix can never drift apart.

> [!warning] Conflicting guidance in the wild — CONFLICT-005
> The dq-studio `studio-config-shape` and `studio-multi-impl` skill files invert this, calling
> `source_systems` authoritative and alias keys the legacy fallback. Current code says otherwise
> (`architecture.py:47`, `:200-231`). What both sources agree on — and what actually matters when
> you edit a project — is the **independence rule**: an alias *value* is decoration and must never
> change deployment scope. See [[std-studio-config-shape]] for the four-concept separation and the
> invariants that enforce it.

**Whitelist both halves or neither.** Adding a newly-editable key means updating **both** the
`ProjectConfigUpdate` Pydantic model in `api/routes.py` **and** `_EDITABLE_PROJECT_KEYS` in
`core/architecture.py`. Updating one alone produces a field the UI can post and the saver silently
drops — the exact silent-failure shape [[prn-studio-design-principles|principle 3, fail loudly]]
exists to prevent.

**Editable-key whitelist.** `save_project_config` writes only `_EDITABLE_PROJECT_KEYS` =
`{project_name, source_system, source_systems, system_aliases, excluded_systems, databases,
profiling_sources}` (`architecture.py:44-52`). **Unknown / project-specific keys are preserved
verbatim** from the existing YAML — but `yaml.safe_dump` **loses comments** (known trade-off; the UI
should warn) (`architecture.py:88-95`).

**Normalisation.** `_normalise_codes_list` (`architecture.py:55-80`) for `source_systems` /
`excluded_systems`: trims, drops blanks, dedupes preserving first-seen order, and **rejects a bare
string** (the common copy-paste bug). `system_aliases` (`architecture.py:125-138`): must be a
mapping; a blank alias value defaults to the code itself.

**`profiling_sources` stubbing.** When a requested system key isn't in `profiling_sources`,
`resolve_profiling_sources` fabricates a stub `source_db = f"SRC{key}"` so the multi-system
profiling view still emits SQL; a DBA hand-edits `source_db` later (`architecture.py:328-384`).

**View patterns** (defaults in `ArchitectureContext`, `spec_model.py:110-119`). Error/Info views
include `{system}`; profiling views deliberately **omit** it (they are cross-system aggregations):

- `optsel_view_pattern` = `DQ_{id}_{system}_{table}_{field}_OptSel` (also `rptsel`, `infsel`)
- `prfsel_view_pattern` = `DQ_{id}_{table}_{field}_PrfSel` (also `prfsum`) — no `{system}`
- `filter_view_pattern` = `{system}_{table}_FILT`; `bridge_view_pattern` = `{table}`

**Profiling resolver defaults.** `profiling_description_sources` default `["snapshot","client","internal"]`
(precedence enforced snapshot > client > internal regardless of list order); `default_description_language`
upper-cased single letter, default `"E"`. `filter_db` is a back-compat property aliasing `prep_db` —
the per-system filter layer collapsed into prep once the DQ Pipeline app took over data prep.

## Common bugs to avoid

- **Hand-editing the YAML from code paths** — including test fixtures. Go through
  `save_project_config` so normalisation applies. A fixture that hand-writes YAML must still
  produce a shape `resolve_architecture` accepts.
- **Removing the `databases.prep → filter → source` fall-through** because "everything is migrated
  now". It is the soft-migration path for legacy projects and saved specs.
- **Assuming `yaml.safe_dump` round-trips comments.** It does not. A save through the Configuration
  page strips every comment in the file — surface that in the UI, don't let a consultant discover
  it after losing annotations.
- **Whitelisting a key in only one of the two places** (see above).

## Inputs & outputs

- **In:** `config/projects/{id}.yaml`.
- **Out:** an `ArchitectureContext` embedded in every [[ref-dqrulespec-data-model|DQRuleSpec]] and
  consumed by the [[ref-view-name-token-resolution|view-name resolver]], the
  [[ref-multi-impl-fan-out-engine|fan-out engine]], and the SQL generator.

> [!note] Implementation status
> The Studio app is **FastAPI + Jinja** (`app.py` + `ui/templates/*.html`), not Streamlit; version
> is single-sourced in `version.py`. The canonical rule SELECT-FROM is `WRKDQ` (one repository —
> rule views are created in AND read from `WRKDQ`, a same-DB read). `WRKDQPREP_ALL` is the upstream
> prep layer whose output is pushed into `WRKDQ`; rules do not read it directly. Error/Info rule
> views read FROM/JOIN `working_db` (`WRKDQ`), matching profiling, so all rule types read from the
> single repository and `WRKDQPREP_ALL` is upstream ETL only. Topology:
> `source → SRCECC_DA → WRKDQPREP_ALL (prep) → WRKDQ (rules created + read here)`.

## Source

- `core/architecture.py:178-384` (resolution, save whitelist, profiling stubbing).
- `core/spec_model.py:87-174` (`ArchitectureContext` dataclass + default view patterns).
- `knowledge-data-config.md` (mined inventory + design-decision notes).

## Related

[[ref-three-database-architecture]] · [[ref-knowledge-base-file-inventory]] ·
[[ref-view-name-token-resolution]] · [[ref-multi-impl-fan-out-engine]] · [[ref-config-editor]] ·
[[ref-profiling-view-generation]] · [[std-view-naming-patterns]] · [[ref-ports-install-and-versioning]] ·
[[std-studio-config-shape]] · [[prn-studio-design-principles]]
