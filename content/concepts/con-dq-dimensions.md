---
id: con-dq-dimensions
type: concept
title: The Seven DQ Dimensions
domain: dq-fundamentals
audience: [consultant, lead, instructor]
level: foundation
status: approved
links:
  - relates:gls-optsel
  - relates:prn-optsel-is-the-universe
  - relates:con-rule-types
  - relates:con-what-is-data-quality
  - relates:con-dq-lifecycle
  - relates:gls-accuracy
  - relates:gls-completeness
  - relates:gls-conformity
  - relates:gls-consistency
  - relates:gls-integrity
  - relates:gls-timeliness
  - relates:gls-uniqueness
sources:
  - vault:dq-methodology/DQ Dimensions.md
  - academy:landing.html#session-1
tags: [dimensions, foundations]
created: 2026-08-20
updated: 2026-08-20
---

## What they are

The methodology recognises **seven** canonical dimensions of data quality. Every DQ rule
measures at least one of them, and every finding is communicated in their language.

| Dimension | Question it answers | Example rule |
|---|---|---|
| [[gls-accuracy]] | Does the value reflect the real-world fact? | Customer's VAT number passes Luhn / EU VAT format check |
| [[gls-completeness]] | Is the value present where the business requires it? | Material has a non-null base unit of measure |
| [[gls-conformity]] | Does the value follow the required format, range, or standard? | Postal code matches country format |
| [[gls-consistency]] | Do related values agree with each other across records and systems? | Customer's currency matches between KNA1 and KNB1 |
| [[gls-integrity]] | Do references resolve — no orphans, no broken keys? | Profit center on the cost element exists in CEPC |
| [[gls-timeliness]] | Is the current data sufficient for the decision it supports? | Material's last-update date is within N months |
| [[gls-uniqueness]] | Is each real-world entity represented exactly once? | No two customers share STCEG (VAT number) |

Every rule is tagged with a dimension — it drives reporting, prioritisation, and the SKP
Category column.

## Why seven, not six

Earlier training material taught a six-dimension model that used *Validity* and omitted
*Conformity* and *Integrity*. The seven-dimension model is canonical: Conformity covers what
Validity loosely meant (format and standard adherence), and Integrity earns its own dimension
because referential breakage is the single most common and most expensive SAP master-data
failure mode.

> [!note]
> When a client uses a different dimension vocabulary (DAMA, DMBOK, their own), map their terms
> onto these seven in the engagement glossary rather than adopting theirs mid-delivery.

## How rules map to a dimension

Most Error rules check one dimension; a few mix two (e.g. an integrity check is often *also* a
completeness check — the reference exists AND is populated). When a rule clearly straddles, pick
the **primary defect category** for the SKP Category column.

### Accuracy vs Conformity — where the line is

**Accuracy** answers "Does the recorded value match the real-world fact?" — e.g., is a customer's
birth year 1905 in the system because they were actually born in 1905?

**Conformity** answers "Does the recorded value meet the format/range/standard we've defined?" — e.g.,
does that same birth year fit within our system's valid range of 1950–present?

**Example — a customer born in 1905:**
- Recorded birth year: `1905`
- **Accurate?** YES — the person was genuinely born in 1905 (real-world fact)
- **Conforming?** NO — our system's standard requires birth years ≥ 1950 (system rule)

The distinction matters: an accurate value can fail conformity (needs code review, not data cleanup);
a conforming value can lack accuracy (cleanup required). They're separate problems with different
remediation paths.

## Why dimensions matter operationally

- **Triage & criticality** — dimension correlates with business impact, but is not absolute. Accuracy and Integrity defects *often* block transactions or disrupt reporting, but this depends entirely on business context. A customer's phone number (Accuracy) might be critical for contact delivery but not for financial posting. Always confirm criticality with the business before assuming Accuracy = always-critical.

- **Completeness tolerance varies** — Completeness gaps (missing required values) are more tolerable when:
  - The system can auto-populate a sensible default (e.g., default tax ID to a placeholder)
  - Downstream processes can continue with partial data
  - The gap is in a secondary (non-critical) field
  Completeness is less tolerable when the missing value is a primary key or a blocking prerequisite for any downstream process.

