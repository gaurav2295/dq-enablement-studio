---
id: con-what-is-data-quality
type: concept
title: What Is Data Quality?
domain: dq-fundamentals
audience: [consultant, lead, instructor]
level: foundation
status: review
sources:
  - academy:landing.html#what-is-dq
  - academy:landing.html#why-matters
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:con-dq-dimensions
  - relates:con-dq-lifecycle
---

## What it is

Data Quality (DQ) is the degree to which data conforms to defined standards and meets business
expectations. It's not a single metric — it's a multidimensional measurement.

**Fitness for purpose** means the data can reliably support the decision it's meant to support. For example, a customer's address is of high quality *for shipping* if it's complete and correctly formatted, but of poor quality *for tax reporting* if the country code is missing (required for GDPR compliance).

> [!note]
> "Data Quality is the fitness of data for a business purpose. Poor quality data costs your
> organization in rework, regulatory fines, customer churn, failed migrations, and bad
> decisions."

**Why DQ matters, in one sentence:** a single bad record in your master data can break
downstream processes, analytics, compliance checks, and entire migration projects.

## Common consequences of poor DQ

- **Rework** — manual data cleanup takes weeks or months
- **Regulatory risk** — non-compliance with data protection laws:
  - **GDPR** (General Data Protection Regulation, EU) — applies to personal data of EU residents; fines up to €20M or 4% of revenue
  - **HIPAA** (Health Insurance Portability and Accountability Act, US) — applies to healthcare data; fines up to $1.5M per violation
  - **SOX** (Sarbanes-Oxley Act, US) — applies to financial reporting; requires data accuracy in SEC filings; violations can result in executive liability
- **Operational failures** — orders not fulfilled, shipments delayed, invoices uncollectable
- **Migration delays** — ERP migrations fail or stall when data isn't clean
- **Bad decisions** — analytics and reporting built on dirty data leads to wrong strategies

## Why data quality matters

Data quality isn't optional — it's fundamental to business success. The numbers:

| Metric | Value | What it means | Source |
|---|---|---|---|
| Organizations | 43% | Report significant data quality problems in master data | Capgemini Data State of the Nation 2024 |
| Annual cost | $15M | Average impact per organization from poor DQ | Gartner Data Quality Impact Study 2023 |
| Risk duration | 60 days | Delay caused by data cleansing in ERP migrations | SAP Transformation Engagement Data 2022–2026 |

Actual costs vary by industry, data volume, and issue complexity.

## In the context of SAP migrations

When organizations migrate from SAP ECC to S/4HANA, master data quality is **the single biggest
risk factor**. Projects fail or stall because:

- Master data hasn't been validated before migration
- Orphaned records exist (foreign keys without parents)
- Required fields are missing or invalid
- Duplicate records confuse business logic

**Data Quality Rules are how you prevent this.** They codify what "bad" means and let you catch
issues early, before they cascade downstream.

## Real-world example: the cost of one bad customer record

A customer record in KNA1 is missing a country code. The system accepts it because the country code field is optional at the functional level, even though tax, shipping, and GDPR compliance all require it. The error isn't caught until S/4HANA migration begins:

**What breaks downstream:**

1. **Billing system** — The invoicing module requires `LAND1` (country) to calculate VAT rates. Invoices for this customer can't be generated. Finance escalates.

2. **Regulatory compliance** — GDPR data-processing reports can't classify personal data by region (required for the DPA). Compliance audit discovers the gap. Potential fine exposure: €10M+.

3. **Shipping & logistics** — The logistics system assumes a default country when one is missing, shipping orders to the wrong region. Two weeks of customer complaints and returns.

4. **Migration delay** — Data quality scanning finds 50,000 similar customer records missing country codes. The migration stalls for 3 weeks while master-data stewards manually research and populate each one.

5. **Analytics poisoned** — Marketing reports built before the cleanup show incorrect customer segmentation by region. Campaign spend is allocated to the wrong markets based on dirty data.

**The business impact:**
- 3 weeks of delayed go-live (opportunity cost: $500K+ in deferred business value)
- 2 weeks of customer-service rework (50+ hours)
- Regulatory exposure requiring legal review
- Analytics-driven decisions based on wrong data (cascading strategic error)

**How DQ rules prevent this:** A simple rule — "A customer must have a country code" — catches this in pre-migration validation, lets you fix 50,000 records in batch, and prevents all downstream failures.
