---
id: ref-skp-assetupload-and-tracker-flow
type: reference
title: SKP AssetUpload & Tracker Flow
domain: platform
audience: [consultant, lead]
level: practitioner
status: review
links:
  - relates:prc-generate-the-skp-assetupload
  - relates:std-clientref-convention
  - relates:std-skp-rule-identifier-convention
  - relates:prc-run-the-bulk-pipeline
  - relates:ref-exporters
  - relates:prn-fetch-check-return
  - relates:gls-tracker
sources:
  - vault:studio-architecture/Studio — SKP AssetUpload & Tracker Flow.md
  - coe:usage rewrite for consultants
tags: [studio, app, methodology, course, skp]
created: 2026-08-20
updated: 2026-08-21
---

## What it is

The SKP tab on the Studio's **Ship** space turns a finished sprint's `DQ_Report_Tracker.xlsx`
into the workbook the client's Syniti Knowledge Platform expects for BulkImport. It is entirely
file-in / file-out: you upload files, you download a file, and nothing talks to SKP. That means it
works offline, needs no client credentials, and can be re-run as often as you like.

This is the *Integrate* step at the end of the methodology. The bulk pipeline fans one conceptual
rule out into many per-system implementations; this flow puts them back together for upload.
Hands-on steps are in [[prc-generate-the-skp-assetupload]].

## What you upload, what you get

| Input | Required | What it contributes |
|---|---|---|
| `DQ_Report_Tracker.xlsx` | Yes | The source rows — one per implementation, with `ClientRef` filled in |
| Specs `.zip` from the bulk export | Optional but usual | Supplies the Implication text and view names the tracker does not carry |
| User list `.xlsx` (name → email) | Optional | Turns the tracker's assignee name into the email address SKP requires |

You download an AssetUpload `.xlsx` (or `.json`) with three sheets: **Rules**, **Enforcements**
and **Categories**.

## The grouping rule — the thing to understand

Tracker rows are grouped by **`ClientRef`** — the `SKP_RULE_NNNN` value. Each distinct `ClientRef`
becomes **one row on the Rules sheet**; every tracker row behind it becomes **one row on the
Enforcements sheet**. Four per-system siblings sharing `SKP_RULE_0042` therefore collapse into one
Rules row and four Enforcements rows. Categories are added per rule, usually three, from the
project's configuration.

So the arithmetic you check afterwards is:

- **Rules** = number of unique, non-blank `ClientRef` values
- **Enforcements** = total tracker rows, minus any that were skipped

A blank `ClientRef` means the row is skipped entirely — it is the single most common reason a rule
you expected to ship is missing from the workbook. See [[std-clientref-convention]] and
[[std-skp-rule-identifier-convention]].

## What gets filled in for you

Enforcement settings come from the project configuration, so you do not type them per rule:

| Setting | Typical default |
|---|---|
| Datastore | `WRKDQ` |
| Enforcement type | `DataQuality` |
| Enforcement method | `SynitiCloudDQ` |
| State / status | `Published` / `Enforced` |
| Priority | `High` |
| Roll up to DQ score | Yes |

If a client wants different defaults, change them in the project configuration once rather than
editing the workbook after export.

## What to expect

- The name → email map you upload is **remembered** between sessions. Everything else about the
  SKP session is not, so finish the export in one sitting.
- Profiling rows are included in current versions and map their Error and Opportunity queries to
  the summary and detail profiling views. Older builds skipped profiling entirely — if your Rules
  count comes back as zero on an all-profiling tracker, that is the reason.
- Implication text renders differently by format: the `.json` output renders bold and line breaks,
  the `.xlsx` output shows the same markers as literal text in the cell. Both are acceptable to
  SKP; the workbook is the normal choice.
- Implications use bold numbering for the Fetch / Check / Return steps, never headings — SKP's
  renderer handles bold and ignores headings. See [[prn-fetch-check-return]].

## Common mistakes

- **Implementer shows names, not emails.** SKP silently rejects a name as "user not found". Upload
  the user list, and check the names match the tracker spelling exactly.
- **Blank `ClientRef` rows.** They vanish without an error. Reconcile the Rules count against your
  own list of rules before uploading.
- **Editing the workbook by hand** after export. Re-run the generator instead, so the tracker
  stays the single source of truth.
- **Uploading a specs zip from a different batch.** Implications then attach to the wrong rules, or
  come back empty.

## Related

[[prc-generate-the-skp-assetupload]] · [[std-clientref-convention]] ·
[[std-skp-rule-identifier-convention]] · [[prc-run-the-bulk-pipeline]] · [[ref-exporters]] ·
[[prn-fetch-check-return]] · [[gls-tracker]]