- **Remediation owner** — different dimensions tend to map to different stewardship teams
  (Accuracy → master-data owner; Conformity → reference-data team; Consistency → MDM; Integrity → data architect).
  
- **Reporting** — executive dashboards typically slice defect counts by dimension to show which
  dimension dominates the backlog.

## In the Studio

The bulk reconciliation Excel auto-derives the dimension from rule-name patterns:

- Keywords like *valid*, *correct*, *properly formatted* → Accuracy.
- Keywords like *must have*, *required*, *populated*, *not null* → Completeness.
- Keywords like *match*, *consistent with*, *agrees with* → Consistency.
- Keywords like *reference*, *exists in*, *valid foreign key* → Integrity.
- Keywords like *unique*, *no duplicates*, *one per* → Uniqueness.
- Keywords like *current*, *within N days* → Timeliness.
- Keywords like *conforms to format*, *must be in format*, *format standard* → Conformity.

This auto-derivation is a starting point — manual override is always allowed. If a rule name is ambiguous
between Accuracy and Conformity (e.g., "postal code format is valid"), consult the rule's implication to
determine which dimension the defect actually represents. The name is the trigger; the definition is the authority.

## DAMA-DMBOK alignment

DAMA-DMBOK (Data Management Body of Knowledge) is the international standard framework for data management, published by DAMA International. Its Data Quality discipline defines six core dimensions: Completeness, Uniqueness, Timeliness, Validity, Accuracy, and Consistency.

Our seven-dimension model is compatible with DAMA-DMBOK — five dimensions map directly (Completeness, Uniqueness, Timeliness, Accuracy, Consistency), and we expand their framework with two additional dimensions:

- **Conformity** — expands on Validity (format, range, and standard adherence)
- **Integrity** — references, orphans, and broken keys (not explicitly called out in DAMA but implied)

When a client references DAMA-DMBOK or brings their own quality framework, map their terms onto these seven dimensions in your engagement glossary. This ensures consistent terminology across all deliverables and stakeholder conversations.

## In practice

- A rule's dimension drives how its **implication** is written — a Completeness finding argues
  a different business risk than an Integrity finding on the same table.
- Profiling has no pass/fail, but profiling output is still organised by dimension so gaps are
  discussed in business language.
- A dimension answers "what's wrong with the data?"; a
  [[con-cleanse-action-categorization|cleanse action]] answers "what do we do about it?" — see
  that unit for how the two map together.

## Questions from consultants

**Q: What is DAMA-DMBOK and what is its role in Data Quality?**

A: See [[qa-what-is-dama-dmbok|What is DAMA-DMBOK and what is its role in Data Quality?]] — it's the international standard framework (six core dimensions). Our seven-dimension model is compatible and extends DAMA by splitting Validity into Conformity and adding Integrity.

**Q: How do we distinguish between Accuracy and Conformity when a value is technically valid but not realistically possible?**

A: See [[qa-accuracy-vs-conformity-impossible-values|How do we distinguish between Accuracy and Conformity when a value is technically valid but not realistically possible?]] — the key is checking the real-world context. If the value is genuinely accurate, update your conformity standard; if it's inaccurate, fix the data.

**Q: Are Accuracy and Integrity always higher priority than other dimensions?**

A: See [[qa-dimension-priority-business-dependent|Are Accuracy and Integrity always higher priority than other dimensions?]] — priority is business-dependent, not fixed. Always confirm criticality with the client before assuming any dimension is "always-critical."

**Q: Why are Completeness gaps considered more tolerable than Accuracy or Integrity issues?**

A: See [[qa-completeness-blocking-transactions|Why are Completeness gaps considered more tolerable than Accuracy or Integrity issues?]] — Completeness is tolerable only for secondary/optional fields. Missing required values (credit limits, ship-to addresses) block transactions just like Accuracy or Integrity defects.

**Q: Why is 'consistent format' mapped to Accuracy instead of Conformity?**

A: See [[qa-format-accuracy-vs-conformity|Why is 'consistent format' mapped to Accuracy instead of Conformity?]] — the keyword mapping is ambiguous; consult the rule's implication. Format adherence is Conformity; format validity for real-world context is Accuracy.
