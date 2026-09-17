---
id: prn-adr-041
type: principle
kind: decision
title: ADR D-41 — Catalog-promotion wrap preserves the catalog SQL verbatim; methodology fields are layered only in the outer SELECT
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-41
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Catalog-promotion wrap preserves the catalog SQL verbatim; methodology fields are layered only in the outer SELECT.

## Rationale

The user reported the correct shape directly: the wrap promoter must preserve the catalog's original SQL body VERBATIM in a derived table, layering methodology fields (the zIsErrorFlag CASE, technical fields) only in the OUTER SELECT — never rewriting the inner query. The aggregate (GROUP BY/HAVING) must stay in the inner subquery, never lifted into the outer CASE; a top-level ORDER BY is stripped silently (illegal inside a view/derived table); when eligibility fails, the outer flag falls back to a literal 1 AS [zIsErrorFlag] with a TODO comment rather than fabricating a CASE that isn't warranted.

## Consequence

Any future catalog-promotion change must keep the catalog body untouched and add methodology only around it — multiple negative assertions in the test class (e.g. no CASE/WHEN COUNT inside the aggregate) directly guard against regressing this structural contract.

> [!note] Provenance
> Architecture decision **D-41** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
