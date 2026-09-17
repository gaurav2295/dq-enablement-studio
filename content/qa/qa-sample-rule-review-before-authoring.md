---
id: qa-sample-rule-review-before-authoring
type: qa
title: Should I review an example rule before writing my first DQ rule?
domain: rule-design
audience: [consultant]
level: practitioner
status: approved
sources:
  - coe:prc-derive-a-dq-rule
created: 2026-09-02
updated: 2026-09-02
links:
  - parent:prc-derive-a-dq-rule
  - relates:std-output-field-sections
  - relates:std-rule-pattern-library
  - relates:gls-optsel
  - relates:gls-rptsel
  - relates:std-cte-rules
---

## Question

Are there any recommended examples or sample rules that demonstrate a well-structured DQ rule to review before creating a new Rule?

## Answer

**Yes — always.** Before authoring your first rule, read a well-structured rule **end-to-end**, focusing on:

### Why Review First?

The rule spec structure is **rigid and repetitive**. Once you recognize the pattern (CTEs, JOIN strategy, zIsErrorFlag CASE, five-section SELECT, OptSel + RptSel pair), writing new rules becomes **pattern-matching, not starting from blank**. It's faster and more accurate than learning from documentation alone.

### What to Review

See [[prc-derive-a-dq-rule|Derive a DQ Rule (single rule)]] — the **"Review an Example Rule"** section includes a complete, annotated rule showing:

- **Three CTEs pre-aggregating** to prevent fan-out when joining back to the master record
- **Cross-system safe joins** (every join includes `AND zSourceSystemID = ...`)
- **Comments explaining intent, not mechanics** ("Join to header to access posting date" vs "Join MSEG to MKPF")
- **Five-section SELECT** in order: Technical → Basic → Org → Value → Activity
- **zIsErrorFlag CASE** for logic, **WHERE** for exclusions
- **Both OptSel and RptSel views** (full records + error filter)

### The Key Patterns to Recognize

| Pattern | Why |
|---|---|
| **CTE pre-aggregation** | Prevents fan-out when joining back to a master record with one-to-many detail tables |
| **zSourceSystemID on every join** | Ensures cross-system correctness; missing it can match wrong records |
| **CASE for validity, WHERE for exclusions** | Status/validity logic goes in SELECT; deletion flags/scope filters go in WHERE |
| **GREATEST/ISNULL for multi-signal logic** | Handles "check any of three dates" or "pick the max" across optional signals |
| **OptSel = all records, RptSel = errors only** | OptSel is the full dataset; RptSel is `SELECT * FROM OptSel WHERE zIsErrorFlag = 1` |

### Checklist: What to Look For When Reviewing an Example Rule

Use this checklist as you read the example rule to ensure you understand each component:

**Output Fields (5 sections in order)**
- [ ] Technical Fields: `zSourceSystemID`, `zConcatenatedKey`, `zIsErrorFlag` present and first
- [ ] Basic Fields: Primary Key (e.g., MATNR) + 2-3 key descriptive columns (e.g., MTART, MATKL)
- [ ] Org Fields: Department/cost center/division filters (if applicable to this rule)
- [ ] Value Context: The field(s) actually under check (e.g., dates, amounts, status)
- [ ] Activity Fields: Tracking fields like creation date, last change date, timestamps

**Logic (zIsErrorFlag)**
- [ ] CASE expression present with clear condition
- [ ] Comments explain the error condition (e.g., "Most recent activity is older than two years")
- [ ] zIsErrorFlag is INTEGER (1 or 0), never text or boolean
- [ ] Condition matches the rule's intent from the rule name

**CTEs & Joins**
- [ ] CTEs pre-aggregate (GROUP BY with MAX/MIN) to avoid fan-out
- [ ] Every CTE and every JOIN includes `AND zSourceSystemID = ...`
- [ ] Comments explain **why** each join exists (purpose), not just mechanics
- [ ] LEFT OUTER joins used unless there's a genuine requirement to filter out non-matches
- [ ] No direct many-to-many joins without deduplication first

**Filters (WHERE clause)**
- [ ] Deletion flags (e.g., LVORM) in WHERE, NOT in CASE
- [ ] Status/validity checks (e.g., "is active") in CASE, NOT in WHERE
- [ ] System filter (zSourceSystemID) in WHERE on main table
- [ ] Each filter has a comment explaining what it excludes (e.g., `/* Exclude records flagged for deletion */`)

**Views (OptSel + RptSel)**
- [ ] OptSel shows all records with zIsErrorFlag populated
- [ ] RptSel is the canonical form: `SELECT * FROM [OptSel] WHERE [zIsErrorFlag] = 1`
- [ ] RptSel name matches OptSel name with `-RptSel` suffix
- [ ] Both views have identical header blocks (Rule ID, name, date, target platform)

### How to Use the Example

1. **Read the SQL top-to-bottom** — comments explain joins and logic
2. **Use the checklist above** — verify each component is present and correct
3. **Trace one record's path** — pick a material number and follow it through the CTEs, joins, and CASE
4. **Compare to your rule** — when you author your own, use this as a template; adapt the tables/fields, keep the structure

### If You Can't Find an Existing Rule

If your project doesn't have sample rules yet:
- Use **Local Derive** on a placeholder rule name to see the generated structure
- Review the [[std-output-field-sections|Output Field Sections]] standard to understand the five-section SELECT
- Review the [[std-cte-rules|CTE Rules]] standard for join strategy and fan-out prevention
- Check the [[std-rule-pattern-library|Rule Pattern Library]] for pre-built patterns by rule type (Error, Info, Profiling)
- Then write your rule spec step-by-step

### Related

- [[prc-derive-a-dq-rule|Derive a DQ Rule (single rule)]]
- [[std-output-field-sections|Output Field Sections]]
- [[std-cte-rules|CTE Rules — When to Use, How to Structure]]
