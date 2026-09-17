---
id: prc-derive-a-dq-rule
type: procedure
title: Derive a DQ Rule (single rule)
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:sops/SOP — Derive a DQ Rule.md
  - academy:index.html#deterministic-derivation
  - academy:index.html#ai-enhancement
  - academy:index.html#interpret-output
  - academy:index.html#apply-corrected
tags: [sop]
created: 2026-08-20
updated: 2026-08-21
links:
  - prereq:prc-write-a-quality-rule-name
  - prereq:prc-studio-onboarding
  - relates:prc-format-an-implication
  - relates:std-implication-template
  - relates:std-view-naming-patterns
  - relates:std-optsel-select-structure
  - relates:std-output-field-sections
  - relates:ref-single-rule-designer
  - relates:ref-ai-static-validator-gate
  - relates:con-multi-implementation-model
  - relates:gls-sibling-implementation
  - relates:qa-sample-rule-review-before-authoring
  - relates:qa-ai-enhance-accept-vs-review
  - relates:qa-when-additional-cte-acceptable
---

## Goal

End-to-end procedure for going from a rule name to a deployable, reviewable, exported DQ rule
using the Studio's single-rule designer.

## When to use

- Authoring a new rule for review before bulk inclusion
- Adapting a catalog rule to a project-specific scope
- Demoing the methodology to a client / new team member

## The Derivation Workflow

Here's the overall process from rule name to deployable spec:

```
┌──────────────────────────────────────────────────────────┐
│ 1. RULE NAME & INTENT                                    │
│    "A material must have activity in the last 2 years"   │
└────────────────────┬─────────────────────────────────────┘
                     │
                     v
┌──────────────────────────────────────────────────────────┐
│ 2. DERIVATION (Local Derive or AI Derive)                │
│    ├─ Domain identified: Material                         │
│    ├─ Spec generated: Output fields, joins, filters      │
│    └─ SQL generated: OptSel + RptSel views               │
└────────────────────┬─────────────────────────────────────┘
                     │
                     v
┌──────────────────────────────────────────────────────────┐
│ 3. REVIEW THE SPEC (You validate)                        │
│    ├─ Output Fields: 5 sections present?                 │
│    ├─ Logic: Error condition correct?                    │
│    ├─ Joins: Left outer + zSourceSystemID?               │
│    └─ Filters: Deletion flags in WHERE?                  │
└────────────────────┬─────────────────────────────────────┘
                     │
                     v
┌──────────────────────────────────────────────────────────┐
│ 4. (OPTIONAL) AI ENHANCE                                 │
│    ├─ AI reviews SQL against spec                        │
│    ├─ Proposes corrections & sample data                 │
│    └─ You accept, reject, or selectively accept          │
└────────────────────┬─────────────────────────────────────┘
                     │
                     v
┌──────────────────────────────────────────────────────────┐
│ 5. WRITE DESCRIPTION (Implication)                       │
│    ├─ Fetch / Check / Return triplet                     │
│    └─ Tag SKP_RULE_ID anchor                             │
└────────────────────┬─────────────────────────────────────┘
                     │
                     v
┌──────────────────────────────────────────────────────────┐
│ 6. EXPORT & STAGE                                        │
│    ├─ Download markdown spec                             │
│    ├─ Drop into project spec folder                      │
│    └─ Ready for bulk pipeline or handoff                 │
└──────────────────────────────────────────────────────────┘
```

## Prerequisites

- Studio running locally (see install docs)
- Project selected (sap_ecc or sap_s4hana)
- Anthropic API key set if you want AI Derive / AI Enhance (optional — Local Derive works
  without)

## Before you start: Review an example rule

Before writing your first rule, read the following well-structured rule **end-to-end**. It demonstrates the correct pattern: CTEs (to prevent fan-out), multi-signal logic, proper commenting, all five output field sections, and both OptSel + RptSel views. See [[qa-sample-rule-review-before-authoring|Should I review an example rule?]] for guidance on what patterns to recognize.

### Example: Material Activity Date Rule

