---
id: con-attribute-usage-analysis
type: concept
title: Attribute Usage Analysis (AUA)
domain: rule-design
audience: [consultant]
level: practitioner
status: review
links:
  - prereq:con-profiling-concepts
  - relates:con-filter-presets
  - relates:prc-run-an-attribute-usage-analysis
  - relates:std-aua-spec-template
  - relates:con-view-types
sources:
  - vault:dq-methodology/Attribute Usage Analysis.md
tags: [methodology, profiling, deep-dive]
created: 2026-08-20
updated: 2026-08-21
---

## What it is

A deep-dive profiling variant that pivots **low-cardinality attributes** by **organisational
structure** instead of the global per-column distribution that [[con-profiling-concepts|standard
profiling]] produces. AUA answers questions of the form *"How does MTART distribute across WERKS
× BUKRS?"* or *"What customer account groups dominate each Sales Org × Distribution Channel?"* —
questions invisible in a single-column profile but central to MDM, governance, and harmonisation
decisions.

AUA lives under ref-schema-profiler as the *Attribute Usage Analysis (Deep Dive)*
sub-section on `/profile`.

## The shape of the question

Standard schema profiling tells you how a column is distributed across the whole table:

| Field | Value | Count | % |
|---|---|---|---|
| MTART | FERT | 142,310 | 38.9% |
| MTART | HALB | 89,001 | 24.4% |
| MTART | ROH | 71,452 | 19.6% |

AUA tells you how that same column distributes within each org-dim slice:

| Plant (WERKS) | MTART | Count | % within plant |
|---|---|---|---|
| 1000 | FERT | 12,400 | 71% |
| 1000 | HALB | 3,002 | 17% |
| 1000 | ROH | 2,103 | 12% |
| 2000 | FERT | 8,801 | 9% |
| 2000 | HALB | 41,002 | 44% |
| 2000 | ROH | 43,201 | 47% |

Two plants, same attribute, totally different mastering implications. Plant 1000 looks like a
finished-goods plant; plant 2000 looks like a semi-finished / raw-material plant. AUA surfaces
that signal; standard profiling cannot.

## The qualifier — what counts as "low-cardinality"

A column qualifies for AUA when its **top 20 distinct values cover ≥ 80% of non-null records**,
computed from the standard profile's Top-N output (already capped at 20K per column — top 20 is
a slice, no extra SQL pass needed).

| Outcome | Meaning |
|---|---|
| Top 20 ≥ 80% | Qualifies — pivot makes sense |
| Top 20 < 80% | Skip — the tail is too long to pivot, profile globally only |

The Studio also accepts an explicit attribute list from the spec — when present, the qualifier
is bypassed for those attributes (assumes the spec author knows what they want).

## The org-dim list — hybrid resolution

Each table has a canonical set of org-dim breakdowns:

| Table | Canonical breakdowns |
|---|---|
| MARA | MTART (Material Type) |
| MARC | WERKS (Plant) |
| MVKE | VKORG × VTWEG (Sales Org × Distr Channel) |
| KNB1 | BUKRS (Company Code) |
| KNVV | VKORG × VTWEG (Sales Org × Distr Channel) |
| BSEG | BUKRS, GSBER, HKONT |
| EKKO | BUKRS, EKORG |

These defaults live in the Studio knowledge base as `org_dimensions.json` — 25 tables seeded;
extend it as new tables surface.

Resolution precedence:

1. Spec `.md` file — if provided, its `Segmentation Attributes` line wins.
2. `org_dimensions.json` — the knowledge-driven defaults.
3. Nothing — the table is skipped with a manifest entry explaining why.

Spec entries fill knowledge gaps; knowledge entries never override the spec.

## Deletion-flag handling

AUA applies the same `auto_active` preset (see [[con-filter-presets|Filter Presets]]) as standard
profiling — `LVORM <> 'X'`, `LOEKZ <> 'X'`, or `LOEVM <> 'X'` depending on the table. The spec can
override with an explicit deletion-flag field.

