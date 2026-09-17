---
id: ref-layer-2-layer-4-datastore-views
type: reference
title: Layer-2/Layer-4 Datastore Views
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - contrast:ref-sql-generator
  - relates:ref-view-name-token-resolution
  - relates:ref-datastore-substitution-and-erp-compat-check
  - relates:ref-deletion-flag-normalization-in-sql-gen
  - relates:ref-three-database-architecture
  - relates:std-view-naming-patterns
  - contrast:con-data-architecture-layers
  - relates:gls-bridge-view
  - relates:gls-filter-view
sources:
  - vault:studio-architecture/Studio — Layer-2-Layer-4 Datastore Views.md
tags: [studio, engine, sap, methodology]
created: 2026-08-20
updated: 2026-08-20
---

> [!note] Not the same "Layer 2/4" as the data architecture
> Layer 2/Layer 4 here is the datastore-view naming (filter view / bridge view), not the
> four-layer data architecture stack in [[con-data-architecture-layers]] (Source → Source DA →
> Prep → Working). Don't map one numbering onto the other.

## Summary

`view_generator.py` emits the two datastore layers that sit *under* the DQ rules: a Layer-2
*relevancy filter* view (what to keep/remove) and a Layer-4 *bridge* view (relevancy-scoped,
system-stamped) — exclusions are realized by flipping the operator (`_FLIP_OP`), every string
literal is `N''`-prefixed for MS SQL, and the whole set deploys via a 2-pass script with
`DROP VIEW IF` guards.

This is a separate generator from the rule SQL (see [[ref-sql-generator]]). It builds the
*plumbing* views — the relevancy layer and the bridge — not the OptSel/RptSel rule views.
`layer_strategy: {layer2: filter, layer4: bridge}` in the project YAML names the two layers.
Reached via `POST /api/views/generate`.

## What it does

Two view types, both with a fuller header than the rule generator (`view_generator.py:307-321`,
`:419-509`):

- **Layer 2 — Relevancy Filter** (`{system}_{table}_FILT`): one per **direct_relevancy** table.
  Applies the relevancy rule (inclusions + exclusions) to scope which rows of a source table are
  in play.
- **Layer 4 — Bridge View** (`{table}`): one per table, **all** tables (not just
  direct_relevancy). Carries one of three scenarios in the header — `direct_relevancy`,
  `secondary_linkage`, `no_relevancy`. The bridge adds `zSourceSystemID`, sourced from
  `filt.[zSourceSystemID]` when a Layer-2 filter exists, else a hardcoded `N'<system>'`.

Header fields: `-- Layer 2: Relevancy Filter` / `-- Layer 4: Bridge View (<scenario>)`, Table,
Source(s), Database, Inclusions, Exclusions, **Dependencies** (list of `[db].[dbo].[table]`),
Generated (`%B %d, %Y`, e.g. "June 30, 2026"). Inline join comments use the `/* TBL → SEG */`
form.

## Key conventions / algorithm

**Exclusion = operator flip** (`_FLIP_OP`, `view_generator.py:661-668`). A relevancy rule is
authored as "what to keep / remove". An INCLUSION emits the operator as-is; an EXCLUSION flips it
to its inverse, so the WHERE expresses the *keep* set:

| authored | flipped (exclusion) |
|---|---|
| `=` | `<>` |
| `IN` | `NOT IN` |
| `LIKE` | `NOT LIKE` |
| `IS NULL` | `IS NOT NULL` |

**`N''` everywhere** (`_build_where_condition`, `:671-725`). Every string literal gets the `N''`
Unicode prefix for MS SQL `NVARCHAR` safety:

- `IN` lists split the CSV and quote each element `N'v'`.
- `BETWEEN` parses `"low AND high"` or `"low,high"`; an **exclusion** BETWEEN becomes `(field <
  N'low' OR field > N'high')`.
