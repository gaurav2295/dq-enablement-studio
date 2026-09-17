---
id: gls-cleanse-action
type: glossary
title: Cleanse Action
domain: cleanse
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:con-dq-dimensions
sources:
  - vault:dq-methodology/Cleanse Action Categorization.md
  - cleanse-canvas:docs/CONTEXT.md
  - bob-dq:CONTEXT.md
tags: [cleanse, taxonomy]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**What the remediation actually involves** once a defect is found. Three routing buckets —
**Obsolete**, **Harmonize**, **Enrich** — tracked operationally as four action types:
`Profile & Assess` (the baseline that precedes any remediation), `Obsolescence`, `Deduplication`,
`Enrichment`.

## Usage

The action answers *"what do we do about it?"*, where a [[con-dq-dimensions|dimension]] answers
*"what is wrong with it?"* — different questions, and each defect carries both.

Three origins use the term, consistently:

- **Cleanse execution** — an object's actions, defining how it gets cleansed.
- **Value/outcomes** — one of the five attributes a key issue carries.
- **The Studio** — auto-derived from rule-name keywords into the reconciliation export, always
  manually overridable.

> [!note] "Cleanse Rules" is scope, not an action
> An earlier five-value list included it. It was reclassified as an object's **scope** — how much
> cleanse work the object is admitted to — not as a unit of work. See
> [[con-cleanse-action-categorization]].
