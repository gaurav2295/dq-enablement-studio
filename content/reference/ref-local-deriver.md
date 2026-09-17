---
id: ref-local-deriver
type: reference
title: Local Derive
domain: studio
audience: [consultant, instructor]
level: practitioner
status: review
links:
  - implements:prn-no-silent-domain-fallback
  - relates:con-catalog-vs-bespoke-rules
  - relates:prc-derive-a-dq-rule
  - relates:std-rule-name-heuristics
  - relates:std-output-field-sections
  - relates:ref-single-rule-designer
  - relates:gls-deterministic-shell
  - relates:gls-domain-unknown
  - relates:gls-tbd-placeholder
sources:
  - vault:studio-architecture/Studio — Local Deriver.md
  - coe:rewritten to usage level for consultant enablement, 2026-08-21
tags: [studio, derivation, methodology, sap, course]
created: 2026-08-20
updated: 2026-08-21
---

## Summary

**Local Derive** is the Studio's no-AI derivation path: you give it a rule name in business
language, it gives you back a complete rule spec — output fields in all five sections, the
error-detection logic, joins, filters and a Fetch/Check/Return description — plus the OptSel and
RptSel SQL generated from that spec.

It is called *local* because nothing leaves your machine and no API key is involved. It reads the
Studio's shipped SAP knowledge (domains, tables, keys, joins, deletion flags) and applies the
methodology to your rule name. It is the default path, and the one you should reach for first.

## When to use it

| Situation | Path |
|---|---|
| The rule is bespoke and sits in a domain the Studio knows (Material, Customer, Vendor, Finance…) | **Local Derive** |
| The rule already exists in the Syniti rule catalog | Catalog import — see [[con-catalog-vs-bespoke-rules]] |
| Local Derive returns a thin or empty spec, or the domain is unusual | AI Derive, then review against the local output |

Local Derive is also the right path when you need to *defend* the output. Give it the same rule
name and the same project settings next month and you get the identical spec and identical SQL —
same field order, same comments, same filter placement. That reproducibility is what makes a rule
certifiable to a client or an auditor, and it is why git diffs on a spec folder show only the logic
you actually changed.

## What to expect from the output

- **A rule name drives everything.** The words you use decide the domain, the object under check
  and the fields matched — so name quality is not cosmetic. Write the name first, to
  [[std-rule-name-heuristics|the naming heuristics]], then derive.
- **The leftmost thing you name is the object.** *"Material missing base unit of measure"* checks
  the material's unit of measure; the first matched phrase becomes the subject of the logic and
  any second one becomes the comparison reference.
- **All five output sections, in SQL order.** Technical, Basic, Org, Value, Activity — see
  [[std-output-field-sections]]. Error rules carry `zIsErrorFlag`; Info rules deliberately do not,
  because Info rules report rather than detect.
- **Deletion flags land in the WHERE clause** as exclusions, not in the error CASE — unless the
  rule is itself a deletion-detection rule, in which case the flag becomes the error condition. It
  is never both.
- **Profiling rules take a different shape entirely** — grouped counts and distributions, no
  per-row error flag, no pass/fail. See [[prn-profiling-has-no-pass-fail]].

### Example: Successful Derivation (End-to-End)

**Rule name you enter:**
```
A material must have a base unit of measure
```

**What Local Derive returns:**
```
STATUS: ✅ SUCCESS
─────────────────────────────

Rule Name: A material must have a base unit of measure

Domain: Material ✅
Object Table: MARA ✅
Field Under Check: MEINS (Base Unit of Measure) ✅

Output Fields:
  - Technical: zSourceSystemID, zConcatenatedKey, zIsErrorFlag ✅
  - Basic: MATNR, MAKTX ✅
  - Org: WERKS, SPART ✅
  - Value: MEINS ✅
  - Activity: ERSDA, LAEDA ✅

Joins:
  MARA left-join MAKT (material description) ✅

Filters (WHERE):
  WHERE ISNULL(MARA.LVORM, '') <> 'X'  /* exclude deleted */ ✅
  AND MARA.zSourceSystemID = 'SRCECC02100' ✅

Error Logic:
  CASE
    WHEN ISNULL(MARA.MEINS, '') = '' THEN 1
    ELSE 0
  END AS [zIsErrorFlag] ✅

Generated Views:
  OptSel: DQ_0001_P02_MARA_Base_Unit_Of_Measure_OptSel ✅
  RptSel: DQ_0001_P02_MARA_Base_Unit_Of_Measure_RptSel ✅

Next Step:
  ✅ Spec is complete and ready to review.
  Review the logic, add an Implication description, and proceed
  to export or AI Enhance if needed.
```

**What happened:**
1. ✅ Rule name matched "Material" domain
2. ✅ "base unit of measure" matched MEINS field in MARA
3. ✅ All five output sections auto-populated
4. ✅ Deletion flag (LVORM) correctly placed in WHERE
5. ✅ Error logic generated from field check (NULL/empty check)
6. ✅ View names generated per naming pattern
7. ✅ You can now review and refine

---

## When it cannot resolve your rule

Local Derive will not guess. Two outcomes are deliberate and worth recognising on screen:

### Unknown Domain

**What you see:** An empty shell with the domain marked as "unknown" and the entire spec flagged for manual review. No tables matched, no joins suggested, no error logic generated.

**Example (Unknown Domain):**

**Rule name you enter:**
```
A transaction must be valid
```

