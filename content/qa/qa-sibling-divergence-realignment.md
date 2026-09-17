---
id: qa-sibling-divergence-realignment
type: qa
title: When a sibling rule diverges from the group, how do I bring it back into alignment?
domain: ai-enhancement
audience: [consultant, developer]
level: practitioner
status: approved
sources:
  - coe:ref-ai-derive-and-enhance-internals and prc-fan-out-a-rule-per-system
created: 2026-09-02
updated: 2026-09-02
links:
  - parent:ref-ai-derive-and-enhance-internals
  - relates:prc-fan-out-a-rule-per-system
  - relates:gls-sibling-implementation
  - relates:gls-fan-out
  - relates:gls-dqops-id
  - relates:con-multi-implementation-model
---

## Question

When a sibling rule is skipped during fan-out because of its divergence, how should that sibling be brought back into alignment with the rest of the group?

## Answer

**A diverged sibling is intentionally skipped, not silently overwritten.** This protects your custom work from being erased by a bulk AI Enhance operation.

### What "Divergence" Means

A sibling is considered **diverged** when:
- You manually edited its SQL or spec (so it no longer matches the original lead rule)
- An AI Enhance changed only that sibling, moving it away from the group's original logic
- The sibling was handled differently in a prior fan-out operation

**Why it's skipped:** Overwriting diverged work could erase important customizations or bug fixes you made for that system's specific data model.

---

### How to Realign a Diverged Sibling

**Option 1: Intentional Divergence (Acceptable)**

If the sibling diverged **for good reason** (client-specific data model, different table structure, system-specific fix):

1. ✅ **Document why it diverged** — in the spec's Description or a comment, note: "This implementation uses custom table ZVEND_CUSTOM instead of VEND due to client's extended vendor structure"
2. ✅ **Mark it as "intentionally customized"** — track this in the tracker's notes so future bulk operations know to skip it
3. ✅ **Leave it as-is** — it's now a Bespoke rule with documented client-specific logic, separate from the lead

**Option 2: Unintended Divergence (Fix It)**

If the sibling diverged **accidentally** (bad edit, incomplete enhancement, leftover debug code):

1. **Understand what diverged** — compare the sibling's current SQL to the lead rule's SQL. What's different?
2. **Manually re-align** — edit the sibling's spec to match the lead rule's logic
3. **Re-derive the sibling** — run a fresh Local Derive using the same rule name, then accept the output
4. **Re-enhance the group** — run AI Enhance on the lead rule again, then propagate to all siblings. The re-aligned sibling should now be accepted instead of skipped

**Does realignment create a new DQOps ID?** No — realigning a sibling (whether by manual edit or re-derive + re-enhance) updates its SQL/spec **in place**; the sibling keeps its existing DQOps ID and SKP_RULE_NNNN. A new ID is only assigned if you delete the sibling and generate it fresh via fan-out.

**What happens to execution history?** Prior pipeline runs, audit results, and parity scores computed under the old (diverged) SQL stay in the tracker as historical records — they are not deleted or rewritten. Only the **next** pipeline run reflects the realigned SQL. If the divergence caused incorrect defect counts in a past report, that report is not auto-corrected; re-run the audit after realignment to get current numbers.

---

### Bulk Fan-Out Behavior with Diverged Siblings

When you **AI Enhance the lead rule and fan-out to all siblings:**

| Sibling Status | What Happens | Why |
|---|---|---|
| **Up-to-date** (matches lead) | ✅ Enhanced; changes applied | Safe to update; in sync |
| **Manually edited by you** | ⏭️ Skipped; not changed | Protects your custom work |
| **Diverged from lead** | ⏭️ Skipped; not changed | Prevents overwriting divergence |
| **Already enhanced by AI** | ⏭️ Skipped; not changed | Prevents double-enhancement |

**Result of bulk enhance:** You'll see a report like:
```
Lead rule (P02): Enhanced ✅
Sibling (P03): Enhanced ✅
Sibling (P05): Skipped ⏭️ (diverged from group)
Sibling (P06): Skipped ⏭️ (already manually edited)
```

---

### Real-World Example

**Scenario:** You fan-out a rule across 4 systems (P02, P03, P05, P06). Three are identical; P05 uses a custom vendor table.

**Initial state (all siblings in sync):**
- Lead (P02): Check VEND table
- Sibling (P03): Check VEND table
- Sibling (P05): Check ZVEND_CUSTOM table (intentional — client's custom extension)
- Sibling (P06): Check VEND table

**You enhance the lead rule (P02):**
- AI suggests adding a CTE for deduplication
- You apply the enhancement to P02

**You propagate to all siblings:**
- P03: ✅ Updated with the new CTE
- P05: ⏭️ Skipped (already diverged; you protect your ZVEND_CUSTOM work)
- P06: ✅ Updated with the new CTE

**Result:** P02, P03, P06 are all in sync; P05 stays as-is (you manage it separately).

**To update P05:** Do it manually or re-derive it if the lead rule logic applies to ZVEND_CUSTOM.

---

### Prevention: Keep Siblings in Sync

To avoid divergence in the first place:

1. **Use the lead rule as template** — when creating siblings, start from the lead's spec, then adapt only the table/field names
2. **Don't hand-edit SQL** — always use the Studio's UI or a fresh derive; hand-edits drift
3. **Re-derive when in doubt** — if you're unsure about a sibling's state, re-derive it fresh from the rule name
4. **Document client-specific variations** — if a system genuinely needs different logic, note it and mark the sibling as intentionally customized

---

### Related

- [[ref-ai-derive-and-enhance-internals|AI Enhance — What It Does and How to Use It]]
- [[prc-fan-out-a-rule-per-system|Fan-out a Rule Per System]]
- [[con-multi-implementation-model|The Multi-Implementation Model]]
