---
id: ref-cleanse-process-areas
type: reference
title: Cleanse Process Areas & Business Process Areas
domain: cleanse
audience: [consultant, lead]
level: practitioner
status: review
links:
  - relates:gls-business-process-area
  - relates:gls-process-area
sources:
  - cleanse-canvas:docs/DATA-MODEL.md
  - cleanse-canvas:docs/PLAN-operational-layer.md
tags: [methodology, cleanse-execution, taxonomy]
created: 2026-08-20
updated: 2026-08-20
---

## Two aggregation dimensions, not one

A cleanse engagement with more than a handful of objects needs an aggregation layer above the
object list, or the plan stops being readable. This engagement pattern uses **two distinct
dimensions**, deliberately kept separate because they answer different questions:

- **Process area** — a cleanse-execution grouping: which objects get worked together because
  they sit in the same functional neighbourhood (procurement, transportation, asset
  management, …). This is the lens the tactical/operational layers use.
- **Business Process Area (BPA)** — a coarser, end-to-end *business-process* grouping (a
  Source-to-Contract / Procure-to-Pay style map), independent of how the cleanse work itself is
  organized. This is the lens the strategic/outcomes layer uses.

An object maps into exactly one process area and, through that, into one BPA — but the two
groupings are computed and reviewed separately, because a process area is a cleanse-delivery
convenience while a BPA is meant to mirror the client's own end-to-end business-process model
(e.g. a Signavio-style map) and should be confirmed against it, not invented independently.

> **Provisional by nature.** Both taxonomies below are worked examples from one supply-chain +
> asset/finance cleanse engagement. The process-area list is a judgement call derived from
> object names and domains where the source data wasn't clean enough to classify automatically,
> and should be reviewed by workstream leads before reuse. The BPA names/groupings are
> explicitly **provisional** pending confirmation against the client's own end-to-end process
> taxonomy on any given engagement — treat both as a reusable *pattern* to adapt, not a fixed
> vocabulary to import verbatim.

## Process areas (cleanse atoms)

Ordered left-to-right for a structured, flow-style view of the plan. In that view every node —
whether an area or a single object — is a **cleanse atom** (the term borrows from Signavio's
"process atoms"), and the area tier exists so that a hundred-plus objects stay legible at a
glance, with drill-down into an area revealing its objects. Each area aggregates the objects
that share a functional neighbourhood:

| # | Process area | What it groups |
|---|---|---|
| 1 | Material & Product Data | Material/product master and related product-data objects |
| 2 | Supplier & Vendor Management | Vendor/supplier master and relationship objects |
| 3 | Org Structure & Users | Organizational units, roles, and user/authorization objects |
| 4 | Sourcing & Contracts | Sourcing, RFx, and contract objects |
| 5 | Purchasing & Orders | Purchase requisitions/orders and related transactional objects |
| 6 | Service Procurement | Service-specific procurement objects |
| 7 | Inventory & Warehouse | Stock, warehouse, and inventory-management objects |
| 8 | Transportation — Network & Master | Transportation master data and network configuration |
| 9 | Transportation — Execution & Settlement | Transportation execution, freight, and settlement objects |
| 10 | Enterprise Asset Management | Equipment, functional location, maintenance objects |
| 11 | Invoice, Tax & Finance | Invoicing and tax-adjacent objects sitting close to procurement |
| 12 | Finance & Controlling | Core finance and controlling objects |

Process areas aggregate **object-level dependency edges** into **area-level edges** the same
way (see [[con-cleanse-execution-model]] on dependency direction and basis): if objects in area
A depend on objects in area B, that rolls up into an A→B area edge carrying a count and a flag
for whether every underlying object edge is still unconfirmed.

## Business Process Areas (BPA)

A coarser, end-to-end business-process lens grouping the twelve process areas into six:

| # | Business Process Area | Member process areas |
|---|---|---|
| 1 | Source-to-Contract | Supplier & Vendor Management, Sourcing & Contracts |
| 2 | Procure-to-Pay | Purchasing & Orders, Service Procurement, Inventory & Warehouse, Material & Product Data, Invoice/Tax & Finance |
| 3 | Plan-to-Maintain | Enterprise Asset Management |
| 4 | Transportation & Logistics | Transportation — Network & Master, Transportation — Execution & Settlement |
| 5 | Record-to-Report | Finance & Controlling |
| 6 | Enabling & Foundational | Org Structure & Users |

BPAs are the grouping the **strategic layer** reports against: outcome tiles, KPI tracking, and
programme-level roll-ups are framed by BPA, not by process area, because BPA is meant to mirror
how the business (not the cleanse team) thinks about its own processes.

## Known overlap with the outcome hierarchy — unreconciled

This process-area / BPA pair is a **separate taxonomy** from the "process area" tier of the
L1–L5 outcome hierarchy used elsewhere in value/outcomes methodology — see
[[con-outcome-hierarchy-l1-l5]], whose L3 tier carries the same name for a different thing.
The overlap between the two is **not yet reconciled** — logged as CONFLICT-002 in
`docs/CONFLICTS.md`. Do not assume the two taxonomies' process-area names line up; treat them
as two independent lenses until a CoE decision merges or formally contrasts them.
