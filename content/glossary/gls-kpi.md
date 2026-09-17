---
id: gls-kpi
type: glossary
title: KPI
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:prn-value-discipline
  - relates:gls-value-formula
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, value-chain]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**KPI = Key Performance Indicator** — the business measure a [[gls-value-lever|value lever]] moves.

The lever owns it, along with its financial-impact type and its [[gls-value-formula|value formula]].

## DQ Examples

| Domain | KPI | Affected by Data Quality |
|---|---|---|
| **Order-to-Cash** | Days Sales Outstanding (DSO) | Incomplete/incorrect customer master, billing dates, payment terms |
| **Procurement** | On-Time Delivery Rate | Inaccurate supplier data, material descriptions, purchase order dates |
| **Supply Chain** | Inventory Turns | Missing material classifications, plant assignments, usage history |
| **Finance** | Accounts Receivable Aging | Incomplete invoice data, customer hierarchies, transaction dates |
| **HR/Payroll** | Payroll Accuracy Rate | Incorrect employee master, cost center assignments, salary definitions |
| **Manufacturing** | Production Schedule Adherence | Missing BOM data, material attributes, plant capacity information |

Each KPI is tied to one or more **data quality rules** that prevent data issues from degrading the metric.

## Usage

A KPI is what makes a lever arguable in the client's own terms: the conversation is about a number
they already report, not about data quality as an abstraction.

Two disciplines: 
- **Name the KPI the client actually uses** (their definition, not a textbook one)
- **Never present a KPI movement as achieved** when it is [[gls-indicative|indicative]] — computed from stated assumptions the reader can open and change

### Example: On-Time Delivery KPI

```sql
-- KPI: Percentage of orders delivered on or before promised date
SELECT
  COUNT(*) AS total_orders,
  SUM(CASE WHEN DeliveryDate <= PromisedDate THEN 1 ELSE 0 END) AS on_time_orders,
  CAST(100.0 * SUM(CASE WHEN DeliveryDate <= PromisedDate THEN 1 ELSE 0 END) 
       / NULLIF(COUNT(*), 0) AS DECIMAL(5,1)) AS on_time_delivery_pct
FROM Sales_Orders
WHERE zSourceSystemID = 'SAP'
  AND OrderDate BETWEEN DATEADD(MONTH, -1, GETDATE()) AND GETDATE()
  AND OrderStatus IN ('Delivered', 'Invoiced');

-- DQ Rules that support this KPI:
-- 1. Promised delivery date must not be NULL (gls-completeness)
-- 2. Promised date >= Order date (gls-conformity)
-- 3. Actual delivery <= Promised date OR documented delay reason (gls-accuracy)
-- 4. Customer master incomplete → cannot route to correct location (gls-customer-master-completeness)
```
