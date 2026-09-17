---
id: prn-studio-workflow-guardrails
type: principle
title: The Nine Workflow Guardrails
domain: studio
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:prn-studio-non-negotiables
  - relates:prn-optsel-is-the-universe
  - relates:ref-bulk-pipeline
  - relates:std-output-field-sections
sources:
  - dq-studio:docs/Studio_Overview.md
tags: [studio, doctrine, methodology, sql, guardrail]
created: 2026-08-20
updated: 2026-08-20
---

## The principle

The Studio encodes nine guardrails **so that the user cannot accidentally produce non-compliant
output.** Where [[prn-studio-non-negotiables]] states what the generated artefacts must look like,
these state what the *application* will and will not do on the user's behalf. Each one closes a
failure mode that was observed in real batches.

## Quick reference: All nine guardrails at a glance

| # | Guardrail | Primary Purpose | Impact |
|---|-----------|-----------------|--------|
| 1 | Mandatory tech fields | Every Error rule carries zSourceSystemID, zConcatenatedKey, zIsErrorFlag | Defect counting works; audit trail is traceable |
| 2 | zIsErrorFlag = INTEGER 1/0 | Ensures RptSel WHERE filter works correctly | Report accuracy; defect counts reconcile |
| 3 | OptSel is the universe | Error-logic lives in CASE, not WHERE clause | Rules scale; status fields don't hide defects |
| 4 | RptSel is canonical wrapper | Single canonical view shape for all Error rules | Deployment is predictable; audit is consistent |
| 5 | Force Error when user says Error | User intent overrides catalog label | Engagement rules apply, not source rules |
| 6 | Sibling fan-out has own id | Each implementation is independently traceable | Tracker reconciliation works; defects map to code |
| 7 | Catalog SQL preserved through AI | AI doesn't re-derive catalog SQL | Authoritative SQL survives; no silent rewrites |
| 8 | Section comments mandatory | OptSel/InfSel must have required field headers | Readers understand field organization |
| 9 | Fetch/Check/Return template | Description follows consistent narrative | Descriptions render the same in MD, Excel, Tracker |

## 1. Methodology fields are mandatory for every Error rule

The Studio enforces that **every** OptSel deployed as Error carries three columns:

| Column | Form |
|---|---|
| `zSourceSystemID` | `<table>.zSourceSystemID AS [zSourceSystemID]` (a literal when the query has a GROUP BY) |
| `zConcatenatedKey` | built with `CONCAT(...)`, separator `'_'` — never a pipe |
| `zIsErrorFlag` | `CASE WHEN <error_condition> THEN 1 ELSE 0 END AS [zIsErrorFlag]`, or `1 AS [zIsErrorFlag]` with a `/* TODO: literal 1 */` marker when no per-row predicate could be extracted |

**No fallback to raw catalog passthrough.** If the promoter cannot extract a clean predicate, the
literal-1 fallback keeps the column *present* so the canonical RptSel filter
(`WHERE [zIsErrorFlag] = 1`) still works, and the audit page surfaces the TODO marker for the DBA
to refine. The guardrail is that the column always exists — a missing tech column is a High
finding, a literal-1 is a Medium one.

See [[std-output-field-sections]], std-req-sql-missing-tech-columns,
ref-zconcatenatedkey-and-ziserrorflag-sql-emission. The argument order inside the `CONCAT(...)`
is deliberately not stated here — it differs between the local-derive and catalog paths, an open
disagreement recorded as CONFLICT-007 in [[std-zconcatenatedkey-convention]] and
ref-catalog-promotion.

## 2. zIsErrorFlag is INTEGER 1/0

Not `'Yes'`/`'No'`, not `'Y'`/`'N'`, not `1` over a pre-filtered set. The OptSel returns the
**universe** with a per-row check; RptSel selects defects via `WHERE [zIsErrorFlag] = 1`.
See [[prn-ziserrorflag-is-integer]].

## 3. OptSel is the universe

The error-detection predicate goes in the `CASE WHEN` driving the flag — never in a top-level
`WHERE`. `WHERE` is reserved for exactly two things:

- the system filter (e.g. `WHERE zSourceSystemID = 'ECCZ02100'`)
- deletion-flag exclusions (`LVORM`, `LOEKZ`, `LOEVM`)

Status fields (`MMSTA`, `PSTAT`, `STATU`) drive the logic CASE — they are **never** relocated to
`WHERE`. See [[prn-optsel-is-the-universe]] and [[con-deletion-flags-vs-status-fields]].

## 4. RptSel is the canonical wrapper

```sql
CREATE VIEW <…RptSel> AS
SELECT * FROM <…OptSel>
WHERE [zIsErrorFlag] = 1
;
```

