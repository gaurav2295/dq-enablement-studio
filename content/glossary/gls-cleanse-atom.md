---
id: gls-cleanse-atom
type: glossary
title: Cleanse Atom
domain: cleanse
audience: [consultant]
level: practitioner
status: deprecated
links:
  - parent:ref-cleanse-process-areas
  - relates:gls-process-area
  - relates:con-cleanse-execution-model
sources:
  - cleanse-canvas:docs/CONTEXT.md
  - cleanse-canvas:docs/DATA-MODEL.md
tags: [taxonomy, cleanse, visualisation]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A node in the structured, flow-style view of a cleanse plan — either a
[[gls-process-area|process area]] or a single object. The term is the client's, borrowed from SAP
Signavio's "process atoms".

## Usage

The atom view exists for legibility: with a hundred-plus objects, the area tier is what keeps the
plan readable at a glance, with drill-down into an area revealing its objects. Dependency edges
between objects roll up into area-level edges carrying a count and a flag for whether every
underlying edge is still unconfirmed.
