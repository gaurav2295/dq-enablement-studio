---
id: prc-run-the-bulk-pipeline
type: procedure
title: Run the Bulk Pipeline
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:sops/SOP — Run the Bulk Pipeline.md
tags: [sop]
created: 2026-08-20
updated: 2026-08-21
links:
  - prereq:con-catalog-vs-bespoke-rules
  - relates:prc-derive-a-dq-rule
  - relates:prc-fan-out-a-rule-per-system
  - relates:prc-generate-the-skp-assetupload
  - relates:std-implication-template
  - relates:ref-bulk-pipeline
  - relates:ref-exporters
  - relates:qa-bulk-pipeline-reprocess-failed-rules
  - relates:qa-bulk-pipeline-warnings-review-priority
---

## Goal

End-to-end procedure for driving the Studio's bulk pipeline from an input Excel of rules to a
complete, deployable bundle.

## When to use

- Starting a new sprint with a batch of catalog + bespoke rules
- Re-running a sprint after spec corrections
- Demonstrating the pipeline to a client / new team member

## Prerequisites

- Input xlsx in the bulk import template (download from `/workspace`)
- Project YAML correct (system_aliases, naming patterns, database identifiers)
- Anthropic API key set if AI Enhance is enabled

## Input xlsx columns

| Column | Required | Notes |
|---|---|---|
| RuleName | Yes | The conceptual rule name — drives derivation |
| RuleType | Yes | Error / Info / Profiling |
| RuleSource | Yes | Catalog or Bespoke |
| CatalogID | When source=Catalog | Format `DQ_NNNN` |
| Systems | Optional | Per-row override of fan-out scope; blank = use project default |
| SKP_RULE_ID | Optional | Manual assignment; blank = auto-counter assigns |
| BusinessProcess | Optional | O2C / P2P / R2R |
| Domain | Optional | Override the auto-detected domain |

## Steps

### 1. Upload

Drop the xlsx into `/workspace`. The Studio reads and validates, then shows a "candidate rules" table
with row counts per RuleSource.

### 2. Choose options

- **AI SQL Review** (recommended for new sprints) — runs AI Enhance per rule
- **Sibling Replicate** (recommended) — when a rule has been AI-enhanced, copy the fix to siblings
- **Fan-out** — usually auto from the `Systems` column plus the project default

### 3. Process

Click **Process All Rules**. The pipeline runs in series. A status bar shows progress; the
reconciliation table populates as each rule completes.

### 4. Review the reconciliation

Sortable table with:

- Status (Draft / SQL Generated / AI Enhanced / AI Replicated from Sibling / Failed)
- Rule name + DQOps ID
- Provenance (Catalog / Bespoke + AI / Local)
- Warnings (unknown tables, missing PKs, stale comments, validator findings)
- Per-rule SQL preview link

### 5. Export the bundle

Click **Download Bulk Export ZIP**. Contains:

- `markdown/` — one `.md` per spec
- `sql/` — one `.sql` per implementation (OptSel + RptSel concatenated)
- `specs/` — one `.json` per spec (machine-readable for downstream tools)
- `Reconciliation_Summary.xlsx` — the table from step 4

### 6. Hand off

- SQL — to the DBA for deployment via the Studio's deploy script bundler
  ([[ref-exporters|Studio — Exporters]])
- Markdown specs — to SharePoint / Confluence for SME review
- Specs zip plus tracker xlsx — into the
  [[prc-generate-the-skp-assetupload|Generate the SKP AssetUpload]] pipeline

## Verification

- All rules show status "SQL Generated" or "AI Enhanced" (not "Failed")
- No row has a red warning chip
- Per-system fan-out scope matches the project YAML's `system_aliases`
- Spot-check 3 random rules' markdown — descriptions follow
  [[std-implication-template|Implication Template]]

**Additional verification (before export):**
- **Check one generated SQL file:** Open a `.sql` file from the bulk export and verify:
  - Header block is present (Rule ID, view name, target platform)
  - All five output field sections are present and in order
  - `zIsErrorFlag` is INTEGER 1/0, never text
  - zSourceSystemID filter is correct for the system
- **Check one fanned-out sibling:** If you fanned out a rule across multiple systems, verify:
  - View names include correct system aliases (e.g., `_P02_`, `_P03_`)
  - Each sibling has a unique DQOps ID
  - The `zSourceSystemID` filter matches the system code (not the alias)

## Common pitfalls

- **Failed rules with "AI Derive failed"** — API key not set, or rate-limited. Retry with delay.
- **Rule fanned out to wrong system** — the `Systems` column on the xlsx overrides the project
  default; check for stale per-row overrides.
- **SKP_RULE_NNNN collision** — manual assignment in the xlsx clashes with an existing ID. The
  auto-counter walks around collisions; manual assignments don't.
- **Bulk-zip too large** — 24 rules with full SQL + markdown is about 3 MB; if your zip is 30 MB,
  something duplicated. Re-run.

## Related

- [[prc-derive-a-dq-rule|Derive a DQ Rule (single rule)]]
- [[prc-fan-out-a-rule-per-system|Fan Out a Rule Per System]]
- [[prc-generate-the-skp-assetupload|Generate the SKP AssetUpload]]
- [[ref-bulk-pipeline|Studio — Bulk Pipeline]]
