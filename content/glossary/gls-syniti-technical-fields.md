---
id: gls-syniti-technical-fields
type: glossary
title: Syniti Technical Fields
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:std-output-field-sections

  - relates:gls-zsourcesystemid
  - relates:gls-zconcatenatedkey
  - relates:gls-ziserrorflag
  - relates:gls-zdomainsegment
sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [technical-fields, sections]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **metadata layer every Studio-generated view carries**, and the first of the five
[[std-output-field-sections|output field sections]]. The mandatory minimum is three, in this
order:

| Field | Meaning |
|---|---|
| [[gls-zsourcesystemid]] | which system the record came from |
| [[gls-zconcatenatedkey]] | the unique record key across systems |
| [[gls-ziserrorflag]] | the error verdict (Error rules only) |

## Usage

[[gls-zdomainsegment|zDomainSegment]] rides in the same section where the Studio emits it — treat
the three above as the minimum, not the maximum. Info rules emit the section without
`zIsErrorFlag`; Profiling rules put `zSourceSystemID` in the `GROUP BY`.

A missing technical column is a High-severity finding, and the section is **locked**
against AI edits ([[std-ai-enhance-scope]]).
