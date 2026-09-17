---
id: prn-fetch-check-return
type: principle
title: Why Fetch-Check-Return
domain: rule-design
audience: [consultant]
level: practitioner
status: review
links:
  - relates:std-implication-template
  - relates:std-rule-description-template
  - relates:std-rule-description-template-profiling
  - relates:prc-format-an-implication
  - relates:prn-profiling-has-no-pass-fail
  - relates:con-rule-types
sources:
  - vault:thought-leadership/Why Fetch-Check-Return.md
tags: [thought-leadership]
created: 2026-08-20
updated: 2026-08-20
---

The three-bullet structure inside every rule description's section 3. Why these three verbs in
this order — and not something cleaner like a one-paragraph narrative.

## The problem we tried to solve

DQ rule descriptions written as free-form paragraphs varied wildly across consultants, sprints,
and clients. Three failure modes recurred:

1. **The "what" hidden in prose** — *"This rule validates that materials in MARA have a valid
   base unit of measure by checking that MEINS is not null or blank for active records."* Where's
   the WHAT exactly? Buried in a 30-word sentence.

2. **The scope unstated** — descriptions jumped straight to "check that…" without naming the
   universe. *"What records does this apply to? Only finished goods? All plants?"*

3. **The impact missing** — descriptions said "marks records as defective" but not what
   *defective* means downstream. The remediator was left guessing.

## Why three explicit bullets

Forcing the author to write **Fetch / Check / Return** separately:

- **Fetch** isolates the data acquisition step — which tables, which joins. A reviewer can spot
  a missing join just by reading this bullet.
- **Check** isolates the defect condition — one place to look for the failure logic. A reviewer
  auditing 50 rules can scan just this line for each.
- **Return** isolates the impact — what does a defect actually mean for the business? Forces the
  author to think about consequences, not just mechanics.

The redundancy with the SQL is intentional. The SQL is one source of truth for *how* the check
runs; the Implication is the source of truth for *why* it matters.

### How each bullet isolates a concern — example

Let's apply this to a real rule to see how Fetch, Check, and Return each isolate one concern:

**Rule:** *"Active material must have valid base unit of measure"*

**Fetch — isolates data acquisition:**
- *"All finished-goods and semi-finished materials from MARA where LVORM ≠ 'X' (not deleted), scoped to system Z01."*
- A reviewer can instantly spot: "Which material types? FERT and HALB only. Do we include deleted materials? No. Which system? Z01."
- If a join is missing (e.g., forgetting to filter out test materials or material hierarchies), the Fetch line reveals it immediately.

**Check — isolates the defect condition:**
- *"Verify that MEINS (base unit of measure) is not null and is not blank."*
- A reviewer scanning 50 rules can read just this line from each and instantly understand the validation logic.
- This is the only place the error condition appears in the rule description — no hidden logic elsewhere.

**Return — isolates the business impact:**
- *"Flag materials without a valid UoM. Without a base unit of measure, planning modules cannot calculate demand, inventory cannot be costed, and supply-chain execution cannot fulfill customer orders."*
- This forces the author to think beyond mechanics: *Why does this matter?* Not just "mark it broken", but "mark it broken because X downstream consequence."
- A remediator reading this knows: *"I need to assign a proper UoM based on the material's physical characteristics, not just fill in a default."*

**The payoff:** A reviewer can audit the scope in 10 seconds, the check logic in 5, and the business impact in 15. Total: 30 seconds per rule. Scanning 50 rules: 25 minutes. If logic were embedded in prose, scanning the same 50 would take hours.

## Before and after — the same rule, two ways

**The old way (free-form paragraph):**

> This rule validates that materials in the MARA table have a valid base unit of measure by checking that MEINS is not null or blank for active finished-goods and semi-finished materials so that planning and costing modules can calculate quantities and costs without error.

*Problems:* One 40-word sentence buries the WHAT, WHERE, and WHY. A reviewer has to parse it all at once. What's the universe? What exactly fails? Why does it matter?

