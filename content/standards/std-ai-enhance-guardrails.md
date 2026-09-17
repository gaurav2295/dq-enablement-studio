---
id: std-ai-enhance-guardrails
type: standard
title: AI Enhance Guardrails — SQL Syntax, Comments, and AI Self-Reference
domain: ai-enhancement
audience: [developer, consultant]
level: practitioner
status: review
sources:
  - dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md
  - dq-studio:docs/ai_enhance_instructions.md
tags: [methodology, convention, sql, agent, governance]
links:
  - relates:std-ai-enhance-scope
  - relates:ref-ai-static-validator-gate
  - relates:std-sql-comment-standards
  - relates:std-zsourcesystemid-convention
  - relates:std-zconcatenatedkey-convention
  - relates:gls-symmetric-field-join
  - contrast:std-output-field-sections
created: 2026-08-20
updated: 2026-08-20
---

## The standard

Two defence layers protect AI-enhanced DQ rule SQL, and they are not the same thing:

- **Deterministic guardrails** — checks that mechanically inspect SQL text and structure. No
  model call; the same input always produces the same output.
- **The AI harness** — the judgment layer wrapped around every AI call and every hand-edit save.
  It runs the deterministic checks against the proposed SQL and records the result.

Deterministic guardrails are the **rules**. The harness is the **mechanism** that runs those
rules against AI output and decides what happens next. This unit is the rulebook; the harness
mechanics are in [[ref-ai-static-validator-gate]] and std-harness-requirements.

Scope: everything the AI Enhance button touches — the deterministic derive path, every AI review
step, and every persistence path an AI Enhance result reaches.

## 1. SQL syntax restrictions

### Strictly prohibited, no exceptions

| Construct | Rewrite as |
|---|---|
| **RIGHT JOIN** | LEFT JOIN with the table order swapped |
| **OUTER APPLY** | A standard LEFT JOIN with WHERE conditions, a CTE, or `EXISTS` / `NOT EXISTS` |

Both are caught automatically as `forbidden-right-join` / `forbidden-outer-apply` findings (High
severity), across every SQL validation path — deterministic derive and AI Enhance alike. The
permitted alternatives are LEFT JOIN, INNER JOIN, a `WITH` CTE, and `EXISTS` / `NOT EXISTS`
correlated subqueries.

### Also never valid, anywhere in generated SQL

| Violation | Why it is fatal |
|---|---|
| `MANDT` compared to a hardcoded client-number literal | Pins the view to one client; breaks on every other |
| `zSourceSystemID` selected as a string literal instead of a column reference | Fabricates provenance — the value must always come off the driving table (the repository-template `'{{SYSTEM}}'` form is a different generation path — see CONFLICT-013) |
| `zConcatenatedKey` delimited with a pipe instead of an underscore | Breaks key comparability across the estate |
| An unresolved `TBD` token — view name, `FROM`, or JOIN body | The artefact is not deployable |
| A symmetric-field JOIN with no `zSourceSystemID` equality alongside it | Cross-system data contamination |

The last one deserves its full statement. A **symmetric-field JOIN** is
`a.FIELD = b.FIELD` — the same field name equated across two peer tables, a cross-table
parity or lookup check rather than a foreign-key-to-description join. It must pair
`zSourceSystemID`:

```sql
-- wrong: two systems' fiscal year variants can match each other
ON t009.PERIV = t001.PERIV

-- right
ON t009.zSourceSystemID = t001.zSourceSystemID
   AND t009.PERIV = t001.PERIV
```

Bracket-quoted field names count (`vv.[PERIV] = t001.[PERIV]`), and **a CTE's own joins are
never exempt**.

## 2. `zSourceSystemID` filtering — mandatory everywhere

| Position | Requirement |
|---|---|
| **Main table WHERE** | The primary table in the `FROM` clause always carries a WHERE filter on `zSourceSystemID`. This stops cross-system contamination at the query's root. |
| **Every join** | A symmetric-field join pairs `zSourceSystemID` (see above). |
| **Every CTE that sources base tables** | Filters on `zSourceSystemID` in its own WHERE clause, referencing the main table's value. |
| **Every CTE's output** | SELECTs and outputs `zSourceSystemID` from the main table, so downstream joins can match on it. |
| **Every join to a CTE** | Includes a `zSourceSystemID` equality alongside the other join conditions. |
| **Never** | A literal — no `'<code>' AS [zSourceSystemID]`, no hardcoded `MANDT` client number. Always a live column reference off the driving table. |

