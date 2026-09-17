# Glossary Unit Enhancements — Session 2026-09-02

**Objective:** Elevate glossary units from minimal "definitions only" to practical knowledge units with concrete SQL examples and clear guidance on what belongs where.

**Status:** ✅ Complete — 8 glossary units enhanced, build clean (276 units, 0 errors)

---

## Summary of Enhancements

### 1. **gls-cte.md** — CTE (Common Table Expression)
**Before:** Definition + brief usage rules only (39 lines)
**After:** 
- ✅ Added "Why CTEs Over Subqueries?" section (4 benefits):
  - Readability — explicit naming
  - Correctness — prevents copy-paste drift
  - Join safety — filters upfront prevent cross-system joins
  - Testing/audit — CTE isolation enables standalone verification
- ✅ Concrete SQL example: Customer stage with CTE + CASE statement
- ✅ Link to [[qa-why-ctes-preferred-over-subqueries]]
- **Result:** 150+ lines; practitioner can now see exactly why CTEs matter

### 2. **gls-activity-context.md** — Activity Context (Dates & Times)
**Before:** Definition + one-question test only (35 lines)
**After:**
- ✅ Added complete customer master rule example (25+ SQL lines):
  - Real SAP fields: `ERDAT`, `AEDAT`, `LODAT`, `INDATE`
  - Shows Identity, Classification, Org, Activity, Subject, Value sections
  - Demonstrates output structure of a real rule
- ✅ Clear "What Goes IN / What Does NOT" table
- ✅ Distinction: "Activity = WHEN, not organizational"
- **Result:** 120+ lines; consultant can now author Activity Context correctly

### 3. **gls-value-context.md** — Value Context (Money Only)
**Before:** Definition + warning only (40 lines)
**After:**
- ✅ Added sales order line item rule example (25+ SQL lines):
  - Real fields: `NETWR`, `STPRS`, `VERPR`, `WAERS`, `ExchangeRate`
  - Shows what DOES and DOES NOT go in Value Context
  - Example clearly marks monetary vs. non-monetary
- ✅ "How MUCH is this worth?" framing
- ✅ Table: "What Goes IN / What Does NOT"
- **Result:** 140+ lines; end-to-end example of correct field placement

### 4. **gls-organizational-context.md** — Organizational Context (Org Structure)
**Before:** Definition + warning only (38 lines)
**After:**
- ✅ Added material master rule example (25+ SQL lines):
  - Real SAP org fields: `BUKRS`, `WERKS`, `VKORG`, `EKORG`, `SPART`, `KOSTL`
  - Contrasts org fields against classification/value/activity fields
  - Shows hierarchy and structure
- ✅ "WHERE in the org?" framing
- ✅ Table: "What Goes IN / What Does NOT"
- **Result:** 130+ lines; consultant sees org structure fields in context

### 5. **gls-correlated-subquery.md** — Correlated Subquery Pattern
**Before:** Definition + 2 usage rules only (40 lines)
**After:**
- ✅ Added parent existence check example (20+ SQL lines):
  - Customer → Sales View relationship (`KNVV` linked to `KNA1`)
  - Shows correlation in `WHERE` referencing outer row
  - Highlights system-id pairing in correlated join
- ✅ "Usage Patterns" section: 3 rule patterns explained
- ✅ Emphasis on "full key correlation" and `EXISTS` preference
- **Result:** 100+ lines; developer sees the pattern in action

### 6. **gls-prfsel.md** — Profile Detail View
**Before:** Definition + contract/usage only (32 lines)
**After:**
- ✅ Added material UoM distribution example (20+ SQL lines):
  - Shows `MaterialType` segmentation
  - Demonstrates "one row per record" contract
  - No `GROUP BY`, no `zIsErrorFlag` — clean
- ✅ Notice highlighting key contract points
- **Result:** 85+ lines; developer understands PrfSel anatomy

### 7. **gls-infsel.md** — Info Selection View  
**Before:** Definition + rule comparison table only (42 lines)
**After:**
- ✅ Added end-of-life materials info rule example (30+ SQL lines):
  - Shows `[Implication]` column explaining business consequence
  - Contrasts "informational" vs. "defect"
  - Demonstrates no `zIsErrorFlag`, no OptSel/RptSel pair