Per [[con-deletion-flags-vs-status-fields]], the deletion-flag exclusion goes in the `WHERE`
clause — it shapes the **universe**, not the per-row check. AUA has no `zIsErrorFlag` — it's
profiling, not error-detection.

## The SQL output — tall pivots, one SELECT per triple

AUA emits **one SELECT block per (table × org-breakdown × attribute) triple**. Tall, not wide.
Each block returns:

| Column | Source |
|---|---|
| `zSourceSystemID` | The system filter (per-system fan-out via system_filter) |
| `org_combination` | The org-dim values, single field or a concatenation for multi-field |
| `attribute_name` | Literal — the attribute being analysed |
| `attribute_value` | The value being counted |
| `occurrences` | `COUNT(*)` |
| `percentage_within_org` | The percentage-window math (see below) |

```sql
-- ============================================================
-- MVKE × Sales Org × Distr Channel × VMSTA
-- ============================================================
SELECT
    MVKE.zSourceSystemID,
    CONCAT(MVKE.VKORG, '-', MVKE.VTWEG) AS org_combination,
    'VMSTA' AS attribute_name,
    MVKE.VMSTA AS attribute_value,
    COUNT(*) AS occurrences,
    CAST(100.0 * COUNT(*)
         / NULLIF(SUM(COUNT(*)) OVER (
             PARTITION BY MVKE.zSourceSystemID, CONCAT(MVKE.VKORG, '-', MVKE.VTWEG)
         ), 0)
         AS DECIMAL(5,1)) AS percentage_within_org
FROM [WRKDQ].[dbo].MVKE
WHERE MVKE.LVORM <> 'X' -- Exclude deletion-flagged records (auto_active)
GROUP BY
    MVKE.zSourceSystemID,
    CONCAT(MVKE.VKORG, '-', MVKE.VTWEG),
    MVKE.VMSTA
;
```

**Tall vs wide rationale:** wide pivots blow up under unknown distinct-value sets and break under
SSMS column limits. The Studio's HTML renderer pivots into the wide grid the user wants to *see*;
the SQL is structured to be hand-editable.

> [!note]
> The `NULLIF(..., 0)` divide-by-zero guard is mandatory — same as the standard profiler.

## What the user does with the SQL

1. Generate the script from `/profile` → AUA card.
2. Open in SSMS, **edit by hand**: add joins for description text, tighten filters, comment out
   blocks they don't care about.
3. Run; export each result set as a tab in the same workbook (or as separate CSVs).
4. Upload the result back to `/profile` → AUA "Render HTML Visualisation" button → standalone
   HTML.

Step 2 is intentional. AUA is project-owned SQL the team maintains; the Studio generates a clean
starting point, not a black box.

## The HTML visualisation

The renderer produces a self-contained HTML file mirroring the Syniti aesthetic of the standard
schema-profiler dashboard:

- **KPI bar** — attributes profiled, org dims covered, total occurrences.
- **Sidebar filters** — by table, by breakdown.
- **Per-attribute cards** — pivot table + small-multiples chart per org-dim slice.
- **Drill-in drawer** — click a cell to see the underlying rows.

Same parsing tolerance as the standard dashboard — accepts `.xlsx`, `.csv`, `.tsv`, `.txt` (SSMS
export), or `.zip` of any of those.

## The AUA Spec `.md` format

Three formats are accepted, all parsing into the same spec structure. Pick the one that matches
where you are in the profiling lifecycle. Full template: [[std-aua-spec-template]].

### Format 1 — multi-table (Studio canonical)

Sprint-level spec — multiple tables in one file. Compact, fast to author.

```markdown
# Attribute Usage Analysis — Sprint 3

## Table: MARC
- Org breakdown: Plant — WERKS
- Attributes: low cardinality

## Table: MVKE
- Org breakdown: Sales Org × Distr Channel — VKORG, VTWEG
- Attributes: low cardinality
```

