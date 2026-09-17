---
id: con-studio-capabilities
type: concept
title: The Four Studio Capabilities
domain: studio
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:con-profiling-concepts
  - relates:con-attribute-usage-analysis
  - relates:ref-single-rule-designer
  - contrast:ref-bulk-pipeline
  - relates:gls-engagement-kit
sources:
  - dq-studio:knowledge/methodology/capabilities.json
tags: [studio, capability, profiling, aua, client-facing, course]
created: 2026-08-20
updated: 2026-08-21
---

## What it is

The Studio presents its work to a client as **four capabilities**, not as a list of pages. Each one
is a self-contained brief — purpose, benefit, impact, and when/how to run it — shown as the
capability cards on the app's landing screen.

The four are deliberately ordered as a diagnostic-to-deliverable arc: **Table Profile** and
**Distribution Profile** measure what is actually there, **Data Quality Rules** enforce what should
be, and **Attribute Usage** answers the cross-organisation question the other three cannot.

| Capability | Headline | Execution space |
|---|---|---|
| Table Profile | Know what's in every field. | Schema Profile |
| Distribution Profile | See the patterns. | Schema Profile |
| Data Quality Rules | Catch errors to fix. | DQ Rules |
| Attribute Usage | See how a value is used across company codes and systems. | Attribute Usage |

> [!note] These spaces are the current navigation — resolved per CONFLICT-014
> The execution spaces named here and in the steps below (Session Setup, Schema Profile, DQ Rules /
> Workspace, Attribute Usage, Ship) are the app's current layout: `/workspace`, `/profile`,
> `/audit`, `/ship`, `/settings`. The seeded page-reference units — [[ref-home-page]],
> [[ref-single-rule-designer]], [[ref-bulk-pipeline]], [[ref-profiler-and-audit-pages]],
> [[ref-config-editor]], [[ref-skp-assetupload-and-tracker-flow]] — described the earlier
> seven-page layout (`/single`, `/bulk`, `/profiler`, `/skp`, `/config`); the 2026-08-21
> reconciliation sweep updated them to the spaces model, noting the old paths as legacy redirects.
> Their engine content was unaffected throughout; only the page framing was stale.

## 1. Table Profile — know what's in every field

**Purpose.** A per-field census of every table you point it at — *before* anyone writes a rule. The
Schema Profile run inventories each column's row counts (raw vs active), null and populated rates,
distinct cardinality, min/max and length stats, and a derived signal for what the field actually
holds. It is generated as pure MS SQL that writes structured results into staging tables, so it
runs inside the client's own environment with **no data leaving it**.

**Benefit.** You start the engagement from evidence, not assumption. In one pass you see which
fields are dense, which are empty, which are free-text chaos, and which are the real keys — so
scoping, estimation and rule design are grounded in the client's actual data on day one.

**Impact.** Turns "we think this field is mostly populated" into "CustomerNumber is 100% populated,
412 distinct, one format." Every downstream rule's opportunity and expected pass-rate is anchored
to a measured baseline — the foundation of business-ready data.

**When.** First, at engagement kickoff — the diagnostic that precedes rule design. Re-run at each
mock or load to measure movement.

**How.**

1. In Session Setup, confirm the source systems and databases for the engagement.
2. On Schema Profile, add the target tables (a row at a time, or upload the xlsx target list).
3. Choose a filter preset per table (e.g. exclude deletion flags) and Generate.
4. Run the produced SQL in the client environment; upload the result to see the dashboard.

**Requires.** The system × table list to profile; read access to the source (or consolidated
working) database; a filter preset per table where deleted/blocked rows should be excluded.

**Produces.** `DQ_Schema_Profile.sql` (the profiling script, runs in-client);
`Sample_Dashboard_Query.sql` (reconstructs the dashboard from staging); the Schema Profile
dashboard HTML — row counts, null/distinct, length and format stats.

See ref-schema-profiler and [[con-filter-presets]].

## 2. Distribution Profile — see the patterns

**Purpose.** The value-level view of a field: the Top-N values and how often each occurs. It comes
from the *same* Schema Profile run — low-cardinality columns get a value distribution showing the
most frequent values, their share of the population, and where the long tail begins.
High-cardinality free-text columns are skipped by a threshold so the run stays fast. It answers the
question *"what values are actually in here, and in what mix?"*

**Benefit.** Distribution is where data-quality problems become visible: a country column that is
60% `DE`, 3% `Germany` and 1% `DEU` is a standardization defect you can now see **and size**. It
reveals the dominant values worth a lookup table and the outliers worth a rule.

**Impact.** Converts a field into a ranked, quantified value set — the raw material for
standardization rules, valid-value lookups and consolidation logic. This is how a field becomes
business-ready: known values, known mix, known outliers.

**When.** Immediately alongside Table Profile — same run, no extra setup. Revisit when defining
valid-value or standardization rules.

**How.**

