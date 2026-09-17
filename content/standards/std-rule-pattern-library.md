---
id: std-rule-pattern-library
type: standard
kind: pattern
title: The Rule-Pattern Library
domain: rule-design
audience: [consultant, developer]
level: advanced
status: review
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - dq-studio:knowledge/methodology/rule_patterns.json
tags: [rule-pattern, derivation, pattern-library, sap]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:ref-local-deriver
  - relates:gls-correlated-subquery
  - relates:gls-rule-pattern
---

## What it is

A small library of parameterised rule **shapes** the standard keyword-matching derivation cannot
express. Ordinary derivation works one keyword hit → one field → one simple `CASE`. Some rules
need a **correlated subquery** — a `CASE` whose result depends on rows in a *different* table
joined back to the universe row. That is structurally different from "does this row's own field
satisfy a condition", so these shapes are handled as their own library rather than being bolted
onto keyword matching.

## The four shapes

| Pattern id | Shape | Universe |
|---|---|---|
| `hierarchy_membership` | every row must resolve to a populated parent node in a related table | `KNVV` (Sold-To sales view) |
| `partner_cardinality` | COUNT of active related rows must satisfy a comparator/threshold | `KNVV` (Sold-To sales view) |
| `org_to_central_parity` | a central record's flag must match the ALL-or-nothing state of its org-level children | the domain's central master table (`KNA1`/`LFA1`) |
| `status_field_check` | a single central-level status/block field's own set/blank state IS the error condition — no related table involved | the domain's central master table (`KNA1`/`LFA1`/…) |

`status_field_check` is structurally simpler than the other three — it has no correlated subquery
at all, because the field it checks lives on the same row the outer query already targets. It sits
in the library anyway so all four patterns share one lifecycle.

Detail units: [[std-pattern-hierarchy-membership]] · [[std-pattern-partner-cardinality]] ·
[[std-pattern-org-to-central-parity]] · [[std-pattern-status-field-check]].

## Lifecycle: intent → slots → skeleton

Every pattern flows through the same steps:

1. **Detect intent** from the rule name — the wording has to match the pattern's known phrasings.
2. **Fill slots** — resolve the concrete tables/fields the pattern needs from the knowledge base,
   or flag exactly which fact is missing.
3. **Build the output fields** for the pattern's universe table.
4. **Build the SQL** for the rule.

**AND semantics on intent.** Every signal in a pattern's phrasing must be present, case-insensitive.
A single keyword is never enough — that is what stops an ordinary rule ("A vendor must not have a
purchasing block") from misfiring just because it shares one signal with a pattern. Parity needs
*both* a flag/block/deletion signal *and* an "across all `<org unit>`" + central/master signal;
cardinality needs *both* a quantifier phrase *and* a partner-function word; hierarchy needs the
hierarchy + parent-customer phrase pair.

**Detection is first-match-wins**, so pattern order matters: `status_field_check` is deliberately
checked last so it cannot shadow `org_to_central_parity`, whose stricter phrasing claims the
"across all … central master level" wording.

## Output fields are indistinguishable downstream

A pattern-derived spec's output fields — the standard Syniti Technical Fields plus the
Basic/Org fields for the universe table — are built to be indistinguishable from a
keyword-matched spec's. Exporters, the validator and the audit engine see one spec shape, not two.

## Slot sources — where the facts come from

Every fact a pattern needs is resolved from the Studio's curated SAP knowledge base rather than
guessed:

- The org-level parity pair (both the block and deletion variants)
- Field type (boolean vs coded) for a status field, cross-checked against the SAP baseline when
  needed
- Join target and correlation keys between the universe table and a related table
- Composite-key / active-check fields, confirmed against the SAP baseline before being trusted
- The partner-function word → SAP partner-function code mapping (e.g. payer, ship-to, sold-to,
  bill-to)
- The domain's central table and key field
- The polarity of the rule (must-have vs must-not-have), read from the rule's own wording

## PartialFill — named-slot warnings, never a generic TBD

When a pattern's phrasing matches but a slot cannot be resolved — for example a domain has no
parity knowledge on file — slot filling returns a **PartialFill** instead of guessing or emitting
a blank. The resulting message always names **the specific slot** and **what knowledge needs
adding** to resolve it. A reviewer reading review-required output should never see the word "TBD"
from this path.

> [!important]
> PartialFill is the pattern library's expression of the no-silent-fallback doctrine: an
> unresolvable fact produces an actionable, named warning, never a guess. See
> [[prn-no-silent-domain-fallback|Why No Silent Domain Fallback]].

## The trust chain

A pattern-derived spec's correctness rests on three independent layers, each catching a different
failure mode:

1. **Knowledge-base-verified slots.** Every table, field and join a pattern uses comes from
   curated knowledge, cross-checked against the SAP baseline where there's a documented gap. A slot
   that cannot be verified produces a PartialFill, not a guess.
2. **The static SQL validator.** Independent of pattern derivation — every spec, pattern-matched
   or keyword-matched, is inspected for the same structural/standards/logic checks before it lands
   in bulk results.
3. **Verification warnings for AI-proposed fields.** When AI enhancement proposes a table/field
   pair, it's checked against the knowledge base and SAP baseline; an unverified pair gets a
   warning instead of silent trust. Pattern-derived rules skip this check entirely — their fields
   are already knowledge-base-verified by construction.

Layer 1 is pattern-specific; layers 2–3 apply to every spec regardless of how it was derived.
Together they replace "trust the output" with "every fact has a traceable source, and everything
downstream is inspected before it ships."

## Related

- [[ref-local-deriver|Local Deriver]] — where pattern detection sits in the derive sequence
- SQL Generator (OptSel/RptSel skeleton)
- SQL Validator (static checks)
- [[std-ziserrorflag-convention|zIsErrorFlag Convention]]
