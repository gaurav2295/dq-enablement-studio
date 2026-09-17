---
id: gls-distinguishing-predicate
type: glossary
title: Distinguishing Predicate
domain: sql-standards
audience: [developer]
level: advanced
status: deprecated
links:
  - relates:prn-catalog-promotion-wraps-instead-of-injecting
  - relates:gls-catalog-promoter
  - relates:gls-ziserrorflag
sources:
  - vault:studio-architecture/Studio — Catalog Promotion (wrap not inject).md
tags: [promotion, logic]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The condition the catalog's **report query** adds on top of its **op query** — a top-level `WHERE`,
a `HAVING`, or a subquery `HAVING` the op query does not have. It is the difference between "the
universe" and "the defects", and therefore *is* the rule's error condition.

## Usage

Promotion is only eligible when both queries exist, their skeletons match up to the first
`WHERE`/`GROUP BY`/`ORDER BY`/`HAVING`/`UNION`, and a distinguishing predicate exists. The promoter
lifts that predicate into a [[gls-ziserrorflag|zIsErrorFlag]] `CASE` in an outer `SELECT`, leaving
the catalog SQL verbatim underneath ([[prn-catalog-promotion-wraps-instead-of-injecting]]).

No distinguishing predicate means no derivable per-row condition — which is where the
[[gls-literal-1-fallback|literal-1 fallback]] comes from.
