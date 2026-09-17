---
id: ref-ai-derive-and-enhance-internals
type: reference
title: AI Enhance — What It Does and How to Use It
domain: ai-enhancement
audience: [consultant, instructor]
level: foundation
status: review
links:
  - relates:ref-ai-static-validator-gate
  - relates:std-ai-enhance-scope
  - relates:std-ai-enhance-guardrails
  - relates:ref-local-deriver
  - relates:prc-derive-a-dq-rule
  - relates:prc-format-an-implication
  - relates:prc-fan-out-a-rule-per-system
  - relates:prc-audit-rule-quality
  - relates:qa-sibling-divergence-realignment
  - implements:prn-no-silent-domain-fallback
  - implements:prn-sql-comments-must-match-local-derive-quality
sources:
  - vault:ai-related/AI Derive & Enhance Internals.md
  - dq-studio:docs/ai_enhance_instructions.md
  - coe:usage rewrite for consultants
tags: [studio, agent, course, sap]
created: 2026-08-20
updated: 2026-08-21
---

## What it is

**AI Enhance** is the button on the rule designer that improves a rule you have already derived.
The Studio derives the rule deterministically first — same input, same output, every time — and the
AI works on top of that. It is an assistant with a short leash, not the author of the deliverable.

Understanding what it is allowed to touch is the difference between using it well and spending an
afternoon undoing it.

## What it does for you

Pressing **AI Enhance** runs four things in order:

1. **Rule name conversion** (optional) — reshapes an informal name into the SynitiONE naming shape.
   Names are capped at 100 characters and trimmed at a word boundary.
2. **Table and field hint** — proposes the primary SAP table and field for the rule, and tells you
   how confident it is. A low-confidence hint is flagged rather than presented as fact.
   - **High confidence:** "MARA (Material Master), field: MEINS (Base Unit of Measure)" — AI matched the table and field clearly from your rule name
   - **Low confidence:** "Table hint: VBAP? Field hint: NETWR? [⚠️ LOW CONFIDENCE]" — AI made a guess that may be wrong; review before accepting. A low-confidence hint indicates the rule name was ambiguous or the domain was unusual for the knowledge base.
3. **Implication** — writes the business "why this matters" text and the specification wording,
   shaped by the rule type. See [[prc-format-an-implication]].
4. **SQL review** — reads the SQL the Studio already generated and proposes corrections, judged
   against the rule's stated intent. You choose whether to apply them.

Everything the AI produced is saved with the rule, alongside a record of what the rule looked like
**before**. That before/after and any warnings survive navigation, a reload, and an app restart, so
a reviewer can always see what was machine-written.

### Example: Before and After AI Enhance

**Before (Local Derive output):**
```sql
WITH order_summary AS (
  SELECT vbap.VBELN, vbap.POSNR, COUNT(*) AS line_count
  FROM [WRKDQ].[dbo].[VBAP] AS vbap
  WHERE vbap.zSourceSystemID = 'SRCECC02100'
  GROUP BY vbap.VBELN, vbap.POSNR
)
SELECT
  vbak.zSourceSystemID,
  vbak.VBELN,
  vbak.ERDAT,
  CASE
    WHEN ISNULL(vbak.ERDAT, '') = '' THEN 1
    ELSE 0
  END AS [zIsErrorFlag],
  ...
FROM [WRKDQ].[dbo].[VBAK] AS vbak
LEFT JOIN order_summary AS os
  ON os.VBELN = vbak.VBELN
WHERE vbak.zSourceSystemID = 'SRCECC02100'
```

**After (AI Enhance suggestions):**
```sql
WITH order_summary AS (
  SELECT vbap.zSourceSystemID, vbap.VBELN, vbap.POSNR, COUNT(*) AS line_count
  FROM [WRKDQ].[dbo].[VBAP] AS vbap
  WHERE vbap.zSourceSystemID = 'SRCECC02100'
  GROUP BY vbap.zSourceSystemID, vbap.VBELN, vbap.POSNR  -- ✅ Added zSourceSystemID
)
SELECT
  vbak.zSourceSystemID,
  CONCAT(vbak.zSourceSystemID, '_', vbak.VBELN) AS [zConcatenatedKey],  -- ✅ Added
  vbak.VBELN,
  vbak.ERDAT,
  CASE
    WHEN ISNULL(vbak.ERDAT, '') = '' THEN 1
    ELSE 0
  END AS [zIsErrorFlag],
  ...
FROM [WRKDQ].[dbo].[VBAK] AS vbak
LEFT JOIN order_summary AS os
  ON os.zSourceSystemID = vbak.zSourceSystemID  -- ✅ Added system alignment
  AND os.VBELN = vbak.VBELN
WHERE vbak.zSourceSystemID = 'SRCECC02100'
```

