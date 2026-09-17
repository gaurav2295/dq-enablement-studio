---
id: ref-output-section-builders
type: reference
title: Output Section Builders
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - parent:ref-local-deriver
  - prereq:ref-field-matching
  - relates:ref-no-silent-material-fallback
  - relates:ref-logic-builder-templates
  - relates:ref-zconcatenatedkey-and-ziserrorflag-sql-emission
  - relates:ref-sql-generator
  - relates:gls-basic-fields
  - relates:gls-value-context
sources:
  - vault:studio-architecture/Studio — Output Section Builders.md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

Five per-section helpers (`_build_output_tech` / `_basic` / `_org` / `_value` / `_activity`) each
emit the `OutputField`s for one column group of a derived spec — auto-injecting the domain key,
org-scope keys, Plant/Company Code, and a value field — then `_resequence` renumbers every field
into SQL output order (Tech → Basic → Org → Value → Activity).

These run inside [[ref-local-deriver|Local Deriver's derive_spec]] after
[[ref-field-matching|field matching]]. Each builder takes the domain definition + the
matched-field list and returns `(fields, pos)`, threading a shared position counter so sections
don't collide before the final resequence.

## What each builder does

- **Basic** (`_build_output_basic`) — first row is always the **domain key field**: element
  `"<DomainFirstWord> Number"` (e.g. "Material Number"), `key="Yes"`, table = `plantTable` if the
  domain has one else `main_table`. Then appends matched fields where `cat=="basic"` **or** (no cat
  **and** table == main_table).
- **Org** (`_build_output_org`) — emits the detected scope's key fields (e.g. WERKS, VKORG, VTWEG,
  SPART) as `key="Yes"`; then **auto-adds Plant** (`<plantTable>.WERKS`, `key="Yes"`) when
  `plantTable` is in `tables_used` and WERKS isn't already a scope key; **auto-adds Company Code**
  (`<coCodeTable>.BUKRS`) under the same in-use-and-not-duplicate guard; finally appends matched
  `cat=="org"` fields, de-duplicated on `table_field`.
- **Value** (`_build_output_value`) — matched `cat=="value"` fields (carry their `aggregation`); a
  back-compat pass for uncategorised fields from **non-main** tables; then the fallback below.
- **Activity** (`_build_output_activity`) — matched `cat=="activity"` fields (carry aggregation).
  Simplest builder: no auto-injection.
- **Tech** (`_build_output_tech`) — `zSourceSystemID` (key), `zConcatenatedKey` (key,
  `value="Calculated"`), `zIsErrorFlag` (`value="BIT (1/0)"`). The concat instruction is assembled
  from **Basic + Org rows whose `key=="Yes"`**, de-duplicated by bare field name, always prefixed
  with `<main_table>.zSourceSystemID`. Info/Profiling rules call `_build_output_tech_info` instead
  — same two key fields but **no `zIsErrorFlag`** (no error detection).

## Key conventions (do / don't)

- **Value fallback fires ONLY when there is at least one confident match.** If `fields` is empty
  AND `matched` is non-empty AND no matched field is non-basic/non-org, inject the domain's first
  `cat=="basic"` field (else the first field) as a Value column, and append a `generic`
  `_MatchedField` so downstream SQL has a column to render.
- **DON'T inject anything when `matched` is empty.** The builder explicitly skips the fallback in
  that case — the code comment says injecting a random field "causes hallucinated SQL." This is
  the value-section half of the [[ref-no-silent-material-fallback|no-silent-fallback]] guard.
- **Plant / Company Code are auto-added only if their table is actually used**
  (`plantTable`/`coCodeTable` in `tables_used`) and not already present as a scope key — never
  speculatively.
- **`_resequence` is the single source of column order**: it renumbers `position` 1..N across
  `[*tech, *basic, *org, *value, *activity]`, so SQL output order is fixed regardless of the order
  builders ran or the per-section counters.
- The Tech concat key uses an underscore separator (`+ '_' +`), per the ADM `zConcatenatedKey` (no
  space) convention — see [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission|zConcatenatedKey &
  zIsErrorFlag SQL Emission]].

> [!note] Implementation status — resolved 2026-07-01 — B3 (zConcatenatedKey separator + NULL keys)
> Canonical rule: the separator is **`_` (underscore)**, NULL-safe (a NULL key column must not null
> the whole key), never NULL, and **identical across local-derive and catalog/promotion**. The app
> now implements this on both paths — the catalog/promotion separator was migrated `'|'`→`'_'`, the
> `CONCAT` is NULL-safe, and a keyless fallback emits `''` (empty string) rather than NULL — so the
> two paths are converged on a NULL-safe `_` concat (KNOWN-ISSUES B3, fixed 2026-07-01).

## Inputs & outputs

| | |
|---|---|
| **Inputs** | `domain_def` (key/plant/coCode tables, fields), `matched` (List[_MatchedField]), `main_table`, `detected_scope`, `tables_used`, shared `pos` |
| **Per-builder output** | `(List[OutputField], pos)` — Value also returns the (possibly augmented) `matched`; Tech/Tech-info build the concat instruction from Basic+Org keys |
| **Final output** | `all_output = [*tech, *basic, *org, *value, *activity]` after `_resequence`, attached to the spec's `output_fields` |
| **Side effects** | Value fallback may append to `matched` and add a table to `tables_used` |

## Source

- `core/local_deriver.py:324-557` — the five `_build_output_*` builders (Basic, Org, Value,
  Activity, Tech / Tech-info)
- `core/local_deriver.py:491-532` — Value-section fallback (inject domain first-basic field only
  when `matched` is non-empty)
- `core/local_deriver.py:1163-1176` — `_resequence` (renumber positions into
  Tech→Basic→Org→Value→Activity SQL order)

## Related

[[ref-local-deriver]] · [[ref-field-matching]] · [[ref-rule-type-detection]] ·
[[ref-no-silent-material-fallback]] · [[ref-logic-builder-templates]] ·
[[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]] · [[ref-sql-generator]] ·
[[ref-profiling-view-generation]] · [[ref-dqrulespec-data-model]]
