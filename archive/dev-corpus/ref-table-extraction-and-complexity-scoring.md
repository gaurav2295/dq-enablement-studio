---
id: ref-table-extraction-and-complexity-scoring
type: reference
title: Table Extraction & Complexity Scoring
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-sql-parser
  - relates:ref-sql-validator
  - relates:ref-sql-generator
  - relates:ref-catalog-promotion
  - relates:ref-view-vs-table-qualification
  - relates:ref-exporters
sources:
  - vault:studio-architecture/Studio — Table Extraction & Complexity Scoring.md
tags: [studio, engine, sql, sap, methodology]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

Two small read-only engines power the Tracker's "Tables" and "Rule Complexity" columns:
`extract_tables_from_sql` returns the alias- and comment-blind list of SAP tables a view
reads, and `score_sql_complexity` sums a point total over tables / data volume / joins /
clauses (driven ENTIRELY by the OptSel) and buckets it Low / Medium / High / Very High.

Both are heuristics for reviewer triage, not validators — they never execute the SQL or
read runtime statistics. They exist so a reviewer can see, at a glance in the export, which
SAP tables a rule touches and which rules deserve a careful performance review before
deploy. Pair with [[ref-sql-parser]] (which rebuilds full specs) and the
[[ref-exporters|Tracker exporter]] that consumes both columns.

## What table extraction does

`extract_tables_from_sql(sql, *, top_level_only=False)` returns the **de-duplicated,
first-occurrence-ordered, uppercased** list of SAP table names a view reads. Conventions
(all load-bearing — do not "fix" them):

- **Aliases are never returned.** `FROM KNVK AS CT` → `["KNVK"]`, not `CT`. The
  `_TABLE_ANCHOR` regex captures only the bare table name after `FROM`/`JOIN`, consuming
  any alias.
- **Comment-blind.** `_strip_comments` deletes `/* ... */` blocks and `-- ...` lines BEFORE
  scanning, so a header banner like `-- View: Defects in KNA1` cannot be mistaken for a
  `FROM`.
- **Qualification-tolerant.** The anchor matches `FROM TBL`, `FROM dbo.TBL`,
  `FROM [DB].[dbo].TBL`, and `FROM [DB].[dbo].[TBL]` — the catalog mixes all of these.
- **Stop-words guard.** `_TABLE_STOPWORDS` (SELECT, WHERE, JOIN, ON, AS,
  LEFT/RIGHT/INNER/FULL/OUTER/CROSS, UNION, WITH, TOP, INTO, …) prevents capturing a SQL
  keyword as a table when the catalog SQL uses unusual line-breaking.
- **Subquery paren handling.** Default `top_level_only=False` INCLUDES subquery tables, so
  `IN (SELECT y FROM TBL2)` contributes `TBL2`. Set `top_level_only=True` to strip balanced
  parens first and return only the visible record-set sources.

`extract_tables_from_specs(sql_optsel, sql_rptsel)` unions both views but **drops any RptSel
"table" ending `_OPTSEL`** — because the canonical RptSel is just `SELECT * FROM <OptSel>`,
so its only reference is the OptSel view, not an SAP table. Result = source-data SAP tables
only.

## Complexity scoring algorithm

`score_sql_complexity(sql_optsel, sql_rptsel)` is **driven entirely by the OptSel**; the
RptSel wrapper is ignored (its FROM points at the OptSel view, which carries the real
complexity). Empty/blank OptSel → `1-Low` (score 0). It calls `extract_tables_from_sql` for
the table list, then sums five components:

| Component | Rule |
|---|---|
| **Table count** | 1→1, 2-3→2, 4-5→3, 6+→4 |
| **Per-table volume** | sum of per-table scores, **capped at 6**. HIGH=3, MEDIUM=2 (default), LOW=1 |
| **JOIN count** | 0→0, 1-2→1, 3-4→2, 5+→3 |
| **Multi-condition joins** | +1 per `ON` clause containing `AND`/`OR` |
| **Clause / function complexity** | see below (additive) |

Clause/function points (all additive):

