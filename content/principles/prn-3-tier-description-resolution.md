---
id: prn-3-tier-description-resolution
type: principle
title: 3-Tier Description Resolution
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-sap-dd-dictionary-tables
  - relates:ref-building-a-per-client-dd-dictionary
  - relates:ref-profiler-and-audit-pages
sources:
  - vault:thought-leadership/3-Tier Description Resolution.md
tags: [thought-leadership]
created: 2026-08-20
updated: 2026-08-20
---

## What it is

The Studio's profiler dashboard turns technical column names into human-readable English
labels by consulting three tiers of metadata, in priority order, and falling back to the next
tier whenever the current one is blank.

## The three tiers

| Tier | Source | Freshness |
|---|---|---|
| **1. Snapshot** | DD% (DD02T/DD03L/DD04T) pulled into WRKDQ during the same profile run | Always matches the run — guaranteed fresh |
| **2. Client** | Per-tenant client dictionary (built once via ingest) | Stale-by-weeks possible; ingested separately |
| **3. Internal** | Bundled internal SAP reference data | Generic SAP knowledge; no tenant-specific terms |

When the dashboard renders, it walks the chain for each (table, column): tier 1 → if blank,
tier 2 → if blank, tier 3 → if blank, leave the technical name showing.

## Why three tiers, not one

### Why not "always use snapshot"

Snapshot requires DD% to be reachable at profile time. Not every engagement has that:

- Some clients give the Studio user a separate sandbox DB with only profile output, no DD%.
- Cloud-hosted SAP sometimes restricts DD% extracts to specific roles.
- Legacy ECC environments may have DD% in a separate schema we don't have access to.

Without tier 2 / tier 3, those engagements lose all label enrichment.

### Why not "always use client"

The client SQLite is built once per tenant, then ages. A schema change on the client side (new
custom Z fields, new module added) is invisible to a months-old SQLite. The snapshot tier
catches up automatically; the client tier doesn't.

### Why not "always use internal"

The internal JSON is generic SAP standard. It doesn't know `Z_BAC_INTERCO_FLAG` is *"Bacardi
inter-company flag"* — that lives in the client's DD%. Tenant-specific names need tier 1 or 2.

## How the tiers compose

For each (table, column) in the profile output: check the snapshot tier first; if it has a
label, use it. If not, check the client tier; if it has a label, use it. If not, check the
internal tier; if it has a label, use it. If none do, show the technical name as-is.

Hits are counted per-tier and surfaced as a **provenance badge** on the dashboard:

> [!note]
> *Descriptions: 82% snapshot · 14% client · 4% internal*

The reader sees at a glance how fresh the labels are. If the badge shows 4% snapshot / 96%
internal, descriptions are mostly generic — investigate why the snapshot didn't reach the
dashboard.

## The config knob

Project YAML can constrain which tiers are allowed:

```yaml
profiling:
  description_sources:
    - snapshot
    - client
    - internal
```

Reduce to `[snapshot]` for strict-freshness mode (rejects fall-throughs). Reduce to `[snapshot,
client]` if internal-generic labels confuse the client's reviewers.

## Reconciliation: when to stop and fix

The provenance badge tells you where the labels came from. Not all distributions need action — some are normal, others signal a real problem.

**Red flags (investigate immediately):**
- **80%+ internal** — your labels are generic SAP dictionary, not your client's business terms. The profiler isn't picking up client-specific names (Z fields, custom tables). Fix: Check that client dictionary ingest completed and snapshot tier is enabled.
- **100% internal** — all three tiers missed every (table, column) pair. Either snapshot/client tiers are disabled, or table/column names are so different from standard SAP that nothing matched.

**Yellow flags (okay to continue, note for next time):**
- **80%+ client** — labels came from the client dictionary built at the start of the engagement. Normal if no fresh snapshot gathered recently. Schedule a fresh snapshot if schema has drifted (new fields, modules added).
- **Mixed (30% snapshot, 40% client, 30% internal)** — exactly how the system is designed to work. You're using all three tiers, which is right. Only investigate if snapshot % suddenly *drops* run-to-run (e.g., 70% → 10%); that signals a broken connection to DD%.

