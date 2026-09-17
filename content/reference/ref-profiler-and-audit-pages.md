---
id: ref-profiler-and-audit-pages
type: reference
title: Profile & Audit Spaces
domain: studio
audience: [consultant, lead]
level: practitioner
status: review
links:
  - relates:prc-generate-a-profile-bundle
  - relates:prc-audit-rule-quality
  - relates:con-profiling-concepts
  - relates:con-filter-presets
  - relates:ref-bulk-pipeline
  - relates:ref-home-page
  - relates:gls-schema-profile
  - relates:gls-dq-score
sources:
  - vault:studio-architecture/Studio — Profiler & Audit Pages.md
  - coe:rewritten to usage level for consultant enablement, 2026-08-21
tags: [studio, profiling, audit, sap, course]
created: 2026-08-20
updated: 2026-08-21
---

## Summary

Two spaces bookend the rule lifecycle. **Profile** runs before any rule exists: it produces a
script you run in the client's environment, and turns the result into a dashboard showing what is
actually in every field. **Audit** runs after a package is built: you feed the deployed rules back
in and it tells you what is wrong with them before the client does.

Same principle at both ends — evidence, not assumption. Profile stops you writing rules against
imagined data; Audit stops you shipping rules nobody checked.

## Profile — discovery before rules

**When.** At engagement kickoff, before rule design. Again at each mock or load to measure
movement, and before deployment to confirm the data still looks the way it did when you authored.

**What you do.** Pick the systems, schemas and tables to profile, choose a filter preset per table
(see [[con-filter-presets]]), set the thresholds, and generate. You get a self-contained SQL bundle
— profiling script, sample dashboard query, manifest and readme. **You run it in the client's
environment**; no client data leaves it and the Studio never connects to their database. Upload the
result back to render the dashboard as a single self-contained HTML file you can email.

The same space also produces the Attribute Usage analysis (see
[[prc-run-an-attribute-usage-analysis]]) and, when a target MDM model is loaded, a target-fit
report measuring how well the source covers it.

**Settings worth understanding:**

| Setting | Default | What it changes |
|---|---|---|
| Working database | the Syniti working DB | Where results are written |
| Top N values | 50 | How deep the value distribution goes before the tail is cut |
| Skip threshold | 100,000 distinct | Above this, value distribution is skipped — free-text columns would swamp the run |
| Approximate-distinct threshold | 1,000,000 | Above this, distinct counts are approximated to keep the run fast |
| Retention | 12 runs | How much history is kept for trending |
| Mode | source database | Profile the source, or the consolidated working database |

> [!note] Divergence bands
> Cross-system comparison currently reads high at 0.50, medium at 0.20 and low at 0.05. Tighter
> bands have been proposed but are not in use — teach the current ones.

The step-by-step runbook is [[prc-generate-a-profile-bundle]].

## Audit — the quality gate before handover

**When.** On every package, before it reaches the client. Also useful as a sample review of an
existing client's deployed rules, and during catalog promotion review.

**What you do.** Three uploads, then run:

1. **The deploy SQL** from your rule package.
2. **The report tracker** from the same package.
3. **Row counts** *(optional but worth the effort)* — download the counts query, run it against the
   client's prep database, upload the result.

**What you get back** is a sorted findings list — severity, category, rule and remediation note —
exportable as an audit report:

- **Structural checks** on each generated view, against the SQL standards.
- **Cross-rule checks** — duplicate view names, near-identical SQL, inconsistent aliasing.
- **Runtime checks**, only if you supplied counts — score validity, outliers, coverage, skew, empty
  views and stale counts, scoring each rule as `100 − (report rows ÷ opportunity rows × 100)`.

The runtime tier is where the real surprises live, which is why counts are worth chasing: without
them, an empty view and a perfect rule look identical.

## Why Audit matters more than per-rule AI review

AI SQL review is off by default in a [[ref-bulk-pipeline|bulk run]] because switching it on turns a
20-minute batch into an hour-plus one. Audit is the deliberate replacement: one structural pass over
the whole package, in seconds. Run it every time. [[prc-audit-rule-quality]] is the consultant
checklist that goes alongside it.

## Common mistakes

- **Profiling after writing the rules.** The order is backwards and the rules will target the wrong
  fields.
- **Skipping the counts upload** and then reporting a package as clean — you have only checked
  structure, not behaviour.
- **Reading a zero-row report view as a passing rule.** It is more often a broken filter.
- **Treating a low-cardinality distribution as complete.** High-cardinality columns are skipped by
  design; absence of a distribution is not absence of a problem.

## Related

[[prc-generate-a-profile-bundle]] · [[prc-audit-rule-quality]] ·
[[prc-run-an-attribute-usage-analysis]] · [[con-profiling-concepts]] · [[con-filter-presets]] ·
[[con-attribute-usage-analysis]] · [[ref-bulk-pipeline]] · [[ref-home-page]]
