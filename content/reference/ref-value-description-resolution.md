---
id: ref-value-description-resolution
type: reference
title: Value-Description Resolution (4 mechanisms)
domain: sap
audience: [developer]
level: advanced
status: deprecated
links:
  - prereq:ref-sap-dd-dictionary-tables
  - relates:ref-deletion-flag-resolver
  - relates:ref-sap-baseline-model
  - relates:gls-check-table
  - relates:gls-domain-fixed-values
sources:
  - vault:sap-knowledge/Value-Description Resolution (4 mechanisms).md
tags: [sap, engine, studio, dd-percent, methodology]
created: 2026-08-20
updated: 2026-08-20
---

## What this is

The Studio can turn a raw coded field value into a human-readable description next to it in a
rule's output — so a reviewer sees "Blocked for procurement/warehouse" instead of a raw code like
`MMSTA = '02'`. A defect that only shows the raw code is meaningless to a business reviewer; this
is what makes generated output readable.

See [[ref-sap-dd-dictionary-tables|SAP DD% Dictionary Tables]] for the SAP dictionary tables these
mechanisms draw from.

## The four mechanisms

| Mechanism | Looks up a text table? | Meaning | Example |
|---|---|---|---|
| `check_table` | Yes | A language-keyed text table supplies the description | MTART → T134T.MTBEZ |
| `single_lang_text` | Yes | A text table with no language dimension | WERKS → T001W.NAME1 |
| `domain_fixed_values` | No | A small enumerated set with descriptions built in | — |
| `self_describing` | No | The field's own value already reads as a description | — |

## Where the descriptions come from

- A hand-built library of common SAP fields ships with the Studio.
- Each project can layer its own custom (Z*/Y*) fields on top; when a project defines the same
  field as the shipped library, the project's own entry wins.
- If a project's lookup data is missing or malformed, the Studio treats it as empty rather than
  failing — description lookup is a convenience, never a blocker to generating a rule.

## Finding the right mechanism for an unrecognised field

When the Studio doesn't yet recognise a field, it can produce a ready-to-run SQL query against the
client's SAP dictionary. Running it and reading the result tells you which mechanism applies:

- A check table exists → use **check_table**
- The field's domain has fixed values → use **domain_fixed_values**
- Neither, and the value is already self-evident text → use **self_describing**

> [!warning] Verify before ship
> Check tables can vary across SAP releases (ECC 6.0 vs S/4HANA). Validate the text table/field
> pair you found against the client's own DD% dictionary before relying on it for a regulated rule.

## Related

- [[ref-sap-dd-dictionary-tables|SAP DD% Dictionary Tables]]
- [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]] — the sibling resolver for
  deletion flags
- Studio — Attribute Usage Analysis (engine) — the consumer of
  these descriptions
- [[ref-sap-baseline-model|SAP Baseline Model (logical vs physical)]]
