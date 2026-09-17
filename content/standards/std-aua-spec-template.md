---
id: std-aua-spec-template
type: standard
title: AUA Spec Template
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - vault:templates/AUA Spec Template.md
tags: [template, profiling, deep-dive]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:con-attribute-usage-analysis
  - relates:con-filter-presets
  - relates:prc-run-an-attribute-usage-analysis
  - relates:con-profiling-concepts
---

## What it is

The `.md` format the Studio reads to drive [[con-attribute-usage-analysis|Attribute Usage
Analysis]]. **Three flavours** are accepted; all parse into the same `AUASpec` struct. Pick
whichever matches your team's authoring habit — the Studio auto-detects which format each file
uses, and you can mix-and-match across files in the same zip upload.

| Format | One file = | Strength | Best for |
|---|---|---|---|
| 1 — Multi-table | many tables | Compact, fast to author | Sprint-level spec covering 5+ tables |
| 2 — Per-table report template | one table | Minimal signal lines, easy to template | Quick stand-up specs before a profile run |
| 3 — Data Profiling Specification | one table | Carries the full profiling deliverable (top-N values per attribute, scope rules, validations) | After a profile run — when the spec author has done the qualifier work offline |

**Quick decision guide:** if you've already run a profile and have the top-N values per attribute,
use **Format 3** (no qualifier upload needed at generation time — the spec carries the explicit
attribute list). If you're spec-ing before you have profile data, use **Format 1** or **2** with
`Attributes: low cardinality` and let the qualifier resolve the list at generation time.

## Format 1 — Multi-table (Studio canonical)

One markdown file. One `## Table:` header per target. Compact when you're spec-ing a sprint of
5+ tables in one go.

```markdown
# Attribute Usage Analysis — <Project / Sprint Name>

## Table: MARC
- Org breakdown: Plant — WERKS
- Attributes: low cardinality

## Table: MVKE
- Org breakdown: Sales Org × Distr Channel — VKORG, VTWEG
- Attributes: low cardinality

## Table: KNB1
- Org breakdown: Company Code — BUKRS
- Attributes: low cardinality
- Deletion flag: LOEVM

## Table: BSEG
- Org breakdown: Company Code × GL Account — BUKRS, HKONT
- Attributes: BSCHL, BUZID, KOART
```

### Field reference

| Bullet | Required | Notes |
|---|---|---|
| `Org breakdown` | yes | `<Human Label> — <FIELD1>, <FIELD2>, …`. Multi-field labels concatenate as `CONCAT(FIELD1, '-', FIELD2)` in SQL |
| `Attributes` | yes | `low cardinality` for auto-qualifier, or a comma-separated list of field names |
| `Deletion flag` | no | Overrides the `auto_active` resolution; use only when the table's flag isn't in `org_dimensions.json` |
| `Universe` | no | Free-text description of the scope (echoed into the SQL banner) |

Multiple `Org breakdown` lines are allowed under one table — the Studio emits one pivot per
breakdown.

## Format 2 — Per-table report template (the user's natural format)

One `.md` file per table, signal-line driven. Closer to the existing report templates the team
writes by hand. Drop a folder of these into a zip and upload.

```markdown
Data Profiling Report Template: MVKE
Rule Header
Rule

Field	Value
Rule ID	
Rule Name	
Data Domain	

Implementation

Field	Value
DQOps ID	

Description
Analyze low-cardinality attributes within MVKE and evaluate their distribution
across Sales Organization and Distribution Channel to identify consistency,
dominant patterns, and opportunities for standardization to support MDM
decision-making.

Attributes Profiled: All MVKE attributes classified as Low-Cardinality in profiling statistics
Segmentation Attributes: MVKE.VKORG, MVKE.VTWEG

Output Fields (Generic Template)

Key Attributes	Attribute Value	Concatenated Key
```

### Signal lines (case-sensitive prefixes)

| Line | Purpose |
|---|---|
| `Data Profiling Report Template: <TABLE>` | Sets the target table. Optional — falls back to the filename stem |
| `Description` (followed by a paragraph) | Captured into the SQL banner comment |
| `Attributes Profiled: All <TABLE> attributes classified as Low-Cardinality` | Triggers the auto-qualifier |
| `Attributes Profiled: <TABLE>.FIELD1, <TABLE>.FIELD2, …` | Explicit attribute list — bypasses qualifier |
| `Segmentation Attributes: <TABLE>.FIELD1, <TABLE>.FIELD2` | The org breakdown. Comma-separated. Table qualifier is stripped |

The parser tolerates blank lines, tab indentation, and the surrounding template scaffolding (Rule
Header / Implementation / Output Fields blocks are ignored).

### Filename convention

Use the table name as the filename so the fallback path works when the
`Data Profiling Report Template:` line is missing:

```
MVKE.md
MARC.md
KNB1.md
KNVV.md
KNVP.md
```

## Format 3 — Data Profiling Specification (the rich post-profile deliverable)