```sql
-- ============================================================
-- DQ Rule: A material must have recorded activity within the last two years
-- Rule ID: 0001
-- View: Opportunity Report (OptSel) (DQ_0001_P02_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_OptSel)
-- Generated: 2026-08-11T13:54:14
-- Target: MS SQL Server
-- ============================================================

CREATE VIEW [dbo].[DQ_0001_P02_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_OptSel] AS

/* Derive the most recent activity date per material from three independent
activity signals before joining to the material master, so the master
record is never fanned out to multiple rows */
WITH cte_material_movements AS (
/* Most recent goods movement date per material from material document items */
SELECT
mseg.MATNR,
mseg.zSourceSystemID,
MAX(mseg.BUDAT_MKPF) AS last_movement_date
FROM [WRKDQ].[dbo].[MSEG] AS mseg
INNER JOIN [WRKDQ].[dbo].[MKPF] AS mkpf
/* Join material document items to their header to access posting date;
same-field join requires source system alignment */
ON mkpf.zSourceSystemID = mseg.zSourceSystemID
AND mkpf.MBLNR = mseg.MBLNR
AND mkpf.MJAHR = mseg.MJAHR
GROUP BY mseg.MATNR, mseg.zSourceSystemID
),

cte_sales_orders AS (
/* Most recent sales order creation date per material from sales order items */
SELECT
vbap.MATNR,
vbap.zSourceSystemID,
MAX(vbak.ERDAT) AS last_sales_date
FROM [WRKDQ].[dbo].[VBAP] AS vbap
INNER JOIN [WRKDQ].[dbo].[VBAK] AS vbak
/* Join sales items to their header to access order date;
same-field join requires source system alignment */
ON vbak.zSourceSystemID = vbap.zSourceSystemID
AND vbak.VBELN = vbap.VBELN
GROUP BY vbap.MATNR, vbap.zSourceSystemID
),

cte_purchase_orders AS (
/* Most recent purchase order date per material from PO line items */
SELECT
ekpo.MATNR,
ekpo.zSourceSystemID,
MAX(ekko.BEDAT) AS last_po_date
FROM [WRKDQ].[dbo].[EKPO] AS ekpo
INNER JOIN [WRKDQ].[dbo].[EKKO] AS ekko
/* Join PO items to their header to access document date;
same-field join requires source system alignment */
ON ekko.zSourceSystemID = ekpo.zSourceSystemID
AND ekko.EBELN = ekpo.EBELN
GROUP BY ekpo.MATNR, ekpo.zSourceSystemID
)

SELECT

-- Syniti Technical Fields
mara.zSourceSystemID AS [zSourceSystemID],
CONCAT(mara.zSourceSystemID, '_', mara.MATNR) AS [zConcatenatedKey],

/* Error when no activity signal falls within the last two years;
a NULL across all three signals also counts as no activity */
CASE
WHEN GREATEST(
ISNULL(CONVERT(DATE, mov.last_movement_date), '1900-01-01'),
ISNULL(CONVERT(DATE, so.last_sales_date), '1900-01-01'),
ISNULL(CONVERT(DATE, po.last_po_date), '1900-01-01')
) < CAST(DATEADD(YEAR, -2, GETDATE()) AS DATE)
THEN 1 /* Most recent activity across all signals is older than two years */
ELSE 0
END AS [zIsErrorFlag],

-- Basic Fields (Primary Key + Context)
mara.MATNR AS [Material Number],
mara.MTART AS [Material Type],
mara.MATKL AS [Material Group],

-- Activity Context (Value Field Under Check)
CONVERT(DATE, mov.last_movement_date) AS [Last Goods Movement Date],
CONVERT(DATE, so.last_sales_date) AS [Last Sales Order Date],
CONVERT(DATE, po.last_po_date) AS [Last Purchase Order Date],
CAST(
GREATEST(
ISNULL(CONVERT(DATE, mov.last_movement_date), '1900-01-01'),
ISNULL(CONVERT(DATE, so.last_sales_date), '1900-01-01'),
ISNULL(CONVERT(DATE, po.last_po_date), '1900-01-01')
) AS DATE) AS [Most Recent Activity Date],
CAST(DATEADD(YEAR, -2, GETDATE()) AS DATE) AS [Two Year Threshold Date]

FROM [WRKDQ].[dbo].[MARA] AS mara

LEFT JOIN cte_material_movements AS mov
/* Bring in the most recent goods movement for this material */
ON mov.zSourceSystemID = mara.zSourceSystemID
AND mov.MATNR = mara.MATNR

LEFT JOIN cte_sales_orders AS so
/* Bring in the most recent sales order activity for this material */
ON so.zSourceSystemID = mara.zSourceSystemID
AND so.MATNR = mara.MATNR

LEFT JOIN cte_purchase_orders AS po
/* Bring in the most recent purchase order activity for this material */
ON po.zSourceSystemID = mara.zSourceSystemID
AND po.MATNR = mara.MATNR

WHERE
/* Exclude records flagged for deletion at the general material level */
ISNULL(mara.LVORM, '') <> 'X'
/* Limit scope to source system P02 */
AND mara.zSourceSystemID = 'SRCECCZ02100'
;

-- ============================================================
-- DQ Rule: A material must have recorded activity within the last two years
-- Rule ID: 0001
-- View: Defects Report (RptSel) (DQ_0001_P02_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_RptSel)
-- Generated: 2026-08-11T13:54:14
-- Target: MS SQL Server
-- ============================================================

CREATE VIEW [dbo].[DQ_0001_P02_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_RptSel] AS
SELECT
*
FROM [dbo].[DQ_0001_P02_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_OptSel]
WHERE [zIsErrorFlag] = 1
;
```

