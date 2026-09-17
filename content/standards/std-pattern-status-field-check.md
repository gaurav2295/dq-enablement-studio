---
id: std-pattern-status-field-check
type: standard
kind: pattern
title: Rule Pattern — Status Field Check
domain: rule-design
audience: [consultant, developer]
level: advanced
status: review
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - dq-studio:knowledge/methodology/rule_patterns.json
tags: [rule-pattern, derivation, sap, status-fields]
created: 2026-08-20
updated: 2026-08-20
links:
  - parent:std-rule-pattern-library

  - relates:std-pattern-org-to-central-parity
  - relates:ref-sap-deletion-flags-vs-status-fields

  - relates:gls-polarity
---

## Intent

A single **central-level status/block field's** own set-or-blank state IS the error condition —
no related table, no correlated subquery.

Two regexes must both match the rule name, case-insensitive: a category-near-block signal, and a
must/should verb phrase **coupled** to the same category word.

```text
\b(?:posting|payment|order|delivery|billing|sales|purchasing)\b[\s\S]{0,25}\bblock\w*\b|\bblock\w*\b[\s\S]{0,25}\b(?:posting|payment|order|delivery|billing|sales|purchasing)\b
\b(?:must|should)\b(?:\s+not)?\s+(?:have|be|assigned|maintained|populated|set)\b[\s\S]{0,20}\b(?:posting|payment|order|delivery|billing|sales|purchasing)\b
```

The pattern is deliberately **last** in the detection array, because detection is first-match-wins
and [[std-pattern-org-to-central-parity|org-to-central parity]]'s stricter "across all
`<org unit>` … central master level" intent must keep priority. This pattern only claims the
DIRECT single-field checks that parity does not fire on.

## Why it exists

Running AI Enhance with no feedback on *"A blocked customer must have a payment block assigned at
the central master level"* produced a structured description that correctly named `KNA1.SPERZ`
(Central Payment Block) in prose — but the generated SQL was a shell: `zIsErrorFlag` a literal
`NULL /* define logic condition */`, a `TBD` view-name slot, and only `KNA1.KUNNR` surviving as an
output field.

Root cause: this shape — "must (not) have a `<category>` block" — is not a parity, cardinality or
hierarchy shape (no "across all X" org aggregation, no partner function, no hierarchy), so no
existing pattern recognized it, and it fell through to a manual `TBD` shell the consultant had to
write by hand. This pattern closes that gap.

## Slots

| Slot | Source | Editable |
|---|---|---|
| `category` | the block/status category word (posting, payment, order, delivery, billing, sales, purchasing) nearest a "block" word, matched against the block/status category vocabulary | yes |
| `table` | the status-field registry entry for the domain with `level="central"` and the matched category; **first entry in registry order wins** when a domain has more than one central match | yes |
| `field` | the same entry's `field` | yes |
| `type` | the same entry's `type` — boolean means set is `'X'`; code means set is any non-blank value | yes |
| `polarity` | `positive` ("must have" — error when blank) or `negative` ("must not have" — error when set), from a must/should + optional not regex over the rule text | yes |
| `central_key_field` | the domain's central key field, resolved the same way as the parity pattern's central key slot | no |

## Skeleton essence

One `CASE`, one predicate, no subquery. Polarity flips the comparison; the field's `type` decides
what "set" means, using the same flag-comparison logic the parity pattern uses:

| Field type | Positive polarity (must have) | Negative polarity (must not have) |
|---|---|---|
| boolean | error when `COALESCE(f, '') <> 'X'` | error when `COALESCE(f, '') = 'X'` |
| code | error when `COALESCE(f, '') = ''` | error when `COALESCE(f, '') <> ''` |

## Worked examples

**Rule (positive polarity — "must have"):** *"A blocked customer must have a payment block
assigned at the central master level"*

**Slots resolved:** `category=payment`, `polarity=positive` → the customer domain's status-field
registry, filtered to `level="central"` plus `category="payment"` → `KNA1.SPERZ`
(`type="boolean"`).

```sql
/* Pattern: status_field_check (payment, polarity=positive) —
   KNA1.SPERZ is an error when it is missing/blank. */
    CASE
        WHEN COALESCE(KNA1.SPERZ, '') <> 'X'
        THEN 1 ELSE 0
    END AS [zIsErrorFlag]
```

**Rule (negative polarity — "must not have"):** *"A vendor must not have a purchasing block"*

**Slots resolved:** `category=purchasing`, `polarity=negative` → the `vendor` array has TWO
`level="central"` plus `category="purchasing"` entries (`LFA1.SPERM` boolean, `LFA1.SPERQ` code)
— the FIRST one in registry order wins (`LFA1.SPERM`), matching the "first writer wins"
convention used elsewhere in slot filling.

```sql
/* Pattern: status_field_check (purchasing, polarity=negative) —
   LFA1.SPERM is an error when it is present/set. */
    CASE
        WHEN COALESCE(LFA1.SPERM, '') = 'X'
        THEN 1 ELSE 0
    END AS [zIsErrorFlag]
```

Both examples use a `boolean` field. A `code`-type field — for example `KNA1.AUFSD`, Central Order
Block — dispatches through the same helper and produces `<> ''` / `= ''` instead of `<> 'X'` /
`= 'X'`.

## Templates the pattern narrates with

- **Description:** "`{domain_label}` records must `{polarity_phrase}` a central `{category}`
  block (`{table}`.`{field}`)."
- **Specification:** "zIsErrorFlag = 1 when `{table}`.`{field}` is `{polarity_state}`."

## Scope boundary (deliberate, v1)

This pattern handles **only** the direct "does the record have this specific central-level
status/block field set or not" check. It does **not** model compound conditions like "if blocked
for any OTHER reason, this specific block must also be set" — a real but structurally different
shape, which would have to reason about every other block field on the same record, not just the
one named in the rule.

> [!warning]
> AI-generated descriptions may narrate that compound nuance in prose. The deterministic SQL
> intentionally does the simpler, unambiguously-correct single-field check rather than guess at a
> condition the rule text does not actually specify. A future pattern can add the compound shape
> without touching this one.

## Intent-detection note — why the second regex is coupled

The second intent regex ties the must/should + verb phrase to the category word (the category must
appear within roughly 20 characters *after* the verb) rather than checking the two signals
independently. This avoids misfiring on rule names that contain a loose "category near block"
signal and a loose "must have" signal that don't actually describe the same clause — for example
*"A customer blocked for posting or payment must have a central master level block"*, which is
really an org-to-central parity rule, not a status-field check.

> [!tip]
> When naming a rule, keep the category word inside the same clause as the must/should verb
> (e.g. "must have a payment block", not "blocked for payment... must have a block") so the
> right pattern fires.

## Related

- [[std-rule-pattern-library|The Rule-Pattern Library]]
- [[std-pattern-org-to-central-parity|Rule Pattern — Org-to-Central Parity]]
- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]] — status fields drive
  the flag; deletion flags do not
