# Deprecation Audit Report — 2026-08-27

**Changeset:** `em-changeset-deprecate-dq-enablement-studio5-2026-08-27.json`
**Date:** 2026-08-27
**Author:** deprecate_dq_enablement_studio5

---

## Summary

This report audits all cross-references to the 7 units marked for deprecation in the changeset. **Action Required:** All wikilinks pointing to these units must be removed or updated before the units can be marked as `deprecated`.

---

## Units to Deprecate (Status: ALL `review`)

| Unit ID | Type | Current Status | Links Found |
|---------|------|----------------|------------|
| `gls-one-mode-one-question` | Glossary | review | 3 files |
| `ref-get-table-last-refresh-date` | Reference | review | 0 files |
| `gls-boa` | Glossary | review | 1 file |
| `gls-crossover` | Glossary | review | 1 file |
| `gls-domain-unknown` | Glossary | review | 1 file |
| `gls-mdg` | Glossary | review | 0 files |
| `gls-key-issue` | Glossary | review | 12 files |

**Total files requiring updates: 18** (some files reference multiple deprecated units)

---

## Detailed Link Analysis

### 1. `gls-one-mode-one-question` (3 references)

**Usage:** Defines the instrument design principle that each mode answers exactly one question.

**Files to update:**

1. **[content/glossary/gls-mode.md:29](content/glossary/gls-mode.md)**
   ```markdown
   ([[gls-one-mode-one-question]]). The five client-facing modes make up the
   ```
   - **Action:** Remove wikilink, reword to standalone text or remove reference entirely
   - **Severity:** HIGH — this is core to mode definition

2. **[content/glossary/gls-the-package.md:36](content/glossary/gls-the-package.md)**
   ```markdown
   modes without the room losing the thread. Under [[gls-one-mode-one-question]] every mode refuses
   ```
   - **Action:** Remove wikilink or reword
   - **Severity:** HIGH — references the principle

3. **[content/glossary/gls-time-to-value.md:34](content/glossary/gls-time-to-value.md)**
   ```markdown
   See [[gls-one-mode-one-question]].
   ```
   - **Action:** Remove entire reference (standalone see-also link)
   - **Severity:** MEDIUM — reference only

---

### 2. `ref-get-table-last-refresh-date` (0 references)

**Status:** ✅ **CLEAN** — No cross-references found. Safe to deprecate.

---

### 3. `gls-boa` (1 reference)

**Usage:** Glossary term for BOA (Business Outcome Architecture / value library).

**Files to update:**

1. **[content/glossary/gls-outcome-category.md:44](content/glossary/gls-outcome-category.md)**
   ```markdown
   list itself is owned by the [[gls-boa|BOA]] value library (the `OUT_CAT` map); neither the
   ```
   - **Action:** Replace `[[gls-boa|BOA]]` with plain text `BOA` or add more context
   - **Severity:** MEDIUM — definitional reference

---

### 4. `gls-crossover` (1 reference)

**Usage:** Glossary term for cross-SoW object relationships.

**Files to update:**

1. **[content/glossary/gls-sow.md:31](content/glossary/gls-sow.md)**
   ```markdown
   Objects that genuinely span two SoWs are handled by an explicit [[gls-crossover|crossover]]
   ```
   - **Action:** Replace `[[gls-crossover|crossover]]` with plain text `crossover` or expand definition inline
   - **Severity:** MEDIUM — definitional reference

---

### 5. `gls-domain-unknown` (1 reference)

**Usage:** Glossary term for unknown domain state in deriver.

**Files to update:**

1. **[content/principles/prn-no-silent-domain-fallback.md:62](content/principles/prn-no-silent-domain-fallback.md)**
   ```markdown
   1. Marks the domain as [[gls-domain-unknown|unknown]] and builds an empty shell — no main
   ```
   - **Action:** Replace `[[gls-domain-unknown|unknown]]` with plain text `unknown` 
   - **Severity:** MEDIUM — principle step definition

---

### 6. `gls-mdg` (0 references)

**Status:** ✅ **CLEAN** — No cross-references found. Safe to deprecate.

---

### 7. `gls-key-issue` (12 references) ⚠️ HIGHEST IMPACT

**Usage:** Core glossary term for the "key issue" concept in the value chain. Critical to the methodology.

**Files to update:**

1. **[content/concepts/con-value-chain.md:47](content/concepts/con-value-chain.md)**
   ```markdown
   [[gls-value-lever]], [[gls-key-issue]]; this unit is about how they connect.
   ```
   - **Severity:** CRITICAL

2. **[content/glossary/gls-bob-dq.md:33](content/glossary/gls-bob-dq.md)**
   ```markdown
   [[gls-business-outcome]] to [[gls-value-lever]] to [[gls-key-issue]] to [[gls-dq-rule]] — with
   ```
   - **Severity:** CRITICAL — defines chain hierarchy

3. **[content/glossary/gls-business-data-driver.md:23](content/glossary/gls-business-data-driver.md)**
   ```markdown
   **The client-facing name for a [[gls-key-issue]].** The same thing, said in the room's language.
   ```
   - **Severity:** CRITICAL — defines relationship

4. **[content/glossary/gls-business-outcome.md:48](content/glossary/gls-business-outcome.md)**
   ```markdown
   [[gls-value-lever]] to [[gls-key-issue]] and on to the rules that measure it. Each outcome
   ```
   - **Severity:** CRITICAL

