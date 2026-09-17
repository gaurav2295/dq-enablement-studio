---
id: con-cleanse-action-categorization
type: concept
title: Cleanse Action Categorization
domain: cleanse
audience: [consultant]
level: practitioner
status: deprecated
links:
  - relates:con-dq-dimensions
  - relates:con-catalog-vs-bespoke-rules
  - relates:con-cleanse-execution-model
  - relates:con-cleanse-task-anatomy
  - relates:ref-cleanse-process-areas
  - relates:gls-cleanse-action
sources:
  - vault:dq-methodology/Cleanse Action Categorization.md
  - cleanse-canvas:docs/DATA-MODEL.md
  - cleanse-canvas:docs/CONTEXT.md
tags: [methodology, dimension]
created: 2026-08-20
updated: 2026-08-20
---

## The three buckets

When a defect is found, what does the remediation actually involve?

| Action | What it means | Typical rules |
|---|---|---|
| **Obsolete** | Records that should be **removed** — unused / superseded / dead | "Customer with no orders in 5 years", "Material with deletion flag and zero stock" |
| **Harmonize** | Records that should be **deduplicated or unified** — overlap, conflict, multi-source variants | "Customer duplicates by STCEG", "Material variants with the same EAN" |
| **Enrich** | Records that should be **completed or standardized** — missing values, inconsistent formats, non-conformant data | "Material missing base UoM", "Customer with non-EU VAT format" |

## Why this categorization

Maps to the **three remediation workflows** the client typically runs:

1. **Obsolete → Cleanup project** — archive, block, soft-delete. Often batch-mode; one decision
   affects many records.
2. **Harmonize → Mastering project** — merge records, pick survivor, redirect references.
   Per-record decisions; often longer-running.
3. **Enrich → Data entry / lookup project** — fill missing values, conform formats. Per-field
   decisions; often parallel to BAU operations.

A defect tagged for Obsolete remediation gets routed to a different team / process than one
tagged for Enrichment.

## How the Studio derives it

Heuristics in the bulk reconciliation export:

- Keywords like *unused*, *not used*, *deleted*, *obsolete* → **Obsolete**.
- Keywords like *duplicate*, *deduplicate*, *unique*, *one per* → **Harmonize**.
- Keywords like *missing*, *populated*, *standardize*, *complete*, *valid format* → **Enrich**.

Manual override is always allowed. The auto-derivation reports its confidence in the
reconciliation Excel.

## Relationship to dimensions

| Cleanse action | Typical [[con-dq-dimensions|dimensions]] |
|---|---|
| Obsolete | Timeliness, Uniqueness |
| Harmonize | Uniqueness, Consistency |
| Enrich | Completeness, Accuracy, Conformity, Integrity |

Most Enrich actions sit under Completeness; most Harmonize under Uniqueness. But the dimension
answers "what's wrong with the data?" while the cleanse action answers "what do we do about it?"
— distinct questions.

## Operational vocabulary — the tracked action types

Execution tooling built on this categorization tracks actions with a **four-value vocabulary**
rather than the three buckets above, because it needs an explicit place for the assessment work
that precedes any remediation decision:

| Tracked action type | Maps to the bucket above |
|---|---|
| **Profile & Assess** | *(not a remediation bucket — precedes all three)* |
| **Obsolescence** | Obsolete |
| **Deduplication** | Harmonize |
| **Enrichment** | Enrich |

`Profile & Assess` is applied to every in-scope object as a baseline — it is how an object
*earns* a subsequent Obsolescence/Deduplication/Enrichment action, not a remediation itself.
The naming difference (Obsolescence/Deduplication vs. Obsolete/Harmonize) is terminology
variance between the routing-oriented framing above and an execution-tracking tool's field
names, not a substantive disagreement — both describe the same three remediation ideas.

> [!warning] Do not conflate action with scope.
> Earlier framings of this vocabulary listed a **fifth** action, "Cleanse Rules" (as in
> "Cleanse Rules, Reports & Pages"). That value was deliberately reclassified as an object's
> **scope** — *how much* cleanse work the object is admitted to at all — not as an action.
> Scope decides whether an object gets remediation work; `actionType` rows are the units of
> work once scope has admitted it. A four-value action vocabulary plus a separate scope
> attribute is the current model; a five-value action list is the superseded one.

Two further attributes travel with a tracked action, independent of its type — see
[[con-cleanse-execution-model]] for the fuller model:

- **`method`** (`Source` | `Staged`) — *where* the action is executed, not what kind it is.
- **`applicable`** (`yes` | `tbc`) — whether the action-type genuinely applies to a given
  object is sometimes still pending confirmation against a per-object execution guideline; no
  execution task should be started against a `tbc` action until it is confirmed.
