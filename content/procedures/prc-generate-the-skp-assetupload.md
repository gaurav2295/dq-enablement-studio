---
id: prc-generate-the-skp-assetupload
type: procedure
title: Generate the SKP AssetUpload
domain: platform
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:sops/SOP — Generate the SKP AssetUpload.md
tags: [sop]
created: 2026-08-20
updated: 2026-08-21
links:
  - prereq:prc-run-the-bulk-pipeline
  - relates:std-clientref-convention
  - relates:std-skp-rule-identifier-convention
  - relates:std-implication-template
  - relates:prc-audit-rule-quality
  - relates:prc-format-an-implication
  - relates:ref-skp-assetupload-and-tracker-flow
---

## Goal

Take the sprint's DQ Report Tracker plus the bulk-export specs zip and produce the SKP
BulkImport workbook, ready for upload to the client's SKP environment.

## When to use

End of sprint, after the bulk pipeline has run and specs are finalised.

## Prerequisites

- DQ Report Tracker `.xlsx` with the `ClientRef` column populated on every Error/Info/Profiling
  row that should ship
- Specs zip from the bulk pipeline (contains `markdown/` and `specs/`)
- The project's SKP configuration in the YAML (datastore, enf_method, default priority)

## Steps

### 1. Open /ship (SKP tab)

The Studio's SKP page. Two uploads are required:

- DQ Report Tracker (`.xlsx`)
- Specs zip (`.zip`)

Optionally a user_map `.xlsx` that maps tracker `AssignedTo` names to email addresses, for the
Implementation Implementer column.

### 2. Click Generate

The exporter:

- Reads the tracker to build tracker rows
- Reads the specs zip and indexes specs by DQOps ID and rule name
- Groups tracker rows by ClientRef into one Rules row plus N Enforcements rows
- Composes each Implication from the matching spec's `description`
- Derives categories per the project's category configuration
- Resolves Implementer name to email via the user_map

**Visual Mapping: Tracker Rows → Rules & Enforcements Sheets**

```
INPUT: DQ Report Tracker (Excerpt)
┌──────────┬───────────┬──────────┬─────────────┬──────────┐
│ ClientRef│ DQOps ID  │ View Name│ RuleType    │ AsgnTo   │
├──────────┼───────────┼──────────┼─────────────┼──────────┤
│SKP_089   │ 0001      │ DQ_..P02 │ Error       │ Alice    │
│SKP_089   │ 0002      │ DQ_..P03 │ Error       │ Bob      │
│SKP_089   │ 0003      │ DQ_..P06 │ Error       │ Charlie  │
│SKP_090   │ 0004      │ DQ_..P02 │ Profiling   │ Alice    │
│SKP_090   │ 0005      │ DQ_..P03 │ Profiling   │ Bob      │
└──────────┴───────────┴──────────┴─────────────┴──────────┘

           │ (Read spec descriptions from markdown/)
           │
           v
INPUT: Specs Zip (Index by DQOps ID)
┌──────────┬──────────────────────────────────┐
│ DQOps ID │ Description (Implication)        │
├──────────┼──────────────────────────────────┤
│ 0001     │ A material must have activity... │
│ 0002     │ A material must have activity... │
│ 0003     │ A material must have activity... │
│ 0004     │ Material usage distribution...   │
│ 0005     │ Material usage distribution...   │
└──────────┴──────────────────────────────────┘

           │ (Group by ClientRef)
           │
           v
OUTPUT: Rules Sheet (One row per ClientRef/SKP_RULE_NNNN)
┌──────────┬─────────────────────────────────────┬──────────┐
│ ClientRef│ Rule Name / Implication             │ Category │
├──────────┼─────────────────────────────────────┼──────────┤
│SKP_089   │ Material Activity (A material must..│ Accuracy │
│SKP_090   │ Material Usage (Material usage dist│ Complete │
└──────────┴─────────────────────────────────────┴──────────┘

           AND
           
OUTPUT: Enforcements Sheet (One row per tracker row/DQOps ID)
┌──────────┬──────────┬─────────────┬──────────────┬──────────┐
│ ClientRef│ DQOps ID │ Alias (P02) │ Error Query  │ Impl By  │
├──────────┼──────────┼─────────────┼──────────────┼──────────┤
│SKP_089   │ 0001     │ P02         │ DQ_..RptSel  │ alice@.. │
│SKP_089   │ 0002     │ P03         │ DQ_..RptSel  │ bob@..   │
│SKP_089   │ 0003     │ P06         │ DQ_..RptSel  │ charlie@ │
│SKP_090   │ 0004     │ P02         │ DQ_..PrfSum  │ alice@.. │
│SKP_090   │ 0005     │ P03         │ DQ_..PrfSum  │ bob@..   │
└──────────┴──────────┴─────────────┴──────────────┴──────────┘

KEY RELATIONSHIPS:
─────────────────
✅ Rules sheet: Unique ClientRefs (SKP_089, SKP_090) — one conceptual rule per ClientRef
✅ Enforcements sheet: All tracker rows — one implementation per system (P02, P03, P06)
✅ DQOps ID: Links each enforcement to its spec for pulling Implication, view names
✅ ClientRef (SKP_RULE_NNNN): Shared across all systems for the same rule concept
```

