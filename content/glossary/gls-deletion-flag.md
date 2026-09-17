---
id: gls-deletion-flag
type: glossary
title: Deletion Flag
domain: sap
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:ref-deletion-flag-resolver
  - relates:prn-deletion-flags-belong-in-where
  - relates:gls-lvorm
  - relates:gls-loevm
  - relates:gls-status-field
sources:
  - vault:sap-knowledge/SAP Deletion Flags vs Status Fields.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [sap, deletion, filters]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The SAP column marking a record as **flagged for deletion** — `'X'` set, blank active. Its
physical name varies by table family: [[gls-lvorm|LVORM]] on master headers and material views,
[[gls-loevm|LOEVM]] on customer/vendor views (and on `KNA1`/`LFA1` themselves), `LOEKZ` on
transactional items.

## Usage

The standing rule: **a deletion flag belongs in the `WHERE`, not in the flag logic.** Deleted
records leave the [[gls-opportunity-universe|universe]] entirely, so the defect rate is computed
over live data ([[prn-deletion-flags-belong-in-where]]).

> [!important]
> The deliberate exception is a **deletion-detection rule**, whose whole subject *is* the flag —
> see [[gls-deletion-detection-rule]].

Never assume the column name. Resolve it per table and per client build — see
[[ref-deletion-flag-resolver]].
