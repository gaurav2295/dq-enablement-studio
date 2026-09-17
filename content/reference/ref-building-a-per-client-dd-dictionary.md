---
id: ref-building-a-per-client-dd-dictionary
type: reference
title: Building a Per-Client DD% Dictionary
domain: sap
audience: [consultant, developer]
level: practitioner
status: review
links:
  - prereq:ref-sap-dd-dictionary-tables
  - implements:prn-3-tier-description-resolution
  - relates:ref-profiler-and-audit-pages
sources:
  - vault:sap-knowledge/Building a Per-Client DD%25 Dictionary.md
tags: [sap, sop, dd-percent]
created: 2026-08-20
updated: 2026-08-21
---

## What this is

How to take a customer's DD02T / DD03L / DD04T export and turn it into a SQLite lookup the
Studio can use — see [[ref-sap-dd-dictionary-tables|SAP DD% Dictionary Tables]] for what those
three tables carry.

## Prerequisites

- The customer's DD% export — typically a zip containing DD02T, DD03L, DD04T as CSV or
  fixed-width text
- Access to the Studio's DD% ingestion tool
- A short, alphanumeric **client slug** (one per tenant — e.g. `bacardi`, `danone`, `acme`)

## Steps

1. **Locate the export.** Customer DD% exports vary in shape:
   - Zipped folder with `DD02T.csv`, `DD03L.txt`, `DD04T.txt`
   - SSMS "Results to Text" fixed-width dumps
   - Tab-separated TSV

   The ingester sniffs the format from the first 16 KB so any of these work.

2. **Run the ingester** against the export, giving it the client slug.

3. **The output** is a per-client dictionary plus a small metadata file recording the ingest
   timestamp, source paths, and row counts.

4. **Verify** the reported row counts. Expect 100K+ tables and 1M+ columns for a typical ECC
   system.

## What it takes

- **Time**: ~60-90 seconds for a typical ECC dump
- **Disk**: ~600-700 MB SQLite file (highly compressed via PRIMARY KEY indexes)
- **RAM during ingest**: < 1 GB (streamed line-by-line, not loaded whole)

## Common surprises

- **Empty `DDLANGUAGE = 'E'` rows** — some clients ship only their primary language (DE, FR, ES)
  and have no English-translation rows. The ingester refuses to write descriptions in those
  cases. The fix: ask the customer to re-export with `DDLANGUAGE IN ('E', '<client-lang>')` so we
  get both.
- **Header rows missing** — SSMS fixed-width exports sometimes omit headers; the ingester falls
  back to positional parsing by filename hint.
- **Unicode encoding** — most exports are UTF-8 with BOM; some legacy are Windows-1252. The
  ingester reads with `utf-8-sig` first, falls back to `cp1252` if decode errors fire.

## After ingest

Once the dictionary is built:

- The Studio's `/profile` page's "Client SAP dictionary" dropdown auto-lists the new slug — see
  [[ref-profiler-and-audit-pages|Profiler & Audit Pages]]
- The 3-tier description resolver uses it as **tier 2** (between in-run snapshot and bundled
  internal) — see [[prn-3-tier-description-resolution|3-Tier Description Resolution]]
- The provenance badge on the dashboard shows the mix (`82% snapshot · 14% client · 4% internal`)

## When to rebuild

The DD% rarely changes — a per-client snapshot is good for a sprint or longer. Rebuild when:

- The customer adds significant custom Z*/Y* tables you'd want descriptions for
- A new SAP module activates (e.g. PM, QM) adding hundreds of tables
- A newer Studio release expects additional schema fields

> [!tip]
> The Studio's in-run DD% snapshot (tier 1) covers the always-fresh case — the per-client SQLite
> is for offline / dashboard scenarios where the source DB isn't reachable.

## Related

- [[ref-sap-dd-dictionary-tables|SAP DD% Dictionary Tables]]
- [[prn-3-tier-description-resolution|3-Tier Description Resolution]]
- [[prc-ingest-a-client-dd-dictionary|SOP — Ingest a Client DD% Dictionary]]
- [[ref-profiler-and-audit-pages|Profiler & Audit Pages]]
