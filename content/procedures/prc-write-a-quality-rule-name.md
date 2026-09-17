---
id: prc-write-a-quality-rule-name
type: procedure
title: Write a Quality Rule Name
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:sops/SOP — Write a Quality Rule Name.md
tags: [sop, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - implements:std-rule-name-heuristics
  - relates:std-implication-template
  - relates:con-catalog-vs-bespoke-rules
---

## Goal

Author a DQ rule name that scores well on the 19-heuristic scorer AND reads cleanly on the
tracker, SKP, and any consumer dashboard.

## When to use

Any time you're naming a new rule — either authoring from scratch or refining an AI-suggested
name.

## The hard constraints

- **Max 100 characters** — an ADM requirement; truncation causes tracker rows to fail
- **Target ≤85 characters** — leaves headroom for prefix / suffix additions downstream
- **Always preserves SAP acronyms verbatim** — PIR, BOM, MRP, PO, SO, GL, AP, AR, UoM, CoA, FI

## The 19 heuristics, in priority order

This is the **authoring checklist** — what a human weighs while writing the name. It is not the
same list as the 19 weighted checks the Studio's scorer computes (length, acronyms, ASCII and
punctuation are not scored at all); for those see [[std-rule-name-heuristics|Rule-Name Heuristics
(the 19, enumerated)]] and Rule-Name Scorer (engine). Both lists apply —
run the checklist, then check the score.

> [!warning] Two unrelated lists of 19 — the count is a coincidence
> This authoring checklist and the scorer's weighted heuristics in
> [[std-rule-name-heuristics]] both happen to contain 19 items. They are **not** the same 19, not a
> renumbering of each other, and not two views of one list — nothing matches item-for-item. Do not
> map one onto the other.

| # | Heuristic | What's measured | Weight |
|---|---|---|---|
| 1 | Length ≤ 100 | Hard cap | High |
| 2 | Length ≤ 85 | Soft target | Medium |
| 3 | Starts with an article ("A ", "An ", "The ") | Reads as a complete sentence | Medium |
| 4 | Uses "must" / "should" / "is" / "has" | Declarative phrasing | High |
| 5 | Names the entity in subject position | Reader knows what the rule is about | High |
| 6 | Names the attribute being checked | Reader knows what's being checked | High |
| 7 | Preserves SAP acronyms verbatim | Domain vocabulary integrity | Medium |
| 8 | No abbreviations of business terms | "Material" not "Mat", "Customer" not "Cust" | Low |
| 9 | No version / sprint numbers | Names are timeless | Medium |
| 10 | No client / project name in the rule itself | Reusable across engagements | Medium |
| 11 | Active voice | "must have" not "should be having" | Low |
| 12 | Singular noun for the subject | "A material" not "Materials" | Medium |
| 13 | No double-negatives | "must have" not "must not lack" | Medium |
| 14 | Specific verb on the check | "be a valid…" not just "be correct" | Medium |
| 15 | Includes criticality / domain context where helpful | "for finished goods" disambiguates universe | Low |
| 16 | No SQL technical terms in the name | "must have a valid UoM" not "MEINS must not be NULL" | High |
| 17 | Reads sensibly when prefixed "Rule:" | The tracker prepends "Rule:" — your name needs to follow gracefully | Low |
| 18 | No trailing punctuation | No periods or exclamations | Low |
| 19 | Plain ASCII (no smart quotes / em-dashes) | Round-trips through Excel + SQL | Low |

## Worked examples

### Good — *"A material must have a valid base unit of measure"*

- Length 47 — well under target
- Starts with "A material" — singular, subject-leading
- "must have" — active, declarative
- "base unit of measure" — full term, no abbreviation
- No SQL field names
- Score ≥ 0.85

### Bad — *"MEINS check"*

- Length 11 — too terse to read
- Uses a SQL field name (MEINS)
- Not a sentence
- Score ≤ 0.2

### Bad — *"Material data quality rule v3 — check MARA.MEINS is not null and not blank for FERT/HALB/ROH materials per Q2 2026 sprint"*