```sql
WITH cte AS (
  SELECT ... FROM table_a
  WHERE zSourceSystemID = <main_table>.zSourceSystemID
)
...
FROM main_table
LEFT JOIN cte
  ON main_table.zSourceSystemID = cte.zSourceSystemID
  AND main_table.key_field = cte.key_field
```

### CTE discipline

- **Every CTE must be used.** A dangling CTE that is never referenced in the outer query is a
  compilation error, not a style problem.
- **A CTE is an internal implementation detail, not an excuse to change the view's external
  shape.** The outer SELECT still exposes the five section headers in order, with
  `zSourceSystemID`, `zConcatenatedKey` and `zIsErrorFlag` present exactly as required.

### `zConcatenatedKey` uniqueness

Checking that the key is built with `CONCAT(...)` and references `zSourceSystemID` is not
enough — it must be **unique at the query's grain**. If a join fans the master record out to
multiple child rows, the key must include enough of the child table's fields to stay unique
per output row, not just the header table's key. If uniqueness cannot be confirmed, say so in
`NOTES` rather than asserting it. The delimiter is always `_` — see
[[std-zconcatenatedkey-convention]].

## 3. Comment handling

### The header banner is non-negotiable

Every SQL output begins with this block, unmodified — no line skipped, abbreviated, or
reformatted:

```sql
-- ============================================================
-- DQ Rule: [Rule name received]
-- Rule ID: [RuleID received]
-- View:    [Opportunity view or Report View]
-- Generated: [Generation Date]
-- Target: MS SQL Server
-- ============================================================
```

Those bracketed placeholders are the prompt's own wording, replaced with real values from the
spec and the current system time. The same banner, with the general authoring placeholders and a
worked example, is [[std-sql-comment-standards]] — this section is the AI-facing statement of it,
not a second standard.

### Section comments use the plain dash form

`-- Basic Fields`, `-- Activity Context`. Never decorative wrappers like
`/* ===== Basic Fields ===== */`.

### Body comments

Every `WHERE` condition, `JOIN`, and `CASE` branch that needs explaining carries a
`/* ... */` comment in plain business language — a reader without SAP expertise should be able
to follow the logic. Comments explain only three things:

1. The rule's purpose.
2. Important business logic.
3. Non-obvious joins.

This is the **maximum** style, not a starting point to expand on:

```sql
-- Identify active customers with no sales orders
-- Join VBAK to determine order existence
```

> [!warning] Never inline in SQL
> No line-by-line narration of what the SQL does syntactically. No verbose or repeated
> explanations, no paragraph comments. **No performance-tuning note, no index suggestion, no
> uniqueness-confidence narration, no edge-case discussion.** All of that belongs in `NOTES` or
> `AI ADDITIONS`. Index suggestions in particular are never DDL either — a view body cannot
> contain `CREATE INDEX` for another object; it would simply fail to compile.

Comments must also never imply uncertainty about the SQL's own correctness — a disclaimer or a
hedge. Genuine uncertainty about an introduced table or field goes in `AI ADDITIONS` / `NOTES`,
never inside the SQL.

**One standard, not two passes.** This bar applies when the model *adds* a comment exactly as
it applies when the model *cleans* one. "Clean up AI wording" and "write a good comment in the
first place" are the same rule.

## 4. Remove AI references

> [!important] Narrow by design
> This applies **only to the AI Enhance flow, and only to comments the model adds during
> enhancement**. It is not a blanket "strip anything AI-ish" pass over arbitrary SQL. It never
> touches a legitimate business comment, a technical comment, or a human-authored comment —
> unless that comment explicitly references AI, Claude, an LLM, or "generated by AI" wording.

Never write, and always strip if present, in SQL comments:

- "Added by AI" / "Generated by AI" / "AI Enhancement" / "AI-generated"
- "Claude" / "LLM" / "model output"
- Any comment stating that a field, join, or table was touched, added, or restructured *by AI
  or a model*.

