---
id: prn-adr-058
type: principle
kind: decision
title: ADR D-58 — The AssetUpload System Name column (col 10) is intentionally left blank
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-58
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The AssetUpload System Name column (col 10) is intentionally left blank.

## Rationale

The per-implementation system code is already encoded in the SQL view name itself (e.g. "..._P02_..."), and the Sprint-1 reference AssetUpload leaves this column empty. Populating it would duplicate information already present in the view name without adding value, and would conflict with SKP's own System Name being a separate, higher-level entity than a per-view system code.

## Consequence

Column 10 must stay blank on every generated AssetUpload row. Any future request to populate it needs a product decision first (it isn't a gap to silently fill in), since SKP's System Name entity operates at a different level than the view-name-embedded system code.

> [!note] Provenance
> Architecture decision **D-58** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
