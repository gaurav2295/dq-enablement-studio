---
id: con-time-based-filters
type: concept
title: Time-Based Filters
domain: rule-design
audience: [consultant]
level: practitioner
status: deprecated
sources:
  - vault:dq-methodology/Time-Based Filters.md
tags: [methodology, filters, scope]
created: 2026-08-20
updated: 2026-08-20
links:
  - contrast:con-deletion-flags-vs-status-fields
  - relates:ref-sap-deletion-flags-vs-status-fields
  - relates:ref-deletion-flag-resolver
  - relates:con-filter-presets
  - relates:std-ziserrorflag-convention
  - relates:gls-activity-context
---

## Definition

A **time-based filter** is a scope filter that restricts a rule's record set by date/time (e.g.
document date within a window) — a distinct filter category from deletion exclusions and
activity/status filters.

## Why it exists

Master data carries a deletion flag (`LVORM` / `LOEVM` / `LOEKZ`) you exclude on. **Transactional
documents** — sales (`VBAK`/`VBAP`), deliveries (`LIKP`/`LIPS`) — have **no master-data deletion
flag**; rejection/closure is expressed differently (`ABGRU`, status). To keep a rule's population
relevant you instead scope by **time**: e.g. only documents created/changed within the last *N*
months, or on/after a cutoff date.

## The three filter categories

| Category | Mechanism (WHERE) | Example |
|---|---|---|
| Deletion exclusion | `<flag> <> 'X'` | `MARA.LVORM <> 'X'` |
| Activity / status (inclusion) | status in the active set | `MARC.MMSTA NOT IN (<blocked>)` |
| Time-based (scope) | date/time in a window | `VBAK.ERDAT >= '<cutoff>'` or `>= DATEADD(month, -N, GETDATE())` |

## When to use

- The table has **no deletion flag** (transactional docs) — use time-based scope instead of (or
  alongside) `ABGRU`/status.
- A rule should only assess **recent / in-scope** records — avoid flagging historical or closed
  documents.

## Conventions

- Common SAP date fields: `ERDAT` (created on), `AEDAT` (changed on), `AUDAT` (document date),
  `BUDAT` (posting date).
- Express the window relatively (`DATEADD`) or as an explicit project **cutoff parameter**;
  surface the cutoff in project config, don't hardcode it.
- A time-based filter is a **scope/inclusion** restriction (lives in the WHERE), **not** the
  error condition — the defect logic stays in the `zIsErrorFlag` CASE.

## Implementation status

> [!tip] Implementation status
> Time-based filters are shipped in the Studio: the generator emits the window in the WHERE
> clause as a scope/inclusion restriction, never the error condition. The no-flag handling is
> also correct: the deletion-flag resolver no longer assigns a `LOEVM` flag to sales documents —
> no-flag tables (`VBAK`/`VBAP`/`LIKP`/`LIPS`) are excluded, so a rule on those tables skips the
> deletion-flag exclusion instead of silently mis-filtering.

## Related

- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]] · [[ref-sap-deletion-flags-vs-status-fields|SAP Deletion Flags vs Status Fields]]
- [[ref-deletion-flag-resolver|Deletion Flag Resolver (3-tier)]] · [[con-filter-presets|Filter Presets]]
