---
id: gls-zconcatenatedkey
type: glossary
title: zConcatenatedKey
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
links:
  - relates:std-zconcatenatedkey-convention
  - relates:gls-syniti-technical-fields
  - relates:gls-composite-key

sources:
  - vault:dq-methodology/Output Field Sections.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
tags: [technical-fields, keys]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The **unique record key across systems** — the technical field that makes a defect row
addressable when the same business key exists in more than one source system. Built with
`CONCAT(...)` and an underscore delimiter from the source-system id plus the record's key
field(s):

```sql
CONCAT(MARA.zSourceSystemID, '_', MARA.MATNR) AS [zConcatenatedKey]
```

## Usage

- **No space in the alias** — an ADM requirement.
- **`CONCAT`, never `+`** — `+` propagates NULLs and drops the row's identity.
- **Underscore, never a pipe** — the pipe form is superseded and is a *blocking* violation on
  the AI-Enhance path ([[std-ai-enhance-guardrails]]).
- Every field the rule's [[gls-composite-key|composite key]] needs must appear in it.

Full recipe, including `COALESCE`/`TRIM` wrapping: [[std-zconcatenatedkey-convention]].
