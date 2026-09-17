---
id: ref-bulk-pipeline
type: reference
title: Bulk Rule Run
domain: studio
audience: [consultant, lead]
level: practitioner
status: review
links:
  - relates:prc-run-the-bulk-pipeline
  - relates:con-catalog-vs-bespoke-rules
  - relates:con-multi-implementation-model
  - relates:ref-local-deriver
  - relates:ref-single-rule-designer
  - relates:ref-profiler-and-audit-pages
  - relates:prc-fan-out-a-rule-per-system
  - relates:prc-audit-rule-quality
  - relates:gls-parent-group
  - relates:gls-rule-package
sources:
  - vault:studio-architecture/Studio — Bulk Pipeline (page).md
  - dq-studio:docs/Studio_Overview.md
  - coe:rewritten to usage level for consultant enablement, 2026-08-21
tags: [studio, pipeline, methodology, course]
created: 2026-08-20
updated: 2026-08-21
---

## Summary

The bulk run is the **workbook-in, package-out** side of the DQ Rules workspace. You upload a list
of rules, the Studio derives every one of them, fans each out to one implementation per source
system, and hands you back a single Rule Package ZIP ready for deployment and handover.

It is the same derivation you see one rule at a time in [[ref-single-rule-designer|the single-rule
workspace]] — applied to hundreds of rules in one pass, with a reconciliation table so you can see
what happened to each row. The click-by-click runbook is [[prc-run-the-bulk-pipeline]].

## When to use it

- Starting a sprint with a batch of catalog and bespoke rules for a domain
- Re-running a sprint after spec corrections, to regenerate a clean package
- Rolling one agreed rule set out across several source systems at once

For a single rule you are still designing, stay in the single-rule workspace — iterate on the name
and the spec there before it goes into a batch.

## What happens to your rules

1. **Import** — upload the rule workbook (xlsx, csv or json). Download the template from the page;
   every sheet in the workbook is read, so Error/Info rules and Profiling rules can sit on separate
   tabs.
2. **Derive** — rows carrying a catalog ID are built from the authoritative catalog SQL; rows
   without one are derived from your rule name by [[ref-local-deriver|Local Derive]]. See
   [[con-catalog-vs-bespoke-rules]].
3. **Fan out** — each Error/Info rule becomes **one implementation per source system**, each with
   its own DQOps id. Profiling rules are the exception: always exactly two implementations (PrfSel
   and PrfSum) under one rule id, with systems applied as a filter rather than a fan-out. See
   [[con-multi-implementation-model]].
4. **AI Enhance** *(optional)* — see below.
5. **Process and reconcile** — rules run in series and a table fills row by row with status,
   assigned ids, provenance and warning badges.
6. **Export** — the Rule Package ZIP: the deploy script, per-rule SQL, markdown specs, the report
   tracker, a batch summary with a failed-rules sheet, and per-rule unit tests.

## AI Enhance — what to turn on

| Option | What it gives you | Default |
|---|---|---|
| Rule-name enhance | Improves the rule name once per parent group; the siblings inherit it | On when AI Enhance is enabled |
| Re-derive from the enhanced name | Rebuilds the spec to match the better name (skipped for catalog rules) | On |
| AI SQL review | Per-rule AI rewrite of the generated SQL | **Off** |

> [!important] Leave AI SQL review off for routine batches
> The structural quality gate for a batch is the [[ref-profiler-and-audit-pages|Audit space]], run
> once on the finished package, not an AI pass on every rule. Turn SQL review on only for a handful
> of new or uncertain rules.

## What to expect on timing

Only the AI steps cost real time; derivation and fan-out are effectively instant. A 96-rule batch
across 4 systems runs in roughly **16–24 minutes** with the defaults. Switch AI SQL review on for
every rule and the same batch takes **an hour or more** — with no better outcome, because the audit
pass catches the structural problems in seconds.

One AI call per parent group is enough because sibling implementations differ only by system code,
alias and id — all mechanical substitutions. That granularity is correct, not a shortcut.

## Common mistakes

- **Unknown system codes in the `systems` column.** A friendly alias is translated for you with a
  yellow badge; an unrecognised code gets a "likely returns zero rows" badge. Read the badges
  before you ship — a zero-row rule looks like a clean pass.
- **Rule names not scored before upload.** The batch will derive a weak name just as happily as a
  good one. Fix names first — see [[prc-write-a-quality-rule-name]].
- **Skipping the audit.** The package is not finished until it has been through
  [[prc-audit-rule-quality]].
- **Expecting profiling rules to fan out per system.** They do not; they produce two views and use
  systems as a filter.

## Related

[[prc-run-the-bulk-pipeline]] · [[ref-single-rule-designer]] · [[ref-local-deriver]] ·
[[con-catalog-vs-bespoke-rules]] · [[con-multi-implementation-model]] ·
[[prc-fan-out-a-rule-per-system]] · [[ref-profiler-and-audit-pages]] ·
[[prc-generate-the-skp-assetupload]]
