---
id: ref-sap-metadata-validators
type: reference
title: SAP Metadata Validators (Pillars A & B)
domain: sap
audience: [developer]
level: advanced
status: review
links:
  - prereq:ref-sap-baseline-model
  - relates:ref-deletion-flag-resolver
  - relates:ref-sap-deletion-flags-vs-status-fields
  - relates:ref-table-validator-and-autocomplete
  - relates:ref-schema-ingestion
  - relates:ref-sap-dd-dictionary-tables
sources:
  - vault:sap-knowledge/SAP Metadata Validators (Pillars A & B).md
tags: [sap, engine, methodology]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

Two cross-checks that grade the Studio's hand-curated SAP metadata against the authoritative
[[ref-sap-baseline-model|SAP Baseline Model (logical vs physical)]]: **Pillar B** (ships today,
Erwin-only — table existence, PK-count-minus-MANDT, FK reachability) and **Pillar A** (deferred
until DD% lands — physical column / deletion-flag verification). When the baseline is absent the
validator goes to standby and CI treats it as a pass.

`core/sap_metadata_validator.py` reads `knowledge/sap/table_metadata.json` (87 curated entries
today) and `knowledge/sap/sap_ecc_baseline.json`, then enumerates every disagreement so the user
knows WHICH curated entries to fix — it never edits the metadata.

## Two pillars

| | Pillar B — ships today | Pillar A — deferred (needs DD%) |
|---|---|---|
| **Trusts** | Erwin XML (logical model) | DD% extracts (physical column names) |
| **Checks** | table existence, PK count, FK reachability | deletion-flag column name, exact PK physical names, column type / nullability |
| **Why split** | Erwin gives logical English names only | only DD% can confirm physical names like `LVORM`, `KUNNR` |

Pillar A is what catches the **KNA1=`LOEVM` bug class** (a customer whose DD03L shows only
`LOEVM`) — it cannot run until DD% has spoken (`BaselineTable.has_physical_columns()`). The
curated metadata now assumes `LOEVM` as the SAP-standard `KNA1`/`LFA1` deletion flag
(KNOWN-ISSUES B1, fixed 2026-07-01), so Pillar A's role is confirming per-customer physical drift
rather than correcting a baked-in wrong default. The `Finding` shape is already future-proof, so
Pillar A lands as new finding *kinds* with no validator rewrite.

## Pillar B — the three checks

(`sap_metadata_validator.py:236-296`)

1. **Table existence** — the table must appear in the baseline, OR be annotated
   `baseline_status: "not_in_export"` (legacy field name `erwin_status`). Missing →
   `kind="table_missing_in_baseline"`, `severity="warn"`.
2. **PK count rough agreement** — metadata PKs typically start with `MANDT`; baseline logical PKs
   usually don't capture it. Expectation: `len(baseline_pks) == len(metadata_pks minus MANDT)`.
   Mismatch → `kind="pk_count_mismatch"`, `warn`. (MANDT is stripped before the compare — same
   single-working-DB justification as `composite_keys.json`.)
3. **FK reachability** — every `related_tables` entry should have an Erwin FK path: outbound on
   this entry's `foreign_keys`, OR inbound via a prebuilt `inbound_index` (built once per run so
   it doesn't walk every table per query). Missing → `kind="fk_link_not_in_baseline"`, `warn` —
   soft because Erwin captures the LOGICAL subset; some relationships exist physically but aren't
   drawn.

## Key conventions

- **Severity contract.** `error` is reserved for hard contracts; everything baseline-soft is
  `warn`. CLI `main()` returns exit 1 **only** if `error_count > 0` (`:327-346`).
- **Standby pass when baseline absent.** If `sap_ecc_baseline.json` has no tables, the validator
  emits exactly one `kind="baseline_not_available"` **warn**, skips every baseline-dependent check
  (so CI isn't flooded with phantom missing-table findings), and — because the report carries 0
  errors — **CI treats it as a pass**. The user still sees the validator is in standby
  (`:187-200`).
- **`not_in_export` → skipped, not a finding.** Opted-out tables (custom Z*/Y*, or modules whose
  Erwin file isn't exported yet) increment `skipped_count`, which tells the user how much metadata
  is currently uncheckable (`:215-225`). Keys starting with `_` are meta blocks and skipped
  (`:211-214`).
- **Provenance everywhere.** The whole SAP subsystem is built so a reviewer can trace a fact's
  origin. [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]] mirrors this:
  `DeletionFlagResolution(table, field, source)` carries `source ∈ {baseline, domain, fallback,
  unknown}` so a reviewer can ask "where did this `LOEVM` come from?" and read the answer off the
  resolution (`deletion_flag_resolver.py:82-94`).
- **Back-compat aliases.** `erwin_available` / `erwin_table_count` are property aliases for
  `baseline_available` / `baseline_table_count`; the legacy kwarg `erwin_truth_path` is honoured
  over `baseline_path` for one deprecation cycle (`:132-147, 160-171`).

## Inputs & outputs

- **In:** `knowledge/sap/table_metadata.json` (curated; `primary_keys`, `related_tables`, optional
  `baseline_status`); `knowledge/sap/sap_ecc_baseline.json` (via `BaselineModel.load_or_empty`).
- **Out:** a `ValidationReport` (`findings`, `tables_checked`, `baseline_available`,
  `baseline_table_count`, `skipped_count`; `error_count`/`warn_count` derived). Runnable from
  pytest and from CLI (`python3 -m core.sap_metadata_validator`, `--verbose` / `--json`).

> [!tip] Implementation status — resolved 2026-07-01 (KNOWN-ISSUES B1, KNA1 deletion flag)
> Canonical rule: **`KNA1` (and `LFA1`) deletion flag is `LOEVM`** (SAP-standard, NOT
> customer-specific). The app now implements this canonical behaviour: the deletion flag for
> `KNA1` & `LFA1` is `LOEVM` across the resolver, standard registry, curated metadata, and domain
> definitions, and DD% is treated as **override-only** (KNOWN-ISSUES B1, fixed 2026-07-01).
> Resolution order is **baseline DD% physical → domain definition → standard registry** — DD%
> confirms or overrides the standard, it is not its source. Pillar A's
> `deletion_flag_matches_baseline` criterion remains the designed mechanism to catch any
> remaining curated-metadata-vs-reality drift once DD% lands; today only Pillar B ships.

## Source

`core/sap_metadata_validator.py:160-346` (Pillar B docstring `:1-78`; standby pass `:187-200`;
skip/meta `:211-225`; three checks `:236-296`; CLI exit code `:327-346`); provenance dataclass
`core/deletion_flag_resolver.py:82-94`.

## Related

- [[ref-sap-baseline-model|SAP Baseline Model (logical vs physical)]]
- [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]]
- [[ref-sap-deletion-flags-vs-status-fields|SAP Deletion Flags vs Status Fields]]
- [[ref-table-validator-and-autocomplete|Table Validator & Autocomplete]]
- [[ref-schema-ingestion|Schema Ingestion (DDL/DBML/CSV)]]
- [[ref-sap-dd-dictionary-tables|SAP DD% Dictionary Tables]]
- [[ref-building-a-per-client-dd-dictionary|Building a Per-Client DD% Dictionary]]
