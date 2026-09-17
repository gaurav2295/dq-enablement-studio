---
id: prn-adr-040
type: principle
kind: decision
title: ADR D-40 — A native Error catalog entry with op+rpt queries must go through the methodology restructure, never ship raw catalog SQL
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-40
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

A native Error catalog entry with op+rpt queries must go through the methodology restructure, never ship raw catalog SQL.

## Rationale

Regression for rule 0142 / the KNA1 address-completeness shape: previously, native Error catalog entries (rpt adds only a WHERE clause on top of op) bypassed promotion entirely and shipped raw catalog SQL — leaving OptSel with no zIsErrorFlag column at all and breaking the canonical RptSel WHERE filter that the rest of the methodology depends on.

## Consequence

Every native Error catalog entry must be restructured so OptSel becomes the universe query plus a per-row zIsErrorFlag CASE, and RptSel is the canonical WHERE [zIsErrorFlag] = 1 wrapper — never the catalog's raw op/rpt SQL passed straight through. Any future catalog promotion path must apply this same restructure before a native Error entry can derive.

> [!note] Provenance
> Architecture decision **D-40** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
