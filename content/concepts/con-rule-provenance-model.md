---
id: con-rule-provenance-model
type: concept
title: The Rule Provenance Model — Existence vs Text
domain: value-outcomes
audience: [consultant, lead]
level: practitioner
status: deprecated
sources:
  - rule-repo:README.md
  - rule-repo:data/catalogue.json (_meta.provenance_semantics, _meta.provenance_values, _meta.composition)
tags: [rule-repo, provenance, governance, honesty]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:gls-provenance
  - contrast:gls-provenance
  - relates:gls-adm-rule-name
  - relates:gls-implication
  - relates:con-catalog-vs-bespoke-rules
  - relates:ref-rule-record-schema
---

## The two questions, kept separate

`syniti-dq-rule-repo` answers two different questions about every rule, on purpose, with two
different fields:

1. **Does the rule exist for a real reason?** — `provenance`. See [[gls-provenance]].
2. **Was the rule's *text* written fresh, or copied?** — `name_source` and
   `implication_source`. See [[gls-name-source]].

Conflating the two is the specific mistake this model exists to prevent: writing a name for a
real rule does not make the rule less real, and copying a name for a newly-derived rule does not
make the rule more real.

> [!info]
> "Provenance" carries a second, unrelated meaning in the Studio: the Catalog-vs-Bespoke
> `RuleOrigin` of a delivered rule (see [[con-catalog-vs-bespoke-rules]]). That axis is about
> *where the SQL came from*; this one is about *whether the rule has ever run in the field*.
> Different questions on different systems — do not read either as a proxy for the other.

## Provenance: what it currently carries

The live catalogue's own metadata defines two operative values:

| Value | Meaning |
|---|---|
| `field_proven` | Observed running in a live SAP DQ deployment. |
| `derived` | Authored to make a value lever walkable — has never run in the field. |

> [!warning]
> **Terminology drift, flagged not resolved (CONFLICT-017).** The repository's README documents
> `provenance` as a three-value set — `field_proven` \| `ai_generated` \| `template_compliant`.
> The catalogue's own `_meta.provenance_values` defines only two, `field_proven` and `derived`,
> and `derived` matches none of the README's three names. `_meta.provenance_semantics` goes
> further still: it states that **every** entry in the served catalogue carries
> `provenance: field_proven`, per ruling F1. Treat `field_proven` \| `derived` as the operative
> vocabulary for this catalogue until an entry actually carrying `ai_generated` or
> `template_compliant` appears; the README's fuller set describes the schema's design lineage,
> not the instantiated data. Logged in `docs/CONFLICTS.md` as CONFLICT-017.

## The critical ruling: text ≠ substance

**Fable ruling F1 (2026-08-04, corrected after a defect was found in wave output): a
field-proven rule stays `provenance: field_proven` even when its name and implication text were
freshly authored by an agent.** What's generated is the wording, not the rule. In the README's
own words, rewriting `provenance` to `ai_generated` just because the text is new is "wrong and
dishonest in the direction that matters most" — it understates how well-evidenced the catalogue
is. `name_source` and `implication_source` carry the "was this text generated" information
separately, and only that information.

An optional `agent_decided: true` flag rides alongside `provenance` for cases where an agent
made a judgment call about existence (for example, deciding a rule was defensibly evidenced)
rather than a source having already settled the question outright.

## Scale, per the catalogue's own numbers

Per `_meta.composition`, the pipeline that produced the current wave assembled 384 rules
classified `field_proven_from_deployment` and 113 `derived_for_lever_coverage` — 497 total.
`_meta` publishes no post-quarantine split of those two labels, so 384/113 is a pipeline-output
figure, not a breakdown of what is served today. `_meta.known_gaps` and the update history record
that quarantined and unrecoverable rules are held outside this catalogue deliberately, not
silently dropped: the served `entry_count` (447) is smaller than the 497 the pipeline produced
because 50 night-run exceptions were quarantined to `review/` on 2026-08-06 by owner ruling.

## Why this matters in a value conversation

A blueprint built entirely from `derived` rules is a hypothesis, however plausible; one built
from `field_proven` rules is a track record. Whoever is reading a rule-backed value claim needs
to be able to tell which they are looking at without cross-checking the source deployment
themselves — that is the whole reason the two fields exist and are never merged.

## Related

- [[gls-provenance]] / [[gls-name-source]] — the glossary-level definitions this concept expands.
- [[ref-rule-record-schema]] — where `provenance`, `name_source`, `implication_source` and
  `agent_decided` sit in the full record.
- [[prn-governed-ratification]] — how a rename that changes `adm_rule_name`'s text is ratified
  without touching `provenance`.
