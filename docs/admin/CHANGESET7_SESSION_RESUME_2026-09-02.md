# Changeset 7 (DQ Studio Workflow) — Session Resume Notes
**Session date:** 2026-09-02 (evening session, ~17:35–18:15)
**Build status at end of session:** ✅ Clean — 294 units, 0 errors, 0 warnings

---

## ⚠️ READ THIS FIRST: Important context for the next session

**A separate/prior session (commit `dcf24de`, by a Haiku 4.5 agent, timestamped 17:08) had already
run a "Phase 1" pass over this same changeset shortly before this session started.** That commit
created 17 **draft QA scaffolds** — files with `Status: Awaiting answer` and an "Expected Answer
Should Cover" outline, NOT actual answers. This session's `SESSION_SUMMARY_2026-09-02.md` (written
earlier in the day) did not know about that commit and said Changeset 7 was "fully pending" — that
was stale by the time this session ran.

**What this session found and did about it:**
- 9 of the 17 scaffolds covered the same questions this session was independently answering.
- This session's answers were the *real* completed content (the scaffolds were empty templates).
- Per user decision, the 9 pairs were **merged**: this session's QA file kept as canonical, with
  the scaffold's useful `links:` (glossary terms, `parent:` relations) and a few sub-angles it
  raised (CTE anti-patterns, DQOps ID handling on realignment, Catalog-update inheritance) folded
  in. The 9 scaffold files were then **deleted**.
- **8 scaffolds remain untouched** — they map to items this session had not reached yet, or to two
  items this session deliberately answered *inside the source unit* instead of as a QA. See the
  table below for what to do with each.

**Before doing anything else next session:** run `git log --oneline -5` and `ls content/qa/` to
confirm no *other* parallel session has touched this changeset again since this file was written.
If another session's commits exist after this one, re-check for new duplicates before continuing.

---

## Changeset file being processed

