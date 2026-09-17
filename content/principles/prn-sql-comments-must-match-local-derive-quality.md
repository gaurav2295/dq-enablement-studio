---
id: prn-sql-comments-must-match-local-derive-quality
type: principle
title: Why SQL Comments Must Match Local-Derive Quality
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-sql-comment-standards
  - relates:ref-ai-derive-and-enhance-internals
  - relates:ref-ai-static-validator-gate
  - relates:prn-optsel-is-the-universe
  - relates:prn-ziserrorflag-is-integer
  - relates:prn-deletion-flags-belong-in-where
  - relates:prn-fetch-check-return
  - relates:prn-no-silent-domain-fallback
sources:
  - vault:thought-leadership/Why SQL Comments Must Match Local-Derive Quality.md
tags: [thought-leadership, methodology, sql, sap, agent, course]
created: 2026-08-20
updated: 2026-08-20
---

## The principle

Comments in a DQ view are not decoration — they are the deliverable. The mandatory section /
WHERE / JOIN / CASE comments exist so a reviewer with no SAP knowledge can understand the
business meaning of every line, and AI-derived SQL must reach that exact bar, no lower, because
the client cannot tell which view a human wrote and which a model wrote.

## Why

The audience for a generated view is a Syniti consultant, a client data steward, or a future
maintainer — not the engine that wrote it. SAP physical names are opaque: `PLKO.PLNTY = 'Q'`
means nothing to a reviewer who doesn't have the data dictionary memorised. The comment is what
turns an opaque filter into a reviewable business statement. If the comment is missing, the
reviewer has to either reverse-engineer SAP semantics or trust the SQL blindly — both defeat the
point of shipping a *reviewable* rule.

So the standard is plain: the reader must understand WHAT a line does and WHY without needing
SAP knowledge.

## The canonical rule — four comment levels, all mandatory

1. **Section comments** before each SELECT group, in fixed order — `-- Syniti Technical Fields`,
   `-- Basic Fields`, `-- Organizational Context`, `-- Value Context`, `-- Activity Context`.
   These are also load-bearing: the SQL Parser switches sections on them.

2. **WHERE / filter comments** — every predicate gets an inline `/* Include: … */` or
   `/* Exclude: … */` saying what it does and why. Example: `PLKO.PLNTY = 'Q' /* Inspection
   Plan Type = Quality Inspection */`.

3. **JOIN comments** — each join carries a brief note on the relationship being traversed.

4. **CASE comments** — the `zIsErrorFlag` CASE must explain what counts as an error vs what
   passes.

This applies to **all DQ rule SQL output**: local derive, AI derive, AI enhance, bulk, single.
There is no "AI gets a pass" tier.

**Scope note:** This standard is specific to DQ rule views (OptSel, RptSel, InfSel, PrfSel, PrfSum).
Other Syniti SQL modules (ETL, data warehouse, bridge views, dimension tables) may follow their own
commenting standards — check the project's architecture documentation. The principle here — "a
non-SAP reviewer must understand the business meaning" — applies everywhere, but the specific format
(section headers, Include/Exclude, CASE structure) is a DQ rule contract.

## A concrete example

```sql
-- Organizational Context
MARC.WERKS AS [Plant]
...
WHERE
    /* Include: only quality inspection plans */
    PLKO.PLNTY = 'Q'
    /* Exclude: drop plans marked for deletion */
    AND ISNULL(PLKO.LOEKZ, '') <> 'X'
```

A non-SAP reviewer reads "quality inspection plans, excluding deleted ones" — without ever
knowing that `PLNTY` is the plan-type field or that `LOEKZ` is a deletion flag. That is the
entire point.

## AI-derivation parity (the directive)

When the AI path runs (AI Derive & Enhance), the output must achieve the same structural
quality as local derivation:

- **Do** include all Syniti Technical Fields — `zSourceSystemID`, `zConcatenatedKey`, and
  `zIsErrorFlag` for Error rules.
- **Do** keep spec and SQL in sync — same tables, joins, fields; domain/object type in the spec
  must match the tables actually used in the SQL.
- **Do** respect the rule type (Error / Info / Profiling) throughout.
- **Don't** ship `zIsErrorFlag` as a string or a literal — it is integer `1` (defect) / `0`
  (pass) via `CASE WHEN <error> THEN 1 ELSE 0 END`.
- **Don't** emit a filter or JOIN with no comment, on any path.

The Studio enforces this mechanically rather than on trust: the [[ref-ai-static-validator-gate|AI
SQL quality gate]] runs the same checks against AI output, and on a serious finding it asks the AI
once more before recording the findings against the rule. Parity is a gate, not an aspiration. See
[[ref-ai-derive-and-enhance-internals|AI Enhance]].

## How it shows up in the engine

The generator interleaves these comments deterministically — `_sql_header` for the banner,
`_build_where` for the per-predicate `Include`/`Exclude` notes, section labels in
`_build_select_parts`, and `_build_joins` for join notes. Because the format is fixed, the
round-trip parser can read a generated view back into a
DQRuleSpec — which only works if the comments are present and
well-formed. Drop them and round-trip breaks. The mechanics live in
SQL Comment & Formatting Standard.

## Questions from consultants

**Q: Is zIsErrorFlag a Boolean or an Integer?**

A: See [[qa-ziserrorflag-boolean-or-integer|Is zIsErrorFlag a Boolean or an Integer?]] — it is always `1` (defect) or `0` (pass), never Boolean, string, or other type.

**Q: Is this commenting standard applicable only to DQ views, or should the same approach be followed for other Syniti-generated SQL objects as well?**

A: See [[qa-sql-comments-dq-views-only|Is the SQL commenting standard applicable only to DQ views?]] — the specific format applies to DQ rule views only, but the principle ("reviewers must understand business meaning without SAP background knowledge") applies everywhere.