**What Local Derive returns:**
```
STATUS: ⚠️ DOMAIN UNKNOWN
────────────────────────────
Rule Name: A transaction must be valid

Domain: [UNKNOWN]
Object Table: [UNKNOWN]
Field Under Check: [UNKNOWN]

Output Fields:
  - Technical: [EMPTY]
  - Basic: [EMPTY]
  - Org: [EMPTY]
  - Value: [EMPTY]
  - Activity: [EMPTY]

Joins: [NONE]

Error Logic:
  [EMPTY — CANNOT DERIVE]

Next Step:
  This rule name does not match any known SAP domain (Material, Customer, Vendor, Finance, etc.)
  Refactor your rule name to include the domain:
    ✅ "A Purchase Order must have a valid vendor"
    ✅ "A Customer must have a billing address"
    Or use AI Derive if this is an unusual/custom domain.
```

**What to do:** Rename with the domain word first:
- ❌ "A transaction must be valid" → tries to find domain in "transaction" (too generic)
- ✅ "A Purchase Order must have a vendor" → matches domain "Purchase Order"
- ✅ "A Material must have a base unit" → matches domain "Material"

**When to use:** Use **AI Derive** when you're confident the rule is valid but the domain is unusual or not in the knowledge base.

---

### Domain Known, No Field Matched (Thin Spec)

**What you see:** A complete spec skeleton with all five output field sections, joins, and filters populated — but the error-detection logic contains a **TBD placeholder** instead of the actual condition.

**Example (Thin Spec):**

**Rule name you enter:**
```
A material must have a valid base unit
```

**What Local Derive returns:**
```
STATUS: ⚠️ THIN SPEC — FIELD NOT MATCHED
────────────────────────────────────────
Rule Name: A material must have a valid base unit

Domain: Material ✅
Object Table: MARA ✅
Field Under Check: [TBD — "base unit" is ambiguous] ⚠️

Output Fields:
  - Technical: zSourceSystemID, zConcatenatedKey, zIsErrorFlag ✅
  - Basic: MATNR, MAKTX ✅
  - Org: WERKS, SPART ✅
  - Value: [TBD — unit field not recognized] ⚠️
  - Activity: ERSDA, LAEDA ✅

Joins:
  MARA left-join MAKT (description) ✅

Filters (WHERE):
  WHERE ISNULL(MARA.LVORM, '') <> 'X'  /* exclude deleted */ ✅
  AND MARA.zSourceSystemID = 'SRCECC02100' ✅

Error Logic:
  CASE
    WHEN [TBD — could be MEINS, BSTME, UMREZ, or another field] THEN 1
    ELSE 0
  END AS [zIsErrorFlag]

Next Step:
  The domain "Material" is recognized and tables are matched.
  But "base unit" is ambiguous (could be MEINS, BSTME, or UMREZ).
  Refactor your rule name to use the exact field name:
    ✅ "A material must have a recorded MEINS (base unit of measure)"
    ✅ "A material must have a base unit of measure in MEINS"
  Then re-derive locally.
```

**What to do:** Rename with the explicit field name:
- ❌ "A material must have a valid base unit" → "unit" is too generic (could be MEINS, BSTME, UMREZ, etc.)
- ✅ "A material must have a recorded MEINS" → MEINS field is now explicit
- ✅ "A material must have a base unit of measure (MEINS)" → field clarified in parentheses

**Why it's "thin":** The structure is there (5 sections, joins, filters), but the core logic (the error condition) is incomplete. It's not an error; it's a signal to refine your rule name.

---

### Comparison Table

| Aspect | Unknown Domain | Thin Spec (Domain Known) |
|--------|---|---|
| **What matched** | Nothing — no domain recognized | Domain matched (e.g., Material), field did not |
| **What you see** | Empty shell, entire spec marked for review | Complete skeleton with TBD placeholder in error logic |
| **Tables shown** | None | Yes, all relevant tables matched |
| **Output fields** | Empty | All five sections present, one field marked TBD |
| **Error condition** | Missing entirely | [TBD — field condition] |
| **Recovery path** | Rename with domain word; or use AI Derive | Rename with explicit field name; re-derive locally |
| **Example fix** | "A **Material** must have a valid unit" | "A material must have a recorded **MEINS**" |

---

### Why Local Derive Doesn't Guess

Local Derive stops at these two points deliberately:

- **Unknown domain** → Would guess the wrong tables; better to stop and ask you to clarify
- **Thin spec** → Would guess the wrong field; better to show you the skeleton and ask you to complete the thought

Both are **signals to improve your input**, not tool failures. The spec is only as smart as your rule name.

## Common mistakes

- **Editing the generated SQL by hand.** The spec is the source of truth; the next derive or
  regenerate rebuilds the SQL and your edit disappears. Fix the spec instead.
- **Treating a TBD placeholder as "good enough to ship".** It is an explicit request for a better
  rule name.
- **Assuming a thin spec means the tool is broken.** It usually means the knowledge base does not
  cover that domain — fall through to AI Derive and compare.
- **Reaching for AI first out of habit.** AI Derive costs time per rule and must reach parity with
  the local output anyway. Derive locally, read the result, and only escalate when it falls short.

## Related

[[con-catalog-vs-bespoke-rules]] · [[prc-derive-a-dq-rule]] · [[ref-single-rule-designer]] ·
[[std-rule-name-heuristics]] · [[std-output-field-sections]] · [[prn-no-silent-domain-fallback]]
