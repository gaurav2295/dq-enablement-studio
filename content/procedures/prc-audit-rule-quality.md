---
id: prc-audit-rule-quality
type: procedure
title: Audit Rule Quality
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:sops/SOP — Audit Rule Quality.md
tags: [sop]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:prc-write-a-quality-rule-name
  - relates:prc-format-an-implication
  - relates:prc-fan-out-a-rule-per-system
  - relates:std-output-field-sections
  - relates:std-ziserrorflag-convention
  - relates:std-zconcatenatedkey-convention
  - relates:std-clientref-convention
  - relates:ref-profiler-and-audit-pages
---

## Goal

End-of-sprint checklist for catching the recurring quality issues before specs reach the
client.

## When to use

- Pre-handoff QA after bulk pipeline completes
- Sample audit of an existing client's deployed rules
- Catalog promotion review

## The checklist

### 1. Rule names — scored

Walk the bulk reconciliation Excel's "Score" column. Any rule below 0.7 needs renaming via
[[prc-write-a-quality-rule-name|Write a Quality Rule Name]]. Below 0.5 = block.

### 2. Implications — all populated, all follow the template

For each rule, open the markdown spec's `### Description` block:

- All three sections present
- Section 3 uses Fetch/Check/Return (Error/Info) OR Fetch/Profile/Surface (Profiling) — not
  mixed
- SKP_RULE_ID anchor at the bottom
- Section 2 names the actual universe, not "all records"

Use [[prc-format-an-implication|Format an Implication]] for fixes.

### 3. SQL — section comments present

Every OptSel must show all five section comments in the SELECT:

```sql
-- Syniti Technical Fields
-- Basic Fields
-- Organizational Context
-- Value Context
-- Activity Context
```

Even if empty. See [[std-output-field-sections|Output Field Sections]].

### 4. WHERE comments — match the literal

For each `zSourceSystemID = '<code>'` line, the preceding `/* Include: Limit to source system <label> */` comment must reflect THIS sibling's system, not the lead's.

This is a known stale-comment issue on fanned-out siblings — see
[[prc-fan-out-a-rule-per-system|Fan Out a Rule Per System]] for the repair flow.

### 5. Deletion flags in WHERE, status in CASE

For each Error rule:

- Deletion-flag check (`LVORM <> 'X'`, `LOEKZ <> 'X'`, `LOEVM <> 'X'`) → MUST be in WHERE
- Status-field check (`MMSTA IN ...`, `PSTAT = ...`) → MUST be inside the zIsErrorFlag CASE
- **Same condition** in both = bug. See
  [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]].

### 6. zIsErrorFlag is integer 1/0

Search for any `zIsErrorFlag` that uses `'Y'`, `'Yes'`, `'1'` (string), `TRUE` → reject and fix
per [[std-ziserrorflag-convention|zIsErrorFlag Convention]].

### 7. zConcatenatedKey — correct spelling

Search for `zConcatenated Key` (with space), `ZConcatenatedKey`, or any other variant. Replace
with `zConcatenatedKey` per [[std-zconcatenatedkey-convention|zConcatenatedKey Convention]].

### 8. Catalog parity (catalog rules only)

For each catalog-source rule, the Studio's [[ref-profiler-and-audit-pages|Audit page]] computes
parity vs the catalog's verbatim
OpQuerySQL / ReportQuerySQL. Parity < 0.8 = investigate; the spec may have drifted from the
catalog.

### 9. Per-system fan-out completeness

For each rule, verify that the generated siblings match your deployment scope. A rule that should fan out to 3 systems but only has 1 sibling is a **generation defect**.

**How to verify:**

1. Pick a rule from the bulk reconciliation Excel (e.g., `SKP_RULE_0042`)
2. Count how many sibling views exist in the SQL export
3. Compare to the deployment scope

| Rule | Expected siblings | Actual siblings | Status | Action |
|---|---|---|---|---|
| SKP_RULE_0042 | 3 (Z02, Z06, Z09) | 3 | ✅ Complete | Deploy |
| SKP_RULE_0043 | 3 (Z02, Z06, Z09) | 1 (Z02 only) | ❌ Incomplete | Re-run bulk pipeline |
| SKP_RULE_0044 | 3 (Z02, Z06, Z09) | 2 (Z02, Z06) | ⚠️ Partial | Check Systems column override |

**Why siblings go missing:**

| Symptom | Likely cause | Fix |
|---|---|---|
| Only 1 sibling when 3 expected | `Systems` column in input XLSX not populated | Add system codes to tracker row |
| Some systems skipped (e.g., Z09 missing) | Alias map incomplete | Add `Z09 → P09` to project config |
| Different rules have different counts | Inconsistent system scope | Verify project's canonical deployment scope |

**Important:** If a rule **should** fan out to 3 systems but doesn't, the Implication cell will be wrong in SKP — it'll reflect only the first system (Z02). Re-run the rule through the bulk pipeline to generate all siblings.

### 10. ClientRef populated

Every rule in the tracker must have a `ClientRef` value. Missing ClientRef causes the row to be **dropped silently** during SKP export — rules vanish from the asset upload without warning.

**How to verify:**

1. Open the bulk reconciliation Excel
2. Scan the `ClientRef` column for blanks
3. For each blank, populate it with the matching `SKP_RULE_NNNN` from the spec

| Tracker Row | SKP_RULE_ID | ClientRef | Status |
|---|---|---|---|
| Rule 0042 | SKP_RULE_0042 | SKP_RULE_0042 | ✅ Populated |
| Rule 0043 | SKP_RULE_0043 | *(blank)* | ❌ Missing |
| Rule 0044 | SKP_RULE_0044 | SKP_RULE_0044 | ✅ Populated |

**What happens if ClientRef is blank:**

```
Bulk pipeline runs → generates specs + SQL ✅
SKP exporter reads tracker → sees blank ClientRef → skips row ⚠️
Asset upload file created WITHOUT rule 0043
User uploads to SKP → rule 0043 vanishes from the system 💥
Audit discovers missing rule in SKP but specs are ready → confusion
```

**Recovery:**

1. Add `ClientRef = SKP_RULE_0043` to the tracker row
2. Re-run the SKP exporter (only the rows with populated ClientRef)
3. Re-upload the updated asset file

**Timing:** Populate ClientRef **before** the bulk pipeline runs, or **immediately after** it finishes, before SKP export.

## Tools

- Studio's Audit screen — parity scoring + reconciliation
- Bulk reconciliation Excel — warnings + scores

## Common patterns when things fail

| Symptom | Likely cause |
|---|---|
| Some siblings missing | `Systems` column override on the input xlsx; or alias map gap |
| Implication cell empty in AssetUpload | Spec's `description` field is empty — older profiling specs may not have it populated |
| Comments lie about system | Stale comment bug on fanned-out siblings — see [[prc-fan-out-a-rule-per-system|Fan Out a Rule Per System]] |
| Catalog rule parity < 0.5 | The bespoke editing has drifted from catalog; either revert or upgrade the catalog entry |

## Questions from consultants

- [[qa-catalog-parity-acceptable-differences|What parity differences are acceptable in catalog audit?]]

## Related

- [[prc-write-a-quality-rule-name|Write a Quality Rule Name]]
- [[prc-format-an-implication|Format an Implication]]
- [[prc-fan-out-a-rule-per-system|Fan Out a Rule Per System]]
- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]]
- [[ref-profiler-and-audit-pages|Studio — Profiler & Audit Pages]]
- Studio — Audit Engine
