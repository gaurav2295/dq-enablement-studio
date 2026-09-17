---
id: gls-lvorm
type: glossary
title: LVORM
domain: sap
audience: [consultant, developer]
level: foundation
status: review
links:
  - parent:gls-deletion-flag
  - relates:ref-sap-deletion-flags-vs-status-fields
  - relates:ref-deletion-flag-resolver
  - relates:gls-loevm
sources:
  - vault:sap-knowledge/SAP Deletion Flags vs Status Fields.md
tags: [sap, deletion, fields]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

SAP's **material-family deletion flag** — `MARA`, `MARC`, `MARD`, `MAKT`, `MARM`, `MBEW`, `MVKE`.
`'X'` = flagged for deletion, blank = active. The name is R/3-era German shorthand,
*Löschvormerkung* ("deletion notice").

## Usage

LVORM is the **highest priority** name in the resolver's scan order
(`LVORM > LOEVM > LOEKZ`) for the rare table that physically carries more than one.

> [!warning]
> LVORM is *not* universal. `KNA1` and `LFA1` carry [[gls-loevm|LOEVM]] as SAP standard, and at
> least one client ECC build has no `LVORM` column on `KNA1` at all — SQL written against an
> assumed `LVORM` fails at execution. Always resolve, never assume.