For Profiling rules the `WHERE` filter is omitted — there is no flag column to filter on. See
[[prn-profiling-has-no-pass-fail]] and ref-profiling-view-generation.

## 5. Force Error when the user says Error

The import template's `rule_type` column is honoured **even when the catalog disagrees.** A catalog
rule tagged Info that the user marks as Error in the template ships as Error with full methodology
applied — no silent downgrade to InfSel.

The user's declaration of intent outranks the catalog's own label, because the catalog label
describes how that rule was *originally* published, not how this engagement is deploying it. The
audit's `tracker-error-shipped-as-infsel` check exists to catch the case where the pipeline
downgraded anyway. See [[con-catalog-vs-bespoke-rules]] and ref-catalog-deriver.

## 6. Sibling fan-out has its own DQOps id

Each fan-out implementation carries its own `rule_id`, kept consistent across its system code,
view-name alias, SQL banner, and tracker identifier.

**The deployed view name, the SQL banner, and the tracker DQOPSID always agree.** All three
carrying the same id is what makes a deployed rule traceable back to one tracker row; the audit's
`tracker-dqops-view-name-mismatch` and `view-name-rule-id-mismatch` checks exist because a partial
swap silently breaks that. See ref-multi-impl-fan-out-engine,
ref-bulk-processor-and-dqops-id-invariants, [[prc-fan-out-a-rule-per-system]].

## 7. Catalog rules preserve their SQL through the AI pipeline

Bulk AI **step 1** (rule-name enhancement) runs on catalog rules; **step 2** (local re-derive) and
**step 3** (per-impl AI SQL review) are guarded so they cannot replace the catalog-derived spec.
The methodology fields injected by the catalog deriver always survive AI processing.

The catalog ships authoritative SQL. Letting a re-derive overwrite it would discard the one part
of the rule that was already validated, in exchange for a name improvement. See
ref-catalog-promotion and [[prn-catalog-promotion-wraps-instead-of-injecting]].

## 8. Section comments are mandatory

```text
-- Syniti Technical Fields
-- Basic Fields
-- Organizational Context
-- Value Context
-- Activity Context
```

The validator flags any OptSel/InfSel missing the required Tech section. The headers appear even
when a section is empty — their absence, not their emptiness, is the defect. See
[[std-output-field-sections]], [[std-sql-comment-standards]],
std-req-sql-section-header-order.

## 9. Description template — Fetch / Check / Return

Every rule's markdown description follows:

```text
**1. Functional/Business Description**
<why this matters>

**2. Specific Relevancy Criteria/Scope**
<what records the rule applies to>

**3. DQ Checks (Conditions)**
- **Fetch** — Retrieve all records from <tables>.
- **Check** — Mark any record where: <error_condition>
- **Return** — Error records are <description of defect impact>.
```

The in-cell line break is written as the literal `<br />` token so the same text renders cleanly in
Markdown, in an Excel paste, and in the Tracker — one description string, three destinations, no
per-destination reformatting. See [[prn-fetch-check-return]] and
[[std-rule-description-template]].

## At-a-glance: Guardrail response matrix

When each guardrail is violated, the Studio responds as follows:

| # | Guardrail | Violation Response | User sees |
|---|-----------|-------------------|-----------|
| 1 | Mandatory tech fields | Emits literal-1 with /* TODO */ | ⚠ Mark for review |
| 2 | zIsErrorFlag = INTEGER | Rejects the spec | ❌ Un-deployable |
| 3 | OptSel is universe | Rejects the spec | ❌ Un-deployable |
| 4 | RptSel is wrapper | Repairs to canonical form | ✅ Auto-fixed |
| 5 | Force Error intent | Emits downgrade warning | ⚠ Mark for review |
| 6 | Fan-out sibling IDs | Audit flag; doesn't block | ⚠ Audit finding |
| 7 | Catalog SQL preserved | Audit flag; doesn't block | ⚠ Audit finding |
| 8 | Section comments | Emits missing headers | ⚠ Mark for review |
| 9 | Fetch/Check/Return | Emits incomplete template | ⚠ Mark for review |

**Key:** Blocks (❌) = rule un-deployable; Repairs (✅) = auto-fixed; Warns (⚠) = audit review needed.

## Why guardrails rather than guidance

Every one of these could have been a documented convention that a reviewer checks. Encoding them in
the app instead moves the check from *after* a 400-rule batch to *during* it. The pattern is
consistent: the app either refuses the non-compliant shape outright (2, 3) or emits the
compliant shape with a loud marker when it cannot fully derive it (1, 6, 8, 9) — it never quietly
ships something that looks finished and is not.

## Related

[[prn-studio-non-negotiables]] · [[ref-bulk-pipeline]] · ref-audit-engine ·
[[prc-run-the-bulk-pipeline]] · [[prc-audit-rule-quality]] · ref-sql-validator
