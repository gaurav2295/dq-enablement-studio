---
id: std-ai-enhance-scope
type: standard
title: AI Enhance Edit Scope — What the Model May and May Not Change
domain: ai-enhancement
audience: [developer, consultant]
level: practitioner
status: review
sources:
  - dq-studio:docs/ai_enhance_instructions.md
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
tags: [methodology, convention, agent, governance]
links:
  - relates:std-ai-enhance-guardrails

  - relates:ref-ai-derive-and-enhance-internals
  - relates:ref-ai-static-validator-gate
  - relates:std-output-field-sections
  - relates:prn-no-silent-domain-fallback
  - relates:gls-ai-additions
  - relates:gls-ai-enhance
  - relates:gls-rule-fulfilment-review
created: 2026-08-20
updated: 2026-08-20
---

## The standard

AI Enhance is a **bounded editor, not an author**. The deterministic shell
([[ref-local-deriver]] plus ref-sql-generator) owns the artefact's structure; the model is
handed that artefact and asked one question first and one question second:

1. **Rule fulfilment** — does this SQL actually check what the rule name says it checks?
2. **Correction** — fix it where it doesn't.

A rule can be syntactically perfect and still useless if its `zIsErrorFlag` logic tests the
wrong condition. That is the defect class AI Enhance exists to catch. Everything else it
touches is scope creep, and scope creep is diffed and reported.

## What the model is given

- The rule name — the business statement of intent.
- The structured spec — output fields already categorised into the five sections
  ([[std-output-field-sections]]), plus joins, filters, and deletion-flag handling already
  applied by the deterministic path.
- The generated SQL (OptSel + RptSel).
- Any extra notes the rule author supplied.

## What AI Enhance MAY change

| Licensed change | Conditions |
|---|---|
| **`zIsErrorFlag` logic** | The core of the review. Correct it whenever it doesn't test what the rule name requires. |
| **Joins** | Only when the rule as built does not fulfil its stated purpose. A changed or added join carries a `/* ... */` comment explaining *why* in business terms, and is listed under `AI ADDITIONS`. |
| **Added output fields** | If an extra field makes the rule more useful or complete. Listed under `AI ADDITIONS` so it is distinguishable from what the deterministic shell produced. |
| **TBD placeholder replacement** | Mandatory, never optional. First `TBD` (table position) resolves to the main table; second (field position) to the main field. Inconsistent table/field references elsewhere in the SQL are corrected throughout to match. |
| **Full restructuring** | When the supplied shape is fundamentally wrong for the rule — it queries one table when the rule needs a related table's status, or its join chain cannot reach the data. Rebuild rather than patch. |

Licensed does not mean unconstrained. Whatever the model changes still obeys the SQL rules in
[[std-ai-enhance-guardrails]] — in particular the mandatory `zSourceSystemID` filtering (main
table, every symmetric-field join, every CTE), the CTE discipline, and the comment rules. Those
are conditions on the licence, not a separate topic.

> [!important] Restructure with a reason, not for its own sake
> Fields, aliases, and sections that don't need touching to make the rule correct are left
> alone. Don't rename or reorder something because it reads better. A rule that still doesn't
> work after a "fix" is a worse outcome than a rebuilt one that does — but a cosmetic rewrite
> of a working rule is pure risk with no upside.

## What is locked

An automated scope check diffs the corrected SQL against the pre-AI shell **section by
section**. Only the `joins` and `logic` sections are editable. Every other region is locked:

- The five output-field sections — Syniti Technical Fields, Basic Fields, Organizational
  Context, Value Context, Activity Context — and their order.
- The three Syniti Technical Fields themselves: `zSourceSystemID`, `zConcatenatedKey`,
  `zIsErrorFlag`.
- The mandatory header comment banner.
- WHERE-exclusion clauses (deletion-flag handling and scope filters the shell applied).

A difference outside the editable sections is a `Fail`-severity finding — see
std-req-ai-edit-scope for the formal contract. Note the practical consequence: a **full
restructure is licensed by the prompt but will register as out-of-scope edits** in the check.
That is intended — the restructure becomes visible and reviewable rather than silently
accepted.

