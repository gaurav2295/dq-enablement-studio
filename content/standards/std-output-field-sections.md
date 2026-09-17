---
id: std-output-field-sections
type: standard
title: Output Field Sections
domain: sql-standards
audience: [consultant]
level: practitioner
status: approved
sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:.claude/skills_canonical/studio-sql-quality.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
  - dq-studio:docs/ai_enhance_instructions.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:gls-optsel
  - relates:std-optsel-select-structure
  - relates:std-sql-comment-standards
  - relates:std-zsourcesystemid-convention
  - relates:std-zconcatenatedkey-convention
  - relates:std-ziserrorflag-convention
  - relates:std-ai-enhance-scope
  - contrast:std-ai-enhance-guardrails
---

## The standard

Every OptSel `SELECT` lists its columns under **five comment-headed sections in this exact
order**. Section headers are mandatory even if a section is empty — reviewers scan for them.

→ **Quick reference:** Scroll down for Visual Reference, Placement Checklist, and Building Checklist sections for fast lookups while authoring.

```sql
SELECT
    -- Syniti Technical Fields
    MARA.zSourceSystemID AS [zSourceSystemID],
    CONCAT(MARA.zSourceSystemID, '_', MARA.MATNR) AS [zConcatenatedKey],
    CASE WHEN ... THEN 1 ELSE 0 END AS [zIsErrorFlag],
    MARA.zDomainSegment AS [zDomainSegment],

    -- Basic Fields
    MARA.MATNR AS [Material Number],
    MAKT.MAKTX AS [Material Description],
    MARA.MTART AS [Material Type],
    MARA.MEINS AS [Base UoM],

    -- Organizational Context
    MARC.WERKS AS [Plant],
    T001W.NAME1 AS [Plant Name],

    -- Value Context
    MBEW.STPRS AS [Standard Price],
    MBEW.WAERS AS [Currency],

    -- Activity Context
    MARA.ERSDA AS [Created On],
    MARA.LAEDA AS [Last Changed]

FROM ...
```

## The five sections

| # | Section | What goes here | The one-question test |
|---|---|---|---|
| 1 | **Syniti Technical Fields** | `zSourceSystemID`, `zConcatenatedKey`, `zIsErrorFlag`, `zDomainSegment` — the metadata layer every Studio-generated view carries | — |
| 2 | **Basic Fields** | Primary key + the main descriptive columns (e.g. material number + material description). Lets a reviewer recognise *which record* this row is about. | *"WHAT is this record?"* |
| 3 | **Organizational Context** | Company code, plant, business area, controlling area — the org dimensions that scope the record | *"WHERE in the org does this record belong?"* |
| 4 | **Value Context** | Money, amounts, and financial values only | *"HOW MUCH is this worth?"* |
| 5 | **Activity Context** | Dates, times, and temporal fields only | *"WHEN did this happen?"* |

## Section definitions — the exact rules

These are the definitions the Studio enforces on every derived and AI-enhanced rule
(`docs/ai_enhance_instructions.md`, fed verbatim into the rule-fulfilment prompt). They are
narrower than "the field under check + supporting values", and deliberately so — the two
sections consultants most often blur are Value and Activity.

**Syniti Technical Fields** — always first, always these three:

| Field | Meaning |
|---|---|
| `zSourceSystemID` | The source system identifier |
| `zConcatenatedKey` | The unique record key across systems |
| `zIsErrorFlag` | The error detection flag — `1` = error, `0` = pass |

`zDomainSegment` rides in the same section where the Studio emits it — see the technical-field
order note further down; treat the three above as the mandatory minimum, not the maximum.

**Basic Fields** — identification and descriptive data from the main table:

- Material number, Customer ID, Order number, Vendor ID, and so on.
- Name, description, and type fields that identify the master record.

**Organizational Context** — structural and hierarchical fields:

- Cost Center (`KOSTL`), Company Code (`BUKRS`), Plant (`WERKS`), Division (`SPART`).
- Business Area, Sales Organization, Purchasing Organization.

> [!warning] Never put an organizational field in Value Context
> This is the single most common miscategorisation. A plant, a company code, and a sales org
> are *where*, never *how much*.

**Value Context** — **only** money, amounts, and financial values:

- Amounts (`NETWR`, `STPRS`, `VERPR`, `DMBTR`).
- Prices, costs, rates, percentages.
- Currencies (`WAERS`).
- **Never dates. Never organizational fields.**

**Activity Context** — **only** dates, times, and temporal fields:

