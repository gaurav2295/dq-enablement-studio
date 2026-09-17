---
id: gls-methodology-banner
type: glossary
title: Methodology Banner
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: deprecated
links:
  - relates:std-sql-comment-standards
  - relates:gls-catalog-promoter
sources:
  - dq-studio:docs/DQ_RULE_STANDARDS.md
  - vault:studio-architecture/Studio — Catalog Promotion (wrap not inject).md
tags: [comments, provenance]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The header comment block every methodology-shaped view carries — rule name, author, creation date,
view type, rule id — and, on a promoted catalog view, the marker saying the SQL came from the
catalog and was **wrapped**, not rewritten.

## Usage

The banner is the artefact's provenance record, which is why a catalog-sourced view without one is
a finding: it means raw catalog SQL reached deployment without going through the
[[gls-catalog-promoter|promoter]].

The banner is also **locked** against AI edits, and the view name's rule id must match the id the
banner states.