**What to notice in this example:**

| Pattern | Why It Matters |
|---|---|
| **Three CTEs pre-aggregate** | Each CTE groups by (MATNR, zSourceSystemID) to avoid fanning out the material record to multiple rows when joining back |
| **Every CTE joins on zSourceSystemID** | Cross-system correctness — a join without zSourceSystemID can match wrong records in multi-system environments |
| **Comments explain joins, not mechanics** | "Join to header to access posting date" (why) not "join MSEG to MKPF" (what) |
| **Five field sections in order** | Technical → Basic → Org → Value → Activity. zIsErrorFlag is in the Technical section, first. |
| **zIsErrorFlag uses CASE, not WHERE** | Status/validity logic belongs in CASE; exclusions (deletion flags, system filters) belong in WHERE |
| **OptSel + RptSel pair** | OptSel shows all records (with error flag); RptSel filters to errors only (`WHERE [zIsErrorFlag] = 1`) |
| **GREATEST to unify multi-signal logic** | When checking "any of three dates", GREATEST finds the max; NULL handling with ISNULL lets missing signals be ignored |

Once you recognize this shape, authoring a new rule becomes pattern-matching, not starting from blank.

---

## Steps

### 1. Author the rule name

Use [[prc-write-a-quality-rule-name|Write a Quality Rule Name]]. Aim for score ≥ 0.7. Example:
*"A material must have a recorded activity within the last two years"*.

> [!important] Precision prevents AI guessing
> A vague rule name (e.g., "A material must be valid") invites Claude to guess what "valid" means and add unrequested logic. A precise name (e.g., "A material must have recorded activity within the last two years") tells Claude exactly what to check. Spend time on clarity here — it pays off later.

### 2. Pick the derivation path

| Path | When |
|---|---|
| **Local Derive** (default) | The Studio's knowledge base covers the domain — fast, deterministic, no API call |
| **AI Derive** | The domain is unusual OR Local Derive returns a thin spec — Claude reads + builds a full spec |
| **Catalog import** | The rule exists in the Syniti AI Generated Rule Catalog 2025 — import by catalog ID |

> [!tip] Local Derive is deterministic
> Re-derive the exact same rule name + inputs next month and you get byte-identical SQL — same
> field order, same comments, same `zSourceSystemID` placement. Nothing about the input (a new
> exclusion, a different field) changes the output unless you change the input. That's what keeps
> git diffs meaningful (you see only the logic you actually changed) and makes the output
> certifiable to an auditor: "here's the rule, generate it again, you get the same output."

### 3. Review the spec

Studio populates: rule identity → output fields (5 sections) → logic → joins → filters. Walk
through each:

- **Output Fields** — Are all five sections present? (Tech / Basic / Org / Value / Activity).
  Are Basic Fields the PK + key descriptive columns? Is the Value Context field actually the
  field under check?
- **Logic** — The `zIsErrorFlag` CASE expression. Does it match the rule's intent? Is the
  condition self-explanatory with a comment?
- **Joins** — Are joins LEFT OUTER unless we genuinely require a match? Do they include
  `AND zSourceSystemID = ...` for cross-system safety?
- **Filters** — WHERE-clause restrictions. Are deletion flags in WHERE (not CASE)? Are status
  fields in CASE (not WHERE)?

#### Good vs. Incorrect Examples

**GOOD — Output Fields (5 sections, correct order):**

| Section | Field | Example | ✅ Correct |
|---------|-------|---------|---|
| **Technical** | zSourceSystemID | SRCECC02100 | Required |
| **Technical** | zConcatenatedKey | 'SRCECC02100_M001' | (MATNR) |
| **Technical** | zIsErrorFlag | 0 (valid) or 1 (error) | Integer 1/0 |
| **Basic** | MATNR | M001 | PK |
| **Basic** | MAKTX | Material Desc | Descriptive |
| **Org** | WERKS | Plant 1000 | Organizational context |
| **Value** | MEINS | EA | Field under check |
| **Activity** | LAEDA | 2026-08-31 | Change date |

✅ **Correct:** All 5 sections present, in order, with the right field types.

---

**INCORRECT — Output Fields (missing section, wrong order):**

| Section | Field | Issue | ❌ Wrong |
|---------|-------|-------|---|
| **Technical** | zSourceSystemID | Present | OK |
| **Technical** | zIsErrorFlag | Present | OK |
| **Basic** | MATNR | Present | OK |
| ~~**Org** MISSING~~ | — | No plant/org context | ❌ Missing section |
| **Value** | MEINS | Present | OK |
| **Activity** | LAEDA | Placed before Value | ❌ Wrong order |

❌ **Incorrect:** Missing Org section, Activity before Value.

---

**GOOD — Joins (LEFT OUTER, zSourceSystemID safety):**

```sql
SELECT
  mara.MATNR,
  mara.zSourceSystemID
FROM [WRKDQ].[dbo].[MARA] AS mara
LEFT OUTER JOIN [WRKDQ].[dbo].[MAKT] AS makt
  ON makt.zSourceSystemID = mara.zSourceSystemID  ✅ System alignment
  AND makt.MATNR = mara.MATNR
LEFT OUTER JOIN [WRKDQ].[dbo].[MARC] AS marc
  ON marc.zSourceSystemID = mara.zSourceSystemID  ✅ System alignment
  AND marc.MATNR = mara.MATNR
```

✅ **Correct:** LEFT OUTER, zSourceSystemID on every join.

---

**INCORRECT — Joins (INNER JOIN, missing zSourceSystemID):**

```sql
SELECT
  mara.MATNR,
  mara.zSourceSystemID
FROM [WRKDQ].[dbo].[MARA] AS mara
INNER JOIN [WRKDQ].[dbo].[MAKT] AS makt
  ON makt.MATNR = mara.MATNR  ❌ No zSourceSystemID
```

❌ **Incorrect:** INNER JOIN (eliminates nulls), missing zSourceSystemID (cross-system risk).

---

**GOOD — Filters (deletion flags in WHERE, status in CASE):**

```sql
WHERE
  mara.zSourceSystemID = 'SRCECC02100'
  AND ISNULL(mara.LVORM, '') <> 'X'  ✅ Deletion flag in WHERE
  AND mara.MTART IN ('FERT', 'HALB')
CASE
  WHEN mara.MEINS IS NULL THEN 1  ✅ Business logic (null check) in CASE
  ELSE 0
END AS [zIsErrorFlag]
```

✅ **Correct:** Deletion flags filter rows out; business logic in CASE.

---

**INCORRECT — Filters (deletion flag in CASE, status in WHERE):**

```sql
WHERE
  mara.zSourceSystemID = 'SRCECC02100'
  AND mara.MTART IN ('FERT', 'HALB')
CASE
  WHEN ISNULL(mara.LVORM, '') <> 'X' THEN 1  ❌ Deletion flag in CASE
  WHEN mara.MEINS IS NULL THEN 1
  ELSE 0
END AS [zIsErrorFlag]
```

