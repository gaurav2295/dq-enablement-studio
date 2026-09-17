---
id: gls-tracker
type: glossary
title: Tracker (DQ_Report_Tracker)
domain: studio
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:ref-skp-assetupload-and-tracker-flow
  - relates:ref-exporters

  - relates:gls-rule-package
  - relates:gls-dqops-id
sources:
  - vault:studio-architecture/Studio — SKP AssetUpload & Tracker Flow.md
  - dq-studio:docs/Studio_Overview.md
tags: [exports, skp, tracker]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

`DQ_Report_Tracker.xlsx` — the row-per-implementation workbook the Studio exports, and the
engagement's working register of what was built, for which system, and where it stands.

## Usage

The tracker is the hand-off artefact between rule design and deployment: one row per
implementation, keyed by its [[gls-dqops-id|DQOps id]], carrying rule name, type, view names,
category and assignee.

Two disciplines attach to it: a row whose spec still carries **unresolved validator findings**
should not be exported (REQ-TRACKER-UNRESOLVED-FINDINGS),
and a tracker Category with a plain descriptive Source phrase is taken as a **literal value**,
never silently dropped (ADR D-56).
