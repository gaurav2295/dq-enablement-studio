---
id: ref-no-silent-material-fallback
type: reference
title: No Silent Material Fallback (unknown domain)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - implements:prn-no-silent-domain-fallback
  - parent:ref-local-deriver
  - relates:ref-field-matching
  - relates:ref-rule-type-detection
  - relates:ref-output-section-builders
  - relates:ref-sql-generator
sources:
  - vault:studio-architecture/Studio — No Silent Material Fallback (unknown domain).md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

When the rule name matches no SAP domain, the [[ref-local-deriver|Local Deriver]] refuses to guess
MARA/MARC — it builds an intentionally un-deployable TBD placeholder spec and raises a
review-required warning, so a confidently-wrong material rule can never reach production.

## What it does

`derive_spec` calls `engine.detect_domain(rule_name)` to resolve the rule's SAP domain. When
detection returns no match, the deriver does **not** default to the `material` domain. Instead it:

- sets `domain_unknown = True`, `domain_id = ""`, and builds a TBD `domain_def` shell with empty
  fields/joins/deletionFlags and `mainTable = ""`;
- short-circuits into a deliberately un-deployable placeholder spec and returns early;
- attaches transients `_domain_confidence = 0.0`, `_fields_matched = 0`, `_domain_unknown = True`,
  and `_review_required` with a `_warnings` entry;
- lists the **covered** domains (`engine.covered_domain_names()`) in the description so the author
  can rephrase the rule name to trigger a detector.

The generated SQL renders `SELECT * FROM /* TBD */;`, which **fails at SQL parse time by design**
— a stale placeholder physically cannot deploy.

The same decision is mirrored on the profiling path (`_derive_profiling_spec`): an unknown domain
yields an empty `main_table` + `domain_unknown = True`, never a material guess.

## Why (the burn that motivated it)

Silently falling back to `material` "produced confidently-wrong MARA/MARC SQL for every FI /
intercompany / banking / project / SD rule whose name didn't trigger any domain detector" (verbatim
code comment). The profiling path comment cites the real-world hit: the **Bacardi Profit Center /
Tax Category / Field Status Group** rules, which are not material at all. A loud TBD that fails to
parse is strictly safer than a plausible-looking material view that ships wrong logic.

See the methodology rationale in [[prn-no-silent-domain-fallback|Why No Silent Domain Fallback]].

## Key conventions (do / don't)

- **DO** treat "no domain matched" as a hard stop: emit the TBD placeholder + `review_required`,
  never a `material` default.
- **DO** keep the placeholder un-deployable — `mainTable = ""` → `SELECT * FROM /* TBD */;` so it
  fails parse.
- **DON'T** confuse *unknown domain* with *domain found but no fields matched*. The latter is a
  separate guard: when a domain IS detected but `matched` is empty (and not
  Info/Profiling/deletion-detection), the deriver sets `_review_required` and the
  [[ref-sql-generator|SQL generator]] emits a **NULL `zIsErrorFlag` with `/* TBD */`** rather than
  fabricating a check. Both guards exist to stop hallucinated SQL.
- **DON'T** inject a random output field when `matched` is empty — the value-section builder
  explicitly skips its fallback in that case for the same reason ("it causes hallucinated SQL").
- The placeholder's canonical [[ref-rule-type-detection|RuleType]] (Error/Info/Profiling) still
  comes from the caller's `report_type`, so the right view type is reserved even for a TBD.

## Inputs & outputs

| | |
|---|---|
| **Input** | `rule_name`, `engine` (knowledge engine); `report_type` (Error/Info/Profiling) |
| **Trigger** | `engine.detect_domain(rule_name)` returns no match |
| **Output spec** | `domain_id = ""`, `main_table = ""`, empty body lists; transients `_domain_unknown=True`, `_domain_confidence=0.0`, `_fields_matched=0`, `_review_required`, `_warnings=[...]` |
| **Output SQL** | `SELECT * FROM /* TBD */;` (fails parse — non-deployable by design) |
| **Author signal** | description enumerates `covered_domain_names()` so the name can be rephrased |

## Source

- `core/local_deriver.py:2457-2564` — Step 1 domain detection + Step 2b domain-unknown
  short-circuit (Error/Info path)
- `core/local_deriver.py:1389-1428` — same no-material-fallback decision on
  `_derive_profiling_spec` (narrative profiling path)
- Related transient `_review_required` (domain found, no field match) set at
  `local_deriver.py:2738-2741`

## Related

[[ref-local-deriver]] · [[ref-field-matching]] · [[ref-rule-type-detection]] ·
[[ref-sql-generator]] · [[ref-dqrulespec-data-model]] · [[ref-knowledge-base-file-inventory]] ·
[[prn-no-silent-domain-fallback]]
