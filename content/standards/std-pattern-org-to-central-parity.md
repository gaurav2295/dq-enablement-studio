---
id: std-pattern-org-to-central-parity
type: standard
kind: pattern
title: Rule Pattern — Org-to-Central Parity
domain: rule-design
audience: [consultant, developer]
level: advanced
status: review
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - dq-studio:knowledge/methodology/rule_patterns.json
tags: [rule-pattern, derivation, sap, parity]
created: 2026-08-20
updated: 2026-08-20
links:
  - parent:std-rule-pattern-library

  - relates:ref-sap-deletion-flags-vs-status-fields

  - relates:std-ziserrorflag-convention
  - relates:gls-org-vs-central
  - relates:gls-parity-pair
---

## Intent

A **central master record's** flag must match the ALL-or-nothing state of its **org-level
children**: if every org-level row is deletion-flagged (or blocked), the central record must be
too. Detected by three regexes that must ALL match the rule name, case-insensitive:

```text
\b(?:marked for deletion|flagged for deletion|blocked (?:for|at))\b
\bacross all\b[\s\S]*\b(?:company codes?|sales organi[sz]ations?|purchasing organi[sz]ations?)\b
\b(?:central master|master record|master level)\b
```

Three independent signals — a flag/block/deletion word, an "across all `<org unit>`" aggregation
phrase, and a central/master phrase — are what keep this pattern from firing on ordinary block
rules. That stricter intent is also why this pattern sits **before** `status_field_check` in the
detection array: it must keep priority over the single-field shape it shares a block signal with.

## Slots

| Slot | Source | Editable |
|---|---|---|
| `central_table` | `domain_def.mainTable` — `KNA1` (customer) or `LFA1` (vendor) | no |
| `variant` | `deletion` when the rule text mentions deletion, else `block` | yes |
| `org_unit` | detected org-unit phrase, mapped to company_code / sales_org / purchasing_org | yes |
| `pairs[].central_field` | deletion: `parity_pairs.json`'s central field (always `LOEVM`); block: `status_fields.json` central entries filtered by category and orgUnit | yes |
| `pairs[].child_table` | deletion: the parity children entry for the org unit; block: the central entry's `parityChild.table` | yes |
| `pairs[].child_field` | deletion: the parity children field; block: the central entry's `parityChild.field` | yes |
| `pairs[].org_field` | the org field for the child — documentary, deliberately **not** used as a correlation filter | yes |
| `pairs[].central_type` / `child_type` | `status_fields.json`'s `type` key per side (boolean means set is `'X'`; code means set is any non-blank value). Deletion pairs are always boolean | yes |

When the org-level entry itself is missing from the KB, field-type dispatch falls back to a
SAP-baseline `CHAR(1)` cross-check — a documented Phase-1 knowledge gap that is cross-checked,
not invented.

## Skeleton essence

Parity is broken — and only broken — when all three of these hold for a pair:

1. the **central** record is NOT flagged;
2. at least one child row **exists** for it (a record with no org-level children cannot be out of
   parity);
3. NO unflagged child row exists — i.e. every child that does exist IS flagged.

Rendered as `central-not-flagged AND EXISTS child AND NOT EXISTS unflagged-child`. The block
variant can resolve **multiple** field pairs — one per matched block category (posting, payment,
…) — each rendered as its own block and `OR`'d together. `_flag_predicate` dispatches boolean
fields (`= 'X'` / `<> 'X'`) versus code fields (`<> ''` / `= ''`) per field; that per-field
dispatch is exactly why the skeletons live in Python rather than JSON.

## Worked example

**Rule:** *"If a customer is marked for deletion across all Company Codes the customer master
record must also be marked for deletion at the central master level"*

**Slots resolved:** `variant="deletion"` (versus `"block"` for the block-parity rules),
`org_unit="company_code"` → `orgField=BUKRS`, one field pair from `parity_pairs.json`:
`KNA1.LOEVM` paired with `KNB1.LOEVM`.

```sql
/* Pattern: org_to_central_parity (deletion) — KNA1 must be marked for deletion
   whenever ALL of its child rows across every Company Codes (BUKRS) are marked for deletion.
   Field pair(s): KNA1.LOEVM<->KNB1.LOEVM. */
    CASE
        WHEN
        (
            COALESCE(KNA1.LOEVM, '') <> 'X'
            AND EXISTS (
                SELECT 1 FROM [WRKDQ].[dbo].[KNB1] AS KNB1
                WHERE KNB1.KUNNR = KNA1.KUNNR
                  AND KNB1.zSourceSystemID = KNA1.zSourceSystemID
            )
            AND NOT EXISTS (
                SELECT 1 FROM [WRKDQ].[dbo].[KNB1] AS KNB1
                WHERE KNB1.KUNNR = KNA1.KUNNR
                  AND KNB1.zSourceSystemID = KNA1.zSourceSystemID
                  AND COALESCE(KNB1.LOEVM, '') <> 'X'
            )
        )
        THEN 1 ELSE 0
    END AS [zIsErrorFlag]
```

## Templates the pattern narrates with

- **Description:** "If `{central_table}` is `{variant_label}` across ALL `{org_label}`
  (`{child_table}`), the central `{central_table}` record must also be `{variant_label}` — parity
  is broken when the central record is NOT `{variant_label}` but every `{child_table}` row for
  that record IS."
- **Specification:** "zIsErrorFlag = 1 when central `{central_table}` is not `{variant_label}`
  AND at least one `{child_table}` row exists for it AND ALL `{child_table}` rows for it ARE
  `{variant_label}` (per pair, OR'd across pairs for multi-block rules)."

## Notes and boundaries

- **This is the deliberate exception to "deletion flags belong in WHERE".** The deletion flag is
  the subject of the rule here, so it appears in the `CASE`, not as a universe exclusion. Pattern
  detection runs before, and gates off, the keyword deletion-detection step precisely so this
  shape is not rewritten into an exclusion.
- **The org field is documentary.** Correlation is on the central key plus `zSourceSystemID`; the
  "across all company codes" aggregation is expressed by the EXISTS / NOT EXISTS pair, not by
  filtering on `BUKRS`.
- **Deletion-intent parity, not an inverted CASE.** Express the parity condition, not an
  inverted-semantics flag comparison.
- **Domain coverage.** Only `customer` and `vendor` carry parity knowledge today; another domain
  produces a `PartialFill` naming the missing KB entry rather than a guess.

## Related

- [[std-rule-pattern-library|The Rule-Pattern Library]]
- [[std-pattern-status-field-check|Rule Pattern — Status Field Check]] — the single-field shape
  this pattern must not shadow
- [[prn-deletion-flags-belong-in-where|Why Deletion Flags Belong in WHERE]]
