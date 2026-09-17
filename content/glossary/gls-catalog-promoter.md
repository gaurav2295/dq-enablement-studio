---
id: gls-catalog-promoter
type: glossary
title: Catalog Promoter
domain: studio
audience: [developer]
level: practitioner
status: review
links:
  - relates:prn-catalog-promotion-wraps-instead-of-injecting

sources:
  - vault:studio-architecture/Studio — Catalog Promotion (wrap not inject).md
tags: [catalog, promotion]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The component that turns a catalog entry's **op query / report query pair** into a deployable
methodology-shaped Error OptSel — by wrapping the catalog SQL in an outer `SELECT` that adds the
Syniti technical fields and the derived [[gls-ziserrorflag|zIsErrorFlag]].

## Usage

**Wrap, never inject.** The catalog SQL is preserved verbatim as a subquery; methodology fields are
layered only in the outer `SELECT` (ADR D-41). That is what keeps the catalog the
authority on what the rule *asks* while the methodology stays the authority on the artefact's
*shape*.

Promotion candidates are **git-governed** — never a runtime write into the live catalog
(ADR D-21).
