---
id: gls-round-trip-parse
type: glossary
title: Round-Trip Parse
domain: sql-standards
audience: [developer]
level: practitioner
status: review
links:
  - relates:std-sql-comment-standards
  - relates:std-output-field-sections
sources:
  - vault:studio-architecture/Studio — SQL Parser (reverse-engineer specs).md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [parser, contract]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

Reading a generated artefact **back** into a structured spec — SQL or exported markdown in, spec
out — so a rule can be edited, re-derived or audited without its original session.

## Usage

Round-tripping is why the comment and section conventions are mandatory rather than cosmetic: the
section headers and the rule's identity banner are what make a generated view readable back into a
structured spec. A view with reordered or missing section comments parses into a lesser spec.

The practical rule for anyone hand-editing generated SQL: keep the shape. Content inside a section
is yours; the section markers are the contract.