## Why this isn't over-engineering

The temptation to simplify ("just pick one!") fails because the engagement constraints vary:

| Engagement | What works |
|---|---|
| Fresh Bacardi sprint with DB access | Tier 1 dominates — snapshot covers everything |
| Returning to a Danone dashboard 3 months later | Tier 2 (client) still works; tier 1 stale data is rejected |
| Demo to a prospect with no client data | Tier 3 (internal) at least gives generic SAP labels |

One tier alone can't cover all three. Three with explicit precedence does. The provenance
counter is the trade-off that makes it work — without it, the user has no signal about which
tier answered, and the temptation to simplify back to one tier returns.

> [!tip]
> This same resolution shape recurs — see [[ref-value-description-resolution]] for the
> analogous four-mechanism cascade used to resolve field *values* rather than descriptions.

## Worked example: A field's journey through all three tiers

Here's how a single field (`MARA.MTART` = Material Type) resolves descriptions in different scenarios.

**Scenario 1: Tier 1 succeeds (snapshot has the label)**

Run the profiler on 2026-09-07 with DD% access.

```
Field: MARA.MTART
Tier 1 (snapshot): "Material Type" ← from DD03L at 2026-09-07
Tier 2 (client):   (not checked, Tier 1 found a match)
Tier 3 (internal): (not checked, Tier 1 found a match)
Result: "Material Type" (Tier 1 wins)
```

**Scenario 2: Tier 1 is blank; Tier 2 succeeds**

Run the profiler without DD% access (client restricted it that day).

```
Field: MARA.MTART
Tier 1 (snapshot): (blank — DD% was inaccessible at profile time)
Tier 2 (client):   "Product Type" ← from client dict built 8 weeks ago
Tier 3 (internal): (not checked, Tier 2 found a match)
Result: "Product Type" (Tier 2 wins; stale but available)
```

**Scenario 3: Tier 1 and Tier 2 blank; Tier 3 succeeds**

Schema changed after the client dict was built; MTART is now new.

```
Field: MARA.MTART
Tier 1 (snapshot): (blank — field changed in schema since snapshot)
Tier 2 (client):   (blank — field didn't exist when dict was built)
Tier 3 (internal): "MTART" ← from SAP standard dictionary
Result: "MTART" (Tier 3 wins; generic but better than nothing)
```

**Scenario 4: All tiers fail; fall back to technical name**

ZXYZ01 is a brand-new custom field not yet documented anywhere.

```
Field: MARA.ZXYZ01
Tier 1 (snapshot): (blank — new field; not in DD%)
Tier 2 (client):   (blank — new field; not in old dict)
Tier 3 (internal): (blank — custom Z field; not in SAP)
Result: "ZXYZ01" (technical name shown; unmapped)
```

### What the profiler displays

The provenance badge tells the story:

| Scenario | Tier 1 | Tier 2 | Tier 3 | Unmapped | Interpretation |
|----------|--------|--------|--------|----------|--------|
| 1 (snapshot fresh) | 85% | 10% | 4% | 1% | Healthy; Tier 1 is authoritative |
| 2 (snapshot unavailable) | 0% | 80% | 15% | 5% | Acceptable; re-snapshot planned |
| 3 (old dict, new schema) | 0% | 0% | 100% | 0% | Stale; plan refresh |
| 4 (many new custom fields) | varies | varies | varies | 5%+ | Review unmapped fields with client |

## Related

- [[ref-sap-dd-dictionary-tables]]
- [[ref-building-a-per-client-dd-dictionary]] · [[prc-ingest-a-client-dd-dictionary]] — how tier 2
  gets built.
- [[ref-profiler-and-audit-pages]] — the pages that render these labels (the profiler dashboard
  renderer itself is not yet a knowledge unit).
