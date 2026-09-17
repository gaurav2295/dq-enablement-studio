---
id: qa-ai-enhance-accept-vs-review
type: qa
title: When should I accept or reject unrequested logic added by AI Enhance?
domain: ai-enhancement
audience: [consultant]
level: practitioner
status: approved
sources:
  - coe:deduced from prc-derive-a-dq-rule and AI enhancement patterns
created: 2026-09-02
updated: 2026-09-02
links:
  - parent:prc-derive-a-dq-rule
  - relates:ref-ai-static-validator-gate
  - relates:gls-ai-enhance
  - relates:gls-ai-additions
  - relates:gls-rule-fulfilment-review
---

## Question

If an AI-enhanced version introduces additional logic that appears correct but was not requested, should that logic be accepted, modified, or rejected by default?

## Answer

**Don't accept blindly.** Unrequested logic is a signal that **your rule name or description isn't precise enough** to capture what you actually want to check.

### The Real Problem

When Claude adds logic you didn't ask for, it means:
- Your rule name is **vague** ("A customer must be valid" invites guessing)
- Your rule description is **incomplete** (missing boundary conditions, scope limits, or explicit exclusions)

**Fix the rule name/description first.** Don't let AI "guess" what your rule should check.

### Decision Tree

```
Did Claude add unrequested logic?
│
├─ YES → Ask: "Did my rule name clearly state what should be checked?"
│        │
│        ├─ NO (vague name) → REJECT the added logic, rewrite the rule name
│        │                     (more specific), re-derive
│        │
│        └─ YES (clear name) → Does the added logic still fit the rule?
│                              │
│                              ├─ YES → ACCEPT (AI is fixing a technical issue)
│                              └─ NO → REJECT, ask Claude for rationale
│
└─ NO → Accept and proceed
```

### Real-World Examples

---

## Example 1: SAFE Enhancement (Accept)

**Rule Name:** *"A material must have a valid base unit of measure"*

**Your generated spec:**
```sql
SELECT
  mara.MATNR,
  mara.MEINS,
  CASE
    WHEN ISNULL(mara.MEINS, '') = '' THEN 1
    WHEN NOT EXISTS (
      SELECT 1 FROM [WRKDQ].[dbo].[T006] AS t006
      WHERE t006.MSEHI = mara.MEINS
    ) THEN 1
    ELSE 0
  END AS [zIsErrorFlag],
  ...
FROM [WRKDQ].[dbo].[MARA] AS mara
```

**AI's suggested enhancement:**
```diff
+ WITH cte_valid_uom AS (
+   -- Deduplicate UoM lookup to prevent multiple matches per system
+   SELECT DISTINCT MSEHI, zSourceSystemID
+   FROM [WRKDQ].[dbo].[T006]
+ )
  SELECT
    mara.MATNR,
    mara.MEINS,
    CASE
      WHEN ISNULL(mara.MEINS, '') = '' THEN 1
      WHEN NOT EXISTS (
-       SELECT 1 FROM [WRKDQ].[dbo].[T006] AS t006
-       WHERE t006.MSEHI = mara.MEINS
+       SELECT 1 FROM cte_valid_uom AS t006
+       WHERE t006.MSEHI = mara.MEINS
+       AND t006.zSourceSystemID = mara.zSourceSystemID
      ) THEN 1
      ELSE 0
    END AS [zIsErrorFlag],
    ...
-   FROM [WRKDQ].[dbo].[MARA] AS mara
+   FROM [WRKDQ].[dbo].[MARA] AS mara
```

**Why: ✅ ACCEPT**

- **AI added:** A CTE to deduplicate the UoM lookup table and enforce zSourceSystemID alignment
- **Intent unchanged:** Still checking "is the UoM in the lookup table?"
- **Improvement:** Prevents the EXISTS from matching multiple rows if T006 has duplicates per system
- **Conclusion:** This is a **technical fix**, not a scope change. Accept it.

---

## Example 2: RISKY Enhancement (Review Carefully)

**Rule Name:** *"An order must have a valid price"*

