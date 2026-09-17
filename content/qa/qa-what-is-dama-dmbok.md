---
id: qa-what-is-dama-dmbok
type: qa
title: What is DAMA-DMBOK and what is its role in Data Quality?
domain: dq-fundamentals
audience: [consultant, lead]
level: foundation
status: review
sources:
  - coe:qa
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:con-dq-dimensions
---

## Question

What is DAMA-DMBOK and what is its role in Data Quality?

## Answer

**DAMA-DMBOK** stands for **Data Management Body of Knowledge**, published by DAMA International. It is the international standard framework for data management disciplines, including data quality.

### DAMA-DMBOK's Data Quality Dimension Model

DAMA-DMBOK defines **six core dimensions** of data quality:
1. **Completeness** — Is required data present?
2. **Uniqueness** — Is each entity represented exactly once?
3. **Timeliness** — Is data current enough for its purpose?
4. **Validity** — Does data follow defined formats and standards?
5. **Accuracy** — Does data reflect real-world facts?
6. **Consistency** — Do related values agree across records and systems?

### Our Seven-Dimension Model vs. DAMA-DMBOK

The DQ CoE methodology is **compatible with but extends** DAMA-DMBOK:
- **Five dimensions map directly:** Completeness, Uniqueness, Timeliness, Accuracy, Consistency
- **Two dimensions expand DAMA:** 
  - **Conformity** — expands DAMA's "Validity" (format, range, and standard adherence)
  - **Integrity** — references, orphans, and broken keys (implied in DAMA but not explicitly called out; the single most common and most expensive master-data failure mode)

### When You Encounter DAMA-DMBOK on a Client Engagement

If a client brings their own data quality framework or references DAMA-DMBOK directly:
- **Map their terms onto our seven dimensions** in the engagement glossary
- Ensure consistent terminology across all deliverables and stakeholder conversations
- This alignment prevents confusion and shows respect for the client's existing standards

### Why This Matters

Using a consistent, standard-aligned vocabulary (whether DAMA or our seven-dimension model) ensures that when you report findings, stakeholders understand *what* dimension is affected and why it matters — rather than debating terminology.

See [[con-dq-dimensions|The Seven DQ Dimensions]] for how each dimension is defined, scored, and used in rule design and remediation prioritization.
