---
id: prc-format-an-implication
type: procedure
title: Format an Implication
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:sops/SOP — Format an Implication.md
tags: [sop, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:std-implication-template
  - relates:std-rule-description-template
  - relates:std-rule-description-template-profiling
  - relates:std-skp-rule-identifier-convention
  - relates:prn-fetch-check-return
  - relates:con-rule-types
  - relates:ref-skp-assetupload-and-tracker-flow
  - relates:prc-derive-a-dq-rule
---

## Goal

How to write or fix the Implication for a DQ rule so it lands correctly in both the markdown
spec AND the SKP AssetUpload.

## What is an Implication?

An **Implication** is the **business-language description** of a DQ rule — the three-section narrative that explains **why** the rule matters, **what** records it checks, and **what the error condition means**. 

It is **not** the SQL. It is the bridge between:
- **Business stakeholders** (who understand the impact but not SQL syntax)
- **The SQL code** (which is precise but hard to audit without context)
- **The SKP tracker and audit screens** (which display the Implication as the user-facing explanation)

### How Implications Influence Rule Logic

1. **Scope clarity** — Section 2 (Scope) defines the *universe* of records being checked. If it says "active materials only," deletion flags go in WHERE. If it says "all materials," deletion flags might go in the CASE (depending on intent).

2. **Error condition source of truth** — Section 3 (Check) states the error condition in plain English **before** the SQL is written. If the Check says "delivery date is earlier than order date," the SQL must match that logic exactly. If the SQL does something else, the Implication has exposed a mismatch.

3. **Audit defense** — When a client disputes a flagged defect, the Implication is the first document reviewed. A precise Implication makes it clear whether the rule is working as intended or whether the SQL drifted from the original intent.

4. **SQL generation** — The deriver uses the Implication (especially Section 3's Check) to inform its SQL generation. A clear, specific Check produces more accurate SQL than a vague one.

## When to use

- Authoring a new rule
- The AssetUpload's Implication cell is empty or shows garbage
- The bulk pipeline auto-generated an Implication that needs editing
- A reviewer flagged the wording as unclear

## Prerequisites

- The rule's name, primary table(s), key field(s), and high-level intent in your head OR
  documented in the spec markdown
- A copy of [[std-implication-template|Implication Template]] in another window

## Steps

### 1. Identify the rule type

- Error / Info → use the **Fetch / Check / Return** triplet
- Profiling → use the **Fetch / Profile / Surface** triplet

If unsure, look at the SQL view suffix: `_OptSel` / `_RptSel` = Error or Info; `_PrfSel` /
`_PrfSum` = Profiling.

### 2. Draft section 1 — Functional/Business Description

Answer: *"Why does this rule matter to the business?"*

- Speak in business outcomes — what breaks if the rule's condition is violated, what risk it
  creates
- Avoid jargon — a finance director should understand what the rule does without an SAP manual
- 1-2 sentences

> [!tip]
> **Good:** "A material missing a base unit of measure cannot be planned, costed, or transacted
> by SAP — a hard blocker for downstream MM/PP/SD flows."
>
> **Bad:** "Checks MARA.MEINS for NULL or empty values across the FERT material universe."

**Common mistakes to avoid:**

| Mistake | Example | Why It's Wrong | Correct Version |
|---------|---------|---|---|
| **Technical field names** | "Checks MARA.MEINS for NULL" | Client doesn't know SAP table names | "Material missing base unit of measure" |
| **SQL-like language** | "WHERE LVORM <> 'X' AND MEINS IS NOT NULL" | Too technical; looks like code | "Active materials with recorded units" |
| **Acronyms without context** | "Material UOM must be present" (UOM = Unit of Measure) | Client might not know the jargon | "Material must have a unit of measure" |
| **Vague business impact** | "Data quality issue with materials" | No context on why it matters | "Missing units prevent accurate costing and planning" |
| **Too much detail** | "Checks the MEINS field in MARA table against a list of 47 valid UOM codes from the TUNIT table, joining on..." | Client wants the "why", not the "how" | "Material units must be valid and recognized" |
| **Passive voice** | "The MEINS field is checked to see if it is NULL" | Weak, hard to scan | "A material must have a non-empty unit of measure" |
| **Multiple rules in one** | "Material must have unit AND must have valid type AND must be active" | Spreads the focus; sounds like three rules | Write three separate implications |

### 3. Draft section 2 — Specific Relevancy Criteria/Scope

Answer: *"Which records does the rule apply to?"*

- Name the primary table(s) and the universe definition
- Include major filters (e.g., deletion flags, status codes, material types)
- One sentence **only**
- **No SQL details** — no WHERE clause mechanics, no join conditions

**For complex multi-table rules:** Mention only the **primary table being checked**. Join tables belong in Fetch, not Scope.

> [!tip]
> **Good:** "Applies to all active (non-deletion-flagged) finished, semi-finished and raw materials in MARA, across all plants, per-system fan-out scope."
>
> **Also good (multi-table):** "Applies to all sales order line items in VBAP that have been created in the last 12 months, with no deletion flags."
>
> **Bad:** "All materials." (vague, no universe definition)
>
> **Bad (too technical):** "All non-deleted MARA records joined to VBAP, MSEG, EKPO on MATNR with zSourceSystemID alignment, filtered by LVORM <> 'X'." (join mechanics belong in Fetch, not Scope)

### 4. Draft section 3 — the triplet

Three bullets, exactly:

**Error/Info:**

```
- **Fetch** <br /> Retrieve all records from <table>, joined with <join_tables>.
- **Check** <br /> Mark any record where: <condition in human terms>.
- **Return** <br /> Error records are <what they break / prevent>.
```

**Profiling:**

```
- **Fetch** <br /> Retrieve all records from <table>, joined with <join_tables>.
- **Profile** <br /> Group by <grouping>; compute COUNT and percentage-within-segment.
- **Surface** <br /> A distribution dataset showing where <attribute> is concentrated,
  scattered, or unused.
```

### Fetch: How Much Detail for Multi-Table Rules?

For rules with multiple joins, balance clarity with brevity:

| Detail Level | Example | Acceptable? |
|---|---|---|
| **Too sparse** | "Retrieve data" | ❌ No — readers don't know which tables |
| **Just right** | "Retrieve all records from `MARA`, joined with `VBAP` for sales order context and `MSEG` for goods movement dates" | ✅ Yes — tables named, joins justified |
| **Too technical** | "Inner-join MARA to VBAP on MATNR, left-join to MSEG on MATNR/zSourceSystemID with CTE pre-aggregation of movements grouped by system" | ❌ No — SQL mechanics, not business context |
| **Also too technical** | "Retrieve records after pre-aggregating movement history by system and material to prevent row multiplication when joining back" | ⚠️ Borderline — explain the **why**, not the **how** |

**Rule:** Name the tables and **briefly justify each join** ("for sales order context", "for approval dates", "for system-level aggregation"). Skip the SQL mechanics (CTEs, ON conditions, WHERE clauses) — those live in the SQL.

**For many joins (3+):** List tables in dependency order. Group related tables if helpful.

> [!example]
> **Good (3-table rule):**
> ```
> - **Fetch** <br /> Retrieve all records from `MARA`, joined with `VBAP` for recent sales 
>   order activity and `EKPO` for recent purchase order activity.
> ```
>
> **Also good (justifies aggregation without SQL):**
> ```
> - **Fetch** <br /> Retrieve all records from `MARA` with the most recent goods movement, 
>   sales order, and purchase order dates aggregated per material and system.
> ```
>
> **Not good (too technical):**
> ```
> - **Fetch** <br /> Retrieve MARA with CTEs pre-aggregating MSEG, VBAP, EKPO grouped by 
>   MATNR and zSourceSystemID, left-joined on primary key match and system alignment.
> ```

### 5. Append the SKP_RULE_ID anchor

```
***SKP_RULE_ID: SKP_RULE_NNNN***
```

Blank line before it. Triple-asterisk. Wrap the NNNN with the actual zero-padded 4-digit ID.

### Complete Example: All Three Sections Together

Here's a fully composed Implication ready for export to SKP:

```markdown
**1. Functional/Business Description**
A sales order line must have a valid delivery date that falls after the order creation date. 
Orders with future delivery dates indicate either data entry errors or unrealistic customer 
expectations, blocking order fulfillment and creating downstream logistics delays.

**2. Specific Relevancy Criteria/Scope**
Applies to all sales order line items in VBAP created within the last 90 days, across all 
sales organizations and distribution channels, excluding cancelled orders (ABGRU <> 'C').

**3. DQ Checks (Conditions)**
- **Fetch** <br /> Retrieve all records from VBAP, joined with VBAK for order creation date and KNA1 for customer 
  context.
- **Check** <br /> Mark any record where: delivery date (EDATU) is NULL, empty, or earlier than order creation date (ERDAT).
- **Return** <br /> Error records are sales orders at risk of fulfillment failure; require manual review and 
  customer communication before picking and packing.

***SKP_RULE_ID: SKP_RULE_0089***
```

**What to notice:**

| Component | Example | Why |
|-----------|---------|-----|
| **Section 1** | "Orders with future delivery dates indicate...blocking order fulfillment" | Business impact, not mechanics |
| **Section 2** | "...created within the last 90 days, excluding cancelled orders (ABGRU <> 'C')" | Universe definition + scope filters |
| **Fetch** | "...joined with VBAK for order creation date..." | Why the join, not the SQL mechanics |
| **Check** | "...delivery date is NULL, empty, or earlier than order date..." | Business language, not code |
| **Return** | "...at risk of fulfillment failure; require manual review..." | Impact on the downstream process |
| **Anchor** | `***SKP_RULE_ID: SKP_RULE_0089***` | Triple-asterisk, bold-italic, 4-digit zero-padded ID |

### 6. Drop into the spec

In Obsidian-edited markdown: replace the spec's `### Description` block with your new content.
The bulk pipeline auto-picks it up from there into the SKP exporter.

In the Studio UI: paste into the spec editor's description field, save.

## Verification

After re-running the SKP AssetUpload export, open the AssetUpload.xlsx in Excel, navigate to
the Rules sheet, find your rule by SKP_RULE_NNNN, and confirm the Implication cell shows:

- All three sections (1, 2, 3)
- `<br />` rendered as line breaks (not literal text — actual breaks)
- SKP_RULE_ID anchor at the bottom in bold-italic

If anything looks wrong, check:

- The bulk session has the latest spec (re-export the bulk zip if you edited the markdown
  externally)
- The pipeline ran with the spec markdown matching the latest state (re-save in the Studio UI
  after an external edit so the session picks it up)

## Common pitfalls

- **`<br />` shows as literal text** — you used `<br>` (HTML4) or `<br/>` (no space). The
  Studio exporter looks for the exact `<br />` form.
- **Section header doesn't render bold** — you used `**1. Description**` (which IS correct) but
  the markdown viewer is rendering it as a hashtag-style header. Re-check the bold-asterisks
  are paired.
- **Empty Implication cell** — the spec's `description` field is empty. Re-author the
  description.
- **Wrong SKP_RULE_ID** — siblings of the same conceptual rule must share the SKP_RULE_NNNN. If
  two siblings show different IDs, the spec metadata is broken — re-fan-out the rule to
  regenerate it.

## Related

- [[std-implication-template|Implication Template]]
- [[std-rule-description-template|Rule Description Template — Error and Info]]
- [[std-rule-description-template-profiling|Rule Description Template — Profiling]]
- [[std-skp-rule-identifier-convention|SKP_RULE Identifier Convention]]
- [[prn-fetch-check-return|Why Fetch-Check-Return]]
- [[prc-derive-a-dq-rule|Derive a DQ Rule (single rule)]] — the end-to-end procedure this step fits into