1. Generate the Schema Profile (Distribution comes from the same run).
2. Open the Distribution view to read Top-N values per low-cardinality column.
3. Tune Top-N and the skip threshold if you need deeper or lighter drill-down.
4. Feed the dominant values into lookup tables and the outliers into DQ rules.

**Requires.** A completed Schema Profile run (no separate configuration); sensible Top-N and
skip-threshold settings for the field cardinalities in scope.

**Produces.** Top-N value distribution per column (from `DQ_Profile_TopValues`); frequency share
and long-tail cutoff per value; candidate valid-value sets for lookup tables.

See [[con-profiling-concepts]] and ref-profiling-metrics-and-divergence-signals.

## 3. Data Quality Rules — catch errors to fix

**Purpose.** Plain-language rules become scored, SQL-backed, deployment-ready DQ checks. Describe a
rule the way the business states it — *"a material must have a valid base unit of measure"* — and
the Studio derives the full spec through the same knowledge engine experts use: domain detection,
output fields, joins, the error-detection logic, and generated OptSel/RptSel SQL. Author one at a
time or hundreds in a bulk run, all in one Workspace session.

**Benefit.** This is the deliverable the client pays for: a governed catalogue of executable rules
with consistent naming, commented SQL and per-rule specs — **not a spreadsheet of intentions.** One
session scales from a single rule to a full domain rollout.

**Impact.** Each rule returns the opportunity universe with a per-row error flag (OptSel) and the
report of failures (RptSel), so a defect is not just described — it is measured, trended, and
handed to remediation with the exact records. This is the engine that moves the DQ score.

**When.** After profiling has revealed the defects worth enforcing. Iterate as new domains come
into scope.

**How.**

1. In DQ Rules, describe a rule (or paste many, or upload the rule list).
2. The Studio derives, scores the name against 19 heuristics, and generates SQL.
3. Refine identity, logic, joins and filters in the section editor; regenerate SQL.
4. Ship the Rule Package (tracker + deploy SQL + specs + tests) from the Ship space.

**Requires.** The rule statements in business language (or a rule list to derive from); the ERP
knowledge pack and project config — systems, databases — from Session Setup; optionally, profiling
insight to target the right tables and values.

**Produces.** The OptSel view (candidate universe with a per-row `zIsErrorFlag`); the RptSel view
(the error report, `zIsErrorFlag = 1`); the Rule Package ZIP — tracker, deploy script, per-rule
specs, unit tests.

See [[ref-single-rule-designer]], [[ref-bulk-pipeline]], [[std-rule-name-heuristics]],
[[prn-optsel-is-the-universe]].

## 4. Attribute Usage — see how a value is used across company codes and systems

**Purpose.** A pivot of how each attribute's values are actually used — by organizational structure
and across source systems. Attribute Usage Analysis breaks a field's values down by org
combinations (Company Code, Sales Org, Plant, Purch Org) and by source system, showing occurrences
and the percentage within each org. It reveals that usage is **not uniform**: a payment term that
dominates one company code is rare in another, and the pattern shifts system to system.

**Benefit.** The highest-value diagnostic for a multi-system, multi-org landscape. It exposes where
a global standard is really local, which org units diverge, and which systems carry the cleanest
version of the truth — the evidence consolidation and harmonization decisions depend on.

**Impact.** Moves the conversation from "is this field populated" to "is this value used
consistently across the business." It is how you prove — with occurrences and percentages per org
and per system — whether an attribute is genuinely harmonized, which is the definition of
business-ready master data.

**When.** During diagnosis of cross-system / cross-org consistency, especially ahead of
consolidation, MDG, or S/4 harmonization decisions.

**How.**

1. In Attribute Usage, define the tables, the org breakdowns (e.g. Company Code), and the
   attributes to analyze.
2. Generate the AUA SQL and run it in the client environment.
3. Upload the result to render the pivot dashboard.
4. Read usage by org and system to target harmonization and consolidation.

**Requires.** The tables and the attributes to analyze; the org-breakdown definitions (Company
Code, Sales Org, etc. with their key fields); access to the consolidated all-systems prep data so
systems can be compared.

**Produces.** `AUA.sql` (the attribute-usage script, separate from Schema Profile); the usage pivot
— attribute value × org combination, with per-system breakdown; the Attribute Usage dashboard HTML
— fill rates and value mix per org, per system.

See [[con-attribute-usage-analysis]], ref-attribute-usage-analysis,
[[prc-run-an-attribute-usage-analysis]], [[std-aua-spec-template]].

## How to use this framing with a client

The four briefs share a deliberate structure — **purpose, benefit, impact, when/how, requires,
produces** — because that is the order a client asks the questions in. Purpose answers "what is
it", benefit answers "why would we", impact answers "what changes as a result", and when/how
answers "what do you need from us". Reading a capability card aloud in a scoping session is
therefore a complete answer, not an introduction to one.

Two of the four (Table Profile, Distribution Profile) come from a **single** Schema Profile run —
worth saying explicitly, because clients otherwise scope them as two separate exercises.