❌ **Incorrect:** Deletion flag in CASE (soft filter), creates confusion about what "error" means.

### 4. Inspect the generated SQL

The Studio renders OptSel + RptSel inline. Read top-to-bottom:

- Banner header has Rule ID + view name
- 5-section SELECT with comments
- Joins commented (purpose, not mechanics)
- WHERE with `/* Exclude: ... */` and `/* Include: ... */` per-filter comments
- zIsErrorFlag CASE with the defect-condition comment
- RptSel is the canonical `SELECT * FROM <OptSel> WHERE [zIsErrorFlag] = 1`

If anything's missing or wrong, edit the spec — DON'T edit the SQL by hand. Spec is the source
of truth.

### 5. (Optional) AI Enhance

Click **AI Enhance**. The AI reviews the SQL against the spec, suggests corrections, and synthesizes a sample-data preview. This single operation produces all three outputs automatically:

- **Corrected SQL diff** — apply if it improves clarity
- **Sample data** — 5-10 rows showing what the OptSel would return. Look right? Apply.
- **Spec changes** — if the AI noticed a missing field, accept the spec edits

All three run together; you cannot toggle them individually. You review all three and decide whether to accept or reject the enhancements as a group (or selectively accept parts).

**What to check in the diff before accepting.** Claude's SQL is advisory — it's reviewing the
*deterministic* SQL the deriver already produced, not replacing your intent. Walk the same
checklist you'd apply to your own SQL:

- Header block still has rule name, ID, view type, date, target platform
- All five field sections still present, still in order (Technical → Basic → Org → Value →
  Activity)
- `zSourceSystemID` still filtered in the main table WHERE, every join ON, and every CTE
- `zIsErrorFlag` is still an INTEGER 1/0, never text
- Your exclusions (deletion flags especially) are still in the WHERE, not folded into the CASE

**If Claude added unrequested logic:** This is a signal your rule name or description isn't precise enough. See [[qa-ai-enhance-accept-vs-review|When should I accept or reject unrequested AI logic?]] for the decision tree.

**Key principle:** Vague rule names invite AI guessing. A precise rule name ensures AI only fills in what's needed. For example:
- ❌ "A customer must be valid" (vague → AI adds multiple validity checks)
- ✅ "A customer must have a non-empty name and email" (precise → AI only checks these fields)

### Examples: What to Accept vs. What to Review

#### ✅ SAFE TO ACCEPT — No Logic Change

**Example 1: Clarifying comment on join logic**
```diff
  INNER JOIN [WRKDQ].[dbo].[VBAK] AS vbak
-   ON vbak.zSourceSystemID = vbap.zSourceSystemID
-   AND vbak.VBELN = vbap.VBELN
+   /* Match on system and order number; join order items (vbap) to 
+      order header (vbak) to access order date; system alignment is 
+      critical because zSourceSystemID may differ in real data */
+   ON vbak.zSourceSystemID = vbap.zSourceSystemID
+   AND vbak.VBELN = vbap.VBELN
```
✅ **Action:** Accept. Comments clarify without changing logic.

---

**Example 2: Formatting consistency (aliases, indentation)**
```diff
-SELECT mseg.MATNR, mseg.zSourceSystemID, MAX(mseg.BUDAT_MKPF) AS last_movement_date
-FROM [WRKDQ].[dbo].[MSEG] AS mseg
+SELECT
+  mseg.MATNR,
+  mseg.zSourceSystemID,
+  MAX(mseg.BUDAT_MKPF) AS last_movement_date
+FROM [WRKDQ].[dbo].[MSEG] AS mseg
```
✅ **Action:** Accept. Formatting improves readability; no logic change.

---

**Example 3: Adding column alias for clarity (already in spec)**
```diff
-SELECT cte.customer_id, cte.total_orders
+SELECT 
+  cte.customer_id,
+  cte.total_orders AS order_count
```
✅ **Action:** Accept **only if** `order_count` is already defined in your spec's Output Fields section. If not, see "Review Carefully" below.

---

