# Changeset 7: DQ Studio Workflow — Processing Strategy

**Status:** Initiated  
**Exported:** 2026-08-31  
**Total Items:** 31 (17 questions + 14 notes)  
**Affected Units:** 10

---

## 📋 CHANGESET INVENTORY

### Questions by Theme (17 total)

**Studio Setup & Navigation (3Q)**
- Q1: Where is project configuration file? → `qa-studio-configuration-file-location.md` ✅ CREATED
- Q2: Are all 5 spaces optional or required? → `qa-studio-spaces-required-vs-optional.md` ✅ CREATED
- Q3: What to do if source system missing? → Clarification note, not separate QA

**Rule Derivation & AI (6Q)**
- Q4: Sample rules to review before creating? → `qa-sample-rules-for-review.md` (PLANNED)
- Q5: Accept/reject unrequested AI logic? → `qa-ai-enhanced-logic-accept-modify-reject-default.md` ✅ CREATED
- Q6: When is additional CTE acceptable? → `qa-when-additional-cte-acceptable-preferred.md` (PLANNED)
- Q7: How much detail in Scope/Fetch? → `qa-implication-detail-scope-fetch-technical.md` (PLANNED)
- Q8: Realign skipped siblings? → `qa-sibling-realignment-after-divergence.md` (PLANNED)

**Catalog & Rules (2Q)**
- Q9: Convert Catalog→Bespoke? Maintain origin? → `qa-catalog-to-bespoke-conversion.md` (PLANNED)
- Q10: Promote Bespoke→Catalog criteria? → `qa-bespoke-to-catalog-promotion-criteria.md` (PLANNED)

**Local Deriver (1Q)**
- Q11: What qualifies spec as thin? → `qa-what-qualifies-as-thin-spec.md` ✅ CREATED

**Quality Gates & Validation (4Q)**
- Q12: Repaired issues visible to user? → `qa-ai-validator-repaired-issues-visibility.md` (PLANNED)
- Q13: What findings trigger serious retry? → `qa-serious-findings-trigger-retry.md` (PLANNED)
- Q14: Why exclude profiling rules? → `qa-profiling-rules-excluded-from-validator.md` (PLANNED)
- Q15: Low-confidence hint meaning? → Enhancement note in ref-ai-derive-and-enhance-internals

**Fan-Out & Multi-System (3Q)**
- Q16: Determine lead spec? Manual selection? → `qa-lead-spec-determination-manual-selection.md` (PLANNED)
- Q17: Validate zSourceSystemID matches alias? → `qa-zsourcesystemid-alias-validation.md` (PLANNED)
- Q18: Add sibling system post-fanout? → `qa-sibling-system-post-fanout-generation.md` (PLANNED)

**Bulk Pipeline (2Q)**
- Q19: Reprocess failed rules individually? → `qa-bulk-pipeline-reprocess-failed-individually.md` (PLANNED)
- Q20: Review priority for warnings? → `qa-bulk-warnings-review-priority.md` (PLANNED)

### Notes by Type (14 total)

**Visual/Diagrams (4)**
- prc-studio-onboarding: Navigation diagram of 5 spaces
- prc-fan-out-a-rule-per-system: Lead rule ↔ siblings, SKP_RULE_NNNN, DQOps IDs
- prc-generate-the-skp-assetupload: Tracker → specs → ClientRefs → Rules/Enforcements mapping
- ref-ai-derive-and-enhance-internals: Before-and-after AI Enhance example

**Screenshots (2)**
- prc-studio-onboarding: Project Hub, Session Setup, Settings/Config, 5 Studio spaces
- con-catalog-vs-bespoke-rules: Audit screen showing Catalog vs Bespoke difference

**Examples & Diffs (3)**
- prc-derive-a-dq-rule: Accept vs Reject diff (safe vs careful review)
- ref-local-deriver: Unknown domain vs known/no-match comparison
- ref-local-deriver: Thin spec example

