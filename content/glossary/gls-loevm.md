---
id: gls-loevm
type: glossary
title: LOEVM
domain: sap
audience: [consultant, developer]
level: foundation
status: review
links:
  - parent:gls-deletion-flag
  - relates:ref-sap-deletion-flags-vs-status-fields
  - relates:ref-deletion-flag-resolver
  - relates:gls-lvorm
sources:
  - vault:sap-knowledge/SAP Deletion Flags vs Status Fields.md
tags: [sap, deletion, fields]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **customer/vendor deletion flag** — the central deletion indicator on `KNA1` and `LFA1`, and
the deletion flag on their org-level views (`KNB1`, `KNVV`, `KNVP`, `KNVI`, `LFB1`, `LFM1`,
`LFM2`). `'X'` = flagged for deletion.

## Usage

`KNA1 = LOEVM` and `LFA1 = LOEVM` are **SAP standard**, not client-specific — a point the resolver
had to learn the hard way after SQL generated against an assumed `LVORM` failed on a real client
build.

The working convention across the corpus: *mostly [[gls-lvorm|LVORM]] on master headers, LOEVM on
customer/vendor view tables, `LOEKZ` on transactional items* — a heuristic to check against
`DD03L`, never a substitute for checking.
