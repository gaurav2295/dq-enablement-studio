---
id: std-clientref-convention
type: standard
title: ClientRef Convention
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - prereq:std-skp-rule-identifier-convention
  - relates:con-multi-implementation-model
  - relates:ref-skp-assetupload-and-tracker-flow
sources:
  - vault:dq-methodology/ClientRef Convention.md
tags: [methodology, convention, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
---

## What it is

The tracker column that holds the [[std-skp-rule-identifier-convention|SKP_RULE_NNNN]] for each
deployed rule. It is the grouping key the SKP AssetUpload exporter uses to collapse per-system
siblings back into one Rules-sheet row.

## In the tracker

`DQ_Report_Tracker.xlsx` has a column named exactly `ClientRef`. One value per tracker row,
populated with the `SKP_RULE_NNNN` for that implementation:

| ID | DQOPSID | ReportType | ClientRef |
|---|---|---|---|
| 1 | 0042 | Error | SKP_RULE_0042 |
| 2 | 0043 | Error | SKP_RULE_0042 |
| 3 | 0044 | Error | SKP_RULE_0042 |
| 4 | 0045 | Error | SKP_RULE_0042 |

All four tracker rows above share `ClientRef = SKP_RULE_0042` → the AssetUpload exporter produces
**1 Rules row + 4 Enforcements rows**.

## In the AssetUpload exporter

The exporter groups tracker rows by ClientRef:

- N rows with the same ClientRef → 1 Rules row + N Enforcements rows.
- Rows with **blank** ClientRef → skipped + warning surfaced to the user.
- Rows with an unknown ReportType → skipped + separate warning.

The grouping preserves first-seen order so the AssetUpload's `Link Id*` column is stable across
exports.

## Profiling rules now included

Pre-2026-05 the AssetUpload exporter hard-skipped Profiling rows (v1 contract). That restriction
was **lifted**: profiling rows with a populated ClientRef now flow alongside Error/Info into the
AssetUpload. Their PrfSel view routes into the "CDQ Opportunity Error Query" column; PrfSum
routes into "CDQ Error Query".

## Why "ClientRef" specifically

Historical naming — predates the formal `SKP_RULE_NNNN` scheme. The column's semantics are
exactly "shared identifier across siblings", which is what `SKP_RULE_NNNN` is, but the column
name on the tracker stays `ClientRef` for back-compat with existing tracker templates and
downstream tools.

## Common pitfalls

> [!warning]
> - **Blank ClientRef on Error/Info rows** → the rule drops out of the SKP delivery silently
>   (with a warning, but easy to miss).
> - **`SKP_RULE 0042`** (space) vs `SKP_RULE_0042` (underscore) — only the underscore form is
>   recognised.
> - **Different ClientRefs on per-system siblings** → SKP shows 4 separate Rules rows instead of
>   1 grouped row.
