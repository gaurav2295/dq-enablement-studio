---
id: std-implication-template
type: standard
title: Implication Template
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:templates/Implication Template.md
tags: [template, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:std-rule-description-template
  - relates:std-rule-description-template-profiling
  - relates:prc-format-an-implication
  - relates:prn-fetch-check-return
  - relates:std-skp-rule-identifier-convention
---

## What it is

The exact 3-section shape every DQ rule's **description / Implication** must follow. Used by:

- The bulk markdown exporter as the spec's Description block
- The SKP AssetUpload exporter as the Implication column (Rules sheet)
- The catalog deriver to render new specs from catalog entries

## Error / Info rule shape

```markdown
**1. Functional/Business Description**
<Why this rule matters — the business impact of records that violate it.
What risk it creates downstream. 1-2 sentences.>

**2. Specific Relevancy Criteria/Scope**
<What records the rule applies to. Tables involved. Universe definition.
1 sentence.>

**3. DQ Checks (Conditions)**
- **Fetch** <br /> Retrieve all records from <tables>, joined with <join tables> for descriptive context.
- **Check** <br /> Mark any record where: <error_condition>
- **Return** <br /> Error records are <description of defect impact>.

***SKP_RULE_ID: SKP_RULE_NNNN***
```

## Profiling rule shape

Profiling has no pass/fail concept, so substitute **Fetch / Profile / Surface** in §3:

```markdown
**1. Functional/Business Description**
<Why this profile matters — what business decision it supports. What
governance / mastering / standardisation question it informs. 1-2 sentences.>

**2. Specific Relevancy Criteria/Scope**
Applies to all records in <base_table>, profiling the <base_field> field
(<attribute>) across <segmentation>. Scoped to: <filters if any>.

**3. Profiling Analysis**
- **Fetch** <br /> Retrieve all records from <base_table>, joined with <join_tables> for descriptive context.
- **Profile** <br /> Group by <grouping_keys>; compute COUNT, COUNT DISTINCT and percentage-within-segment of each distinct value.
- **Surface** <br /> A distribution dataset — `<PrfSel_view>` carries the record-level detail and `<PrfSum_view>` carries the aggregated percentage view — showing where <attribute> is concentrated, scattered, or unused across <segmentation>.

***SKP_RULE_ID: SKP_RULE_NNNN***
```

## Format details

- **Section headers** wrapped in `**1. …**` (bold) — exactly that numbering
- **Bullet labels** wrapped in `**Fetch**` (bold)
- **`<br />` after the label** — this renders as a line break inside Excel cells AND inside SKP's markdown-to-HTML converter. Without it, the label runs into the body text on the same line
- **SKP_RULE_ID anchor** at the bottom in `***bold-italic***` — SKP picks this up as the canonical reference

## Worked example — Error rule

```markdown
**1. Functional/Business Description**
A material missing a base unit of measure cannot be planned, costed, or
transacted by SAP. This is a hard blocker for FERT / HALB / ROH materials
and creates downstream errors in PP, MM, and SD.

**2. Specific Relevancy Criteria/Scope**
This rule applies to all active (non-deletion-flagged) materials in MARA,
across all plants, restricted to the per-system fan-out scope.

**3. DQ Checks (Conditions)**
- **Fetch** <br /> Retrieve all records from `MARA`, joined with `MAKT` for the language-specific description.
- **Check** <br /> Mark any record where: `MEINS IS NULL OR MEINS = ''`.
- **Return** <br /> Error records are materials that cannot be processed in any of the downstream MM/PP/SD flows until a base UoM is assigned.

***SKP_RULE_ID: SKP_RULE_0042***
```

## Worked example — Profiling rule

```markdown
**1. Functional/Business Description**
Surfaces how Profit Center is distributed across Controlling Area in Finance.
Reveals concentration, dispersion, and gaps in profit center usage so governance,
harmonisation, and master-data standardisation decisions are grounded in
observed populations rather than assumed ones.

**2. Specific Relevancy Criteria/Scope**
Applies to all records in `CEPC`, profiling the `PRCTR` field (Profit Center)
across system (zSourceSystemID).

**3. Profiling Analysis**
- **Fetch** <br /> Retrieve all records from `CEPC`, joined with `CEPCT` (description) and `TKA01` (controlling area name) for descriptive context.
- **Profile** <br /> Group by `zSourceSystemID, CEPC.KOKRS, CEPC.PRCTR`; compute COUNT, COUNT DISTINCT and percentage-within-segment of each distinct value.
- **Surface** <br /> A distribution dataset — `DQ_0001_CEPC_PRCTR_PrfSel` carries the record-level detail and `DQ_0001_CEPC_PRCTR_PrfSum` carries the aggregated percentage view — showing where Profit Center is concentrated, scattered, or unused across system.

***SKP_RULE_ID: SKP_RULE_0001***
```

## Common mistakes

- ❌ Omitting `<br />` after the label — body text collapses onto the same line in Excel
- ❌ Numbering changes (`### 1.` instead of `**1.**`) — SKP's markdown→HTML converter only knows the bold form
- ❌ Skipping section 2 because "it's obvious" — auditors fail rules without explicit scope statements
- ❌ Using `Check / Validate / Verify` for profiling rules — those imply pass/fail; use Fetch / Profile / Surface

## Related

- [[std-rule-description-template|Rule Description Template — Error and Info]]
- [[std-rule-description-template-profiling|Rule Description Template — Profiling]]
- [[prc-format-an-implication|SOP — Format an Implication]]
- [[prn-fetch-check-return|Why Fetch-Check-Return]]
