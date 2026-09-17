---
id: std-zconcatenatedkey-convention
type: standard
title: zConcatenatedKey Convention
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
sources:
  - vault:dq-methodology/zConcatenatedKey Convention.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
  - dq-studio:docs/Studio_Overview.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - parent:std-output-field-sections
  - relates:std-zsourcesystemid-convention
  - relates:ref-sap-key-fields-and-critical-data-elements
  - relates:ref-local-deriver
  - relates:gls-composite-key
  - relates:gls-zconcatenatedkey
---

## What it is

The **composite-key column** the Studio emits on every OptSel / RptSel / PrfSel view. Used by
ADM and downstream consumers to identify a record uniquely across systems.

## Format — exact spelling

```
zConcatenatedKey
```

- One word. **No space** between "Concatenated" and "Key".
- Lower-case `z`, camel-case the rest.
- Always wrapped in `[zConcatenatedKey]` brackets in SQL output.

> [!warning] Wrong spellings
> `zConcatenated Key` (space) silently breaks ADM ingestion. `ZConcatenatedKey` (capital Z) is
> wrong casing. `zConcatenatedID`, `zCompositeKey`, `zKey` are the wrong name entirely.

This is an ADM ingestion requirement, not a stylistic preference. A wrong spelling means the load
skips the column without error.

## The four requirements

The DQ Rule Standards state that every Opportunity View must include `zConcatenatedKey`, and that
the value must be:

1. **Unique for each record** — this is the ADM record identity, so a duplicate key means two rows
   collapse into one opportunity.
2. **Prefixed with `zSourceSystemID`** — always the first element.
3. **Built from all relevant primary key fields** — every PK column of the grain, none omitted.
4. **Null-safe** — a NULL in any element must not null the whole key.

And it must be built with `CONCAT`, never with `+` string concatenation (in T-SQL, `'A' + NULL`
yields NULL and silently destroys the key).

## Value template

```sql
CONCAT(
    COALESCE(TRIM(zSourceSystemID),'NA'),
    '_',
    COALESCE(TRIM(<pk1>),'NA'),
    '_',
    COALESCE(TRIM(<pk2>),'NA')
) AS [zConcatenatedKey]
```

The system ID prefixes the composite key so the same business record from different source
systems gets different `zConcatenatedKey` values — necessary because two systems can legitimately
reuse the same internal IDs.

Underscores between fields. No type coercion (the source columns are already character-typed in
SAP).

> [!important] Null handling is mandatory, not optional — see CONFLICT-010
> Each element is wrapped `COALESCE(TRIM(<field>),'NA')`. `TRIM` removes the trailing blanks SAP
> CHAR columns carry (without it, `'0000012345   '` and `'0000012345'` produce different keys for
> the same record); `COALESCE(...,'NA')` substitutes a literal so a NULL element degrades one
> segment instead of nulling the entire key. An earlier statement of this convention said "no
> trimming, no padding" — that is superseded by the standards doc.

Worked example — the KNA1 sales-area grain (customer plus sales organisation, distribution
channel and division):

```sql
CONCAT(
    COALESCE(TRIM(zSourceSystemID),'NA'),
    '_',
    COALESCE(TRIM(KUNNR),'NA'),
    '_',
    COALESCE(TRIM(VKORG),'NA'),
    '_',
    COALESCE(TRIM(VTWEG),'NA'),
    '_',
    COALESCE(TRIM(SPART),'NA')
) AS zConcatenatedKey
```

## Examples

Key composition per table. The expressions below show **which** fields go in and in what order;
each element still takes the `COALESCE(TRIM(...),'NA')` wrapper shown above.

| Table | Primary key | Generated zConcatenatedKey expression |
|---|---|---|
| MARA | MATNR | `CONCAT(zSourceSystemID, '_', MATNR)` |
| MAKT | MATNR + SPRAS | `CONCAT(zSourceSystemID, '_', MATNR, '_', SPRAS)` |
| KNA1 | KUNNR | `CONCAT(zSourceSystemID, '_', KUNNR)` |
| KNB1 | KUNNR + BUKRS | `CONCAT(zSourceSystemID, '_', KUNNR, '_', BUKRS)` |
| BSEG | BUKRS + BELNR + GJAHR + BUZEI | `CONCAT(zSourceSystemID, '_', BUKRS, '_', BELNR, '_', GJAHR, '_', BUZEI)` |
| CEPC | KOKRS + PRCTR + DATBI | `CONCAT(zSourceSystemID, '_', KOKRS, '_', PRCTR, '_', DATBI)` |

## The separator is `_`, never `|`

The element separator is a single underscore. A pipe (`|`) is specifically forbidden, and the
generator normalises to `_` on **every** path — including when a catalog entry's own SQL used a
pipe, and including when a spec instruction spells out a different separator. One separator across
local-derive and catalog paths is what lets two keys from different derivation routes be compared
or joined at all.

A pipe delimiter is blocked at generation time, so a pipe never reaches a deployed view. When no
key fields are resolvable the Studio falls back to a non-NULL empty string with a loud comment
(`/* zConcatenatedKey: NO KEY FIELDS — define them */ '' AS [zConcatenatedKey]`) rather than a
NULL — a NULL key breaks the downstream scoring joins silently, an empty one fails visibly.

> [!warning] The catalog path orders the arguments differently — see CONFLICT-007
> This standard requires `zSourceSystemID` **first**, and the local-derive path honours it. The
> catalog-promotion path emits `CONCAT(src.<key>, '_', src.zSourceSystemID)` instead — key first,
> system last. Separator and NULL-safety agree across both paths; **argument order does not**, so
> the same record profiled through the two routes yields two different keys. Logged as
> CONFLICT-007.

## Where the PK fields come from

The Studio carries canonical PK definitions for SAP tables (41 single-PK and 44 composite) and
uses them to build the CONCAT expression automatically.

## Related

- [[std-zsourcesystemid-convention|zSourceSystemID Convention]]
- [[std-output-field-sections|Output Field Sections]] — zConcatenatedKey appears in the *Syniti Technical Fields* section
- [[ref-sap-key-fields-and-critical-data-elements|SAP Key Fields and Critical Data Elements]]
