---
id: std-skp-rule-identifier-convention
type: standard
title: SKP_RULE Identifier Convention
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:dq-methodology/SKP_RULE Identifier Convention.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:con-multi-implementation-model
  - relates:std-clientref-convention
  - relates:std-implication-template
  - relates:con-rule-types
  - relates:ref-skp-assetupload-and-tracker-flow
---

## The convention

The shared identifier that groups all per-system siblings of one conceptual rule.

## Format

```
SKP_RULE_NNNN
```

- Literal `SKP_RULE_` prefix (underscore between RULE and the number)
- Zero-padded integer — typically 4 digits (`SKP_RULE_0042`); 5 digits when needed
  (`SKP_RULE_12345`)
- One per **conceptual rule**, shared across N per-system implementations

## What it identifies

A "conceptual rule" — the business intent like *"A material must have a base UoM"* — independent
of which systems it deploys to. Siblings:

| `rule_id` (DQOps) | `system_filter` | `system_alias` | `skp_rule_id` (shared) |
|---|---|---|---|
| 0042 | SRCECCZ02100 | P02 | **SKP_RULE_0042** |
| 0043 | SRCECCZ03100 | P03 | **SKP_RULE_0042** |
| 0044 | SRCECCZ06100 | P06 | **SKP_RULE_0042** |
| 0045 | SRCS4SG2100  | PG3 | **SKP_RULE_0042** |

Four DQOps `rule_id`s, one SKP_RULE_NNNN. Each impl gets its own deployment record + tracker
row; SKP groups them on the AssetUpload Rules sheet. See
[[con-multi-implementation-model|Multi-Implementation Model]] for why the split happens at all.

## Where it appears

- **`spec.skp_rule_id`** — set on every spec the Studio derives
- **`spec.parent_rule_key`** — defaults to `skp_rule_id` (allows future restructuring)
- **Tracker `ClientRef` column** — the deployment-side groupby key
- **Spec markdown header** — `| SKP Rule ID | SKP_RULE_0042 |`
- **Implication suffix** — every rule's Implication ends with `***SKP_RULE_ID: SKP_RULE_0042***`
- **SKP AssetUpload** — Rules sheet `link_id` resolves SKP_RULE_NNNN groupings

## Auto-counter

The Studio's bulk processor auto-assigns SKP_RULE_NNNN to new rules. It:
- Walks forward from the starting point looking for the lowest integer not already in use
- Honours user-assigned high numbers — if you manually set `SKP_RULE_9999`, the counter keeps
  handing out sequentials around it rather than jumping past
- Always emits 4-digit zero-padded form

## Profiling rules

Profiling rules also carry an SKP_RULE_NNNN. They have only 2 implementations (PrfSel + PrfSum)
but the grouping mechanism is the same. See
[[con-rule-types|Rule Types — Error, Info, Profiling]].

## Related

- [[con-multi-implementation-model|Multi-Implementation Model]]
- [[std-clientref-convention|ClientRef Convention]]
- [[std-implication-template|Implication Template]] — the SKP_RULE_ID suffix on every Implication