### 3. Read the summary line

Format:

```
✓ AssetUpload.xlsx downloaded
Rules: N | Enforcements: M | Categories: K
Specs zip: P spec(s) parsed, Q matched to tracker rows by DQOPSID
User map: U name→email mapping(s) loaded
<Warnings>
```

What to look for:

- **Rules count > 0** — if zero, see [[prc-audit-rule-quality|Audit Rule Quality]]; usually a
  ClientRef gap or a v1-contract issue
- **matched to tracker rows by DQOPSID = P** (all specs matched) — if Q < P, some specs don't
  have a corresponding tracker row (extra specs uploaded, or DQOps ID drift)
- **Warnings section** — surface all warnings to the user

### 4. Open the AssetUpload xlsx

Verify:

- Rules sheet: one row per SKP_RULE_NNNN, Implication populated, Rule Type carried correctly
- Enforcements sheet: one row per tracker implementation; Implementation CDQ Error Query and
  CDQ Opportunity Error Query columns point at the right views
  - Error/Info: Error = RptSel, Opportunity = OptSel
  - Profiling: Error = PrfSum, Opportunity = PrfSel
- Categories sheet: 3 per Rule (or whatever the project configures)
- Implementations / SMEs: typically v1 leaves these light

### 5. Final review

- Open Excel, set column widths, confirm no `#REF!` or truncated text
- Implementations: confirm the Implementer column shows email addresses, not raw names
  (otherwise SKP rejects on import)
- Implication cell: confirm bold and line breaks render in Excel's wrap-text mode

### 6. Hand off

Upload to the client's SKP environment via their BulkImport flow.

## Verification

- Rules count equals the unique ClientRefs from the tracker (minus blank-ClientRef skips)
- Enforcements count equals total tracker rows minus skipped rows
- Categories count equals Rules × N (where N is the project's category dimensions, usually 3)
- Spot-check 3 random Implication cells — they render the canonical Fetch/Check/Return shape

## Common pitfalls

- **Rules: 0** — all tracker rows were Profiling and the Studio is older than 2026-05 (the v1
  contract excluded profiling). Update to a current build of the Studio.
- **Implications empty** — spec markdowns don't have a `### Description` block. Use
  [[prc-format-an-implication|Format an Implication]], or ask the Studio team to re-run the
  implication-enrichment step if specs were generated pre-2026-05.
- **Implementer column shows names not emails** — the user_map xlsx wasn't uploaded, or names
  don't match. SKP silently rejects non-email values as "user not found".
- **PrfSum view name missing** — profiling rules need the PrfSum view derived from PrfSel via a
  suffix swap. Confirm you're on a current build of the Studio.

## Related

- [[std-clientref-convention|ClientRef Convention]]
- [[std-skp-rule-identifier-convention|SKP_RULE Identifier Convention]]
- [[std-implication-template|Implication Template]]
- [[prc-audit-rule-quality|Audit Rule Quality]]
- [[prc-run-the-bulk-pipeline|Run the Bulk Pipeline]]
- [[ref-skp-assetupload-and-tracker-flow|SKP AssetUpload & Tracker Flow]] — what the flow does,
  and what to check in the output
