---
id: std-coded-field-text-translation
type: standard
title: Coded Fields Carry Their Text Translation
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
  - relates:std-output-field-sections
  - relates:std-sql-comment-standards
  - relates:prn-3-tier-description-resolution
  - relates:ref-local-deriver

  - relates:gls-coded-field
  - relates:gls-spras
---

## The standard

Any **coded / technical field** that appears in a rule must have its **text translation brought
into the rule and output alongside it**, with the join preset.

A coded field is a domain-value key that has a SAP check-table text translation — `MTART`,
`WERKS`, `BUKRS`, `KTOKK`, and any other value where a translation is available.

## Preset, not left for AI Enhance

The join is part of the derived rule from the start. It is **not** something AI Enhance is
expected to notice and add later.

That ordering matters because AI Enhance's SQL review is deliberately limited to joins and
error-flag logic — relying on it to invent description joins would make output quality depend on
a model's attention rather than on the deriver. Deterministic
first, AI for judgement.

## What it looks like

```sql
SELECT
    -- Basic Fields
    MARA.MATNR AS [Material Number],
    MARA.MTART AS [Material Type],
    T134T.MTBEZ AS [Material Type Description],

    -- Organizational Context
    MARC.WERKS AS [Plant],
    T001W.NAME1 AS [Plant Name]

FROM [WRKDQ].[dbo].[MARA] AS MARA

LEFT OUTER JOIN [WRKDQ].[dbo].[MARC] AS MARC
    ON MARC.MATNR = MARA.MATNR
    AND MARC.zSourceSystemID = MARA.zSourceSystemID
    /* Plant-level extension of the material */

LEFT OUTER JOIN [WRKDQ].[dbo].[T134T] AS T134T
    ON T134T.MTART = MARA.MTART
    AND T134T.SPRAS = 'E'
    AND T134T.zSourceSystemID = MARA.zSourceSystemID
    /* Material type text — the code alone is unreadable to a steward */

LEFT OUTER JOIN [WRKDQ].[dbo].[T001W] AS T001W
    ON T001W.WERKS = MARC.WERKS
    AND T001W.zSourceSystemID = MARC.zSourceSystemID
    /* Plant name for the report */
```

The translation sits in **the same section as the code it translates** — `MTBEZ` next to `MTART`
in Basic Fields, `NAME1` next to `WERKS` in Organizational Context. It never migrates into Value
Context just because it is a lookup; section membership follows what kind of field it is
([[std-output-field-sections|Output Field Sections]]).

Three things are load-bearing in that join shape:

- **`LEFT OUTER JOIN`, never `INNER`.** A missing text entry must not drop the record from the
  opportunity population — that would silently shrink the universe and break the
  [[prn-optsel-is-the-universe|OptSel-is-the-universe]] contract.
- **Language restriction on text tables** — `SPRAS = 'E'` (or the engagement's agreed language),
  otherwise the join fans out one row per installed language.
- **System-qualified join** — `zSourceSystemID` on both sides, because check tables are
  consolidated across systems in the prep database and the same code can mean different things in
  two systems.

## Why the translation has to be in the rule

The output of a DQ rule lands on a data steward's desk as rows to remediate. `MTART = 'ZFRT'`
tells them nothing; `Material Type = ZFRT / Freight Item` tells them whether the record is
genuinely wrong. The same argument runs through
[[std-sql-comment-standards|SQL Comment Standards]] and the business-readable aliases in
[[std-output-field-sections|Output Field Sections]] — the rule must be legible without an SAP
dictionary open alongside it.

It also removes an argument at review time. A reviewer looking at a coded value has no way to
judge whether the rule's logic is right; a reviewer looking at the code plus its text does.

## Where the translation comes from

The Studio resolves value descriptions through several mechanisms rather than one lookup — check
table, domain fixed values, client overlay and knowledge base. See
[[ref-value-description-resolution|Value-Description Resolution (4 mechanisms)]] and
[[prn-3-tier-description-resolution|3-Tier Description Resolution]] for the precedence and the
rule about not falling back silently.

The implementation is deterministic: the deriver's coded-field lookup step builds these joins
before any AI step runs.

## Related

- [[std-output-field-sections|Output Field Sections]]
- [[ref-value-description-resolution|Value-Description Resolution (4 mechanisms)]]
- [[prn-3-tier-description-resolution|3-Tier Description Resolution]]
- [[ref-local-deriver|Local Deriver]]