#### ⚠️ REVIEW CAREFULLY — Logic or Schema Change

**Example 4: New CTE that wasn't in the original spec**
```diff
  WITH cte_orders AS (
    SELECT order_id, customer_id, order_date
    FROM [WRKDQ].[dbo].[VBAK]
  ),
+ cte_order_statuses AS (
+   /* AI noticed that some orders have status 'cancelled' and added
+      this CTE to pre-filter them before joining to avoid duplicate counts */
+   SELECT order_id, status
+   FROM [WRKDQ].[dbo].[VBAK]
+   WHERE status NOT IN ('cancelled', 'deleted')
+ ),
  cte_final AS (
    SELECT ...
```
⚠️ **Action:** Review. Why did AI add this? 
- If the **rule description** didn't mention status exclusion, this is scope creep → **Reject** and re-derive with a more precise rule name
- If you **did** mention "exclude cancelled orders" but the deriver missed it → **Accept** (AI fixed a real omission)
- **Check:** Does the exclusion match your business rule exactly? (cancelled vs. cancelled AND deleted?)

---

**Example 5: New field added to output (not in spec)**
```diff
  SELECT
    dq.zSourceSystemID,
    dq.zRecordKey,
    dq.zErrorFlag,
    dq.zErrorCode,
-   dq.zRuleID
+   dq.zRuleID,
+   dq.zExecutionTimestamp  /* AI added this */
```
⚠️ **Action:** Reject unless your spec's **Output Fields** section includes `zExecutionTimestamp`. Adding unrequested fields breaks the contract with the audit tracker.

---

**Example 6: Logic change — softening of a WHERE clause**
```diff
  WHERE
    mara.MATNR IS NOT NULL
    AND mara.LVORM = ''  /* Not marked for deletion */
-   AND mara.MTART IN ('FERT', 'HALB', 'RAWM')  /* Finished, Semi, Raw */
+   AND (mara.MTART IN ('FERT', 'HALB', 'RAWM') OR mara.MTART IS NULL)
```
❌ **Action:** Reject. AI added "OR IS NULL" to be defensive, but your rule explicitly scoped to specific material types. This silently changes which rows fail the quality check.

---

**Example 7: Duplicate-row prevention CTE (fan-out fix)**
```diff
  WITH cte_invoices AS (
    SELECT 
      rbkp.belnr,
      rbkp.gjahr,
      MAX(rbkp.budat) AS invoice_date
    FROM [WRKDQ].[dbo].[RBKP] AS rbkp
    GROUP BY rbkp.belnr, rbkp.gjahr
  )
+ cte_invoice_items_dedup AS (
+   /* Pre-aggregate invoice items to prevent fan-out when joined to 
+      invoice header; without this, multiple line items fan the 
+      header record and multiply error flags */
+   SELECT 
+     rbpos.belnr,
+     rbpos.gjahr,
+     COUNT(DISTINCT rbpos.buzei) AS item_count
+   FROM [WRKDQ].[dbo].[RBPOS] AS rbpos
+   GROUP BY rbpos.belnr, rbpos.gjahr
+ )
```
✅ **Action:** Accept **if** your rule fans out across multiple systems. The CTE is preventing a real bug (duplicate flags due to 1:N joins). Read the comment to confirm the intent, then accept.

---

**Example 8: Data type coercion (risky)**
```diff
  CASE 
-   WHEN mara.LAEDA >= DATEADD(YEAR, -2, CAST(GETDATE() AS DATE)) THEN 0
-   ELSE 1
+   WHEN CONVERT(DATE, mara.LAEDA) >= DATEADD(YEAR, -2, GETDATE()) THEN 0
+   ELSE 1
```
⚠️ **Action:** Review. AI changed date logic. Questions:
- Does `CONVERT(DATE, mara.LAEDA)` handle NULLs the same way the original did?
- Does the rule date column always exist and have valid values, or do you need explicit NULL handling?
- **If uncertain:** Reject and let the deterministic deriver handle it, or add the NULL handling explicitly to your rule description.

---

#### ❌ REJECT — Rule Scope Violation