**Your generated spec:**
```sql
SELECT
  vbap.VBELN,
  vbap.POSNR,
  vbap.NETPR,
  CASE
    WHEN ISNULL(vbap.NETPR, 0) <= 0 THEN 1
    ELSE 0
  END AS [zIsErrorFlag],
  ...
FROM [WRKDQ].[dbo].[VBAP] AS vbap
WHERE vbap.zSourceSystemID = 'SRCECC02100'
```

**AI's suggested enhancement:**
```diff
+ WITH cte_material_prices AS (
+   -- Get material master price to compare against order price
+   SELECT mara.MATNR, mara.STPRS AS material_standard_price
+   FROM [WRKDQ].[dbo].[MARA] AS mara
+ )
  SELECT
    vbap.VBELN,
    vbap.POSNR,
    vbap.NETPR,
+   mat.material_standard_price,
    CASE
      WHEN ISNULL(vbap.NETPR, 0) <= 0 THEN 1
+     WHEN vbap.NETPR > (mat.material_standard_price * 1.5) THEN 1
+     WHEN vbap.NETPR < (mat.material_standard_price * 0.5) THEN 1
      ELSE 0
    END AS [zIsErrorFlag],
    ...
  FROM [WRKDQ].[dbo].[VBAP] AS vbap
+ LEFT JOIN cte_material_prices AS mat
+   ON mat.MATNR = vbap.MATNR
  WHERE vbap.zSourceSystemID = 'SRCECC02100'
```

**Why: ⚠️ REVIEW CAREFULLY, Likely REJECT**

- **AI added:** Price variance checks (±50% of material master price)
- **Intent expanded:** Original rule only checked "is price > 0?"; AI added "is price reasonable?"
- **Problem:** Your rule name ("valid price") is vague — AI guessed what "valid" means, but you may have meant something different:
  - Did you want to check price is non-zero only?
  - Or check if it's within tolerance of material master?
  - Or check against a contract price list?
  - Or prevent prices from being X% different from history?
- **Conclusion:** **REJECT** the added variance checks. Instead:
  1. Rewrite your rule name more precisely: *"An order line must have a non-zero price"* (if you only want the > 0 check)
  2. Or create a separate rule: *"An order line's price must be within ±50% of the material master price"* (if you do want variance checking)

---

## The Pattern

| Scenario | Accept? | Rationale |
|----------|---------|-----------|
| AI adds a CTE to prevent duplicate-match issues | ✅ Accept | Technical fix, intent unchanged |
| AI adds zSourceSystemID alignment to a join | ✅ Accept | Technical correctness, rule still does the same thing |
| AI adds a NULL-handling edge case | ✅ Accept | Defensive coding, rule intent unchanged |
| AI expands the error condition (adds new checks) | ⚠️ Review | Scope expansion — rewrite your rule name first |
| AI changes the tables being checked | ❌ Reject | This changes the rule fundamentally; rewrite the name/description |
| AI adds conditional logic you didn't mention | ⚠️ Review | Ask: did I describe this scenario clearly enough? |

---

## What to Do Before Accepting

**Checklist for unrequested AI logic:**

- [ ] Read Claude's explanation for WHY the logic was added
- [ ] Ask: "Does this logic still check exactly what my rule name says?"
- [ ] If NO → Reject; rewrite the rule name to be more precise
- [ ] If YES but scope expanded → Reject; split into two rules (one for each check)
- [ ] If YES and it's defensive coding (NULL handling, dedup, system alignment) → Accept

---

## The Real Lesson

> **Precise rule names prevent AI guessing.** A vague rule name invites unrequested logic. A precise rule name ensures AI only fills in what's needed.

Compare:
- ❌ "A customer must be complete" (vague → AI adds multiple completeness checks)
- ✅ "A customer record must have a non-empty name, email, and country code" (precise → AI only checks these three fields)

---

### Related

- [[prc-derive-a-dq-rule|Derive a DQ Rule (single rule)]]
- [[prc-write-a-quality-rule-name|Write a Quality Rule Name]]
- [[ref-ai-static-validator-gate|AI Static-Validator Gate]]
