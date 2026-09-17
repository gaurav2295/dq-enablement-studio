---
id: gls-mdg
type: glossary
title: MDG (SAP Master Data Governance)
domain: sap
audience: [consultant, lead]
level: foundation
status: deprecated
links:
  - relates:con-studio-capabilities
  - relates:gls-reference-data
sources:
  - dq-studio:docs/Studio_Overview.md
  - vault:sap-knowledge/SAP Data Domains.md
tags: [sap, governance, mdm]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

SAP's **Master Data Governance** product — the target MDM platform many clients are moving to, in
which master data is created and changed through governed workflows rather than direct entry.

## Usage

MDG matters to a DQ engagement in two ways: it is a common **target model** a cleanse has to land
in (ref-target-mdm-model-fit), and its governed fields tell you which defects will stop
recurring once it is live and which will not. Rules that police what MDG will enforce anyway have
a short shelf life; rules that police what it does not are the durable ones.
