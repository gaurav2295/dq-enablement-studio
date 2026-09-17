---
id: ref-single-rule-designer
type: reference
title: Single Rule Workspace
domain: studio
audience: [consultant, instructor]
level: foundation
status: review
links:
  - prereq:std-rule-name-heuristics
  - relates:prc-derive-a-dq-rule
  - relates:ref-local-deriver
  - relates:ref-bulk-pipeline
  - relates:ref-home-page
  - relates:con-view-types
  - relates:prn-optsel-is-the-universe
  - relates:std-implication-template
  - relates:gls-optsel
  - relates:gls-rptsel
sources:
  - vault:studio-architecture/Studio — Single Rule Designer.md
  - coe:rewritten to usage level for consultant enablement, 2026-08-21
tags: [studio, rule-design, methodology, course]
created: 2026-08-20
updated: 2026-08-21
---

## Summary

The DQ Rules workspace, used **one rule at a time**, is where you take a rule stated in business
language and end up with scored, commented, deployable SQL — a full spec, the OptSel and RptSel
views, and a Fetch/Check/Return description you can hand to a client.

This is the learning surface of the Studio: everything the [[ref-bulk-pipeline|bulk run]] does to
hundreds of rules, this does to one, with every step visible. Work here until the shape of a rule
is second nature.

## When to use it

- Authoring a new rule you want to review carefully before it goes into a batch
- Adapting a catalog rule to a client's specific scope
- Demonstrating the methodology to a client or a new team member
- Diagnosing a rule that came out wrong in a batch — reproduce it here, alone

## The loop you work in

1. **Type the rule name.** Business language, not table names: *"A material must have a valid base
   unit of measure."*
2. **Read the score.** The name is scored 0–1 against the naming heuristics. **0.7 or above** is a
   quality name; the hard ceiling is 100 characters, the target is 85. Profiling rules are not
   scored at all. See [[std-rule-name-heuristics]].
3. **Derive.** Local Derive is the deterministic default and needs no API key — see
   [[ref-local-deriver]]. AI Derive is the fallback for domains the knowledge base does not cover;
   it must reach parity with the local output, not diverge from it.
4. **Inspect.** Read the spec (output fields, logic, joins, filters), then the generated OptSel and
   RptSel SQL, then the description. Regenerate the SQL or the description independently while you
   iterate.
5. **Export.** Write the rule out as a Markdown spec for the project's spec folder — the
   human-readable, hand-editable face of the rule.

The full walkthrough with review checklists at each step is [[prc-derive-a-dq-rule]].

## What to expect

- **A weak name warns, it does not block.** Score below 0.7 and you get a critique plus suggested
  alternatives, but you can proceed. Do not treat that as permission — the name is the input the
  whole derivation reads, so a bad name produces a bad rule.
- **Deriving runs the whole chain.** Score, derive, then generate SQL with the multi-system context
  already attached — so what you see is what a deployed implementation looks like, filter and all.
- **OptSel is the universe, RptSel is the defects.** OptSel returns every candidate row with a
  per-row `zIsErrorFlag` of 1 or 0; RptSel is always the same wrapper selecting from OptSel where
  the flag equals 1. See [[prn-optsel-is-the-universe]] and [[con-view-types]].
- **Profiling rules are a different shape.** No score, no error flag; they produce PrfSel and
  PrfSum instead.
- **The description follows Fetch / Check / Return** in three numbered sections — see
  [[std-implication-template]].

> [!note] The Markdown round trip
> You can export a rule to Markdown, hand-edit the spec, and import it back. The SQL is
> deliberately **not** read back in: the import rebuilds the *spec*, and the next derive or
> regenerate rebuilds the SQL from it. That keeps Markdown as the record of intent while
> guaranteeing the SQL always matches the current spec rather than a stale hand-edit. Practical
> consequence: **never hand-edit SQL you want to keep** — change the spec.

## Worked example

*"Material missing base unit of measure"* scores **0.92** — clear subject, named field, SAP term
preserved. It resolves to the material master, and the error condition is a null check on the base
unit of measure, emitted as a 1/0 flag on every candidate row; RptSel then filters to the failures.

Compare two weaker names: *"MARA MEINS validation"* scores **0.38** (technical, no business
meaning) and *"DQ rule for customer country"* scores **0.32** (no condition stated).

## Common mistakes

- **Editing the SQL instead of the spec.** The spec wins on the next regenerate.
- **Proceeding past a low score because the derivation "looked fine".** Rename and re-derive; it
  costs seconds.
- **Naming the table rather than the business object.** The deriver reads business words.
- **Skipping the description.** The implication is a client deliverable, not an optional field.

## Related

[[prc-derive-a-dq-rule]] · [[ref-local-deriver]] · [[ref-bulk-pipeline]] ·
[[std-rule-name-heuristics]] · [[prc-write-a-quality-rule-name]] · [[con-view-types]] ·
[[std-implication-template]] · [[ref-home-page]]
