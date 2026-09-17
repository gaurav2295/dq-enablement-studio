---
id: gls-status-field
type: glossary
title: Status Field
domain: sap
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-pattern-status-field-check
  - relates:ref-sap-deletion-flags-vs-status-fields
  - relates:gls-deletion-flag
  - relates:gls-polarity
sources:
  - vault:sap-knowledge/SAP Deletion Flags vs Status Fields.md
  - dq-studio:knowledge/erp/sap_ecc/status_fields.json
tags: [sap, status, blocks]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A SAP **block or status** column recording that a record is restricted for a particular activity —
central payment block (`KNA1.SPERZ`), central order block (`KNA1.AUFSD`), purchasing block
(`LFA1.SPERM`), and their org-level equivalents. Catalogued in the Studio's `status_fields.json`
registry with a `level` (central / org), a `category` (posting, payment, order, delivery, billing,
sales, purchasing) and a `type` (`boolean` — set means `'X'`; `code` — set means any non-blank).

## Usage

The distinction from a [[gls-deletion-flag|deletion flag]] is the one to hold on to:

| | Deletion flag | Status field |
|---|---|---|
| Meaning | the record is on its way out | the record is live but restricted |
| Default handling | filtered out in `WHERE` | **checked** — it is often the defect itself |

A rule whose subject is a status field derives through the
[[std-pattern-status-field-check|status-field-check pattern]], where the field's `type` decides
what "set" means and the rule's [[gls-polarity|polarity]] decides which state is the error.