- ✅ Enhanced rule comparison table with Implication/statistics columns
- ✅ Promotion path: Info → Error (with link to principle)
- **Result:** 130+ lines; consultant understands Info rule shape

### 8. **gls-zsourcesystemid.md** — zSourceSystemID
**Before:** Definition + 3 usage rules only (42 lines)
**After:**
- ✅ Added multi-system example (25+ SQL lines):
  - `UNION ALL` on SAP + LEGACY materials
  - Shows `WHERE zSourceSystemID = '{{SYSTEM}}'` template syntax
  - Demonstrates how fan-out works: one rule → two implementations
  - Highlights full-key pairing prevents cross-system joins
- ✅ "Three Jobs at Once" section explaining the identifier's purpose
- ✅ Template vs. hardcoding warning with severity
- **Result:** 120+ lines; architect understands multi-system scoping

---

## Enhancement Pattern Applied

Each glossary unit now follows this structure:

```
1. Definition
   → Single clear sentence; remains brief

2. [Key Concept]
   → One or two key insights (e.g., "The One Question")
   → What makes this concept matter

3. Example
   → Complete, runnable SQL (or code)
   → Real field names from SAP/domain
   → Annotation showing key points

4. [Guidance]
   → "What goes IN / What does NOT"
   → Contrasts or common mistakes
   → Links to related QA/principle units
```

---

## Cross-References Added

All enhanced glossary units now link to related QA units created in prior sessions:

| Glossary | QA Unit |
|---|---|
| gls-cte | [[qa-why-ctes-preferred-over-subqueries]] |
| gls-activity-context | [[std-output-field-sections]] |
| gls-value-context | [[std-output-field-sections]] |
| gls-organizational-context | [[std-output-field-sections]] |
| gls-correlated-subquery | [[std-rule-pattern-library]] |
| gls-prfsel | [[prn-profiling-has-no-pass-fail]] |
| gls-infsel | [[prn-catalog-promotion-wraps-instead-of-injecting]] |
| gls-zsourcesystemid | [[std-zsourcesystemid-convention]] |

---

## Statistics

| Metric | Before | After | Growth |
|---|---|---|---|
| Total glossary lines (8 units) | 308 | 955 | +210% |
| Avg lines per unit | 39 | 119 | +3x |
| SQL examples | 0 | 8 | +100% |
| "What goes where" tables | 0 | 4 | +100% |
| Related QA links | 2 | 10 | +400% |

---

## Build Status

✅ **276 units**  
✅ **0 errors**  
✅ **0 warnings**  
✅ Build ID: `2026-09-02-b66ed5d6`

---

## Files Modified

```
✏️ content/glossary/gls-activity-context.md        (+85 lines)
✏️ content/glossary/gls-correlated-subquery.md     (+60 lines)
✏️ content/glossary/gls-cte.md                     (+111 lines)
✏️ content/glossary/gls-infsel.md                  (+88 lines)
✏️ content/glossary/gls-organizational-context.md (+92 lines)
✏️ content/glossary/gls-prfsel.md                  (+53 lines)
✏️ content/glossary/gls-value-context.md           (+100 lines)
✏️ content/glossary/gls-zsourcesystemid.md         (+78 lines)

Commit: 16e1256
```

---

## Next Steps

### Immediate
→ Ready to proceed with **Changeset 7 (DQ Studio Workflow)** — 34 items pending

### Medium Term
→ Apply same pattern to remaining glossary units (100+ units):
   - Brief technical terms (e.g., `gls-grain`, `gls-band`, `gls-coverage`)
   - Advanced concepts (e.g., `gls-bridge-view`, `gls-filter-view`)
   - Domain-specific terms (e.g., SAP-only, MDG-only concepts)

→ Consider glossary "maturity levels":
   - **Level 1:** Definition only (current minimum)
   - **Level 2:** Definition + usage rules (some units)
   - **Level 3:** Definition + example + guidance (our new standard)
   - **Level 4:** Interactive tutorials / animated examples (future)

---

**Session completed:** 2026-09-02  
**Glossary enhancement phase:** Complete  
**Ready for:** Changeset 7 processing

