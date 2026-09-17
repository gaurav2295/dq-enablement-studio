---
id: std-pattern-partner-cardinality
type: standard
kind: pattern
title: Rule Pattern — Partner Cardinality
domain: rule-design
audience: [consultant, developer]
level: advanced
status: review
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - dq-studio:knowledge/methodology/rule_patterns.json
tags: [rule-pattern, derivation, sap, customer]
created: 2026-08-20
updated: 2026-08-20
links:
  - parent:std-rule-pattern-library
  - relates:std-pattern-hierarchy-membership
  - relates:ref-deletion-flag-resolver
  - relates:std-ziserrorflag-convention
  - relates:ref-sap-table-families
  - relates:gls-partner-function
---

## Intent

The **count** of active related rows for a universe record must satisfy a comparator and
threshold taken from the rule's quantifier. Detected by two regexes that must BOTH match the
rule name, case-insensitive — one for the cardinality quantifier, one for the partner-function
word:

```text
\b(?:exactly one|at least one|only one)\b
\b(?:sold-to|sold to|ship-to|ship to|bill-to|bill to|payer)\b
```

A quantifier without a partner word — or a partner word without a quantifier — is an ordinary
rule, not this pattern.

## Slots

| Slot | Source | Editable |
|---|---|---|
| `universe_table` | `domain_def.salesTable` — fixed `KNVV`, the Sold-To sales-area view | no |
| `child_table` | `engine.get_join('KNVV', 'KNVP')` target — fixed `KNVP` | yes |
| `partner_function_word` | detected in the rule text: the lexicon word that is **not** the Sold-To subject | yes |
| `partner_function_code` | `partner_lexicon[partner_function_word]` — the `PARVW` value | yes |
| `comparator` / `threshold` | the quantifier: "at least one" → `<` / `1`; "exactly one" or "only one" → `<>` / `1` | no |
| `active_check_table` | fixed `KNA1` — the partner's own central master record | no |
| `active_check_join_field` | fixed `KUNN2` — `KNVP`'s partner-customer column, verified physical in the SAP ECC baseline and deliberately **not** part of `KNVP`'s composite PK | no |

**Partner lexicon:** `payer → RG`, `ship-to → WE`, `sold-to → AG`, `bill-to → RE`. Sold-To (`AG`)
is the pattern's fixed universe subject, never the counted child — the capture logic excludes the
subject word from the counted-partner search.

## Skeleton essence

A correlated scalar `COUNT(*)` compared against the threshold:

- correlate the child rows on the full sales-area key (`KUNNR`, `VKORG`, `VTWEG`, `SPART`) plus
  `zSourceSystemID`;
- restrict to the resolved partner function: `PARVW = '<code>'`;
- "active" is a nested `EXISTS` against the partner's own central master, requiring the partner
  is not deletion-flagged (`COALESCE(KNA1.LOEVM, '') <> 'X'`);
- error when the count **fails** the acceptance condition — the comparator in the SQL is the
  inverse of the rule's prose.

## Worked example

**Rule:** *"A Sold-To customer must have at least one active Ship-To customer assigned"*

**Slots resolved:** the quantifier ("at least one") sets `comparator="<"`, `threshold=1`; the
partner-function word "ship-to" resolves via `partner_lexicon` to `PARVW='WE'`;
`child_table=KNVP` (the `KNVV → KNVP` join); the active check cross-references `KNA1.LOEVM` via
`KNVP.KUNN2`.

```sql
/* Pattern: partner_cardinality — active ship-to (PARVW='WE') rows in
   KNVP for this KNVV Sold-To must satisfy COUNT < 1. */
    CASE
        WHEN (
            SELECT COUNT(*)
            FROM [WRKDQ].[dbo].[KNVP] AS KNVP
            WHERE KNVP.KUNNR = KNVV.KUNNR
              AND KNVP.VKORG = KNVV.VKORG
              AND KNVP.VTWEG = KNVV.VTWEG
              AND KNVP.SPART = KNVV.SPART
              AND KNVP.zSourceSystemID = KNVV.zSourceSystemID
              AND KNVP.PARVW = 'WE'
              AND EXISTS (
                  SELECT 1 FROM [WRKDQ].[dbo].[KNA1] AS KNA1_PARTNER
                  WHERE KNA1_PARTNER.KUNNR = KNVP.KUNN2
                    AND KNA1_PARTNER.zSourceSystemID = KNVP.zSourceSystemID
                    AND COALESCE(KNA1_PARTNER.LOEVM, '') <> 'X'
              )
        ) < 1
        THEN 1 ELSE 0
    END AS [zIsErrorFlag]
```

> [!important]
> Note the **inverted comparator**. "At least one" fails the check — and therefore flags the row —
> when the COUNT is `< 1`, i.e. zero. "Exactly one" (a different acceptance rule, the Payer
> example) instead uses `<>` against threshold `1`. The prose states the acceptance condition;
> the `CASE` states the error condition.

## Templates the pattern narrates with

- **Description:** "Each Sold-To customer's active `{partner_function_word}` partner-function
  assignment(s) in `{child_table}` (PARVW=`'{partner_function_code}'`) must satisfy the
  cardinality rule: `{cardinality_desc}`. 'Active' means the assigned partner customer's own
  central master (`{active_check_table}`) is not deletion-flagged."
- **Specification:** "zIsErrorFlag = 1 when COUNT(active `{child_table}` rows WHERE
  PARVW=`'{partner_function_code}'` for this Sold-To's sales area) `{comparator}` `{threshold}`."

## Notes and boundaries

- The deletion flag `LOEVM` appears here **inside** the correlated subquery as part of the
  definition of "active partner" — it is qualifying the counted child rows, not excluding rows
  from the universe. The universe-level deletion exclusion still belongs in `WHERE`; see
  [[prn-deletion-flags-belong-in-where|Why Deletion Flags Belong in WHERE]].
- `KUNN2` is used as a join field but is not part of `KNVP`'s composite primary key; the baseline
  lookup exists to confirm the column before the pattern trusts it.
- Only the four lexicon partner functions are covered. A new partner word is a JSON-only change
  (add it to `partner_lexicon`), not a code change.

## Related

- [[std-rule-pattern-library|The Rule-Pattern Library]]
- [[std-pattern-hierarchy-membership|Rule Pattern — Hierarchy Membership]] — same `KNVV` universe
- [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]]
