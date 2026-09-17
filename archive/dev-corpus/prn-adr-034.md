---
id: prn-adr-034
type: principle
kind: decision
title: ADR D-34 — SKP BulkImport AssetUpload filenames are frozen forever, regardless of the v3 naming migration
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-34
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

SKP BulkImport AssetUpload filenames are frozen forever, regardless of the v3 naming migration.

## Rationale

The two AssetUpload.xlsx/.json filenames are an external SKP BulkImport contract, not Studio-internal naming — SKP's own import tooling expects these exact names. The v3 canonical-naming migration touched export/naming.py broadly but must never touch these two literals.

## Consequence

TestSkpAssetUploadNamesUnchanged greps api/routes.py directly for the literal names rather than trusting the constant, guarding against silent drift if a future refactor renames the constant without updating the route. Any future naming-convention change must explicitly carve out these two filenames.

> [!note] Provenance
> Architecture decision **D-34** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
