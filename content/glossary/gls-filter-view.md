---
id: gls-filter-view
type: glossary
title: Filter View (Layer 2)
domain: sql-standards
audience: [developer]
level: advanced
status: review
links:
  - relates:con-data-architecture-layers
  - relates:gls-bridge-view
  - relates:con-filter-presets
sources:
  - vault:studio-architecture/Studio — Layer-2-Layer-4 Datastore Views.md
tags: [architecture, datastore-views]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **Layer-2 relevancy filter** view (`{system}_{table}_FILT`) — one per *direct-relevancy*
table. It applies the table's relevancy rule (inclusions and exclusions) to scope which rows are
in play at all.

## Usage

A relevancy rule is authored as "what to keep / remove". An **inclusion** emits its operator
as-is; an **exclusion** flips it to the inverse (`=`→`<>`, `IN`→`NOT IN`, `LIKE`→`NOT LIKE`,
`IS NULL`→`IS NOT NULL`) so the `WHERE` always expresses the *keep* set. Every string literal is
`N''`-prefixed for MS SQL.

Filter views exist only where a table has direct relevancy; every table gets a
[[gls-bridge-view|bridge]], not every table gets a filter.
