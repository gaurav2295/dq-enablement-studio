---
id: ref-key-issue-vocabulary
type: reference
title: Key Issue Vocabulary (rule-repo linkage)
domain: value-outcomes
audience: [consultant, lead]
level: practitioner
status: review
sources:
  - rule-repo:README.md
  - rule-repo:data/catalogue.json (_meta.key_issue_vocabulary, _meta.composition)
tags: [rule-repo, key-issues, value-outcomes, governance]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:ref-rule-record-schema
---

## What it is

The versioned, governed list a rule's `linkage.key_issue_ids[]` joins against. Per the
catalogue's own metadata, the current wave links against `key-issue-library.json` **v0.2**,
holding **55 key issues**. The library carries no currency of its own — per that same metadata,
"key issues carry no currency; value aggregates at the value lever only" — which matches the
discipline from the value-chain side: a key issue sits between the lever (which owns the money)
and the rules (which own the evidence) and borrows from neither.

> [!note]
> The library version moves faster than this line. `_meta.key_issue_vocabulary` names v0.2 (55
> key issues), while `_meta.update_note` in the same block records the 2026-08-06 night run
> linking against a governed key-issue → lever map at library **v0.4/0.5**. Take 55 as the count
> at the version the vocabulary field names, and query the server for the live list rather than
> assuming either number is current.

## Composition, at the catalogue level

`_meta.composition` records the pipeline's output as 384 `field_proven_from_deployment` rules
plus 113 `derived_for_lever_coverage` rules (497 total) before quarantine — see
[[con-rule-provenance-model]] for what those provenance labels mean. Every one of those rules
carries the same `linkage` shape, whether or not a `key_issue_ids[]` entry was successfully
attached; an unlinked rule is an honest gap, not a hidden one (see [[ref-rule-record-schema]]).

Of that 497, **447 are outcome-linked and served**; the remaining 50 are documented exceptions,
quarantined by owner ruling on 2026-08-06 rather than force-linked. That ratio is the honest
coverage statement to quote — not "497 linked rules".

## Structure: how a rule joins to the vocabulary

A rule record does not link to a key issue by name — it links by id, through a small structured
join:

```
rule.linkage:
  key_issue_ids: [ <id>, ... ]     # the fine join — which key issues this rule evidences
  value_lever                       # the coarser join — which lever the rule ultimately backs
  outcome_category                  # coarsest — which BOA outcome bucket the lever exports to
  edges: [ { target, confidence, method }, ... ]   # per-edge evidence for all three joins above
```

`key_issue_ids[]` is deliberately the fine-grained join: several rules typically evidence one
key issue, and one key issue typically feeds exactly one value lever (see [[con-value-chain]]
for the full outcome → lever → key issue → rule chain). A rule can carry more than one key issue
id only when it genuinely evidences two distinct defects — the same one-best-fit discipline that
governs the edges themselves (see [[prn-governed-ratification]]).

Each `edges[]` entry pairs a `target` (a `lever:`, `key_issue:` or `outcome:` reference) with a
`confidence` (0–1) and a `method`. This reference intentionally does not enumerate the library's
55 entries — the library is governed vocabulary maintained outside this repository's own
metadata, and a consultant needing the live list should query the server in `server/`, not treat
this note as the source of truth for current codes.

## Related

- Key issue / value lever / outcome category — the value-chain definitions this vocabulary is
  joined against.
- [[con-value-chain]] — the full outcome-to-evidence chain this vocabulary sits inside.
- [[prn-governed-ratification]] — how a `linkage` edge earns its `method` and confidence.