## The table/field trust rule

The model may use its own SAP knowledge to introduce a table or field that *should* be part of
the rule even if it isn't in the supplied spec or SQL — it is not limited to what is already
there. But:

> [!warning] Anything introduced is unverified until proven otherwise
> Any table or field the model introduces that wasn't already present **must be flagged
> "unverified — confirm against the SAP dictionary before deploying"**. Never state an
> introduced table/field as if it were already confirmed. This applies to a full rebuild
> exactly as it applies to a single added field.

Enforced by an automated table/field trust check — see std-req-trust-ai-unverified-field.

For conventions the prompt does not restate — deletion flags versus status fields, for example
— the model relies on its own SAP knowledge, which is why the deterministic layer re-checks
the result rather than trusting it ([[ref-deletion-flag-resolver]],
[[con-deletion-flags-vs-status-fields]]).

## The fixed response format

The model responds in exactly five sections, in this order. Anything outside them is dropped,
not surfaced:

| Section | Contents |
|---|---|
| `=== RULE FULFILLMENT ===` | Yes/No — does this SQL implement what the rule name states? One or two sentences of reasoning. |
| `=== SQL REVIEW ===` | Numbered problems found: what's wrong, why it matters, how it was fixed. Or "SQL is valid and matches the specification". |
| `=== CORRECTED SQL ===` | Complete, clean, executable MS SQL Server query. |
| `=== AI ADDITIONS ===` | Fields added and why; joins touched and why; for a restructure, the before shape, the after shape, and why the rebuild was necessary. "No additions." when nothing changed. |
| `=== NOTES ===` | Confidence level, unverified table/field flags, edge cases, anything uncertain. |

A sixth block, `=== STRUCTURED METADATA ===`, carries a single JSON object describing every
output column, join and logic condition that ended up in `CORRECTED SQL`, so the caller can
refresh its own UI metadata **without re-parsing the SQL text** — free-text SQL is not
reliably machine-parseable once the model has restructured it.

```json
{
  "output_fields": [
    {"section": "Basic", "element": "Company Code", "table_field": "t001.BUKRS"}
  ],
  "joins": [
    {"source": "T001", "target": "T009", "join_type": "LEFT",
     "join_key": "t009.zSourceSystemID = t001.zSourceSystemID AND t009.PERIV = t001.PERIV"}
  ],
  "logic": [
    {"element": "Missing a valid fiscal year variant", "table_field": "t009.PERIV", "operator": "IS NULL"}
  ],
  "filters": []
}
```

`section` is one of `Tech` / `Basic` / `Org` / `Value` / `Activity`. The Syniti Technical
Fields are always assumed present and are never listed. Include an entry **only when the
corrected SQL genuinely differs** from the input spec: if only the `zIsErrorFlag` logic
changed, `output_fields` and `joins` are empty arrays and `logic` still describes the
corrected check. Omit a key entirely rather than guessing — the caller fills mechanical
defaults (position, empty strings) for anything left out.

No other section names. No sample-data section — this is a correctness decision, not a demo.

## Why this is a standard, not advice

The scope licence is enforced in three independent places, which is what makes it a rule:

| Layer | Mechanism |
|---|---|
| Prompt | The live instructions given to the model |
| Harness | An automated scope check — section diff against the pre-AI shell; each out-of-scope difference is recorded as a **finding** |
| Gate | The AI-Enhance compliance gate blocks a non-compliant save — see [[std-ai-enhance-guardrails]] |

Editing the prompt without mirroring the change here (and vice versa) is how the two drift.
The Studio's own rule: any comment-handling or table/field-trust change must be applied in
both files by hand, or the model never sees it.

## Related

- [[std-ai-enhance-guardrails|AI Enhance Guardrails]]
- REQ-AI-EDIT-SCOPE
- [[std-output-field-sections|Output Field Sections]]
- [[ref-ai-derive-and-enhance-internals|AI Enhance — What It Does and How to Use It]]
- [[ref-ai-static-validator-gate|The AI SQL Quality Gate]]
