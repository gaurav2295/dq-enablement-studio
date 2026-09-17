---
id: qa-vector-studio-input-sheet
type: qa
title: What sheet does vector-studio consume as input? Do we export from DQ Studio?
domain: delivery
audience: [consultant, lead]
level: foundation
status: review
sources:
  - coe:gls-vector-studio
created: 2026-09-03
updated: 2026-09-03
links:
  - parent:gls-vector-studio
  - relates:gls-dq-studio
  - relates:gls-bob-canvas
---

## Question

Input is sheet, which sheet is it referring to? Do we take export from DQ Studio and feed it to vector studio for enhancement?

## Answer

**Yes — the workflow is: DQ Studio → export results → vector-studio ingests those results.**

### The Workflow

```
┌──────────────────────────────────┐
│ 1. DQ Studio                     │
│    - Authorship                  │
│    - Rule execution (owns loop)  │
│    - Generates SQL & runs it     │
│    - Output: Result sheets       │
└──────────────────┬───────────────┘
                   │ (export)
                   v
┌──────────────────────────────────┐
│ 2. vector-studio                 │
│    - Consumes result sheets      │
│    - Elevates results into value │
│    - Prioritizes & sequences     │
│    - Output: Blueprint           │
└──────────────────────────────────┘
```

### What Sheet?

The **input sheet** to vector-studio is the **DQ Studio result export**:

- **Not a database** — vector-studio never connects to customer systems directly
- **A sheet (spreadsheet/file)** — typically the bulk reconciliation or audit summary from DQ Studio
- **Contains evaluated results** — defect counts, parity scores, compliance status per rule

**Example input columns:**
- Rule ID, Rule Name
- Total Records Checked
- Error Count (defects found)
- Error Rate (%)
- Parity Score (vs catalog)
- Impact Category (Business, Technical, Compliance)

### What vector-studio Does with the Sheet

1. **Consumes the data** — reads the result sheet
2. **Elevates to value** — translates "500 defects in Material Master" into "prevents $2M supply chain loss"
3. **Prioritizes** — ranks rules by business impact (which to fix first)
4. **Sequences** — determines execution order (dependencies, prerequisites)
5. **Produces a blueprint** — a prioritized, sequenced, valued action plan

### Key Distinction: "Never Authors SQL"

The phrase "never authors SQL" means:

- ✅ vector-studio **refines presentation** of results (how to show impact)
- ✅ vector-studio **prioritizes and sequences** rules for remediation
- ❌ vector-studio does **not modify** the rules themselves
- ❌ If a rule needs changing, that happens in **DQ Studio** (not patched in vector-studio)

**Why?** This separation keeps the tool clear of customer systems and ensures the **single source of truth** (the rule) stays in DQ Studio.

### Example Flow

**Step 1: DQ Studio runs rules**
```
Rule 0089: Material Activity Check
- Executed SQL against WRKDQ database
- Found 45 materials with no activity in 2 years
- Result: 45 error records, 98% compliance rate
```

**Step 2: Export result sheet**
```
CSV/XLSX with columns:
- Rule_ID, Rule_Name, Total_Records, Error_Count, Compliance%, Impact
- 0089, Material Activity, 10000, 45, 98%, Critical
```

**Step 3: vector-studio consumes & elevates**
```
Priority Ranking:
1. Rule 0089 (Material Activity) — 45 defects × $50K per material = $2.25M impact
2. Rule 0092 (Vendor Master) — 12 defects × $10K = $120K impact
3. Rule 0101 (Customer Address) — 3 defects × $5K = $15K impact

Recommended Action Sequence:
1. Fix Rule 0089 first (highest financial impact)
2. Then Rule 0092 (operational impact)
3. Then Rule 0101 (customer-facing, but lower cost)
```

---

### Related

- [[gls-vector-studio|vector-studio]]
- [[gls-dq-studio|DQ Studio]]
- [[gls-bob-canvas|BOB Canvas]]
