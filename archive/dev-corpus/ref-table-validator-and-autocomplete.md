---
id: ref-table-validator-and-autocomplete
type: reference
title: Table Validator & Autocomplete
domain: sap
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-local-deriver
  - relates:ref-sql-generator
  - relates:ref-schema-ingestion
  - relates:ref-sap-metadata-validators
  - relates:ref-value-description-resolution
  - relates:ref-deletion-flag-resolver
sources:
  - vault:sap-knowledge/Table Validator & Autocomplete.md
tags: [studio, engine, sap, agent, course]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

`TableValidator` is the enforcement point for "SAP table names use autocomplete-with-validation,
not free text" — a name is valid only if it is in the table registry, harvested from the knowledge
base, or matches a custom `Z*`/`Y*` prefix; everything else fails validation and gets up to 5
fuzzy suggestions.

This is the SAP-side gate that stops a typo'd or invented table name from reaching the
[[ref-local-deriver|Studio — Local Deriver]] or [[ref-sql-generator|SQL generator]]. Three
independent capabilities live here: **validate** (yes/no + metadata), **search**
(autocomplete-as-you-type), and **suggest** (fuzzy "did you mean").

## What it does

On construction it builds one merged in-memory table map (`self._tables`, name → info dict) from
several sources, then serves three public methods plus `get_info` / `__contains__`. Names are
normalised to **upper-case** everywhere; lookups are case-insensitive.

## Table sources (merged at load, registry wins)

| Order | Source file | `source` tag | Notes |
|---|---|---|---|
| 1 | `erp/<id>/table_registry.json` (`tables[]`) | `registry` | Richest metadata — `name`, `description`, `module`, `category` (`:169-183`) |
| 2 | `domains.json`, `joins.json`, `primary_keys.json` | `knowledge_base` | Harvested, minimal entry. **Only added if not already in registry** (`:185-262`) |

KB harvest pulls every table it can find: domain-level named tables (`mainTable`, `coCodeTable`,
`salesTable`, `purchTable`, `itemTable`, `depTable`, `plantTable`, `descTable`), plus
`orgScopes`, `fields`, `fieldScopes`, and `deletionFlags` tables; both `source`/`target` of every
join; and every `primary_keys.json` key. (`:200-251`)

## Custom Z*/Y* are always valid

`custom_table_prefixes` is read from `erp/<id>/config.json` (ships as `["Z", "Y"]`) and compiled
into `^(Z|Y)` with `re.IGNORECASE`; fallback when no config is `_DEFAULT_CUSTOM_PREFIX_RE = ^[ZY]`.
(`:148-161`) A match short-circuits to valid with `source="custom"`, `module="Custom"`,
`category="custom"`, `description="Custom table"`. (`:307-316`)

## validate() — the gate

`validate(table_name)` (`:268-326`) returns a `ValidationResult(valid, table_name, description,
module, category, source, suggestions)`:

1. Empty / whitespace → `valid=False`, `source="unknown"`, `"Empty table name"`.
2. Known (registry or KB) → `valid=True` with that entry's metadata.
3. `Z*`/`Y*` → `valid=True`, `source="custom"`.
4. Otherwise → `valid=False`, `description="Table not recognised"`, plus `suggest(name, limit=5)`.

> [!tip] Do / Don't (agent)
> **Do** route every user-supplied SAP table name through `validate()` before deriving. **Do**
> allow any `Z*`/`Y*` name through unchallenged. **Don't** accept free-text table names, and
> **don't** silently drop an unknown name — surface the suggestions.

## search() — autocomplete ranking

`search(query, limit=10)` (`:342-403`) walks the sorted name list and buckets each hit, returning
them in strict priority order (deduped, capped at `limit`):

1. **Exact** name match
2. Name **starts with** query
3. Name **contains** query
4. **Description** contains query

So typing `MAR` returns MARA/MARC/MARD before a table whose *description* merely mentions
"market".

## suggest() — fuzzy "did you mean"

`suggest(table_name, limit=5)` (`:409-455`) scores every known name; **lower is better**:

```
score = edit_distance(q, name)        # two-row Levenshtein
        - (shared_prefix_len * 0.5)   # reward a matching prefix
        + (len_diff * 0.3)            # penalise length difference
```

Sorted by `(score, name)`. This is one of three independent fuzzy implementations in the
codebase — [[ref-schema-ingestion|Schema Ingestion (DDL/DBML/CSV)]] has its own table/field
suggesters with different rules, so don't assume a shared utility.

## Inputs & outputs

- **In:** a table name (any case) or a partial query string.
- **Out:** `validate` → `ValidationResult` (`.to_dict()` for JSON responses); `search` → list of
  info dicts (`name`, `description`, `module`, `category`, `source`); `suggest` → list of name
  strings. `get_info(table)` enriches a known table with its `primary_key` from
  `primary_keys.json` on demand (`:472-495`); `__contains__` honours the custom prefix
  (`:556-561`).

## Source

`core/table_validator.py:1-563` — `validate` (`:268`), `search` (`:342`), `suggest` (`:409`),
`_load_registry` (`:169`), `_load_knowledge_base_tables` (`:185`), `_load_custom_prefix_re`
(`:148`), `ValidationResult` (`:27`).

## See also

- [[ref-sap-baseline-model|SAP Baseline Model (logical vs physical)]] — the deeper
  logical/physical name model; the validator only checks *names exist*, not physical-column
  fidelity
- [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]] ·
  [[ref-value-description-resolution|Value-Description Resolution (4 mechanisms)]] — sibling SAP-
  knowledge resolvers, same provenance-tag pattern
- [[ref-schema-ingestion|Schema Ingestion (DDL/DBML/CSV)]] — the other place fuzzy table/field
  suggestion lives
- [[ref-sap-metadata-validators|SAP Metadata Validators (Pillars A & B)]] — curated-metadata vs
  baseline cross-checks
- [[ref-knowledge-base-file-inventory|Studio — Knowledge Base File Inventory]] — the JSON files
  this validator harvests
- [[ref-local-deriver|Studio — Local Deriver]] ·
  [[ref-architecture-context-and-project-yamls|Studio — Architecture Context & Project YAMLs]]
