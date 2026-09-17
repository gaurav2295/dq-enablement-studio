---
id: ref-field-matching
type: reference
title: Field Matching (longest-key-wins)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - parent:ref-local-deriver
  - relates:ref-logic-builder-templates
  - relates:ref-no-silent-material-fallback
  - relates:ref-output-section-builders
  - relates:ref-dqrulespec-data-model
  - relates:ref-sap-baseline-model
sources:
  - vault:studio-architecture/Studio — Field Matching (longest-key-wins).md
tags: [studio, engine, methodology, sap]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`_match_fields` turns the free-text rule name into an ordered list of SAP `table.field` matches:
an exact-substring pass deduped so the longer key wins on overlapping spans, position-sorted so
`matched[0]` is the rule's OBJECT, with an all-significant-words pass-2 fallback only when pass 1
finds nothing.

## What it does

After [[ref-local-deriver|the Local Deriver]] detects the domain, it calls
`_match_fields(rule_lower, domain_fields)` to resolve which of the domain's known fields the rule
name is talking about. `domain_fields` is the domain's field dictionary keyed by **business
phrase** (e.g. `"balance"`, `"balance sheet indicator"`, `"old material number"`); each value
carries `table`, `field`, `desc`, `cat`, and `agg`. The result is a list of `_MatchedField`
objects whose order is load-bearing downstream.

## Algorithm (concrete, in order)

1. **Pass 1 — exact substring.** For every `field_key` in `domain_fields`, if `field_key in
   rule_lower`, record a match and its `position` = byte offset of first occurrence in the rule
   text.
2. **Longest-key-wins overlap dedupe.** When two matched keys hit the **same span**, keep the
   LONGER key and drop the shorter. Verbatim example: rule `"…balance sheet indicator…"` matches
   both `"balance"` (→ `SKB1.SALDO`) and `"balance sheet indicator"` (→ `SKA1.XBILK`); the longer
   key (XBILK) must win — otherwise the rule would check account balance instead of the
   balance-sheet flag.
3. **Position sort.** Order surviving matches by their `position` in the rule text so the
   **leftmost phrase lands at `matched[0]`**. By SAP rule-naming convention the rule's OBJECT
   comes first, so `matched[0]` = *what is checked* and `matched[1]` = *the reference*. This is
   critical for comparison/consistency rules.
4. **Pass 2 — word-overlap fallback (only if pass 1 matched nothing).** Strip a leading article
   (`a|an|the|this`), split into words, and for each field key keep only its **significant
   words** (>3 chars). A key qualifies only when **ALL** its significant words appear in the rule
   AND **at least 2** words overlap. Candidates sort by overlap count descending. The 2-word
   floor is deliberate: a single-word overlap is too ambiguous — it stops `"old material"` from
   matching the bare key `"material"`.

## Why the ordering and dedupe matter

- `matched[0]` drives the `LogicEntry.table_field` in [[ref-logic-builder-templates]] — the
  per-row `zIsErrorFlag` check is built against the OBJECT.
- Comparison logic ("X must align with Y") reads `matched[0]` as X and `matched[1]` as Y; wrong
  ordering inverts the check.
- Longest-key-wins prevents a generic substring (`"balance"`) from shadowing the specific
  business phrase (`"balance sheet indicator"`) the author actually meant.
- Pass 2 stays conservative on purpose: a loose fallback re-introduces the hallucinated-SQL risk
  that the [[ref-no-silent-material-fallback]] guard exists to prevent.

> [!tip] Implementation status — resolved 2026-07-01
> Canonical `_match_fields` is the 4-step algorithm above (source refs
> `core/local_deriver.py:168-256`). The app now implements steps 2–3: pass 1 records each match's
> `position` (byte offset in the rule text), applies longest-key-wins overlap dedupe on the same
> span, and position-sorts so `matched[0]` follows rule-text order rather than dict-insertion
> order — a short key can no longer shadow a longer one. Pass 2 (the all-significant-words /
> ≥2-overlap fallback) was already present and continues to match the canonical rule. This closes
> the previously tracked missing dedupe + position-sort item.

## Inputs & outputs

| | |
|---|---|
| **Input** | `rule_lower` (lowercased rule name); `domain_fields` (business-phrase-keyed dict of `{table, field, desc, cat, agg}`) |
| **Output** | ordered `List[_MatchedField]`; `matched[0]` = rule OBJECT |
| **`_MatchedField`** | `__slots__ = (key, table, field, desc, cat, agg)`; `.table_field` property → `"<table>.<field>"` (`:36-46`) |
| **Empty result** | feeds the deriver's review-required / TBD guards — no field is invented |

## Source

- `core/local_deriver.py:168-256` — `_match_fields` (pass 1 exact substring + position, overlap
  dedupe, position sort, pass 2 word-overlap)
- `core/local_deriver.py:36-46` — `_MatchedField` (`__slots__`, `table_field` property)

## Related

- [[ref-local-deriver]]
- [[ref-rule-type-detection]]
- [[ref-logic-builder-templates]]
- [[ref-no-silent-material-fallback]]
- [[ref-output-section-builders]]
- [[ref-dqrulespec-data-model]]
- [[ref-sap-baseline-model]]
