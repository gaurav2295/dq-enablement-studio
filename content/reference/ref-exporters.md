---
id: ref-exporters
type: reference
title: Studio Exports and Deliverables
domain: studio
audience: [consultant, lead]
level: practitioner
status: review
links:
  - relates:ref-skp-assetupload-and-tracker-flow
  - relates:prc-run-the-bulk-pipeline
  - relates:prc-generate-the-skp-assetupload
  - relates:prc-audit-rule-quality
  - relates:std-view-naming-patterns
  - relates:std-clientref-convention
  - relates:gls-batch-summary
  - relates:gls-rule-package
  - relates:gls-tracker
sources:
  - vault:studio-architecture/Studio — Exporters (Tracker-Deploy-Audit-Dashboard).md
  - coe:usage rewrite for consultants
tags: [studio, course, export, methodology, sap]
created: 2026-08-20
updated: 2026-08-21
---

## What it is

Everything you hand to a client comes out of the Studio as a **downloaded file**. Deriving and
generating happen inside the app; exporting is the last mile that turns a finished batch into
deliverables. This unit is the catalogue: what each export is, when you take it, and what to
check before it leaves your laptop.

## What you can download

| Export | File | What it is for |
|---|---|---|
| Deploy script | `DQ_Rule_Deploy.sql` | One bundled script the customer runs to create every rule view in the batch, in the right order. Safe to re-run — it replaces rather than errors. |
| Report Tracker | `DQ_Report_Tracker.xlsx` | One row per deployed view. This is the spine: the audit and the SKP upload both key off it. |
| Batch summary | `Batch_Summary.xlsx` | Two sheets — **Reconciliation** (what was produced) and **Failed Rules** (what did not make it). Your evidence that a partial batch is accounted for. |
| Rule package | `DQ_Rule_Package.zip` | Everything above plus per-rule SQL, markdown specs and unit tests, zipped. The normal end-of-sprint handover. |
| Per-rule SQL | one `.sql` per rule | For reviewing or shipping a single rule. |
| Rule spreadsheet | rule export `.xlsx` | Import-shaped: it round-trips back into the bulk importer, so you can edit rules in Excel and reload them. |
| Rule markdown | `DQ_<id>_<name>.md` | The human-readable spec for a rule, and the format the rule repository stores. |
| Audit report | audit `.xlsx` | The audit findings for the batch, sorted by severity. |
| Profiler dashboard | self-contained `.html` | Profiling results as a single HTML file that opens on any laptop — no server, no internet. |
| SKP AssetUpload | `.xlsx` or `.json` | The BulkImport workbook for the client's SKP environment. See ref-skp-assetupload-and-tracker-flow. |

## When to take which

- **During a sprint** — per-rule SQL and markdown while you iterate on individual rules.
- **After a bulk run** — the rule package zip. It contains the deploy script, tracker and batch
  summary together, which is what the client's DBA and your own QA both need.
- **After the audit** — the audit report, attached to the QA record for the sprint.
- **After profiling** — the dashboard HTML, which is genuinely client-shareable as-is.
- **At integrate time** — the AssetUpload workbook, built from the tracker. Steps live in
  [[prc-generate-the-skp-assetupload]].

## What to expect

- Exports land in your **Downloads** folder. They are never written back into a repository, and
  they are not stored in the app — if you need them again, export again.
- Session work is held in memory. Close or restart the Studio and an unexported batch is gone.
  Export before you walk away.
- View names in every export use the production **system alias** (for example `P02`), not the raw
  source code. Deviating breaks the joins between the tracker, the audit and SKP — see
  [[std-view-naming-patterns]].
- The 4-digit rule id inside each view name must match the rule id in the SQL header banner. If it
  drifts, the audit reports it as a high-severity finding rather than failing silently.
- A batch with failures still exports. Failed rules are listed on their own sheet, not dropped.

## Common mistakes

- **Shipping the deploy script without the tracker.** The client can create the views, but nobody
  can reconcile or upload them afterwards.
- **Renaming views by hand** to make them read nicer. Every downstream join is on the generated
  name.
- **Ignoring the Failed Rules sheet** because the batch "looked fine". Check it every time; it is
  the difference between a partial batch and an unnoticed gap.
- **Exporting before the audit.** Run [[prc-audit-rule-quality]] first, fix, then export the
  package you intend to hand over.
- **Losing the batch to a restart.** Nothing is persisted between sessions except the SKP user
  map, so export as you go.

## Related

[[prc-run-the-bulk-pipeline]] · [[prc-generate-the-skp-assetupload]] · [[prc-audit-rule-quality]] ·
[[ref-skp-assetupload-and-tracker-flow]] · [[std-view-naming-patterns]] ·
[[std-clientref-convention]] · [[gls-tracker]] · [[gls-batch-summary]] · [[gls-rule-package]]