- `_parse_condition` (`:621-657`) splits a combined string into `(operator, value)` — handles
  `IS NULL`, `IS NOT NULL`, `NOT IN`, `IN`, `NOT LIKE`, `LIKE`, `BETWEEN`, and `>= <= <> = > <`.

**2-pass deploy script** (`generate_deploy_script`, `:514-608`):

1. **Pass 1** — emit ALL Layer-2 (filter) views.
2. **Pass 2** — emit ALL Layer-4 (bridge) views.

Each view is preceded by an idempotent guard:

```sql
IF OBJECT_ID('[db].[dbo].[<view>]', 'V') IS NOT NULL DROP VIEW [db].[dbo].[<view>];
GO
```

The ordering matters because bridges depend on filters — filters first guarantees the bridge's
`FROM` resolves on a clean deploy.

## Inputs & outputs

- **In:** a set of tables with relevancy rules (inclusions/exclusions), the resolved
  `ArchitectureContext` (databases, `system_aliases`, view-name patterns), `layer_strategy`.
- **Out:** Layer-2 filter views (direct_relevancy tables only) + Layer-4 bridge views (all
  tables) + a single deterministic 2-pass deploy script.

## Source

- `core/view_generator.py:307-321`, `:419-509` — Layer-2 / Layer-4 view headers.
- `core/view_generator.py:621-657` — `_parse_condition`.
- `core/view_generator.py:661-668` — `_FLIP_OP` (exclusion operator inversion).
- `core/view_generator.py:671-725` — `_build_where_condition` (`N''`, IN, BETWEEN).
- `core/view_generator.py:514-608` — `generate_deploy_script` (2-pass + DROP-IF guards).
- Detail: `knowledge-mining/sql-generation.md` §7.6, §13.

> [!tip] Implementation status — resolved 2026-07-01
> - **B2 (view-name `{system}`)** — Canonical view names are
>   `DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}` for Error/Info views, and the layer
>   views here use `{system}_{table}_FILT` (filter) and `{table}` (bridge). `{system}` must be
>   the **production** system / agreed alias (e.g. `PD1`), never the interim QA system. The
>   `system_aliases` **keys** are authoritative; the value only fills the cosmetic view-name
>   slot, so the filter value and the name suffix can't drift. The app now enforces a single
>   canonical view-name pattern — the YAML resolver defaults were aligned to the dataclass so
>   `{system}` is always present, and the canonical Error/Info pattern now carries the `{desc}`
>   token.
> - **B4 (prep layer)** — The canonical topology is `source → SRCECC_DA → WRKDQPREP_ALL
>   (upstream prep) → WRKDQ (rules created + read here)`, owned by `architecture.md` + its
>   mermaid, not per-YAML. `WRKDQPREP_ALL` is the upstream prep layer — it applies relevancy
>   criteria, merges sources, performs logical aggregation, and applies scope for one or many
>   source systems — and its output is **pushed into `WRKDQ`**; rule views do NOT read
>   `WRKDQPREP_ALL`. The canonical SELECT-FROM target is **`WRKDQ`** (one repository, same-DB
>   read): rule views are created in AND read from `WRKDQ`. Profiling views already read
>   `FROM WRKDQ` correctly, and the app now reads Error/Info rule views `FROM`/`JOIN` `WRKDQ`
>   too — one repository, matching profiling, with `WRKDQPREP_ALL` scoped to upstream ETL only.
>   The bridge's `Database`/`Dependencies` resolve from this standard model.

## Related

- [[ref-sql-generator]]
- [[ref-view-vs-table-qualification]]
- [[ref-view-name-token-resolution]]
- [[ref-datastore-substitution-and-erp-compat-check]]
- [[ref-deletion-flag-normalization-in-sql-gen]]
- [[ref-sql-parser]]
- [[ref-three-database-architecture]]
- [[ref-architecture-context-and-project-yamls]]
- [[std-view-naming-patterns]]
