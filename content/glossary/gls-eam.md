---
id: gls-eam
type: glossary
title: Enterprise Asset Management (EAM)
domain: sap
audience: [consultant]
level: foundation
status: deprecated
links:
  - relates:ref-cleanse-process-areas
  - relates:ref-sap-modules
  - relates:gls-business-process-area
sources:
  - cleanse-canvas:docs/CONTEXT.md
  - vault:sap-knowledge/SAP Modules — FI, CO, MM, SD, PP, QM, PM.md
tags: [sap, domains, cleanse]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The asset-maintenance side of an SAP landscape and the object family that comes with it — work
centre, functional location, equipment, bill of material, task list, maintenance plan, work order.

## Usage

EAM is both a **data domain** and, on many programmes, a **workstream**: it is one of the twelve
cleanse process areas and maps to the Plan-to-Maintain
[[gls-business-process-area|Business Process Area]].

Its objects are unusually dependency-heavy — equipment depends on functional location, task lists
on work centres — which is why EAM cleanse plans are sequenced more strictly than master-data-only
plans.