**The new way (Fetch / Check / Return):**

- **Fetch** — All finished-goods and semi-finished materials from MARA where LVORM ≠ 'X' (not deleted), scoped to system Z01.
- **Check** — Verify that MEINS (base unit of measure) is not null and not blank.
- **Return** — Flag records where MEINS is missing. Without a valid UoM, planning modules cannot calculate demand, inventory cannot be costed, and supply-chain execution stalls.

*Benefits:* Three bullets, each answering one question. A reviewer can audit the scope in 10 seconds, the check logic in 5, and the impact in 15. Scanning is fast. Reuse is easy (the Check is reusable; other rules might re-fetch the same universe).

## Why these three verbs, not others

| Considered | Rejected because |
|---|---|
| Read / Compare / Output | Too generic; doesn't fit profiling |
| Query / Validate / Surface | "Validate" loaded — implies pass/fail, doesn't fit Info or Profiling |
| Identify / Inspect / Report | "Inspect" is reviewer language, not engine language |
| Pull / Apply / Flag | Reads as engineering jargon |
| **Fetch / Check / Return** | All three are common-English verbs with clear meanings in DQ context; "Check" has natural pass/fail semantics; "Return" forces the impact-thinking |

For profiling, the substitution to **Fetch / Profile / Surface** keeps the same three-beat
rhythm while swapping the middle/end verbs to match the actual contract (no pass/fail, surfaces
a distribution — see [[prn-profiling-has-no-pass-fail]]).

## The downstream payoff

The Fetch/Check/Return structure appears across the entire DQ workflow. Understanding where and why it's reused shows why the three-bullet discipline matters.

**Spec Markdown** — the source of truth
- The rule specification document (often a markdown file or wiki page) that consultants author and maintain
- Contains the rule name, description (with Fetch/Check/Return bullets), SQL logic, scope, and implications
- This is the one place the business logic lives; everything else references it

**SKP AssetUpload's Implication cell** — verbatim copy
- SKP is Syniti's DQ execution platform where rules run, report results, and feed data to downstream systems
- When you upload a rule to SKP, the Implication cell (which explains the business context) is populated with the Fetch/Check/Return bullets copied **verbatim** from the spec
- SKP users (data stewards, auditors) read this cell to understand *why* the rule matters and *what* constitutes a defect

**The Audit Screen** — parity comparison
- A visual screen where auditors compare: "Does what we're actually checking match what we documented we would check?"
- The Audit screen pulls the Fetch/Check/Return bullets from SKP and lines them up against the OptSel/RptSel SQL logic
- If the SQL and the bullets disagree (e.g., Fetch says "FERT only" but OptSel evaluates all material types), it's an audit finding

**Parity Comparison** — automated validation
- A report that checks whether the Spec Markdown matches the deployed SKP rule matches the actual SQL
- Fetch/Check/Return being in all three (spec, SKP, SQL) makes parity checkable: compare the three documents side-by-side
- If they diverge, the rule has drift and needs correction

**Client-facing deliverables** — stakeholder communication
- Consultants paste the Fetch/Check/Return bullets directly into executive summaries, risk assessments, and quality reports
- Business stakeholders (who don't read SQL) can understand the rule's purpose and impact in plain language
- One consistent template means no translation or re-authoring needed

**Why this matters:** The Fetch/Check/Return structure is **one template used by four different audiences** (spec authors, SKP operators, auditors, executives). Because all four use the exact same three bullets, consistency is guaranteed at every touch point. If the bullets are clear, the spec is clear. If the spec is clear, the audit is defensible. If the audit is defensible, the client signs off.

## Related

- [[std-implication-template]]
- [[std-rule-description-template]]
- [[std-rule-description-template-profiling]]
- [[prc-format-an-implication]]
- [[prn-profiling-has-no-pass-fail]] — why the profiling variant swaps Check/Return
- [[con-rule-types]] — the Error/Info/Profiling split this triplet serves
