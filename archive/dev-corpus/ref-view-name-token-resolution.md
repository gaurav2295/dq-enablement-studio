---
id: ref-view-name-token-resolution
type: reference
title: View Name Token Resolution
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-sql-generator
  - relates:ref-generate-sql-dispatcher
  - relates:ref-view-vs-table-qualification
  - relates:ref-profiling-view-generation
  - implements:std-view-naming-patterns
  - relates:ref-dqrulespec-data-model
sources:
  - vault:studio-architecture/Studio — View Name Token Resolution.md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

Every DQ view name is a `{token}` template — `DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}`
— resolved by plain string substitution, where `{system}` follows a 4-step precedence ending in
the literal `SYS`, `{desc}` is a 50-char keyword-extracted slug, and any token absent from the
pattern is silently dropped.

`resolve_view_name(pattern, **kwargs)` does flat `{token}` substitution. All five tokens —
`{id}`, `{system}`, `{table}`, `{field}`, `{desc}` — are always passed, but only the ones
literally present in the pattern string appear in the output. This sits downstream of
[[ref-local-deriver|derive_spec]] and feeds the [[ref-sql-generator|SQL generator]] and the
`CREATE VIEW [dbo].[<name>]` emit.

## Token resolution (concrete)

- **`{id}`** — 4-digit zero-padded rule id (`DQ_0042_…`). MUST equal the `-- Rule ID:` SQL banner;
  the [[ref-sql-parser|parser]] and [[ref-sql-validator|validator]] route on it.
  `view-name-rule-id-mismatch` (validator, High) fires when `DQ_NNNN_` in the name diverges from
  the banner (leading zeros stripped) — that's the sibling-replication bug signature.
- **`{system}`** — production system ID / agreed alias (e.g. `P06`, `PD1`). Resolved by
  `_resolve_system_token(spec)` with a strict precedence (below). Never the interim QA system.
- **`{table}` / `{field}`** — SAP physical names, table uppercased. `{table}` =
  `_determine_main_table` (first join's source, else first `TABLE.FIELD` in output fields,
  fallback `"TBD"`). `{field}` for OptSel/RptSel = last segment of the first logic entry's
  `table_field` (fallback `"TBD"`); InfSel uses first BASIC field; PrfSel/PrfSum uses
  `profiled_field`.
- **`{desc}`** — Title_Case slug from `create_description_from_rule_name`, capped at 50 chars (see
  below).
- **`{ViewType}`** — literal suffix baked into the pattern: `_OptSel | _RptSel | _InfSel | _PrfSel
  | _PrfSum`. Separator is `_` throughout.

Docstring example: `DQ_0042_P06_KNA1_KTOKD_OptSel` (id=0042, system-alias=P06, table=KNA1,
field=KTOKD).

## The `{system}` precedence — 4 steps, never empty

`_resolve_system_token(spec)` (`sql_generator.py:33-54`):

1. `spec.system_alias` — explicit friendly form on the impl (e.g. `"P06"`).
2. `resolve_system_alias(arch, spec.system_filter)` — look up `arch.system_aliases` for the
   per-impl `zSourceSystemID` code; fall through to the code itself when unmapped.
3. `arch.source_system` — legacy single-system fallback.
4. Literal `"SYS"` — guarantees the token is never empty.

Example: a `Z06` impl with `system_aliases: {Z06: P06}` produces `DQ_0042_P06_KNA1_…` instead of
`DQ_0042_SRCECCZ06_…`. The `system_aliases` **keys** are the authoritative `zSourceSystemID`
filter values; the **value** is only this cosmetic view-name slot — so the WHERE filter and the
name suffix can never drift.

## The `{desc}` slug — keyword extraction, 50-char cap

`create_description_from_rule_name(rule_name)` (`sql_generator.py:1890-1958`): strip leading
articles (A/An/The/This) → strip modal phrases (`must be|have|include|contain|equal|match|not|…`)
→ strip auxiliaries (`shall|should|can|cannot|…`) → strip prepositions → drop stop-words → take up
to 6 significant words (>2 chars) → Capitalize each → join with `_` → strip non-word chars →
truncate to 50 chars. Empty input → `"Rule_Description"`.

> Example: `"A material must have a valid base unit of measure"` → `Material_Valid_Base_Unit_Measure`.

## Canonical rule (do / don't)

- **DO** keep `{id}` equal to the `-- Rule ID:` banner, always. Routing depends on it.
- **DO** use the production `{system}` / agreed alias — never the interim QA system.
- **DO** treat `{desc}` as FIXED once assigned (rename churn breaks downstream references).
- Error/Info views (OptSel/RptSel/InfSel) **include** `{system}`; profiling views (PrfSel/PrfSum)
  **omit** it by default (optional for per-system profiling). The project YAML resolver is the
  production path and must be the single canonical pattern set.

> [!note] Implementation status — resolved 2026-07-01 — B2 (view-name `{system}`)
> Canonical: OptSel/RptSel/InfSel patterns include `{system}`. There is now one canonical
> view-name pattern set: the `architecture.py::resolve_architecture` YAML resolver defaults were
> aligned to the `spec_model.ArchitectureContext` dataclass, so `{system}` is present on both
> paths and the system code appears regardless of path. The app now uses the single
> system-included pattern set as canonical.

> [!note] Implementation status — resolved 2026-07-01 — B6 (`{desc}`)
> Canonical: `{desc}` is part of the name. The canonical pattern now includes the `{desc}` token —
> `DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}` — so the 50-char slug is emitted into the
> resolved view name. The app now bakes `{desc}` into the default-resolved name.

## Inputs & outputs

| | |
|---|---|
| **Inputs** | pattern string (from `ArchitectureContext.naming`), `spec` (for `{system}`, `{table}`, `{field}`, `{desc}` derivation), `arch` (aliases / source_system) |
| **Output** | resolved view name string; consumed as `CREATE VIEW [dbo].[<name>]` (always 2-part, never 3-part) |
| **Length** | only the 50-char cap on `{desc}` is enforced in this code; canonical target is total name ≤128 (SQL Server). The ≤100/≤85 ADM limit is the rule name, not the view name |

## Source

- `core/sql_generator.py:33-54` — `_resolve_system_token` (4-step `{system}` precedence ending in
  `"SYS"`)
- `core/sql_generator.py:1890-1958` — `create_description_from_rule_name` (50-char keyword slug)
- `core/architecture.py:281-315` — `resolve_system_alias` + `resolve_view_name` (plain `{token}`
  substitution)
- `core/spec_model.py:107-121`, `446-453` — dataclass default patterns (with `{system}`);
  `architecture.py:262-272` — YAML default patterns (without)

## Related

- [[ref-sql-generator]]
- [[ref-generate-sql-dispatcher]]
- [[ref-view-vs-table-qualification]]
- [[ref-profiling-view-generation]]
- [[ref-sql-parser]]
- [[ref-sql-validator]]
- [[ref-architecture-context-and-project-yamls]]
- [[ref-multi-impl-fan-out-engine]]
- [[ref-dqrulespec-data-model]]
- [[std-view-naming-patterns]]
