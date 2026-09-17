---
id: ref-deletion-flag-normalization-in-sql-gen
type: reference
title: Deletion Flag Normalization in SQL Gen
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - implements:prn-deletion-flags-belong-in-where
  - prereq:ref-deletion-flag-resolver
  - relates:ref-generate-sql-dispatcher
  - relates:ref-local-deriver
  - relates:ref-dqrulespec-data-model
  - relates:ref-logic-case-predicate-templates
  - relates:con-deletion-flags-vs-status-fields
  - relates:std-deletion-filter-marker
sources:
  - vault:studio-architecture/Studio — Deletion Flag Normalization in SQL Gen.md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`_normalise_deletion_flags` moves any `LVORM` / `LOEKZ` / `LOEVM` predicate out of the error CASE
and into the WHERE as an EXCLUSION — except for deletion-DETECTION rules, where the deriver sets
`_deletion_is_error=True` to keep the flag as the error condition.

This is the code that enforces the methodology rule: **a deletion flag belongs in the WHERE (as a
scope exclusion), never in the `zIsErrorFlag` CASE — unless the rule's whole point is to detect
deletion.** Duplicating the same condition in both WHERE and CASE is dead code and is never
correct. It runs in two places: defensively at the top of [[ref-generate-sql-dispatcher|generate_sql]],
and at derivation time in [[ref-local-deriver]].

## What it does

`_normalise_deletion_flags(spec)` (`core/sql_generator.py:84-129`), called first thing inside
`generate_sql`:

- **The set**: `_DELETION_FLAG_FIELDS = {"LVORM", "LOEKZ", "LOEVM"}` (`sql_generator.py:81`).
- **Sweep `spec.logic`**: any logic entry whose `table_field` references a deletion flag is
  **removed from `spec.logic`** and **re-added to `spec.filters`** as a `FilterType.EXCLUSION`
  with the micro-DSL condition `IF <tbl>.<flag> = 'X' THEN Exclude`. The flag therefore renders
  in the WHERE (`/* Exclude: … */ ISNULL(<tbl>.<flag>,'') <> 'X'`), not in the per-row CASE.
- **Opt-out for deletion-detection**: when `spec._deletion_is_error` is `True`, the sweep is
  skipped — the flag stays in `spec.logic` and becomes the
  `CASE WHEN <tbl>.<flag> = 'X' THEN 1 ELSE 0 END` error condition. Removing it would flag
  nothing, because the WHERE exclusion would have already dropped every record the rule means to
  surface.
- **Defensive layer**: both derivers already classify correctly; this pass also catches
  AI-constructed or hand-edited specs that mis-placed a deletion flag in logic.

## Why two paths agree — the deriver side

The deriver decides intent *before* SQL generation, and the dispatcher is the safety net:

- `_detect_deletion_intent(rule_name)` (`local_deriver.py:1018-1035`) — regex
  `_DELETION_INTENT_RE` matches `marked for deletion | flagged for deletion | not be deleted |
  deletion (flag|indicator)`. It deliberately does **not** match "must have an active material"
  (there, deletion stays an exclusion).
- On a match (and the rule is not info/profiling and has no other matched logic),
  `_build_deletion_logic` (`local_deriver.py:1047-1070`) emits `element="Marked For Deletion"`,
  `value="1 - If (<tf> = 'X')\n0 - If (<tf> <> 'X')"`, sets `deletion_is_error=True`, and records
  `deletion_skip={(main_table, flag)}`.
- `_build_exclusions(... skip_flags=deletion_skip)` then **skips** that flag so it is *not* also
  emitted as a WHERE exclusion — preventing the duplicate.
- `_deletion_is_error` is the **only transient (underscore) attribute round-tripped through
  serialization** (`spec_model.py:352-357`, restored `:461-463`), so a manual edit → regenerate
  cycle preserves deletion-detection intent.

> [!note] Resolution order is upstream of this pass
> *Which* column is the flag for a given table (the `LVORM` vs `LOEVM` vs `LOEKZ` choice) is
> decided earlier by the 3-tier [[ref-deletion-flag-resolver|Deletion Flag Resolver]]: baseline
> DD% physical columns → domain definition → standard registry. `_normalise_deletion_flags` only
> re-homes a predicate it is *given*; it does not pick the column.

## Do / don't (for AI-derived and hand-edited specs)

- **DO** put a deletion flag in `spec.filters` as an EXCLUSION for a normal rule (e.g. "an
  inspection plan must have an active material" → WHERE excludes `LVORM = 'X'`, CASE checks the
  *status* field — see [[ref-sap-baseline-model]]).
- **DO** set `_deletion_is_error=True` for a genuine deletion-detection rule, and let the flag
  drive the CASE.
- **DON'T** put the same deletion condition in **both** WHERE and CASE — it is logically
  redundant (the WHERE already removed those rows; the CASE branch is dead).
- **DON'T** call `generate_optsel` directly to bypass this pass — only `generate_sql` guarantees
  normalisation runs.

## Concrete example

| Rule intent | `_deletion_is_error` | Where the flag lands |
|---|---|---|
| "Material must have a valid base UoM" | `False` | WHERE: `/* Exclude: deleted */ ISNULL(MARA.LVORM,'') <> 'X'` |
| "Material must not be marked for deletion" | `True` | CASE: `WHEN MARA.LVORM = 'X' THEN 1 ELSE 0 END AS [zIsErrorFlag]` |

> [!tip] Implementation status — resolved 2026-07-01 (B1 — KNA1/LFA1 deletion flag)
> The canonical per-table flag for **KNA1 and LFA1 is `LOEVM`** (SAP-standard, *not*
> customer-specific). Some curated metadata historically guessed `LVORM`; a customer's DD03L
> extract that lacks physical `LVORM` would fail at deploy. The app now standardizes KNA1 = LOEVM
> and LFA1 = LOEVM across the resolver, registry, curated metadata, and domain definitions, with
> DD% acting as override-only (confirm/override authority).

## Source

- `core/sql_generator.py:81` — `_DELETION_FLAG_FIELDS = {"LVORM","LOEKZ","LOEVM"}`
- `core/sql_generator.py:84-129` — `_normalise_deletion_flags` (logic → filters EXCLUSION;
  opt-out on `_deletion_is_error`)
- `core/local_deriver.py:1018-1035` — `_detect_deletion_intent` / `_DELETION_INTENT_RE`
- `core/local_deriver.py:1047-1070` — `_build_deletion_logic` (sets `deletion_is_error`,
  `deletion_skip`)
- `core/local_deriver.py:957-1002` — `_build_exclusions(..., skip_flags=…)` skips the detection
  flag
- `core/spec_model.py:352-357`, `:461-463` — `_deletion_is_error` round-trip through
  serialization

## Related

- [[ref-generate-sql-dispatcher]]
- [[ref-local-deriver]]
- [[ref-logic-case-predicate-templates]]
- [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]]
- [[ref-sql-generator]]
- [[ref-deletion-flag-resolver]]
- [[ref-sap-baseline-model]]
- [[ref-dqrulespec-data-model]]
- [[std-deletion-filter-marker]]