- Length 137 — over the hard 100 cap
- Includes version + sprint
- Uses SQL field names
- Compound conditions
- Score ≤ 0.3

## Steps

1. **Identify the entity** — the subject of the rule (Material, Customer, Vendor, Profit Center,
   GL Account)

2. **Identify the attribute** — what's being checked (base UoM, country code, currency, VAT
   number)

3. **Identify the constraint** — must have / must be valid / must match / must be unique

4. **Compose**: `"A [entity] must [constraint] [attribute]"`

5. **Optionally add scope** if it disambiguates: `"... for finished goods"`, `"... in the EU"`

6. **Drop into the Studio's single-rule editor** — the inline scorer shows your score immediately
   and flags any heuristics that didn't pass

## Pattern templates

| Constraint type | Template | Example |
|---|---|---|
| Presence | "A [entity] must have a [attribute]" | A material must have a base unit of measure |
| Format | "A [entity] must have a valid [attribute]" | A customer must have a valid VAT number |
| Consistency | "A [entity]'s [attr1] must match its [attr2]" | A customer's currency must match its company code currency |
| Uniqueness | "A [entity] must have a unique [attribute]" | A vendor must have a unique tax registration number |
| Reference | "A [entity]'s [attribute] must exist in [table]" | A GL posting's account must exist in the chart of accounts |
| Range | "A [entity]'s [attribute] must be [range]" | A document posting date must be within the current fiscal year |

## Common pitfalls

- Using "data" or "record" instead of the entity — *"A record must have …"* tells the reader
  nothing
- Saying "must not be null" — say what it should have instead (positive framing)
- Compound rules — *"A material must have a UoM and a description"* should be TWO rules, scored
  separately, fixable separately
- Field names in the rule name — *"MARA.MEINS must be populated"* leaks SQL into the business spec

## Checklist vs. Scorer — when to use each

**The authoring checklist** (the 19 items above) is your *personal guide* while you're writing the rule name. As you compose, mentally scan the checklist: "Did I include an article? Does it start with a determiner? Any possessives? Any SQL field names?" It's a thinking tool.

**The Studio scorer** is the *objective evaluator*. Once you've dropped your name into the rule editor, the scorer gives you an immediate 0–100 score and flags any heuristics that didn't pass. It's your automated quality gate.

**The workflow:**

1. **Authoring phase:** Use the checklist to guide composition. Aim for a name that addresses all 19 items (or as many as possible).
2. **Verification phase:** Paste your name into the Studio editor. The scorer shows you exactly which heuristics failed (red X) and which passed (green checkmark).
3. **Refinement phase:** Use the scorer's feedback to iterate. The scorer's suggestions are more precise than the checklist — it tells you which exact heuristic to fix, not just "something is wrong."

**Example 1:** Your name is "Material must have base unit." The checklist tells you "missing an article." The scorer shows you red X on heuristic #18 (Must Start with Determiner) — exact diagnosis. Revision: "A material must have a base unit." Score jumps from 0.65 to 0.88.

**Example 2:** Your name is "KNA1 records must have a valid country code." You followed the checklist, so you included an article and avoided some obvious pitfalls. But the scorer flags red X on heuristic #5 (No Technical Names) because `KNA1` is a SAP table name. The suggestion: use "Customer" instead. Revision: "A customer must have a valid country code." Score jumps from 0.72 to 0.95. The checklist alone wouldn't have caught this because you focused on grammar; the scorer catches domain-specific naming rules.

## Verification

After dropping the name into the Studio editor:

- Scorer shows ≥ 0.7 (target ≥ 0.85 for catalog promotion)
- Each red-X heuristic gets addressed before saving
- Pre-existing rules with the same intent are flagged — avoid duplicates

## Related

- [[std-implication-template|Implication Template]] — the description body for whatever rule you
  just named
- [[con-catalog-vs-bespoke-rules|Catalog vs Bespoke Rules]] — catalog rules use this same naming
  heuristic
- Studio — Rule-Name Scorer
- [[std-rule-name-heuristics|Rule-Name Heuristics (the 19, enumerated)]]
