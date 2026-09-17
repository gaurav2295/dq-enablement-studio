---
id: std-rule-description-template
type: standard
title: Rule Description Template — Error and Info
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:templates/Rule Description Template — Error and Info.md
tags: [template, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:std-implication-template
  - contrast:std-rule-description-template-profiling
  - relates:prc-format-an-implication
  - relates:prn-fetch-check-return
  - relates:con-rule-types
---

## What it is

The markdown spec block + description body for Error and Info rules.

## What goes where

| Section | Lives in | Source |
|---|---|---|
| Rule Identity table | Spec markdown top | Spec metadata |
| **Description** H3 | Inside spec markdown's Business Context section | `spec.description` |
| Output Fields tables | Spec markdown body | `spec.output_fields[]` grouped by section |
| Logic, Joins, Filters | Spec markdown body | `spec.logic / .joins / .filters` |
| **Implication** cell (SKP) | AssetUpload xlsx | Read from `spec.description` |

The `spec.description` is the **single source of truth** — it feeds both the markdown's
Description block and the SKP Implication cell.

## The description body — exactly this shape

```markdown
**1. Functional/Business Description**
<Why this rule matters in plain business terms. Avoid SAP field names if
you can express the intent without them — a non-technical reviewer should
get the gist. 1-2 sentences.>

**2. Specific Relevancy Criteria/Scope**
This rule applies to <records of type X> in <table(s)>, scoped to <filters>.
<1 sentence on the universe definition.>

**3. DQ Checks (Conditions)**
- **Fetch** <br /> Retrieve all records from `<PrimaryTable>`, joined with `<JoinTables>` for descriptive context.
- **Check** <br /> Mark any record where: `<error_condition_in_human_terms>`.
- **Return** <br /> Error records are <description of impact — what they break, what they prevent>.
```

For **Info** rules (not pass/fail), substitute `**3. DQ Checks (Conditions)**` with
`**3. Records Surfaced**` and change the Return line:

```markdown
**3. Records Surfaced**
- **Fetch** <br /> Retrieve all records from `<PrimaryTable>`.
- **Check** <br /> Identify records where: `<info_condition>`.
- **Return** <br /> Records matching the condition, presented for review (no defect status).
```

## A worked example

**Rule:** *"A material must have a valid base unit of measure"*

```markdown
**1. Functional/Business Description**
A material missing a base unit of measure cannot be planned, costed, or
transacted by SAP. This is a hard blocker for FERT/HALB/ROH materials
and creates downstream errors in PP, MM, and SD.

**2. Specific Relevancy Criteria/Scope**
This rule applies to all active (non-deletion-flagged) finished, semi-
finished and raw materials in MARA, across all plants, restricted to
the per-system fan-out scope.

**3. DQ Checks (Conditions)**
- **Fetch** <br /> Retrieve all records from `MARA`, joined with `MAKT` for the language-specific description.
- **Check** <br /> Mark any record where: `MEINS IS NULL OR MEINS = ''`.
- **Return** <br /> Error records are materials that cannot be processed in any of the downstream MM/PP/SD flows until a base UoM is assigned.

***SKP_RULE_ID: SKP_RULE_0042***
```

## The SKP_RULE_ID anchor — always last

The trailing `***SKP_RULE_ID: SKP_RULE_NNNN***` line:

- Stays on its own paragraph (blank line before it)
- Triple-asterisk wrapped → renders as bold + italic in both markdown viewers AND the SKP AssetUpload's markdown-to-HTML converter
- Anchors the spec back to its SKP record so reviewers can trace back

## Common mistakes

- ❌ Using H1/H2 headers (`# 1. Functional…`) instead of `**1. …**` — SKP's renderer only handles the bold form
- ❌ Skipping `<br />` after a bullet label — body text runs into the label on the same line in Excel
- ❌ Section 2 says "All records" with no scope — that's useless; always name the universe
- ❌ Section 3 Return line repeats the Check — Return should describe **impact** (what breaks), not what was checked

## Related

- [[std-implication-template|Implication Template]] — the shared shape that this and Profiling both build on
- [[std-rule-description-template-profiling|Rule Description Template — Profiling]]
- [[prc-format-an-implication|SOP — Format an Implication]]
- [[prn-fetch-check-return|Why Fetch-Check-Return]]
