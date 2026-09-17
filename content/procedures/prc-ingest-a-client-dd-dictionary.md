---
id: prc-ingest-a-client-dd-dictionary
type: procedure
title: Ingest a Client DD% Dictionary
domain: sap
audience: [consultant, developer]
level: practitioner
status: deprecated
sources:
  - vault:sops/SOP — Ingest a Client DD%25 Dictionary.md
tags: [sop, dd-percent]
created: 2026-08-20
updated: 2026-08-21
links:
  - prereq:ref-sap-dd-dictionary-tables
  - implements:prn-3-tier-description-resolution
  - relates:ref-building-a-per-client-dd-dictionary
  - relates:prc-generate-a-profile-bundle
---

## Goal

Take a customer's DD02T/DD03L/DD04T export and build a per-client SQLite database that the
Studio's dashboard layer can use as tier-2 description enrichment.

## When to use

- New client engagement — build their dictionary once at the start
- Client added significant custom Z*/Y* tables — rebuild
- DD% wasn't reachable at profile time — use the per-client SQLite as the tier-2 fallback

## Prerequisites

- The customer's DD% export (zip / folder / loose files)
- Access to the Studio's DD% ingestion tool
- A short alphanumeric client slug (e.g. `bacardi`, `danone`, `acme`)
- ~1 GB free disk

## The DD% files the script expects

| File | Format | Required |
|---|---|---|
| DD02T | CSV / TSV / SSMS fixed-width — Table descriptions | Yes |
| DD03L | CSV / TSV / SSMS fixed-width — (Table × Field × Data Element) map | Yes |
| DD04T | CSV / TSV / SSMS fixed-width — Data Element descriptions | Yes |

Filenames can vary (`DD02T.csv`, `DD_02T.txt`, `Table_descriptions.csv`); the ingester sniffs by
filename hint plus content.

## Steps

### 1. Receive and verify the export

Open the zip / folder; confirm DD02T, DD03L, DD04T are present. Eyeball a few rows of each:

- DD02T should have `TABNAME, DDLANGUAGE, DDTEXT` columns (or the fixed-width equivalent)
- DD03L should have `TABNAME, FIELDNAME, ROLLNAME, ...`
- DD04T should have `ROLLNAME, DDLANGUAGE, DDTEXT, ...`

If the customer shipped DD% in a single non-English language, request a re-export including
`DDLANGUAGE = 'E'`.

### 2. Pick a slug

Short, alphanumeric, lowercase. One per tenant. Conventions:

- Customer name truncated to 6–10 chars: `bacardi`, `danone`, `nestlé` → `nestle`
- No spaces, hyphens, or underscores ideally
- Stable forever — the slug appears in the Studio's `/profile` dropdown

### 3. Run the ingester

Point the Studio's DD% ingestion tool at the export and give it the client slug. Status output
shows:

- Per-file row counts read
- Filename detection: which file matched DD02T / DD03L / DD04T
- Insert progress (streaming, low-memory)
- Output location

### 4. Output

The tool builds a per-client dictionary plus a small metadata record: ingest timestamp, source
file paths, row counts per table.

### 5. Verify

Check the reported table and column counts. Expected counts for a typical ECC system:

- Tables: 100K–600K rows
- Columns: 1M–7M rows

If counts look low (e.g. under 50K tables), the source export likely missed languages or is
a partial extract — re-export.

### 6. Test in the Studio

Restart the Studio (or refresh if it's already running). Open `/profile` — the "Client SAP
dictionary" dropdown should now list the new slug. Pick it before generating a dashboard.

## Time and disk

- Ingest time: 60–90 seconds for a typical ECC export
- Output SQLite: 500 MB – 1 GB depending on the SAP system size
- Memory during ingest: under 1 GB (streamed, not loaded whole)

## Common pitfalls

- **DDLANGUAGE='E' missing** — the customer's export only has DE / FR / ES. The ingester refuses
  to populate descriptions in those cases. Re-export with E plus their primary language.
- **Filename hints don't match** — the ingester tries DD02T / DD03L / DD04T as stems. If files are
  named `Dictionary_Tables.csv`, rename to match the hint, or specify the mapping explicitly.
- **Unicode decode error** — legacy exports are occasionally Windows-1252, not UTF-8. The ingester
  falls back automatically; if it still fails, re-export with `chcp 65001` set in SSMS.
- **Studio doesn't see the new slug** — restart the Studio so the client list refreshes.

## Related

- [[ref-sap-dd-dictionary-tables|SAP DD% Dictionary Tables]]
- [[ref-building-a-per-client-dd-dictionary|Building a Per-Client DD% Dictionary]]
- [[prn-3-tier-description-resolution|3-Tier Description Resolution]]
- [[prc-generate-a-profile-bundle|Generate a Profile Bundle]]