`em-changeset-dq-studio-workflow-31-08-26-2026-08-31 (1).json` (originally in
`C:\Users\GKALWANI\Downloads\`) — **34 ops** (13 questions + 21 notes) across 10 units. Not yet
moved to `feedback/applied/` — **do not move it until all 34 items are resolved** (25 done, 1
skipped, 8 remaining).

---

## Status of all 34 feedback items

### ✅ Done (25 items)

| # | Unit | Type | What happened |
|---|------|------|----------------|
| 1 | prc-studio-onboarding | note | 5-space sidebar navigation diagram created (indigo rounded-square badges, numbered 1–5), embedded as description in the unit |
| 2 | prc-studio-onboarding | note | Added descriptions of Home/Project Hub, Session Setup, Project Configuration (all fields), AI Integration — based on 4 real screenshots the user provided |
| 3 | prc-studio-onboarding | question | ⏭️ **Skipped by explicit user request** ("skip this unit") — but note: scaffold `qa-studio-configuration-file-location.md` already exists answering this. Next session should decide: use the scaffold's answer, or leave skipped. |
| 4 | prc-studio-onboarding | question | `qa-optional-studio-spaces-per-engagement.md` — 5 real-world engagement scenarios + decision table |
| 5 | prc-studio-onboarding | note | Enhanced Step 3: source systems are free-text input, not a dropdown; added "+Add System" walkthrough |
| 6 | prc-derive-a-dq-rule | question | `qa-sample-rule-review-before-authoring.md` + a full annotated example rule (Material Activity Date, OptSel+RptSel) embedded in the procedure + a review checklist |
| 7 | prc-derive-a-dq-rule | question | `qa-ai-enhance-accept-vs-review.md` — corrected an earlier wrong deduction (fan-out ≠ joins); real answer is "vague rule names invite unrequested AI logic"; 2 SQL diff examples (safe vs risky enhancement) |
| 8 | prc-derive-a-dq-rule | note | Step 5 (AI Enhance) rewritten to remove the incorrect "fan-out" explanation, links to the QA above, added a rule-naming-precision callout in Step 1 |
| 9 | prc-derive-a-dq-rule | question | `qa-when-additional-cte-acceptable.md` — sourced from `std-cte-rules.md`; includes anti-patterns (over-CTEing, redundant CTEs, hiding logic in CTE) |
| 10 | prc-format-an-implication | question | **Answered inline in the unit** (Steps 3–4), not as a QA — per explicit user instruction. A stale scaffold `qa-implication-detail-scope-fetch-technical.md` still exists for this; probably delete it next session since the real answer lives in the procedure. |
| 11 | con-catalog-vs-bespoke-rules | question | Enhanced unit with a "Converting a Catalog rule to Bespoke" section + `qa-catalog-to-bespoke-rule-conversion.md` (worked example, price-variance rule; includes "does it inherit future Catalog updates" — answer: no) |
| 12 | con-catalog-vs-bespoke-rules | question | Enhanced unit with "Promoting a Bespoke rule to Catalog" section + `qa-bespoke-to-catalog-promotion.md` (5 criteria, decision table, 2 worked examples — one promoted, one rejected) |
| 13 | ref-local-deriver | question | "Thin spec" already defined in the unit; confirmed with user, no new QA needed |
| 14 | ref-local-deriver | note | Added full worked terminal-style examples for **Unknown Domain** and **Thin Spec** outcomes, plus a comparison table |
| 15 | ref-local-deriver | note | Covered by the Item 14 enhancement |
| 16 | ref-local-deriver | note | Covered by the Item 14 enhancement (spec skeleton contents now explicit) |
| 17 | prc-format-an-implication | note | Added a complete 3-section + SKP_RULE_ID worked example (sales order delivery-date rule) |
| 18 | prc-format-an-implication | note | Added a "What is an Implication?" section explaining the concept and how it drives SQL generation |
| 19 | ref-ai-derive-and-enhance-internals | note | Added a full before/after SQL diff example (order_summary CTE gaining zSourceSystemID) |
| 20 | ref-ai-derive-and-enhance-internals | question | `qa-sibling-divergence-realignment.md` — intentional vs unintended divergence, realignment steps, **DQOps ID is preserved (not regenerated) on realignment**, execution history is not retroactively corrected |
| 21 | ref-ai-derive-and-enhance-internals | note | Added a plain-language explanation of high- vs low-confidence table/field hints with examples |
| 22 | ref-ai-static-validator-gate | question | **Answered inline in the unit** (new "Auto-repairs" section says findings appear on the Reconciliation sheet), not as a QA. A stale scaffold `qa-ai-validator-repaired-issues-visibility.md` still exists; consider deleting next session. |
| 23 | ref-ai-static-validator-gate | note | Added a "Quality Gate vs. Audit Rule Quality" comparison table to the unit |
| 24 | ref-ai-static-validator-gate | question | `qa-ai-quality-gate-serious-findings.md` — serious vs lesser findings table, retry mechanics (exactly one retry, no loop) |
| 25 | ref-ai-static-validator-gate | question | `qa-profiling-rules-quality-gate-exclusion.md` — structural reason (no zIsErrorFlag/OptSel-RptSel pair to check), trade-off table vs a hypothetical profiling-specific gate |

### ⏳ Remaining (8 items) — scaffolds already exist for most of these!

**Good news: draft scaffolds from the `dcf24de` commit already exist for 5 of these 8 items,
with a "Question / Context / Why This Matters / Expected Answer Should Cover" outline ready to
fill in.** Read each scaffold, then follow this session's pattern: deduce/verify the answer with
the user, write the real QA content into the same file (or a differently-named one, then delete
the scaffold), add a `parent:`/`relates:` link from the source unit, build clean.

| # | Unit | Type | Text | Existing scaffold to fill in (or delete if answered elsewhere) |
|---|------|------|------|------|
| 26 | prc-fan-out-a-rule-per-system | question | How is the lead spec determined when multiple implementations already exist for the same SKP_RULE_NNNN? Can the lead be changed manually/selected? | `content/qa/qa-lead-spec-determination-manual-selection.md` |
| 27 | prc-fan-out-a-rule-per-system | note | Visual example: relationship between a lead rule and its generated siblings, shared SKP_RULE_NNNN, system-specific DQOps IDs | *(no scaffold — net-new; needs a diagram/table like the sibling examples already done this session)* |
| 28 | prc-fan-out-a-rule-per-system | question | Does the Studio validate that the generated zSourceSystemID filter matches the correct alias mapping before deployment? | `content/qa/qa-zsourcesystemid-alias-validation-fanout.md` |
| 29 | prc-fan-out-a-rule-per-system | question | If a sibling system is added to the project after fan-out has already been completed, what is the recommended process for generating the missing sibling rule? | `content/qa/qa-sibling-system-post-fanout-generation.md` |
| 30 | prc-run-the-bulk-pipeline | question | If some rules succeed and others fail during a bulk run, can the failed rules be reprocessed individually, or must the entire batch be run again? | `content/qa/qa-bulk-pipeline-reprocess-failed-individually.md` |
| 31 | prc-run-the-bulk-pipeline | question | What should be reviewed first when a rule completes with warnings but does not fail the pipeline? | `content/qa/qa-bulk-warnings-review-priority.md` |
| 32 | prc-generate-the-skp-assetupload | note | Visual mapping example: tracker rows, specs, ClientRefs, DQOps IDs → Rules and Enforcements sheets | *(no scaffold — net-new)* |

**Also pending a decision (not part of the 8 above, but loose ends from Items 3, 10, 22):**
- `content/qa/qa-studio-configuration-file-location.md` — scaffold for the skipped Item 3. Decide: adopt its content (it may already have a reasonable answer path — re-check with user) or leave skipped.
- `content/qa/qa-implication-detail-scope-fetch-technical.md` — stale scaffold for Item 10, which was answered directly inside `prc-format-an-implication.md`. Likely delete.
- `content/qa/qa-ai-validator-repaired-issues-visibility.md` — stale scaffold for Item 22, which was answered directly inside `ref-ai-static-validator-gate.md`. Likely delete.

---

## QA units created this session (12 total, after the merge)

1. `qa-optional-studio-spaces-per-engagement.md`
2. `qa-sample-rule-review-before-authoring.md`
3. `qa-ai-enhance-accept-vs-review.md`
4. `qa-when-additional-cte-acceptable.md`
5. `qa-catalog-to-bespoke-rule-conversion.md`
6. `qa-bespoke-to-catalog-promotion.md`
7. `qa-sibling-divergence-realignment.md`
8. `qa-ai-quality-gate-serious-findings.md`
9. `qa-profiling-rules-quality-gate-exclusion.md`

(9 files above; the other ~8 QA units mentioned in chat during the session were the *scaffolds*
from the other session, now deleted where merged.)

## Source units enhanced this session

- `content/procedures/prc-studio-onboarding.md`
- `content/procedures/prc-derive-a-dq-rule.md`
- `content/procedures/prc-format-an-implication.md`
- `content/concepts/con-catalog-vs-bespoke-rules.md`
- `content/reference/ref-local-deriver.md`
- `content/reference/ref-ai-derive-and-enhance-internals.md`
- `content/reference/ref-ai-static-validator-gate.md`
- `content/standards/std-cte-rules.md` (added a QA link in "Questions from consultants")

## Deleted this session (superseded scaffolds, merged into the files above)

- `qa-studio-spaces-required-vs-optional.md`
- `qa-sample-rules-for-review-before-creating.md`
- `qa-ai-enhanced-logic-accept-modify-reject-default.md`
- `qa-when-additional-cte-acceptable-preferred.md`
- `qa-catalog-to-bespoke-rule-origin-conversion.md`
- `qa-bespoke-to-catalog-promotion-criteria.md`
- `qa-sibling-realignment-after-divergence.md`
- `qa-serious-findings-trigger-validator-retry.md`
- `qa-profiling-rules-excluded-from-validator.md`

---

## How to resume next session

1. **Sanity check first:** `git log --oneline -5` and diff against this file's assumptions —
   confirm no other session touched Changeset 7 content again since this was written.
2. **Build clean baseline:** `python3 build/build.py` — should show ~294 units, 0 errors, 0
   warnings before you touch anything.
3. **Work Items 26–32** using the existing scaffolds as your outline — same workflow as this
   session: state a deduced answer, ask the user to confirm/correct (they push back hard on wrong
   deductions — see Item 7's "fan-out ≠ joins" correction and Item 20's real-vs-invented CTE
   reasoning), then write the real content, delete/replace the scaffold, build clean.
4. **Resolve the 3 loose-end scaffolds** (config file location, Implication detail, auto-repair
   visibility) — likely just delete two of them since the answers already live in source units;
   decide the third (Item 3) with the user.
5. **Two net-new visual items remain** (27, 32) — both want a relationship diagram/table (lead ↔
   siblings ↔ SKP_RULE_NNNN ↔ DQOps IDs, and tracker-row ↔ spec ↔ ClientRef ↔ DQOps ID → Rules/
   Enforcements sheet mapping). Ask the user for a screenshot of the Ship/fan-out screens if one
   isn't already in this conversation's history, same as was done for Items 1 and 2.
6. **When all 34 items are done:** move the changeset JSON to `feedback/applied/`, do a final
   `python3 build/build.py`, and write a final session summary (following the style of
   `SESSION_SUMMARY_2026-09-02.md`) documenting the complete Changeset 7 closure.

---

## Key corrections/lessons from this session (don't repeat these mistakes)

- **"Fan-out" means multi-system rule replication, not query-join multiplication.** Don't conflate
  the two when writing about CTEs or AI Enhance.
- **Don't invent examples/screenshots — ask the user first**, but once they say "create your own,"
  do so confidently and completely (see Items 7, 14 for good examples of user-corrected then
  self-authored content).
- **When the user says "check the unit" or "deduce it,"** read the actual source content before
  answering — don't guess from the question text alone.
- **Not every question needs a QA unit** — sometimes the user wants the answer folded directly
  into the source procedure (Items 10, 22). Ask if unsure.
- **Heading levels:** this codebase's build only supports `##`/`###` — any `####` gets
  demoted with a build warning. Keep QA unit sub-sections at `###`.