### Format 2 — per-table report template (stand-up form)

Minimal signal lines, easy to template. Used before the profile runs.

```markdown
Data Profiling Report Template: MVKE

Description
Analyze low-cardinality attributes within MVKE and evaluate their distribution
across Sales Organization and Distribution Channel to identify consistency,
dominant patterns, and opportunities for standardization.

Attributes Profiled: All MVKE attributes classified as Low-Cardinality in profiling statistics
Segmentation Attributes: MVKE.VKORG, MVKE.VTWEG
```

### Format 3 — Data Profiling Specification (post-profile deliverable)

The richest form — carries the full profiling deliverable inline. Authored after a profile run,
when the spec author has reviewed the Top-N output and selected which attributes matter. Each
attribute gets its own `### FIELDNAME _(distinct values: N)_` H3 section with the per-system
top-N value table.

```markdown
# Data Profiling Specification: MVKE (Material - Sales Data)

## Scope - Inclusion / Exclusion

| | Criteria |
|---|---|
| **Inclusion** | Finished-goods materials (MTART IN ('FERT','ZFPR','ZMDA')); active at sales level (LVORM <> 'X'). |
| **Exclusion** | Non-finished-goods material types; sales-level deleted records (LVORM = 'X'). |

## Segmentation / Organizational Column

- **Organizational column:** VKORG + VTWEG (Sales Organization + Distribution Channel)

## Low-Cardinality Attributes - Top 50 Values

### MEGRU  _(distinct values: 2)_
| # | Value | Total Count | Total % |
| 1 | *(blank)* | 579,615 | 100.00% |
| 2 | `ZUL` | 19 | 0.00% |

### PRAT1  _(distinct values: 2)_
```

The parser reads every H3 carrying the `_(distinct values: N)_` tail as one explicit attribute —
no coverage-qualifier upload is needed, because the spec already carries the qualifier output.
The inclusion-filter prose becomes the SQL banner; the user adds the actual WHERE clause when
editing the generated SQL.

### Format selection by lifecycle stage

| Lifecycle stage | Recommended format |
|---|---|
| Pre-profile (planning) | Format 1 (sprint) or Format 2 (per-table stand-up) with `Attributes: low cardinality` |
| Post-profile (deliverable) | Format 3 — carries the Top-N data + chosen attribute list inline |
| Explicit attribute override (any stage) | Format 1 with comma-separated `Attributes: MTART, KTOKD, MMSTA` |

The parser auto-detects which format each file uses and dispatches accordingly. Multi-file zips
are flattened and aggregated into one spec.

## What AUA is NOT

- Not an error rule — there's no `zIsErrorFlag`, no pass/fail.
- Not a column-grain profile — that's standard profiling, which AUA depends on (the qualifier
  reads its top-20 output).
- Not for high-cardinality attributes (MATNR, KUNNR, document numbers) — pivots collapse to one
  row per distinct value with ~0% concentration; nothing to learn.
- Not a replacement for SAP authorisation analysis or master-data quality reporting — it's an
  **input** to those decisions, not the conclusion.
- Not a stored view — AUA outputs are one-off result sets, not one of the
  [[con-view-types|OptSel / RptSel / InfSel / PrfSel / PrfSum]] view types.

## When to run AUA

| Trigger | Why AUA helps |
|---|---|
| New MDM scoping engagement | Reveals which org dims actually segment the data — informs harmonisation scope |
| Pre-migration cutover | Spot which legacy values cluster in which org units → drive value-mapping tables |
| Catalog rule tuning | When an Error rule's `IS NULL` check produces wildly different defect rates per plant/company-code, AUA tells you whether the rule needs scoping refinement |
| Governance reviews | Distribution-of-distributions makes outlier org units visible |
