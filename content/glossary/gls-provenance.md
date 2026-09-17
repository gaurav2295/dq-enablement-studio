---
id: gls-provenance
type: glossary
title: Provenance (field_proven vs derived)
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: deprecated
links:
  - contrast:con-rule-provenance-model
  - relates:gls-dq-rule
  - relates:gls-rule-repository
  - relates:con-catalog-vs-bespoke-rules
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, rules, provenance, honesty]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**How the *rule* came to exist.** Two values:

| Value | Meaning |
|---|---|
| `field_proven` | Observed running in a live SAP data-quality deployment |
| `derived` | Authored to make a value lever walkable, and **has never run in the field** |

## Usage

The distinction is **load-bearing**: it is the difference between *"this works"* and *"this
should work"*. A blueprint built entirely from `derived` rules is a hypothesis, however
plausible; one built from `field_proven` rules is a track record. The instrument must let a
reader tell which they are looking at.

These two are the operative values in the served catalogue. The rule repository's README
documents a fuller three-value set that the data does not currently use — see
[[con-rule-provenance-model]], which records that drift rather than resolving it.

`provenance` describes the rule. It says nothing about the rule's *text* — that is
[[gls-name-source]], and the two are deliberately separate because writing a name for a real
rule does not make the rule less real.

> [!important]
> Never present a `derived` rule as evidence that something has been done before. Coverage built
> on derived rules is stated, not claimed — the same posture as [[gls-propose-and-promote]].
