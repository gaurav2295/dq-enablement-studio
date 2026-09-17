---
id: std-rule-description-template-profiling
type: standard
title: Rule Description Template — Profiling
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:templates/Rule Description Template — Profiling.md
tags: [template, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - contrast:std-rule-description-template
  - relates:std-implication-template
  - relates:con-profiling-concepts
  - relates:prn-profiling-has-no-pass-fail
  - relates:prc-format-an-implication
  - relates:prn-fetch-check-return
---

## What it is

Profiling-specific description shape. Same 3-section structure as
[[std-rule-description-template|Error/Info]] but **Fetch / Profile / Surface** instead of
**Fetch / Check / Return** because profiling has no pass/fail concept.

## The description body

```markdown
**1. Functional/Business Description**
Surfaces how `<attribute>` is distributed across `<segmentation>` in `<domain>`.
Reveals concentration, dispersion, and gaps in `<attribute>` usage so
governance, harmonisation, and master-data standardisation decisions are
grounded in observed populations rather than assumed ones.

**2. Specific Relevancy Criteria/Scope**
Applies to all records in `<base_table>`, profiling the `<base_field>` field
(`<attribute>`) across `<segmentation>`. Scoped to: `<filters if any>`.

**3. Profiling Analysis**
- **Fetch** <br /> Retrieve all records from `<base_table>`, joined with `<join_tables>` for descriptive context.
- **Profile** <br /> Group by `<grouping_keys>`; compute `COUNT, COUNT DISTINCT` and percentage-within-segment of each distinct value.
- **Surface** <br /> A distribution dataset — `<PrfSel_view>` carries the record-level detail and `<PrfSum_view>` carries the aggregated percentage view — showing where `<attribute>` is concentrated, scattered, or unused across `<segmentation>`.

***SKP_RULE_ID: SKP_RULE_NNNN***
```

## Why three verbs?

| Verb | What it describes |
|---|---|
| **Fetch** | The data acquisition step — which records are being read, joined for context |
| **Profile** | The aggregation step — how the values are bucketed and counted |
| **Surface** | The output step — what dataset is produced and what insight it supports |

Compare to Error rules' Fetch / Check / Return:

| Error/Info | Profiling | What changed |
|---|---|---|
| Fetch | Fetch | Same — read source records |
| **Check** | **Profile** | Error checks pass/fail; profiling computes distributions |
| **Return** | **Surface** | Error returns defects; profiling surfaces a dataset for human review |

The naming difference is on purpose — keeps the vocabulary aligned with what the rule actually
does.

## A worked example

**Rule:** *"Profile of Profit Center usage by Controlling Area"*

```markdown
**1. Functional/Business Description**
Surfaces how `Profit Center` is distributed across `Controlling Area` in
Finance / Controlling. Reveals concentration, dispersion, and gaps in
Profit Center usage so governance, harmonisation, and master-data
standardisation decisions are grounded in observed populations rather
than assumed ones.

**2. Specific Relevancy Criteria/Scope**
Applies to all records in `CEPC`, profiling the `PRCTR` field (Profit Center)
across `system (zSourceSystemID)` and `Controlling Area (KOKRS)`.

**3. Profiling Analysis**
- **Fetch** <br /> Retrieve all records from `CEPC`, joined with `CEPCT` (description) and `TKA01` (controlling area name) for descriptive context.
- **Profile** <br /> Group by `zSourceSystemID, KOKRS, PRCTR`; compute `COUNT, COUNT DISTINCT` and percentage-within-segment of each distinct value.
- **Surface** <br /> A distribution dataset — `DQ_0001_CEPC_PRCTR_PrfSel` carries the record-level detail and `DQ_0001_CEPC_PRCTR_PrfSum` carries the aggregated percentage view — showing where `Profit Center` is concentrated, scattered, or unused across system and controlling area.

***SKP_RULE_ID: SKP_RULE_0001***
```

## What NOT to write in a profiling description

Avoid pass/fail vocabulary in §1 and §3:

- ❌ "Validates that…", "Checks that…", "Mark records where…", "Defects are…"
- ✅ "Surfaces…", "Reveals…", "Group by…", "Compute…"

This isn't pedantry — auditors reading profiling rules with Error-rule vocabulary get confused
about what the rule's contract is. Clean separation keeps the reviewer's mental model intact.

## Related

- [[std-implication-template|Implication Template]]
- [[std-rule-description-template|Rule Description Template — Error and Info]]
- [[con-profiling-concepts|Profiling Concepts]]
- [[prn-profiling-has-no-pass-fail|Why Profiling Has No Pass-Fail]]
- [[prc-format-an-implication|SOP — Format an Implication]]
