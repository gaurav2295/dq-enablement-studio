---
id: prn-adr-056
type: principle
kind: decision
title: ADR D-56 — A tracker Category with a plain descriptive Source phrase is taken as a literal value, not silently dropped
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-56
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

A tracker Category with a plain descriptive Source phrase is taken as a literal value, not silently dropped.

## Rationale

Previously, a Category whose Source was a plain phrase like "SAP ECC Customer Master Data" was silently dropped, because the resolver only recognised a fixed set of descriptors — users had to know the undocumented static: prefix convention to get a literal value through at all.

## Consequence

Any non-descriptor string in a Category's Source is now taken as a literal value and carried verbatim onto every rule using that category. Any future descriptor addition must preserve this fallback so an unrecognised phrase degrades to "use it literally", never to silent data loss.

> [!note] Provenance
> Architecture decision **D-56** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
