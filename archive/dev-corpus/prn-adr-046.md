---
id: prn-adr-046
type: principle
kind: decision
title: ADR D-46 — Substring/keyword matching in the local deriver prefers the longest overlapping key, never the first match
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-46
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Substring/keyword matching in the local deriver prefers the longest overlapping key, never the first match.

## Rationale

Regression for the GVTYP/XBILK rule: a rule mentioning 'balance sheet indicator' has two overlapping JSON keys — "balance" (-> SKB1.SALDO) and "balance sheet indicator" (-> SKA1.XBILK). The shorter key used to win because it matched first, wrongly binding SKB1; short keys must not silently win over longer, more-specific keys that overlap them.

## Consequence

The longer, more-specific overlapping key always takes precedence — SKA1.XBILK is bound instead of SKB1.SALDO for this phrasing. Any future keyword/lexicon addition must be checked against this greediness guard if it could overlap an existing shorter key.

> [!note] Provenance
> Architecture decision **D-46** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