**Clarifications (3)**
- prc-studio-onboarding: Missing source system/database handling
- ref-local-deriver: Spec skeleton when domain known but no field matched
- prc-format-an-implication: Define Implication, rule logic influence

**Comparisons/Audit (2)**
- con-catalog-vs-bespoke-rules: RuleOrigin, 'no catalog ref', parity scoring on Audit
- ref-ai-static-validator-gate: AI SQL Quality Gate vs Audit Rule Quality

---

## 🎯 PROCESSING APPROACH

### Phase 1: Create QA Units (In Progress)
**Status:** 3 of ~17 QA units created

**Approach:**
1. Create one QA unit per question
2. Each QA contains:
   - Clear question statement
   - Context (why this matters)
   - Related concepts (wikilinks)
   - Expected answer structure
   - Status: "Awaiting answer"

**Estimated QA Count:** 17 units  
**Created So Far:**
- ✅ qa-studio-configuration-file-location
- ✅ qa-studio-spaces-required-vs-optional
- ✅ qa-what-qualifies-as-thin-spec
- ✅ qa-ai-enhanced-logic-accept-modify-reject-default

**To Create:** 13 more QA units (in progress)

### Phase 2: Enhance Source Units (After QAs Complete)
**Affected Units:**
1. `prc-studio-onboarding` — Add navigation diagram, screenshots, clarifications
2. `prc-derive-a-dq-rule` — Add Accept/Reject diff, sample rules
3. `con-catalog-vs-bespoke-rules` — Add Audit screen example, RuleOrigin explanation
4. `ref-local-deriver` — Add thin spec example, domain comparison
5. `prc-format-an-implication` — Add complete example with Implication definition
6. `ref-ai-derive-and-enhance-internals` — Add before-after example, low-confidence explanation
7. `ref-ai-static-validator-gate` — Add comparison with Audit Quality
8. `prc-fan-out-a-rule-per-system` — Add visual mapping of lead ↔ siblings
9. `prc-run-the-bulk-pipeline` — Already covered by QAs
10. `prc-generate-the-skp-assetupload` — Add visual mapping tracker → rules

### Phase 3: Build & Validate
- Run `python3 build/build.py`
- Verify all wikilinks resolve
- Move changeset file to feedback/applied/
- Create session summary

---

## 📊 ESTIMATED EFFORT

| Phase | Items | Est. Time |
|-------|-------|-----------|
| Phase 1 (QA Creation) | 17 QA units | 1-2 hours |
| Phase 2 (Source Enhancement) | 10 units + visuals | 2-3 hours |
| Phase 3 (Build & Validate) | 1 build cycle | 30 min |
| **TOTAL** | **34 items** | **3.5-5.5 hours** |

---

## ❓ QUESTIONS FOR YOU

Before I continue with full Phase 1 (creating all 17 QA units):

1. **➡️ Approach OK?** Is this the right way to process Changeset 7?
   - Create QA units for questions
   - Enhance source units with note guidance
   - Create/add visual examples where requested

2. **📝 QA Unit Quality?** Do the 4 QA units created so far look good?
   - Question clearly stated?
   - Context section helpful?
   - Expected answer structure useful?

3. **⏱️ Proceed with Full Phase 1?** Should I create the remaining 13 QA units now?

4. **📸 Visuals?** For the 4 diagrams/screenshots requested:
   - Should I create placeholder descriptions in the source files?
   - Or create ASCII diagrams/mockups?
   - Or skip for now (you'll add later)?

5. **🔗 Any Clarifications Needed?** Do you want me to reach out on specific questions before writing QA units?

---

## 🚀 Next Steps (Waiting for Your Approval)

**If YES → Proceed:**
- Continue creating 13 more QA units (next 2 hours)
- Then enhance 10 source units with note guidance
- Build and validate

**If ADJUSTMENTS:**
- Tell me what to change, I'll adapt the approach

**Status:** Ready to continue on your signal 🎯