5. **[content/glossary/gls-business-rule.md:26](content/glossary/gls-business-rule.md)**
   ```markdown
   One [[gls-key-issue]] holds many business rules.
   ```
   - **Severity:** CRITICAL

6. **[content/glossary/gls-cleanse-action.md:36](content/glossary/gls-cleanse-action.md)**
   ```markdown
   - **Value/outcomes** — one of the five attributes a [[gls-key-issue|key issue]] carries.
   ```
   - **Severity:** HIGH

7. **[content/glossary/gls-criticality.md:21](content/glossary/gls-criticality.md)**
   ```markdown
   One of the five attributes a [[gls-key-issue|key issue]] carries: **how badly it bites** — the
   ```
   - **Severity:** HIGH

8. **[content/glossary/gls-governed-vocabulary.md:22](content/glossary/gls-governed-vocabulary.md)**
   ```markdown
   The rule that [[gls-key-issue|key issues]], their names and their
   ```
   - **Severity:** HIGH

9. **[content/glossary/gls-process-area.md:29](content/glossary/gls-process-area.md)**
   ```markdown
   | Value/outcomes (bob-dq) | ...Also one of the five attributes a [[gls-key-issue]] carries. |
   ```
   - **Severity:** HIGH

10. **[content/glossary/gls-readiness-risk.md:21](content/glossary/gls-readiness-risk.md)**
    ```markdown
    One of the five attributes a [[gls-key-issue|key issue]] carries: **what this data problem
    ```
    - **Severity:** HIGH

11. **[content/reference/ref-key-issue-vocabulary.md:26](content/reference/ref-key-issue-vocabulary.md)**
    ```markdown
    [[gls-key-issue]] describes the same discipline from the value-chain side: a key issue sits
    ```
    - **Severity:** CRITICAL

12. **[content/reference/ref-key-issue-vocabulary.md:76](content/reference/ref-key-issue-vocabulary.md)**
    ```markdown
    - [[gls-key-issue]] / [[gls-value-lever]] / [[gls-outcome-category]] — the value-chain
    ```
    - **Severity:** CRITICAL

---

## Recommended Actions by Severity

### 🔴 CRITICAL (5 references to `gls-key-issue`)
- **con-value-chain.md** — Rewrite to describe the concept without linking
- **gls-bob-dq.md** — Inline the definition or restructure the chain description  
- **gls-business-data-driver.md** — Define relationship inline; this is definitional
- **ref-key-issue-vocabulary.md** (2 refs) — Expand or replace with inline definitions

### 🟠 HIGH (10 references)
- All other references to `gls-key-issue` — Replace wikilinks with plain text
- References to `gls-one-mode-one-question` — Simplify or reword
- References to `gls-boa`, `gls-crossover`, `gls-domain-unknown` — Use plain text

### 🟢 CLEAN (2 units)
- `ref-get-table-last-refresh-date` ✅
- `gls-mdg` ✅

---

## Build & Validation

After updating all links:

1. Run the build to verify no validation errors:
   ```bash
   python3 build/build.py
   ```

2. Verify `dist/validation-report.md` is empty or shows no deprecation warnings

3. Update the 7 unit files to `status: deprecated` and add `supersedes:` references if applicable

4. Commit all changes together:
   ```bash
   git add content/ dist/
   git commit -m "deprecate: mark 7 units as deprecated, remove all cross-references"
   ```

---

## Summary Table: Link Removal Checklist

| File | Unit | Line | Action | Priority |
|------|------|------|--------|----------|
| gls-mode.md | gls-one-mode-one-question | 29 | Remove/reword wikilink | HIGH |
| gls-the-package.md | gls-one-mode-one-question | 36 | Remove/reword wikilink | HIGH |
| gls-time-to-value.md | gls-one-mode-one-question | 34 | Remove standalone reference | MEDIUM |
| gls-outcome-category.md | gls-boa | 44 | Convert to plain text | MEDIUM |
| gls-sow.md | gls-crossover | 31 | Convert to plain text | MEDIUM |
| prn-no-silent-domain-fallback.md | gls-domain-unknown | 62 | Convert to plain text | MEDIUM |
| con-value-chain.md | gls-key-issue | 47 | Rewrite to inline definition | **CRITICAL** |
| gls-bob-dq.md | gls-key-issue | 33 | Rewrite to inline definition | **CRITICAL** |
| gls-business-data-driver.md | gls-key-issue | 23 | Rewrite to inline definition | **CRITICAL** |
| gls-business-outcome.md | gls-key-issue | 48 | Convert to plain text / inline | HIGH |
| gls-business-rule.md | gls-key-issue | 26 | Convert to plain text / inline | HIGH |
| gls-cleanse-action.md | gls-key-issue | 36 | Convert to plain text / inline | HIGH |
| gls-criticality.md | gls-key-issue | 21 | Convert to plain text / inline | HIGH |
| gls-governed-vocabulary.md | gls-key-issue | 22 | Convert to plain text / inline | HIGH |
| gls-process-area.md | gls-key-issue | 29 | Convert to plain text / inline | HIGH |
| gls-readiness-risk.md | gls-key-issue | 21 | Convert to plain text / inline | HIGH |
| ref-key-issue-vocabulary.md | gls-key-issue | 26, 76 | Rewrite / inline definitions | **CRITICAL** |

---

## Next Steps

1. ✅ Review this audit report
2. ⏳ Update all 18 files per the checklist above
3. ⏳ Run `python3 build/build.py` to validate
4. ⏳ Mark the 7 units as `status: deprecated`
5. ⏳ Commit all changes together
