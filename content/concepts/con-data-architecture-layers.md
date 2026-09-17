---
id: con-data-architecture-layers
type: concept
title: Data Architecture Layers
domain: studio
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:con-multi-implementation-model
  - relates:std-zsourcesystemid-convention
  - relates:std-view-naming-patterns
  - relates:con-view-types
sources:
  - vault:dq-methodology/Data Architecture Layers.md
tags: [methodology, architecture]
created: 2026-08-20
updated: 2026-08-20
---

> [!note] Not the same "Layer 2/4" as the datastore views
> This unit's four layers (Source → Source DA → Prep → Working) are a different numbering scheme
> from the Layer 2/Layer 4 in ref-layer-2-layer-4-datastore-views, which names the relevancy
> filter view and the bridge view. Don't map one numbering onto the other.

## The flow

The path data takes from source SAP system to deployed DQ rule view:

```
Source SAP system (per-tenant DB, e.g. SRCECCZ02100)
        │  extract
        ▼
SRCECC_DA — Source DA: raw per-system extract, one row per source
record with original keys
        │  consolidate + add zSourceSystemID
        ▼
WRKDQPREP_ALL — Prep: upstream consolidated layer; tables here carry
zSourceSystemID, zDomainSegment, etc. Its output is PUSHED INTO WRKDQ.
        │  push prepped tables into WRKDQ
        ▼
WRKDQ — Working: one repository where the DQ rule views are CREATED
IN AND SELECT FROM (same-DB read). OptSel / RptSel / PrfSel / PrfSum
live here. SKP reads from this.
```

## Per-layer semantics

| Layer | DB name (typical) | Purpose | Who writes here |
|---|---|---|---|
| **Source** | `SRCECCZxxxxx`, `SRCS4SGxxxx` | Live SAP — read-only, the truth | SAP itself |
| **Source DA** | `SRCECC_DA` | Daily/periodic extract of source tables | The DQ Pipeline app |
| **Prep** | `WRKDQPREP_ALL` | Upstream consolidated cross-system layer; tables carry `zSourceSystemID`; output pushed into WRKDQ | The DQ Pipeline app |
| **Working** | `WRKDQ` | One repository — DQ rule views are created in and read from here (same-DB) | The Studio (creates and reads the rule views here) |

## What the Studio configures per layer

The project configuration names which database serves as the source, prep, and working layer
for the engagement. Confirming these three is part of project setup — see
ref-architecture-context-and-project-yamls for the full contract, and
ref-three-database-architecture for the canonical resolution of the three layers.

## Why the split exists

- **Source DA isolation** — extraction from real SAP happens once, in one place. DQ rules don't
  query SAP directly.
- **Prep is the consolidation point** — `zSourceSystemID` is added here (see
  [[std-zsourcesystemid-convention]]), relevancy/merge/aggregate/scope are applied across
  systems, and the prepped output is pushed into WRKDQ so rules can read one logical table that
  spans systems.
- **Working is the deployment surface** — rule views are created in AND read from WRKDQ (one
  repository, same-DB read); SKP, downstream BI, ADM tools all read from WRKDQ. Re-running rule
  generation never touches the underlying data.
