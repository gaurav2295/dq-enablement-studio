---
id: gls-op-report-query
type: glossary
title: Op Query / Report Query
domain: studio
audience: [developer]
level: practitioner
status: review
links:
  - relates:gls-opportunity-universe
sources:
  - vault:studio-architecture/Studio — Rule Catalog Structure.md
tags: [catalog, sql]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The two SQL statements a catalog entry carries: `op_query_sql` — **the universe**, every candidate
row with no error filter — and `report_query_sql` — the same query narrowed to the defects. HANA
variants are stored but unused by the MS SQL pipeline.

## Usage

The pair is the catalog's equivalent of the [[gls-optsel|OptSel]] / [[gls-rptsel|RptSel]] pair,
and the same discipline applies: the report query must be the op query filtered down, or the
counts do not reconcile.

Because it is a *filtering* relationship, the diff between them is extractable — that is the
[[gls-distinguishing-predicate|distinguishing predicate]] the promoter needs.
