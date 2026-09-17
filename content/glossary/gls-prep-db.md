---
id: gls-prep-db
type: glossary
title: Prep Database (WRKDQPREP_ALL)
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:con-data-architecture-layers
  - relates:gls-working-db
sources:
  - vault:studio-architecture/Studio — Layer-2-Layer-4 Datastore Views.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [architecture, databases]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **consolidated prep layer** — the upstream ETL database (`WRKDQPREP_ALL`) that applies
relevancy criteria, merges sources, performs logical aggregation and applies scope for one or many
source systems. Its output is pushed into the [[gls-working-db|working database]].

## Usage

"Consolidated" is the operative word: it is where many source systems become one set of tables
carrying [[gls-zsourcesystemid|zSourceSystemID]], which is what makes a single rule view able to
span systems at all.

Rule views do **not** read the prep DB. The one place it is legitimately the target is catalog
`{datastore}` substitution.
