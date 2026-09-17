---
id: gls-uniqueness
type: glossary
title: Uniqueness
domain: dq-fundamentals
audience: [consultant, lead, instructor]
level: foundation
status: review
links:
  - relates:con-dq-dimensions
sources:
  - coe:seven-dimension model per CONFLICT-001
  - vault:dq-methodology/DQ Dimensions.md
tags: [dimensions, foundations]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**Is each real-world entity represented exactly once?** Uniqueness is a set-level dimension — it
can't be evaluated one record at a time the way [[gls-accuracy]] or [[gls-completeness]] can. The
rule has to group records by the identifying attributes of the real-world entity and flag any
group with more than one member, which makes it sensitive to how loosely or tightly the matching
key is defined.

## Example rule

No two customer master records share the same VAT registration number (`STCEG`). Two `KNA1`
records with different customer numbers but the same VAT ID are almost certainly the same legal
entity, entered twice — by different users, different acquisitions, or a failed dedup during a
prior migration.

## Cost of a defect

A duplicate customer or vendor record splits transaction history across two masters — spend
visibility on that vendor understates the real total, a customer's credit exposure is calculated
against only half their orders, and duplicate vendor masters are a known root cause of duplicate
payments. Uniqueness defects also compound in mass mailings and outreach: the same entity
contacted twice erodes trust in the data and in the process that used it.
