---
id: qa-non-negotiables-auto-correction
type: qa
title: How can you tell if the Studio auto-corrected a violation or if it was compliant?
domain: studio
audience: [lead, developer]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

When a non-negotiable is enforced automatically (e.g., the Studio adds section comments 
if they're missing), how can a DBA reviewer tell whether the output was corrected by the 
Studio or was already compliant when the AI generated it?

## Answer

**Two mechanisms: inline comments (in the SQL) and audit metadata (in the tracker).**

### 1. Inline comments (in the SQL spec)

When the Studio auto-corrects, it adds an `/* auto-repaired */` marker:

```sql
-- Syniti Technical Fields     /* auto-repaired */
zSourceSystemID,
zConcatenatedKey,
zIsErrorFlag,

-- Basic Fields                /* auto-repaired */
MARA.MATNR,
MARA.PLANT,
```

The marker indicates: "This section comment was added/fixed by the Studio."

If the comment is original (not repaired):
```sql
-- Syniti Technical Fields     /* original */
```

Or no marker at all = original (the AI wrote it correctly).

### 2. Audit metadata (in the tracker)

The rule's tracker record includes a `corrections_applied` field:

```json
{
  "rule_id": "DQ_0087",
  "ai_quality_status": "PASSED_WITH_REPAIRS",
  "corrections_applied": [
    "section_comment_added: Syniti Technical Fields",
    "section_comment_added: Basic Fields",
    "zIsErrorFlag type corrected: VARCHAR → INTEGER"
  ],
  "original_spec": "<url to AI's original output>",
  "repaired_spec": "<url to corrected output>"
}
```

If no corrections: `ai_quality_status: PASSED_CLEAN`

### How to use this for review

**As a DBA auditing the rule:**

1. **Check `ai_quality_status`**
   - `PASSED_CLEAN` = AI got it right, no repairs needed
   - `PASSED_WITH_REPAIRS` = AI missed something; Studio fixed it
   - `FAILED` = Can't fix automatically; rule blocked for manual review

2. **Review `corrections_applied`** list
   - What specific violations were fixed?
   - Are the repairs reasonable?

3. **Compare original vs repaired** (if needed)
   - Click the `original_spec` URL to see what the AI produced
   - Click the `repaired_spec` URL to see the corrected version
   - Understand the delta

### Transparency

The Studio makes no "silent" corrections — every auto-repair is logged and visible.
If you see a marker or a repair flag, you know the Studio touched it.

> [!tip]
> AI correctness varies by rule complexity. Simple rules: `PASSED_CLEAN` is common. 
> Complex rules: `PASSED_WITH_REPAIRS` is expected. The marker tells you which.
