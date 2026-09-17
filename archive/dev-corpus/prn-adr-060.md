---
id: prn-adr-060
type: principle
kind: decision
title: ADR D-60 — The SKP user-list CSV parser strips whitespace from emails
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-60
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

The SKP user-list CSV parser strips whitespace from emails.

## Rationale

SKP exports sometimes ship emails with trailing spaces (e.g. "anna.pascal@Syniti.com "). An un-stripped value would fail downstream matching/lookup even though it's visually the same address.

## Consequence

The user-list CSV parser strips whitespace from every parsed email so the value is usable verbatim in the AssetUpload cell and in user_map lookups. Any future SKP export-format quirk discovered the same way should get the same normalize-on-parse treatment.

> [!note] Provenance
> Architecture decision **D-60** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
