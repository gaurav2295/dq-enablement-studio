---
id: prn-adr-057
type: principle
kind: decision
title: ADR D-57 — AssetUpload's CDQ Error/Opportunity Error Query columns follow the SKP OptSel/RptSel convention
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-57
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

AssetUpload's CDQ Error/Opportunity Error Query columns follow the SKP OptSel/RptSel convention.

## Rationale

Columns 19/20 of the Enforcements AssetUpload follow a fixed SKP convention. For Error rules: col 19 (CDQ Error Query) points at the RptSel view (filtered defects), derived from the tracker's OptSel name by literal OptSel -> RptSel substitution, and col 20 (CDQ Opportunity Error Query) carries the OptSel view verbatim (the "all candidates + zIsErrorFlag" query). For Profiling rows, the same two columns instead map to the Profiling-specific views: col 19 to PrfSum (aggregated) and col 20 to PrfSel (record-level) — reusing the same two SKP query-role columns Error rules use for RptSel/OptSel.

## Consequence

Any future rule type added to the tracker-to-AssetUpload exporter must map onto these same two SKP query-role columns rather than inventing new column semantics; changing the OptSel->RptSel substitution convention would break every existing Error-rule AssetUpload row, not just new ones.

> [!note] Provenance
> Architecture decision **D-57** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
