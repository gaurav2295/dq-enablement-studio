---
id: gls-rule-repository
type: glossary
title: Rule Repository
domain: delivery
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-snapshot
  - relates:con-catalog-vs-bespoke-rules
  - relates:ref-rule-record-schema
sources:
  - bob-dq:CONTEXT.md
  - bob-dq:CLAUDE.md
tags: [bob-dq, instruments, catalogue]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**`syniti-dq-rule-repo`** — the **single catalogue of best rules**.

It is served three ways:

| Consumer | Transport |
|---|---|
| dq-studio | MCP |
| bob-canvas | MCP |
| The rule explorer | Local HTTP |

## Usage

*Single* is the operative word: one catalogue, many consumers. A rule that is good enough to
reuse belongs here, not copied into a project. Rules reaching the value chain carry their
[[gls-provenance]] stamp from this catalogue.

When the rule server is not running, bob-canvas falls back to an embedded
[[gls-snapshot]] — always labelled as such.

Catalogue vocabulary is **governed**: rule names and their mapping to key issues and value
levers change only by an explicit owner ruling (the repository's
[[prn-governed-ratification|ADR 0002]]). Agents may propose
and may apply owner-ratified principles to bulk queues, recording the principle, method and date
on every row — never invent vocabulary autonomously.

For how the Studio-side catalogue is structured, see ref-rule-catalog-structure and
[[con-catalog-vs-bespoke-rules]].
