---
id: qa-why-casing-important-zsourcesystemid
type: qa
title: Why is casing important for zSourceSystemID?
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-zsourcesystemid-convention
---

## Question

Why is casing important?

## Answer

**SQL Server treats column names case-sensitively in joins and WHERE clauses** if the database collation is configured for case sensitivity. More importantly, **consistency prevents silent failures**.

The canonical form is **`zSourceSystemID`** (lowercase `z`, camelCase). Variations:

| Form | Problem |
|------|---------|
| `ZSourceSystemID` | Uppercase Z breaks the convention that z-prefixed = Syniti-added metadata |
| `ZSOURCESYSTEMID` | Hard to read; breaks the visual identifier |
| `zSourceSystemId` | Trailing `d` instead of `ID` — might not match the table definition |
| `zSourceSystem` | Missing trailing `ID` — doesn't exist in the table; join fails silently |

**Real impact:** If you write `WHERE MARA.zSourceSystem = 'Z01'` (missing the `ID`), the filter silently does nothing — SQL doesn't error, it just returns all rows. The defect count explodes, and you don't find the bug until audit.

Always match the **exact spelling and casing** from `SAP_ECC_Complete.json` or your data dictionary.

## Related

- [[std-zsourcesystemid-convention|zSourceSystemID Convention]]
