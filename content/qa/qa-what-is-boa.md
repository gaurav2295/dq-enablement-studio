---
id: qa-what-is-boa
type: qa
title: What is BOA? Is it the knowledge base or the rule generation engine?
domain: delivery
audience: [consultant, lead]
level: foundation
status: review
sources:
  - coe:gls-boa
created: 2026-09-03
updated: 2026-09-03
links:
  - parent:gls-boa
  - relates:gls-bob-vs-boa
  - relates:gls-vector-studio
---

## Question

What is BOA? It's stated as a source, does this mean this is referring to the knowledge base or something else? Is this the engine that takes the input from the users and generates the Rule structure/frame using the knowledge base?

## Answer

**No to both.** BOA is neither the knowledge base nor the rule generation engine.

### What BOA Is NOT

- ❌ **Not the knowledge base** — the Studio's knowledge base is the Local Derive knowledge of SAP domains (tables, fields, joins, deletion flags)
- ❌ **Not the rule generation engine** — that's Local Derive (deterministic) and AI Derive (Claude-powered) inside the Studio
- ❌ **Not the rule structure generator** — the Studio generates rule specs, SQL, and view names

### What BOA Actually Is

**BOA = Business Outcomes Activation** — a **value framework and reference repository** that:

1. **Translates DQ results into business impact**
   - Example: "We found 500 defects in material master" → "Fixing these prevents $2M revenue loss in supply chain"

2. **Contains a value library with:**
   - 18 [[gls-value-lever|value levers]] (ways DQ creates value: reduce waste, prevent fraud, improve planning, etc.)
   - 6 [[gls-outcome-category|outcome categories]] (business domains impacted: Finance, Supply Chain, Operations, etc.)

3. **Ensures evidence-based, honest reporting**
   - "Volumes are not value" — 500 defects matter only if they translate to business impact
   - "Never inflate" — don't overstate the value
   - "Distinct lenses are never summed" — don't double-count impact across categories

### How BOA Fits with the Studio

| Role | Component |
|------|-----------|
| **Rule derivation** | Studio (Local Derive, AI Derive) — generates specs, SQL, views |
| **Value articulation** | BOA — explains why those rules matter to the business |

**In workflow terms:**
1. Studio: "We created Rule 0089 to check material activity"
2. BOA: "Rule 0089 prevents supply chain delays worth $500K annually"

---

### BOA vs BOB (Important Distinction)

- **BOB** = the DQ offering (what you deliver to the client)
- **BOA** = the engine behind BOB (the value framework)

**For client conversations:** Use "the value library" or "outcomes framework" instead of acronyms — the distinction is internal.

---

### Related

- [[gls-boa|Business Outcomes Activation (BOA)]]
- [[gls-bob-vs-boa|BOA vs BOB — The Distinction]]
- [[gls-value-lever|Value Lever]]
- [[gls-outcome-category|Outcome Category]]