The format teams produce **after** running a schema profile and reviewing the Top-N values per
column. One `.md` file per table, but unlike Format 2 it carries the **entire profiling
deliverable** — rule header, scope (inclusion / exclusion), organizational column, and one
`### FIELDNAME _(distinct values: N)_` H3 section per low-cardinality attribute (each with its
own per-system top-N value table).

The Studio reads the H3 attribute headers as the **explicit** attribute list. No qualifier upload
is needed when generating AUA SQL — the spec already represents the qualifier output.

```markdown
# Data Profiling Specification: MVKE (Material - Sales Data)

## Rule Header

### Rule

| Field | Value |
|---|---|
| Rule ID | _(to assign)_ |
| Rule Name | MVKE Low-Cardinality Attribute Distribution |
| Data Domain | Material Master Data |
| Object Type | MVKE - Sales Data for Material |
| Business Process | Master Data Management - profiling & standardization |
| Business Impact | Inconsistent low-cardinality values fragment reporting and block harmonization across systems |
| Rule Type | Profiling / Distribution analysis |
| Source | Schema Profiler Top-N export (25/27 May run) |

### Implementation

| Field | Value |
|---|---|
| DQOps ID | _(to assign)_ |
| System | ECCZ02100, ECCZ03100, ECCZ06100, S4SG2100 |
| View Type | Generated profiling view |
| Generated View | DQ_Profile_TopN (MVKE) |

## Description

Analyse low-cardinality attributes within **MVKE** and evaluate their value distribution to identify
master-data inconsistencies and standardization opportunities. Attributes below are those classified
**low-cardinality** (≤ 10 distinct values) in the profiling statistics; each shows its **top 50 values**
by record count, broken out across the four source systems.

## Scope - Inclusion / Exclusion

| | Criteria |
|---|---|
| **Inclusion** | Finished-goods materials (MTART IN ('FERT','ZFPR','ZMDA')); active at sales level (LVORM <> 'X'). |
| **Exclusion** | Non-finished-goods material types; sales-level deleted records (LVORM = 'X'). |

## Segmentation / Organizational Column

- **Organizational column:** VKORG + VTWEG (Sales Organization + Distribution Channel)
- **Concatenated key:** MATNR + VKORG + VTWEG
- **Verification:** Confirmed present in profiling; correct sales-area segmentation key.

## Low-Cardinality Attributes - Top 50 Values

### MEGRU  _(distinct values: 2)_

| # | Value | Total Count | Total % | ECCZ02100 | ECCZ03100 | ECCZ06100 | S4SG2100 |
|---|---|---|---|---|---|---|---|
| 1 | *(blank)* | 579,615 | 100.00% | 170387 | 92816 | 316388 | 24 |
| 2 | `ZUL` | 19 | 0.00% | 2 | 1 | 16 | 0 |

### PRAT1  _(distinct values: 2)_

| # | Value | Total Count | Total % | ECCZ02100 | ECCZ03100 | ECCZ06100 | S4SG2100 |
|---|---|---|---|---|---|---|---|
| 1 | *(blank)* | 524,774 | 90.54% | 118930 | 90247 | 315573 | 24 |
| 2 | `X` | 54,860 | 9.46% | 51459 | 2570 | 831 | 0 |

… (one H3 section per attribute) …
```

### Signal lines (case-insensitive)

| Line | Purpose | Studio uses it for |
|---|---|---|
| `# Data Profiling Specification: <TABLE>` | H1 — sets the target table | Table name (falls back to filename stem) |
| `## Scope - Inclusion / Exclusion` table | Inclusion filter prose | `universe_label` — echoed into the SQL banner; user adds the actual WHERE by hand |
| `- **Organizational column:** <fields>` | Org-dim bullet | `OrgBreakdown.fields` (splits on `+` or `,`) |
| `### FIELDNAME  _(distinct values: N)_` | One H3 per attribute | Each becomes one entry in `explicit_attributes` |

### Org-column expression parsing

| Spec input | Parsed fields | Rendered label | SQL `org_combination` |
|---|---|---|---|
| `VKORG + VTWEG (Sales Organization + Distribution Channel)` | `[VKORG, VTWEG]` | `Sales Org × Distr Channel` | `CONCAT(MVKE.VKORG, '-', MVKE.VTWEG)` |
| `BUKRS (Company Code)` | `[BUKRS]` | `Company Code` | `KNB1.BUKRS` |
| `WERKS (Plant)` | `[WERKS]` | `Plant` | `MARC.WERKS` |

The parenthetical descriptor is dropped — only the raw SAP codes feed the SQL. Splitter accepts
`+`, `,`, or `/` between codes.

### Attribute H3 fingerprint — exact

The `_(distinct values: N)_` tail is what distinguishes attribute-list H3s from other H3 headers
in the spec (`### Rule`, `### Implementation`, etc). Without that tail, an H3 is ignored. The `N`
value itself is informational — it isn't otherwise used when reading the spec.

### Worked example — what the Studio produces

For the MVKE spec above:

