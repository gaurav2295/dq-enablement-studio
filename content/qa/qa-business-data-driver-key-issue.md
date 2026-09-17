---
id: qa-business-data-driver-key-issue
type: qa
title: What exactly is a "key issue" that a Business Data Driver refers to?
domain: value-outcomes
audience: [consultant, lead]
level: foundation
status: review
sources:
  - coe:gls-business-data-driver
created: 2026-09-03
updated: 2026-09-03
links:
  - parent:gls-business-data-driver
  - relates:gls-business-rule
---

## Question

What exactly is the key issue that's being referred here?

## Answer

A **"key issue"** is a **specific data quality problem** that the business cares about. It's the internal/technical name for what's wrong with the data.

A **"Business Data Driver"** is the **client-friendly version** of that same key issue — how you describe it to the client in their business language.

### Key Issue vs. Business Data Driver

| Aspect | Key Issue (Internal) | Business Data Driver (Client-Facing) |
|--------|---|---|
| **Audience** | Data team, specs, internal docs | Clients, executives, business users |
| **Language** | Technical DQ terminology | Business/domain language |
| **Example** | "Material master completeness" | "Product catalog readiness" |
| **Another example** | "Vendor master accuracy" | "Supplier data reliability" |
| **Another example** | "Customer reference data gaps" | "Customer master data quality" |

### Real Examples

**Scenario: Manufacturing company client**

**Internal (Key Issue):**
- "Bill of Materials table missing required assembly instructions"

**Client-facing (Business Data Driver):**
- "Manufacturing readiness — missing assembly specs delay production"

---

**Scenario: Financial services client**

**Internal (Key Issue):**
- "General Ledger account master has orphaned cost center codes"

**Client-facing (Business Data Driver):**
- "Financial reporting accuracy — invalid cost allocations risk audit findings"

---

**Scenario: Retail client**

**Internal (Key Issue):**
- "SKU master has duplicate item numbers across divisions"

**Client-facing (Business Data Driver):**
- "Inventory visibility — duplicate SKUs cause fulfillment errors and shrinkage"

### The Mapping

There is **one authoritative mapping** between Key Issues and Business Data Drivers:

```
┌─────────────────────────────────┐
│ TERMS Map (Single Source)       │
├─────────────────────────────────┤
│ Key Issue → Business Driver     │
│ ─────────────────────────────── │
│ Material completeness → Product │
│                        readiness│
│ Vendor accuracy → Supplier      │
│                  reliability    │
│ Customer gaps → Customer master │
│                 data quality    │
└─────────────────────────────────┘
```

**Why one map?** To prevent drift between internal and client language — when the business definition changes, you update the TERMS map once, and the change propagates everywhere.

### How It Works in Practice

**Step 1: Identify the Key Issue**
```
Technical team: "We found 500 materials with NULL base unit of measure"
Internal spec: Key Issue = "Material master incompleteness"
```

**Step 2: Translate to Business Data Driver**
```
Client language: "Product catalog incompleteness — missing unit info delays
manufacturing planning and creates quote errors"
Business Driver = "Manufacturing readiness"
```

**Step 3: Use Consistently**
```
Internal docs: "Resolve key issue: Material master incompleteness"
Client report: "Address data driver: Manufacturing readiness (500 materials missing units)"
Toolkit: Both names point to the same record in TERMS map
```

---

### Related

- [[gls-business-data-driver|Business Data Driver]]
- [[gls-business-rule|Business Rule]]
- [[std-client-vocabulary|Client Vocabulary]]