That attribution belongs in the `AI ADDITIONS` response section — never inside the SQL itself.

**Two layers, belt and braces:**

1. **Prompt-side** — the live instructions tell the model to list additions under
   `AI ADDITIONS` and never label them "by AI" inside the comment; comments read as ordinary
   engineering commentary.
2. **Deterministic post-processing** — a case-insensitive denylist regex catches anything that
   slips through:

```text
AI[- ]?(Enhance(d|ment)?|generated|added|assisted)
generated by
added by AI
Claude
LLM
model output
```

Extend the list as new phrasings are observed. **Every addition needs a test case.**

## 5. The AI harness rules, mapped to enforcement

| # | Rule | Enforced by |
|---|---|---|
| 1 | Enhance the SQL, preserve the original business rule — never rewrite it into a different rule | Prompt scope plus an automated scope check ([[std-ai-enhance-scope]]) |
| 2 | Never hallucinate a table or field without flagging it unverified | An automated table/field trust check |
| 3 | No RIGHT JOIN, no OUTER APPLY | Automated SQL validation |
| 4 | No unsupported SQL Server or project-incompatible syntax | Automated SQL validation, full check catalogue |
| 5 | Prefer readable CTE-based SQL when it clarifies a multi-table check | Prompt guidance only — a style preference, deliberately not a blocking check |
| 6 | Follow existing naming conventions | Automated naming checks |
| 7 | Comments useful, concise, technical | §3 above, an automated comment check |
| 8 | No AI/Claude/LLM self-reference anywhere in SQL comments | §4 above |
| 9 | No disclaimers inside SQL | §4 above — a disclaimer is a form of AI self-reference |
| 10 | No hidden assumptions — an introduced table/field is flagged, not silently assumed | The table/field trust rule |
| 11 | Output only the documented response format | The five fixed sections; anything outside is dropped, not surfaced |

> [!note] There is no single "preserves business intent" check
> Business-intent preservation, executability, and "no unsupported syntax" are the **composite
> outcome** of the whole check catalogue. An unresolved alias, a missing `END`, a forbidden JOIN
> pattern — each is a concrete way SQL fails to execute or drifts from intent. `AIEditScopeCheck`
> adds the complementary, AI-specific half: that the correction only touched the sections it was
> licensed to touch.

## 6. Severity is not the same as blocking

A check's **severity** describes correctness impact. The **AI-Enhance blocking allowlist** is a
separate decision about whether a legitimate exception exists that would false-positive if the
check blocked everywhere.

Never flip a check's severity to High purely to make it block. The worked example is
`join-missing-system-id-pairing`: Medium severity, because a real if less common legitimate
exception exists (the foreign-key-lookup join pattern already in production), but on the
blocking allowlist anyway once real-world evidence showed the false-negative cost outweighed
the false-positive risk.

## Validation checklist

- [ ] No RIGHT JOIN, no OUTER APPLY.
- [ ] No AI/Claude/LLM references remain in final SQL comments.
- [ ] Original business logic preserved — locked sections unchanged.
- [ ] SQL remains executable: balanced parens and brackets, every `CASE` has an `END`, no
      unresolved aliases, no JOIN without `ON`.
- [ ] Required aliases and output columns preserved.
- [ ] No hallucinated SAP objects introduced without the "unverified" flag.
- [ ] Comments technical, concise, useful — no line-by-line narration, no
      performance/index/uniqueness commentary.
- [ ] No hardcoded `MANDT`, no `zSourceSystemID` literal, no pipe delimiter, no unresolved
      `TBD`, and every symmetric-field JOIN — bare or bracket-quoted, CTE-internal included —
      pairs `zSourceSystemID`.
- [ ] The compliance enforcement applied only on the AI-Enhance-accept flow; an ordinary
      hand-edit save is unaffected.

## Related

- [[std-ai-enhance-scope|AI Enhance Edit Scope]]
- [[ref-ai-static-validator-gate|AI Static-Validator Gate]]
- SQL Validator (static checks)
- [[std-sql-comment-standards|SQL Comment Standards]]
- [[std-zsourcesystemid-convention|zSourceSystemID Convention]]
- [[std-zconcatenatedkey-convention|zConcatenatedKey Convention]]