**Example 9: Adding a business rule that wasn't requested**
```diff
  CASE 
    WHEN customer.name IS NULL THEN 1
    WHEN customer.email IS NULL THEN 1
+   WHEN customer.email NOT LIKE '%@%.%' THEN 1  /* AI added format check */
    ELSE 0
```
❌ **Action:** Reject. Your rule was "A customer must have a name and email" (presence only). The format check is a new requirement not in the spec. The AI inferred it because your rule name was vague. Re-derive with a clearer name: "A customer must have a non-empty name and valid email format" if that's what you actually want.

---

### Decision Tree: Accept vs. Reject

| Change Type | Accept? | Why |
|-------------|---------|-----|
| Comments, formatting, readability | ✅ Always | No logic change |
| Column alias already in spec | ✅ Yes | Clarifies existing data |
| New column NOT in spec | ❌ No | Breaks audit contract |
| CTE for fan-out prevention | ✅ If rule fans out | Fixes a real bug |
| CTE for pre-filtering | ⚠️ Review | Check against spec scope |
| WHERE clause softening (OR conditions) | ❌ No | Changes row outcomes silently |
| NULL handling additions | ⚠️ Review | Verify NULL behavior matches intent |
| Business rule expansion | ❌ No | Re-derive with precise rule name |
| Date/type coercions | ⚠️ Review | Verify NULL, edge-case handling |

You don't have to catch every one of these by eye — the Studio's own static validator runs the
same checks on Claude's output and, on a HIGH-severity finding, automatically retries the AI call
once with the findings injected before you ever see the result. See
[[ref-ai-static-validator-gate|AI Static-Validator Gate]] for exactly what it catches and what it
doesn't (it's fail-soft: findings are stamped for your review, not silently fixed or hidden).

### 6. Write the description

Open the spec's Description field. Use [[std-implication-template|Implication Template]] —
Fetch / Check / Return (or Fetch / Profile / Surface for profiling). Tag SKP_RULE_NNNN at the
bottom.

### 7. Export to markdown

Click **Markdown Spec** — download the .md. Drop into the project's spec folder. The markdown
includes:

- Rule identity table
- Output Fields (5 sections)
- Logic / Joins / Filters
- The Sample Data block (if AI Enhanced)
- The Description block (your Implication)

### 8. Score the rule

Confirm the rule-name scorer shows ≥ 0.7. If not, refine the name and re-derive.

## Verification

- Spec markdown opens cleanly in any markdown viewer
- The view names follow [[std-view-naming-patterns|View Naming Patterns]]
- SKP_RULE_NNNN appears in both the rule identity table AND the Implication anchor
- Re-running export produces identical output (deterministic)

## Common pitfalls

- **Local Derive returns thin spec** — fall through to AI Derive; the knowledge base doesn't
  cover every domain
- **AI Derive picks the wrong table** — set the AI table hint explicitly; the AI sometimes
  infers from rule wording differently than intended
- **Output Fields missing a section** — re-derive; section omission means the deriver got
  confused. If persistent, add a hint via the project YAML's `output_section_overrides`
- **Expecting an AI-enhanced fix to silently overwrite every sibling** — if this rule
  [[con-multi-implementation-model|fans out]] to multiple systems, propagating an enhancement to
  the group skips (and reports) any sibling that was already independently enhanced or has
  diverged from the shared pattern — it never clobbers real per-sibling work. See
  [[gls-sibling-implementation|Sibling Implementation]].
- **Accepting a CTE Claude added without checking why** — a CTE that pre-aggregates a lookup
  table before joining is usually fixing a fan-out (duplicate rows multiplying your error flags),
  not adding complexity for its own sake. Read the explanation before accepting or rejecting it.

## Related

- [[prc-studio-onboarding|Studio Onboarding — Your First Hour]]
- [[prc-write-a-quality-rule-name|Write a Quality Rule Name]]
- [[prc-format-an-implication|Format an Implication]]
- [[std-implication-template|Implication Template]]
- [[std-optsel-select-structure|OptSel SELECT Structure]]
- [[ref-single-rule-designer|Studio — Single Rule Designer]]
- [[ref-ai-static-validator-gate|AI Static-Validator Gate]]
- [[con-multi-implementation-model|Multi-Implementation Model]]
