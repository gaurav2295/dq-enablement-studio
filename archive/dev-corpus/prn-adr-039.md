---
id: prn-adr-039
type: principle
kind: decision
title: ADR D-39 — Catalog FTS5 search treats every query token as literal text, never as FTS5 query syntax
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-39
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Catalog FTS5 search treats every query token as literal text, never as FTS5 query syntax.

## Rationale

A malicious or merely careless search string (SQL-injection-shaped input, unbalanced quotes, bare FTS operators like OR/NOT/*) must never raise sqlite3.OperationalError from an FTS5 query-syntax error. The catalog index has to survive adversarial input from a search box, not just well-formed queries.

## Consequence

Every token reaching the FTS5 query is escaped/quoted so it's always treated as literal text. The test is parametrized over 9 adversarial strings and additionally asserts the underlying row count is untouched — proof against a real injection, not just "didn't crash". Any future change to the search-query builder must preserve this literal-text guarantee.

> [!note] Provenance
> Architecture decision **D-39** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
