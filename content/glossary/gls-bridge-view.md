---
id: gls-bridge-view
type: glossary
title: Bridge View (Layer 4)
domain: sql-standards
audience: [developer]
level: advanced
status: review
links:
  - relates:con-data-architecture-layers
  - relates:gls-filter-view
  - relates:gls-zsourcesystemid
sources:
  - vault:studio-architecture/Studio — Layer-2-Layer-4 Datastore Views.md
tags: [architecture, datastore-views]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **Layer-4** datastore view, named for the table it fronts (`{table}`): relevancy-scoped and
system-stamped. One is generated for **every** table in scope, and it is what adds
[[gls-zsourcesystemid|zSourceSystemID]] — from the Layer-2 filter where one exists, otherwise from
a hardcoded system literal.

## Usage

Bridges are the *plumbing* under the DQ rules, not rule views: a rule's `FROM` resolves against
bridges, so the rule never has to restate relevancy. Each bridge header declares which of three
scenarios it is — `direct_relevancy`, `secondary_linkage`, `no_relevancy`.

Deployment is two-pass — all [[gls-filter-view|filter views]] first, then all bridges — because a
bridge's `FROM` depends on its filter.
