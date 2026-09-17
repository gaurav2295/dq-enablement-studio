---
id: gls-working-db
type: glossary
title: Working Database (working_db)
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:con-data-architecture-layers
  - relates:gls-prep-db

sources:
  - vault:studio-architecture/Studio — Layer-2-Layer-4 Datastore Views.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [architecture, databases]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**`WRKDQ` — the one rule repository.** The database a DQ rule view is `CREATE`d in *and* reads
`FROM`. One repository, same-DB read.

## Usage

The canonical topology is `source → SRCECC_DA → WRKDQPREP_ALL (upstream prep) → WRKDQ`. The
[[gls-prep-db|prep database]] applies relevancy, merges sources and scopes systems, and its output
is **pushed into** `WRKDQ`; rule views do not read the prep layer directly, and never read the raw
source database.

> [!warning] Always select FROM `working_db`, not `prep_db`
> Rule views select `FROM` the working database (`WRKDQ`), never the prep layer directly.
> Catalog `{datastore}` substitution genuinely does target the prep DB — that asymmetry is real,
> not a bug.
