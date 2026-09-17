---
id: std-deletion-filter-marker
type: standard
title: Deletion Filter Marker Block
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [methodology, convention, sql, sap, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - implements:prn-deletion-flags-belong-in-where
  - relates:ref-deletion-flag-resolver
  - relates:std-view-naming-patterns
  - relates:std-optsel-select-structure
---

## What it is

A pair of marker tokens wrapped around the deletion-flag predicates in an Opportunity View's
`WHERE` clause, so the generator can toggle whether deleted / marked-for-deletion records are part
of the population — without rewriting the SQL.

```sql
WHERE {{DELETION_FILTER_START}}
    LFA1.LOEVM <> 'X'
    AND LFB1.LOEVM <> 'X'
{{DELETION_FILTER_END}}
```

## When the block appears

The block is emitted when **one or more tables in the rule's `FROM` / `JOIN` list carries a
deletion flag**, per that table's `deletion_fields` in the batch context — for example
`LFA1.LOEVM`, `MARA.LVORM`.

- Every flagged table in the join set contributes a predicate. A vendor rule joining `LFA1` and
  `LFB1` excludes on both, because a vendor can be flagged at general-data level, at company-code
  level, or both.
- If the view already has other `WHERE` predicates, the marker block is `AND`-ed alongside them.
- Rules where **no** joined table has a deletion flag omit the block entirely — an empty marker
  block is not emitted.

## What the generator does with it

The generator strips the marker tokens and then takes one of two paths, per the user's choice at
generation time:

| Choice | Result |
|---|---|
| **Exclude deleted data** (default) | Marker tokens stripped, the enclosed predicates kept |
| **Include deleted data** | The whole block dropped — tokens and predicates together |

Either way the deployed SQL contains no `{{...}}` tokens. The markers exist only in the template
form of the rule, alongside `{{SYSTEM}}` and `{{DATABASE_NAME}}` — see
[[std-view-naming-patterns|View Naming Patterns]].

## Why a toggle rather than a fixed filter

Excluding deleted records is right almost always: a material flagged for deletion is not a
remediation target, and counting it inflates the defect number with work nobody will do.

But not always. Two cases need the deleted rows in:

- **Pre-migration scoping** — you want to know how much of the legacy estate is dead before
  deciding what to carry across.
- **Deletion-detection rules**, which are the deliberate exception to "flags are exclusions".
  There the flag *is* the subject of the rule, so filtering on it in the
  `WHERE` would empty the population.

Making it a toggle keeps one authored rule serving both, instead of two near-identical rules
drifting apart.

> [!warning] The flag still never appears in the CASE
> Toggling the marker block changes the **population**, not the check. A deletion flag belongs in
> `WHERE`; a *status* field (`MMSTA`, `PSTAT`, `STATU`) drives `zIsErrorFlag`. Never put the same
> condition in both — see [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]]
> and [[prn-deletion-flags-belong-in-where|Why Deletion Flags Belong in WHERE]].

## Comment the block like any other filter

The marker tokens are machinery, not documentation. The predicates inside still take their
`/* Exclude: ... */` comments per [[std-sql-comment-standards|SQL Comment Standards]]:

```sql
WHERE {{DELETION_FILTER_START}}
    /* Exclude: vendors flagged for deletion at general-data level */
    LFA1.LOEVM <> 'X'
    /* Exclude: vendors flagged for deletion at company-code level */
    AND LFB1.LOEVM <> 'X'
{{DELETION_FILTER_END}}
```

## Related

- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]]
- [[prn-deletion-flags-belong-in-where|Why Deletion Flags Belong in WHERE]]
- [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]]
- Deletion Flag Normalization in SQL Gen