- Creation date (`ERDAT`, `DATAB`, `DATUM`), modification date (`LAEDA`, `AEDAT`).
- Posting date, document date, activation and deactivation dates.
- Last-activity timestamp, frequency counters (how many days, how many months).
- **Never monetary values. Never organizational fields.**

> [!important] The field under check does not automatically live in Value Context
> An earlier reading of this standard put "the field(s) under check" in Value Context — so a
> UoM rule filed `MEINS` there and a date-comparison rule filed its dates there. That is
> superseded: the section is decided by **what kind of field it is**, not by whether the rule
> happens to be checking it. A checked date belongs in Activity Context; a checked material
> type belongs in Basic Fields. (Resolved: field type always determines section, never the rule's intent.)
>
> Where the per-field `classification` lookup below disagrees with a judgement call, the
> catalog classification wins — it is a lookup, not an argument.

## The whole-view field order

Sections are the SELECT-list half of a wider ordering the DQ Rule Standards mandate for the
Opportunity View as a whole:

1. Header comment block
2. `CREATE VIEW` statement using the naming convention
3. `zConcatenatedKey`
4. `zSourceSystemID`
5. All basic fields
6. The logical check — `zIsErrorFlag`
7. Organizational fields
8. Value fields
9. Activity fields
10. `FROM` the source table(s) directly — `MARA`, `MARC`, `KNA1`, …

> [!note] The list above puts `zConcatenatedKey` first — the SELECT list does not
> The standards doc's whole-view outline (§3.3) names `zConcatenatedKey` before `zSourceSystemID`,
> while its own SELECT-list specification (§3.4) fixes the order as `zSourceSystemID`,
> `zConcatenatedKey`, `zIsErrorFlag`. The **SELECT-list order is the operative one** — it is what
> the generator emits and what the round-trip parser reads. Read §3.3 as "these things appear, in
> these groups", not as a column order.

> [!note] Technical-field order inside section 1
> The standards doc fixes the *Syniti Technical Fields* section as **exactly** `zSourceSystemID`,
> `zConcatenatedKey`, `zIsErrorFlag`, in that order. `zDomainSegment` is a Studio addition that
> rides in the same section. (Studio addition; Info and Profiling rules emit the same section
> **without** `zIsErrorFlag`.)

### Which technical fields each rule type carries

| Rule type | `zSourceSystemID` | `zConcatenatedKey` | `zIsErrorFlag` | `[Implication]` | `zDomainSegment` |
|---|---|---|---|---|---|
| **Error** | yes | yes | yes (a CASE) | no | conditional |
| **Info** | yes | yes | no | yes | conditional |
| **Profiling** | yes (in the GROUP BY) | typically no | no | no | conditional |

`zConcatenatedKey` has **no space** in the name — an ADM requirement — and is built with
`CONCAT(...)` and an underscore delimiter, never `+` and never a pipe:
`CONCAT({table}.zSourceSystemID, '_', {table}.{key})`. The pipe form is a **blocking**
violation on the AI-Enhance path ([[std-ai-enhance-guardrails]]) and `+` is unsafe because it
propagates NULLs. Full recipe, including
the `COALESCE`/`TRIM` wrapping: [[std-zconcatenatedkey-convention]]. Older material still shows
the `{table}.{key} + '|' + {table}.zSourceSystemID` form — that is superseded, not an
alternative.

### `zDomainSegment` — conditional, and a plain column reference

It is added to the Tech section only when the rule's tables intersect a Customer, Vendor or
Material master table. Coverage, header table first because it carries the underlying classifier:

| Domain | Tables (priority order) |
|---|---|
| Customer | KNA1 (carries KTOKD), KNB1, KNVV, KNVI, KNVP, KNVK, KNVA, KNVD, KNVS, KNAS, KNB5, KNBK |
| Vendor | LFA1 (carries KTOKK), LFB1, LFM1, LFM2, LFAS, LFB5, LFBK, LFBW, LFC1, LFC3 |
| Material | MARA (carries MTART), MARC, MARD, MAKT, MBEW, MVKE, MARM, MEAN, MLAN, MLGN, MLGT |

Three rules govern how it is emitted:

- It is an **ordinary table reference** — `KNA1.zDomainSegment AS [zDomainSegment]`. **Not** a JOIN
  to a lookup table, **not** a CASE. The DQ Pipeline app pre-computes the column on the master
  tables themselves; the Studio only references it.
- It is a **classification, not an identifier** — so it never appears in the `zConcatenatedKey`
  recipe and is never marked `key="Yes"` on the OutputField.
- It is **never added to catalog-sourced SQL.** Catalog SQL ships verbatim by contract, and the
  spec's `output_fields` list is reverse-engineered from that SQL — injecting a Tech field would
  make the spec and the SQL disagree.

When a rule spans two domains (rare — say a Customer rule joining MARA), the source table is picked
by: earliest keyword mention in the rule name, then the same test on `data_domain`, then
`main_table` membership, then a deterministic alphabetical fallback. See
ref-multi-impl-fan-out-engine.

## Each section maps to a SAP field classification

The four non-technical sections are not a matter of taste — they map 1:1 onto each real SAP
field's `classification` in `SAP_ECC_Complete.json`:

| `classification` | Section |
|---|---|
| `Basic Field` | Basic Fields |
| `Organizational Field` | Organizational Context |
| `Value Field` | Value Context |
| `Activity Field` | Activity Context |

So the section a column lands in is *looked up*, not argued about. For tables absent from the
catalog, classify from domain knowledge using the same four buckets.

## Two rules for every real SAP column

**1. Carry a business-friendly bracketed alias**, derived from that field's `description` in
`SAP_ECC_Complete.json`, shortened and cleaned to a short Title Case phrase.

| Field | Catalog description | Alias |
|---|---|---|
| `LIFNR` | Account Number of Vendor or Creditor | `[Vendor Number]` |
| `NAME1` | Name 1 | `[Vendor Name]` |
| `BUKRS` | Company Code | `[Company Code]` |
| `SKONT` | Cash Discount Percentage | `[Cash Discount Percent]` |
| `ERDAT` | Date on Which the Record Was Created | `[Created On]` |

**2. Fully-qualify with the source table alias** — `LFA1.LIFNR`, never bare `LIFNR` — so each
section stays unambiguous across joins.

```sql
SELECT
    -- Syniti Technical Fields
    LFA1.zSourceSystemID AS [zSourceSystemID],
    CONCAT(...) AS [zConcatenatedKey],
    CASE WHEN ... THEN 1 ELSE 0 END AS [zIsErrorFlag],

    -- Basic Fields
    LFA1.LIFNR AS [Vendor Number],
    LFA1.NAME1 AS [Vendor Name],

    -- Organizational Context
    LFA1.BUKRS AS [Company Code],

    -- Value Context
    LFB1.SKONT AS [Cash Discount Percent],

    -- Activity Context
    LFA1.ERDAT AS [Created On]
FROM ...
```

> [!warning] Always select the live column for zSourceSystemID
> The example above shows the correct form: `LFA1.zSourceSystemID AS [zSourceSystemID]`. 
> A string literal or template token there is a High-severity, save-blocking violation 
> ([[std-ai-enhance-guardrails]]).

> [!note] Section header spellings
> The Studio generator emits `-- Organizational Context`, `-- Value Context`, and `-- Activity Context`.
> Match this spelling in your rules to ensure consistency with the generator output.

## Why this order

Reviewer flow when reading a defect record (top to bottom):
1. *"Which system did this come from?"* — Tech fields
2. *"Which record is this?"* — Basic fields
3. *"Where in the org?"* — Organizational Context
4. *"How much is it worth?"* — Value Context
5. *"When did it happen?"* — Activity Context

The defect itself is not a sixth question — `zIsErrorFlag` answered it in line 1. Sections 4
and 5 exist to give the remediator the financial and temporal context needed to prioritise the
fix, whichever section the checked field itself lives in.

Maps to the natural questioning a remediator asks. Out of order or unlabelled sections force the
reader to scan back-and-forth.

## Empty sections

If a rule genuinely has no Organizational Context fields (e.g. a profiling rule on the
configuration tables), still emit the comment header with nothing under it:

```sql
    -- Organizational Context

    -- Value Context
    ...
```

The blank section says *"reviewed, none applicable"* rather than *"forgot to think about org
context."*

## Why mandatory

AI-derived SQL is scored against this structure during audit. Missing section comments drop the
parity score against the catalog and trigger warnings on the bulk reconciliation Excel.

## Field Section Visual Reference

**When building an Error/Info OptSel view, consult this structure:**

```
┌─────────────────────────────────────────────────────────────┐
│            DQ Rule Output Field Section Structure            │
│                  (Error / Info Rules Only)                   │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  SELECT                                                       │
│    -- 1️⃣ Syniti Technical Fields                            │
│    zSourceSystemID, zConcatenatedKey, zIsErrorFlag,          │
│    zDomainSegment                                            │
│                                                               │
│    -- 2️⃣ Basic Fields                                        │
│    "WHAT is this record?"                                    │
│    Material# + Material Description                          │
│                                                               │
│    -- 3️⃣ Organizational Context                             │
│    "WHERE in the org?"                                       │
│    Plant, Company Code, Business Area                        │
│                                                               │
│    -- 4️⃣ Value Context                                       │
│    "HOW MUCH?"                                               │
│    Amounts, Prices, Costs, Currencies                        │
│                                                               │
│    -- 5️⃣ Activity Context                                    │
│    "WHEN?"                                                    │
│    Dates, Times, Timestamps                                  │
│                                                               │
│  FROM source_tables                                          │
│  WHERE universe_restrictions                                 │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

## Quick Reference — Section Placement Checklist

**When building an OptSel view, use this to verify correct placement:**

| Field Type | Belongs in | ✅ Examples | ❌ Never in | 
|---|---|---|---|
| **Primary Key** | Basic Fields | MATNR, KUNNR, LIFNR | Value, Activity |
| **Description** | Basic Fields | Material Name, Customer Name | Value, Activity |
| **Material Type** | Basic Fields | MTART (FERT, HALB) | Org, Value, Activity |
| **UoM, Currency Code** | Basic Fields | MEINS, WAERS (EA, KG) | Value, Activity |
| **Company Code** | Organizational | BUKRS (1000, 2000) | Basic, Value, Activity |
| **Plant** | Organizational | WERKS (1000, 2000) | Basic, Value, Activity |
| **Cost Center** | Organizational | KOSTL (CC001) | Basic, Value, Activity |
| **Division** | Organizational | SPART (01, 02) | Basic, Value, Activity |
| **Price Amount** | Value Context | STPRS, NETWR | Org, Activity |
| **Cost Amount** | Value Context | DMBTR, VERPR | Org, Activity |
| **Percentage** | Value Context | Tax%, Discount% | Org, Activity |
| **Creation Date** | Activity Context | ERDAT, DATAB | Org, Value |
| **Last Changed** | Activity Context | LAEDA, AEDAT | Org, Value |
| **Posting Date** | Activity Context | BUDAT, DBDAT | Org, Value |

## Step-by-Step Building Checklist

**Actionable steps when authoring a view:**

```
STEP 1: SELECT block structure
  ☐ Add "-- Syniti Technical Fields" comment
  ☐ Add "-- Basic Fields" comment
  ☐ Add "-- Organizational Context" comment
  ☐ Add "-- Value Context" comment
  ☐ Add "-- Activity Context" comment
  ☐ Do NOT reorder these comments

STEP 2: Syniti Technical Fields (always first)
  ☐ zSourceSystemID (table.zSourceSystemID, NOT a literal)
  ☐ zConcatenatedKey (CONCAT(table.zSourceSystemID, '_', table.key))
  ☐ zIsErrorFlag (CASE WHEN error THEN 1 ELSE 0 END)
  ☐ zDomainSegment (if Customer/Vendor/Material table present)

STEP 3: Basic Fields
  ☐ Primary key(s)
  ☐ Description/name columns
  ☐ Type/category fields
  ☐ All aliased with [Business Friendly Label]

STEP 4: Organizational Context
  ☐ Review: does this field answer "WHERE in the org"?
  ☐ If yes (Plant, Company, Cost Center): place it here
  ☐ If no: move to correct section
  ☐ If no org fields: leave section empty but keep comment

STEP 5: Value Context
  ☐ Review: is this field ONLY money/amount/currency?
  ☐ If yes: place it here
  ☐ If it's a date: MOVE to Activity Context
  ☐ If it's org-related: MOVE to Organizational Context
  ☐ If no value fields: leave empty but keep comment

STEP 6: Activity Context
  ☐ Review: is this field ONLY a date/time/timestamp?
  ☐ If yes: place it here
  ☐ If it's money: MOVE to Value Context
  ☐ If no activity fields: leave empty but keep comment

STEP 7: Verify no drift
  ☐ Read top-to-bottom: does each section name match its content?
  ☐ No Value fields in Activity or vice versa?
  ☐ No Org fields outside Organizational Context?
  ☐ Run SELECT mentally: "What question does each section answer?"
```

## Questions from consultants

- [[qa-profiling-rules-five-section-structure|Does the five-section structure apply to profiling rules?]]

## Related

- [[std-sql-comment-standards|SQL Comment Standards]]
- [[std-zsourcesystemid-convention|zSourceSystemID Convention]]
- [[std-zconcatenatedkey-convention|zConcatenatedKey Convention]]
- [[std-ziserrorflag-convention|zIsErrorFlag Convention]]
- [[std-ai-enhance-scope|AI Enhance Edit Scope]] — the sections are locked against AI edits