- **Table** → `MVKE`
- **Org breakdown** → `Sales Org × Distr Channel [VKORG, VTWEG]`
- **Primary key** (from `org_dimensions.json`) → `MATNR, VKORG, VTWEG`
- **Deletion flag** (from `org_dimensions.json`) → `LVORM`
- **Explicit attributes** → `MEGRU, PRAT1, PRAT2, PRAT3, PRAT4, PRAT5, PRAT6, PRAT7, PRAT8, PRAT9, PRATA, SKTOF, VAVME, ZZHLFNR1, PROVG, ZZQTYPE, BONUS, VERSG, ZZHLFNR2, ZZBRANDNATURE, SCHME, RDPRF` (22 attributes)
- **Universe banner in SQL** → `Finished-goods materials (MTART IN ('FERT','ZFPR','ZMDA')); active at sales level (LVORM <> 'X').`
- **SQL emitted** → 22 SELECT blocks (one per attribute), each pivoted by `VKORG × VTWEG`, with `WHERE MVKE.LVORM <> 'X'`

The user then **edits the generated SQL by hand** to inject the inclusion clause
(`AND MATNR IN (SELECT MATNR FROM MARA WHERE MTART IN ('FERT','ZFPR','ZMDA'))`) into each block —
AUA generates the structure, not the project-specific scope filters. The inclusion banner serves
as a reminder.

### When to use Format 3 vs Format 1/2

| Situation | Use |
|---|---|
| You've run a profile + reviewed the Top-N output + selected which attributes matter | **Format 3** (carries everything inline) |
| You want a stand-up spec before the profile runs, qualifier will resolve the attribute list | **Format 1** or **2** with `Attributes: low cardinality` |
| You want explicit attributes but don't have the full profile output yet | **Format 1** with `Attributes: MTART, KTOKD, MMSTA` (comma list) |

Format 3 specs are typically the **archival deliverable** of a profiling sprint — they replace
the original Format 2 stub once profile data is in hand.

## What the breakdown label produces

| Spec input | Human label rendered | SQL `org_combination` |
|---|---|---|
| `WERKS` | `Plant` | `MARC.WERKS` |
| `BUKRS` | `Company Code` | `BSEG.BUKRS` |
| `VKORG, VTWEG` | `Sales Org × Distr Channel` | `CONCAT(MVKE.VKORG, '-', MVKE.VTWEG)` |
| `LAND1, REGIO` | `Country × Region` | `CONCAT(KNA1.LAND1, '-', KNA1.REGIO)` |

If a field doesn't have a registered friendly label, the raw field name is used instead.

## Worked example — full per-table spec

The exact file structure used in the Danone sprint (`MVKE.md` excerpt):

```markdown
Data Profiling Report Template: MVKE

Description
Analyze low-cardinality attributes within MVKE and evaluate their distribution
across Sales Organization and Distribution Channel to identify consistency,
dominant patterns, and opportunities for standardization to support MDM
decision-making.

Attributes Profiled: All MVKE attributes classified as Low-Cardinality in profiling statistics
Segmentation Attributes: MVKE.VKORG, MVKE.VTWEG
```

What the Studio produces from this:

- Reads `org_dimensions.json` for MVKE → primary_key `[MATNR, VKORG, VTWEG]`, deletion_flag `LVORM`
- Spec overrides breakdown to `VKORG × VTWEG`
- Qualifies attributes from the latest profile output (top-20 ≥ 80% coverage)
- Emits one tall SELECT per qualifying attribute
- Banner comment quotes the Description paragraph

## Common pitfalls

- ❌ Forgetting the `<TABLE>.` qualifier on segmentation fields (Format 2) — works (parser strips it) but harder to read in source control
- ❌ Mixing `## Table:` headers with the report-template body — pick one format per file
- ❌ Listing an attribute that's not low-cardinality and not in `Attributes Profiled:` — gets silently dropped during qualifier pass; check the manifest
- ❌ Forgetting the deletion-flag override when the table isn't in `org_dimensions.json` — the Studio degrades to `no_filter` with a manifest warning
- ❌ Format 3: dropping the `_(distinct values: N)_` tail from an attribute H3 — the parser uses that tail to distinguish attribute headers from other H3s (`### Rule`, `### Implementation`). Without it the attribute is ignored
- ❌ Format 3: writing the org-column bullet as `- Organizational column: VKORG, VTWEG` (no bold markdown emphasis) — works in the latest parser, but anyone reading the spec by eye expects the canonical `- **Organizational column:** VKORG + VTWEG (...)` form. Keep the bold + parenthetical descriptor for human readers
- ❌ Format 3: relying on the inclusion-filter prose to actually filter records — it doesn't. The Studio echoes it into the SQL banner as a reminder; the user adds the WHERE clause by hand when editing the generated SQL

## Related

- [[con-attribute-usage-analysis|Attribute Usage Analysis]] — the full contract this template feeds
- [[con-filter-presets|Filter Presets]] — `auto_active` is the AUA default
- [[prc-run-an-attribute-usage-analysis|SOP — Run an Attribute Usage Analysis]] — operator-side instructions
