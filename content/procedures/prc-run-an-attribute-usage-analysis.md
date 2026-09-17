---
id: prc-run-an-attribute-usage-analysis
type: procedure
title: Run an Attribute Usage Analysis
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:sops/SOP — Run an Attribute Usage Analysis.md
tags: [sop, profiling, deep-dive]
created: 2026-08-20
updated: 2026-08-21
links:
  - prereq:con-attribute-usage-analysis
  - prereq:prc-generate-a-profile-bundle
  - relates:std-aua-spec-template
  - relates:con-profiling-concepts
  - relates:con-filter-presets
---

## Goal

Take a list of profiling targets and produce a runnable SSMS deep-dive script plus a downstream
HTML visualisation, end to end. AUA is the *Attribute Usage Analysis (Deep Dive)* sub-section of
the Schema Profiler — see [[con-attribute-usage-analysis|Attribute Usage Analysis]] for the
methodology contract.

## When to use

- After a standard profile bundle has been generated and reviewed — AUA reads its Top-N output to
  apply the low-cardinality qualifier
- MDM scoping engagements where you need to see how attributes distribute *per org unit*, not
  globally
- Pre-migration cutover validation — spotting which legacy values cluster in which plants /
  company codes / sales orgs
- Catalog rule tuning — when an Error rule's defect rate varies wildly by plant or company code,
  AUA tells you whether the rule needs re-scoping

## Prerequisites

- Studio running locally
- A profiling target list already loaded on `/profile` (the AUA endpoint reads from the same
  session state — no separate upload)
- Optional: an AUA spec `.md` file (per-table report-template format, or multi-table Studio
  canonical) — pasted as `.md`, `.markdown`, `.txt`, or zipped together
- Optional: a recent profile-results upload — the qualifier reads it to filter low-cardinality
  attributes
