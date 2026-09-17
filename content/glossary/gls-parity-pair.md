---
id: gls-parity-pair
type: glossary
title: Parity Pair
domain: rule-design
audience: [developer]
level: advanced
status: review
links:
  - parent:std-pattern-org-to-central-parity
  - relates:gls-org-vs-central
  - relates:gls-status-field
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - dq-studio:knowledge/methodology/rule_patterns.json
tags: [rule-pattern, sap, parity]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **(central field, org-level field)** couple a parity rule compares — for example a central
block flag and its company-code-level counterpart, or a central deletion flag and its sales-area
counterpart.

## Usage

Parity pairs are knowledge, not inference. They come from curated SAP reference data the Studio
maintains for each domain — covering both the block variant (a status field and its org-level
counterpart) and the deletion variant (a central deletion flag and its org-level counterpart).

A multi-block rule ("blocked for posting or payments") resolves to **several** pairs, combined
together. Where a domain has no parity knowledge at all, slot filling returns a
PartialFill naming exactly what's missing — never a guess.