**Changes made:**
- ✅ Added `zSourceSystemID` to CTE GROUP BY (cross-system safety)
- ✅ Added `zConcatenatedKey` field (technical requirement)
- ✅ Added `zSourceSystemID` equality to LEFT JOIN (prevents matches across systems)

**Your choice:** Review the changes, then **Accept** (applies them) or **Reject** (keeps the original)

## What it will not do

- It will not invent the deployable rule from nothing. If the rule name matches no known domain,
  the Studio produces an honest, deliberately un-deployable placeholder rather than a
  confidently wrong guess — see [[prn-no-silent-domain-fallback]]. Fix the name or add context;
  do not let the AI fill the gap.
- It will not swap the table you chose. If you picked the table to profile and the rule wording
  sounds like a different domain, an AI rewrite that moves to another table is **refused** and the
  original SQL is kept, with a note explaining why.
- It will not remove what you added. Your edits, filters and comments survive a review pass.
- It will not lower the bar. AI output has to reach the same structural quality as deterministic
  derivation: all Syniti technical fields present, spec and SQL in agreement, rule type respected,
  comments up to standard. The quality gate enforces that — see [[ref-ai-static-validator-gate]].

**Why these guardrails exist:**

These restrictions preserve three principles:

1. **Deterministic outputs** — If you run the same rule name tomorrow, you get the same spec and SQL. This makes rules auditable and git-diff-friendly (you see only the logic you actually changed). Breaking this would make rules non-reproducible.

2. **No silent logic drift** — AI should suggest corrections, not overwrite your intent. If the AI silently swapped your table or added an exclusion you didn't ask for, you'd deploy the wrong rule without realizing it. The guardrails force all changes to be reviewed.

3. **Your edits are sacred** — Once you've hand-edited a field, a comment, or a filter, the AI respects that as intentional. This protects client-specific customizations and domain expertise you've embedded in the spec.

The precise boundary of what the model may change is [[std-ai-enhance-scope]]; the rules it is
checked against are [[std-ai-enhance-guardrails]].

## What to expect

- **Error and Info rules** are reviewed against the DQ standards — field sections in order, the
  error-flag pattern, deletion flags in the WHERE clause and status fields in the CASE.
- **Profiling rules** are reviewed as a pair — detail and summary — with the percentage column
  checked, and no mention of error flags, because profiling has no pass or fail.
- **Fan-out.** When you enhance across siblings, a sibling that you already enhanced by hand is
  skipped and reported, and a sibling whose content has diverged from the group is always skipped
  rather than overwritten. See [[qa-sibling-divergence-realignment|How to realign a diverged sibling]] and [[prc-fan-out-a-rule-per-system]].
- **In bulk, SQL review is off by default.** At batch scale the audit is the structural gate —
  running a review on every rule costs hours. Derive in bulk, then audit. See
  [[prc-audit-rule-quality]].

## Common mistakes

- **Treating the table hint as an answer.** Check it against the client's actual data model,
  especially when the confidence flag is low.
- **Applying corrected SQL without reading the diff.** The before/after is stored for exactly this
  reason.
- **Enhancing a placeholder rule** and assuming the result is deployable. A rule with no matched
  domain needs a better name first.
- **Running AI review across a whole bulk batch** to "be safe". Use the audit instead.
- **Assuming AI Enhance replaces review.** The human reviewer is the final gate, always.

## Related

[[ref-ai-static-validator-gate]] · [[std-ai-enhance-scope]] · [[std-ai-enhance-guardrails]] ·
[[ref-local-deriver]] · [[prc-derive-a-dq-rule]] · [[prc-format-an-implication]] ·
[[prc-fan-out-a-rule-per-system]] · [[prc-audit-rule-quality]] ·
[[prn-no-silent-domain-fallback]] · [[prn-sql-comments-must-match-local-derive-quality]]