- `CASE`: ≥1 `WHEN` → +1; ≥4 `WHEN` → +1 more.
- `IN (SELECT …)` → +2; `EXISTS (SELECT …)` → +2; `NOT EXISTS (SELECT …)` → +2.
- `LIKE`/`NOT LIKE`: ≥1 → +1; ≥3 → +1 more.
- any of `TRY_CONVERT`/`CONVERT`/`CAST`/`PARSE` → +1.
- `GROUP BY` → +1; `HAVING` → +1; `OVER(` → +2.
- recursive CTE (`WITH … RECURSIVE`) → +3.
- `UNION [ALL]` → +1.

**Volume classification** (`_table_volume_score`) is a hardcoded SAP-table-size registry —
edit the dicts to refine the heuristic:

- **`_HIGH_VOLUME_TABLES`** (10M-100M+ rows): Finance/CO line items `BSEG, BKPF, ACDOCA,
  FAGLFLEXA, GLT0, COEP/COSP/COSS/COBK/COFI, AUFK/AFRU/AFKO/AFPO`; material movements
  `MSEG/MKPF/MARDH/MCHB/MCHA`; SD line items
  `VBAP/VBAK/VBRP/VBRK/LIPS/LIKP/VBFA/VBPA/VBKD/VBUK/VBUP`; purchasing
  `EKPO/EKKO/EKBE/EKES/EKET`; pricing conditions `KONV/KONP/KONA`; history `MBEW_HIST`;
  quality `QALS/QAPP/QASR`.
- **`_LOW_VOLUME_TABLES`** (<10K rows): T-config (`T001*, T002, T024*, T134/T161/T163/T169`),
  TV* sales config, org/master-of-master `T882/TKA01/TKA02/T880`, cost/activity master
  `CSKS/CSKT/CSLA/…`, profit-center/set `CEPC*/SETHEADER/SETNODE`, customer/vendor
  sub-shards `KNVK/KNVP/…, LFM2/LFAS/LFB5/LFBK/LFBW`, material detail
  `MARC/MARD/MAKT/MVKE/MARM/MAEX/MEAN/MLAN`, info-records `EINA/EINE/T024L`.
- **Everything else defaults to MEDIUM** — covers the bulk of master data (`KNA1, LFA1,
  MARA, VBAK` headers, etc., 100K-10M rows).

### Buckets and rendering

`_BUCKET_THRESHOLDS` maps the raw score to a tier (note: SD headers `VBAP/VBAK` are counted
high-volume here):

```text
score <= 4           → 1-Low
5  <= score <=  9    → 2-Medium
10 <= score <= 14    → 3-High
score > 14           → 4-Very High
```

`format_complexity(result)` renders the Tracker cell as `"<bucket>-<label>"` — e.g.
`"3-High"`.

## Inputs & outputs

| | |
|---|---|
| **Extractor input** | any DQ-rule SQL (CREATE VIEW + body, or just the body); empty → `[]` |
| **Extractor output** | `list[str]` of uppercased SAP tables, first-occurrence order |
| **Scorer input** | OptSel + RptSel SQL strings (RptSel ignored); empty OptSel → `1-Low` |
| **Scorer output** | `ComplexityScore(bucket, label, score, parts)` — `parts` is the per-component breakdown for reviewer transparency |

> [!success] Implementation status — resolved 2026-07-01 (KNOWN-ISSUES B10)
> The Studio app shell is **FastAPI + Jinja** (`app.py` + `ui/templates/*.html`), not
> Streamlit — relevant when wiring these into an export page. `CLAUDE.md` was corrected to
> state FastAPI + Jinja. Both engines are
> framework-agnostic and run server-side at export time.

## Source

- `core/sql_table_extractor.py:31-134` — stop-words, `_TABLE_ANCHOR`, `_strip_comments`,
  `extract_tables_from_sql`, `extract_tables_from_specs`.
- `core/sql_complexity.py:44-275` — volume dicts, `_table_volume_score`,
  `_BUCKET_THRESHOLDS`, `score_sql_complexity`, `format_complexity`.
- Detail: `knowledge-mining/sql-generation.md` §9-10.

## Related

[[ref-sql-parser]] · [[ref-sql-validator]] · [[ref-sql-generator]] · [[ref-catalog-promotion]]
· [[ref-view-vs-table-qualification]] · [[ref-zconcatenatedkey-and-ziserrorflag-sql-emission]]
· [[ref-exporters]] · [[ref-sap-baseline-model]]