- SQL Server access (where you'll run the generated script)

## Steps

### 1. Confirm the standard profile is in session

`/profile` must already show targets in the targets card. AUA reuses that list — it does NOT
take a fresh xlsx upload. If you've reloaded the page, re-upload the targets first.

### 2. Author or import the AUA spec

The spec drives which **org breakdowns** to pivot by and which **attributes** to profile.
Resolution order:

1. **Spec `.md` file** wins for both org-dim and attribute selection
2. **Knowledge file** (`knowledge/methodology/org_dimensions.json`, 25 tables seeded) fills
   org-dim gaps
3. **Profile-results upload** fills attribute gaps via the top-20 ≥ 80% coverage qualifier
4. **No data** — the table is skipped with a manifest entry

**Three `.md` formats are supported** (auto-detected per file). Pick the one that matches where
you are in the profiling lifecycle:

**Format 1 — Multi-table (sprint spec, pre-profile)**

```markdown
# Attribute Usage Analysis — Sprint 3

## Table: MVKE
- Org breakdown: Sales Org × Distr Channel — VKORG, VTWEG
- Attributes: low cardinality
```

Multiple tables in one file. Authoring habit: compact, fast.

**Format 2 — Per-table report template (stand-up form, pre-profile)**

```markdown
Data Profiling Report Template: MVKE

Description
Analyze low-cardinality attributes within MVKE...

Attributes Profiled: All MVKE attributes classified as Low-Cardinality
Segmentation Attributes: MVKE.VKORG, MVKE.VTWEG
```

One file per table, signal-line driven. Used to template the spec before the profile runs.

**Format 3 — Data Profiling Specification (post-profile deliverable)**

```markdown
# Data Profiling Specification: MVKE (Material - Sales Data)

## Scope - Inclusion / Exclusion
| | Criteria |
|---|---|
| **Inclusion** | Finished-goods materials (MTART IN ('FERT','ZFPR','ZMDA')); active at sales level (LVORM <> 'X'). |

## Segmentation / Organizational Column
- **Organizational column:** VKORG + VTWEG (Sales Organization + Distribution Channel)

## Low-Cardinality Attributes - Top 50 Values
### MEGRU  _(distinct values: 2)_
| # | Value | Total Count | Total % |
|---|---|---|---|
| 1 | *(blank)* | 579,615 | 100.00% |
| 2 | `ZUL` | 19 | 0.00% |
```

The post-profile deliverable. Authored after a profile run, it carries the full top-N analysis
inline. Every `### FIELDNAME _(distinct values: N)_` heading becomes one entry in the explicit
attribute list — **no profile-results upload needed**, since the spec already encodes the
qualifier output. The inclusion-filter prose becomes the SQL banner (you add the actual WHERE by
hand when editing the generated SQL).

> [!tip]
> Format 3 is now the format the team is standardising on for archival sprint deliverables. The
> other two remain valid for early-stage / lightweight specs.

See [[std-aua-spec-template|AUA Spec Template]] for the full reference and worked examples.

### 3. Generate the script

In the *Attribute Usage Analysis (Deep Dive)* card on `/profile`:

1. Select the spec `.md` file(s) — multiple files or a zip both accepted
2. Optionally attach the latest profile-results file — drives the low-cardinality qualifier
   (top 20 ≥ 80% coverage)
3. Confirm `prep_db` (default `WRKDQ`) and project name
4. Click **Generate AUA Script**

The Studio produces `DQ_Attribute_Usage_Analysis.sql`: one SELECT block per (table × org-breakdown
× attribute) triple, each with:

- A banner comment naming the triple
- `auto_active` deletion-flag exclusion in the WHERE clause (LVORM / LOEKZ / LOEVM per the table)
- Percentage-window math partitioned by `(zSourceSystemID, org_combination)` with a
  `NULLIF(..., 0)` guard

### 4. Edit the SQL by hand

This is the **point** of generating SQL instead of running it inline — the team owns the script
and maintains it:

- Add joins for description text (MAKT for MARA, etc.)
- Tighten filters per the project's scope
- Comment out blocks you don't care about
- Rename `attribute_name` literals to human labels if you want

Save the edited script into the project's `/sql/` folder.

### 5. Run the script in SSMS

Open the script, connect to the target SQL Server, execute. AUA produces one result set per
SELECT block. Run time: ~30 seconds per (table × breakdown × attribute) triple. A typical 5-table
sprint with 8 attributes each runs in 3–5 minutes.

### 6. Export the results

In SSMS, switch each result-set tab and export. Either:

- **Workbook approach** — paste each result into a tab of a single `.xlsx` workbook (preferred —
  the HTML renderer picks up sheet boundaries cleanly)
- **CSV-per-tab approach** — save each result as a separate `.csv` / `.tsv` / `.txt`, then zip them

Both formats are accepted by step 7. Required columns in each export:

| Column | Purpose |
|---|---|
| `zSourceSystemID` | The per-system slice |
| `org_combination` | The org-dim value (single field, or `CONCAT(F1, '-', F2)`) |
| `attribute_name` | Literal — which attribute this row belongs to |
| `attribute_value` | The distinct value being counted |
| `occurrences` | `COUNT(*)` for the (system, org, attribute, value) cell |
| `percentage_within_org` | The window math output |

Plus implicit `table_name` and `org_breakdown_label` — emitted in the banner comments and inferred
by the renderer.

### 7. Render the HTML visualisation

Back on `/profile` — AUA card — **Step 2: Upload AUA results**. Drop the `.xlsx`, zip, or loose
files. Click **Render HTML**.

The Studio produces a standalone HTML file with:

- A KPI bar (attributes profiled, org dims covered, total occurrences)
- Sidebar filters by table and breakdown
- Per-attribute cards with a pivot table and small-multiples chart per org-dim slice
- A drill-in drawer on cell click

Save the HTML alongside the SQL in the project folder; it's self-contained (no external assets).

## Verification

- The generated SQL passes a syntax check in SSMS without errors
- Each SELECT block returns non-zero rows (a zero-row block means the deletion-flag exclusion
  wiped the whole universe — check that)
- Percentage-within-org values sum to ~100% (allow ±0.2 for rounding) within each
  (zSourceSystemID, org_combination) slice
- The HTML visualisation renders the expected number of attribute cards
- Spot-check a known attribute (MTART × WERKS is the canonical one) — the distribution looks sane

## Common pitfalls

- **Targets card empty** — AUA can't read targets from nowhere. Re-upload the targets xlsx on the
  standard profiler card first.
- **Spec format mismatch** — the parser auto-detects, but mixing format-1 `## Table:` headers with
  format-2 `Data Profiling Report Template:` lines, or with format-3
  `# Data Profiling Specification:` plus attribute headings, in the same file confuses the
  dispatcher. Pick one format per file.
- **Format 3 attributes silently dropped** — headings without the `_(distinct values: N)_` tail
  are ignored. The parser uses that tail as the fingerprint to distinguish attribute headings from
  other headings (`### Rule`, `### Implementation`). Keep the tail intact.
- **Format 3 inclusion filter not auto-applied** — the prose in the Scope table appears in the SQL
  banner but does NOT generate a WHERE clause. You edit the generated SQL to inject the actual
  filter (e.g. `AND MATNR IN (SELECT MATNR FROM MARA WHERE MTART IN ('FERT','ZFPR','ZMDA'))`) into
  each block. AUA generates structure, not project-specific scope.
- **Table not in `org_dimensions.json`** — the Studio skips it with a manifest warning. Either
  extend the JSON (preferred — submit a PR) or add an explicit `- Org breakdown:` line in the
  spec.
- **Percentage doesn't sum to 100%** — usually means the deletion-flag column changed in this
  system (e.g. a Z*/Y* clone of MARA without LVORM). Override the deletion flag in the spec.
- **HTML viz shows "no data"** — the export columns don't match the required schema. Re-export
  with explicit column aliases in the SELECT.
- **Block named "MARA × MTART × MTART" runs but produces one row at 100%** — you tried to pivot an
  org-dim by itself. Org breakdown and attribute must be different fields.

## Related

- [[con-attribute-usage-analysis|Attribute Usage Analysis]] — the methodology contract
- [[std-aua-spec-template|AUA Spec Template]] — the `.md` formats
- [[con-profiling-concepts|Profiling Concepts]] — what column-grain profiling produces; AUA
  depends on its Top-N output
- [[con-filter-presets|Filter Presets]] — `auto_active` resolution
- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]] — why deletion
  exclusions go in WHERE
- [[prc-generate-a-profile-bundle|Generate a Profile Bundle]] — the prerequisite standard profile
