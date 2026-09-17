---
id: prn-studio-non-negotiables
type: principle
title: The Studio Non-Negotiables
domain: studio
audience: [consultant, developer, lead]
level: practitioner
status: review
kind: decision
links:
  - relates:prn-sql-comments-must-match-local-derive-quality
  - relates:prn-ziserrorflag-is-integer
  - relates:prn-optsel-is-the-universe
  - relates:prn-deletion-flags-belong-in-where
  - relates:prn-fetch-check-return
  - relates:prn-studio-workflow-guardrails
sources:
  - dq-studio:CLAUDE.md
tags: [studio, doctrine, methodology, sql, non-negotiable]
created: 2026-08-20
updated: 2026-08-20
---

## The principle

Eight rules govern everything the Studio's generation engines emit. They are not style
preferences and they are not per-project settings: **a change that violates one of them is a
bug, not a variation.** They are written into the app's own internal engineering standards so
that every path — local derive, catalog derive, AI enhance, bulk fan-out — is held to the same
output shape.

Each one below states the rule, then *why* it exists, then where the detail lives.

## 1. SQL commenting standard

**Rule.** AI-derived SQL must match locally-derived quality. Five mandatory section comments
appear in every OptSel/InfSel SELECT list — `-- Syniti Technical Fields`, `-- Basic Fields`,
`-- Organizational Context`, `-- Value Context`, `-- Activity Context` — and every WHERE/filter,
every JOIN and every CASE carries a comment explaining *what* and *why* in business terms.
Applies to **all** output: local, AI, bulk and single-rule.

**Why.** The SQL is a client deliverable read by DBAs who were not in the design workshop. A
comment that names the business intent is the only thing that survives handover. Left unstated,
the AI path silently degrades to bare SQL and the two derivation paths stop being comparable.

**Detail:** [[prn-sql-comments-must-match-local-derive-quality]] ·
[[std-sql-comment-standards]] · [[std-output-field-sections]]

## 2. zIsErrorFlag is INTEGER 1/0

**Rule.** Never `'Yes'`/`'No'`, never `'Y'`/`'N'`, never a bare `1` over a pre-filtered set.
OptSel emits `CASE WHEN <error_condition> THEN 1 ELSE 0 END AS [zIsErrorFlag]`.

**Why.** Downstream scoring sums the column. A string flag makes the sum impossible and a
pre-filtered `1` makes every rule report a 100% defect rate. Integer 1/0 is what lets
`SUM([zIsErrorFlag])` be the defect count and `COUNT(*)` the opportunity count in one pass.

**Detail:** [[prn-ziserrorflag-is-integer]] · [[std-ziserrorflag-convention]] ·
std-req-sql-undefined-error-flag

## 3. OptSel is the universe, RptSel is the wrapper

**Rule.** OptSel returns **all** candidate rows with the per-row flag; the error predicate lives
in the `CASE`, never in the `WHERE`. `WHERE` is only for record-set restrictions — the system
filter and deletion-flag exclusions. RptSel is exactly
`SELECT * FROM <OptSel> WHERE [zIsErrorFlag] = 1`.

**Why.** The denominator has to survive. If the OptSel pre-filters to defects, the opportunity
count vanishes and the rule is either dropped as "no opportunities" or reported at a meaningless
100%. One universe view plus one dumb wrapper also means there is exactly one place to audit when
a client challenges a number.

**Detail:** [[prn-optsel-is-the-universe]] · [[gls-optsel]] · [[con-view-types]] ·
[[std-optsel-select-structure]]

## 4. Logic vs Filters

**Rule.** The error-detection condition drives the flag (it belongs in `spec.logic`); it is
**never** a filter Exclusion. Inclusions define scope (e.g. `zSourceSystemID = 'Z02'`);
Exclusions remove records from the universe (e.g. `LVORM = 'X'`).

**Why.** This is the spec-level form of rule 3. Once a defect condition is recorded as an
Exclusion, every regeneration of the SQL puts it back in the `WHERE` — the shape drifts back to
wrong on the next derive. Keeping the distinction in the spec model makes the correct SQL the
only SQL the generator can produce.

**Detail:** ref-dqrulespec-data-model · [[con-filter-presets]] · [[con-time-based-filters]]

## 5. Deletion flags vs status fields

**Rule.** Deletion flags (`LVORM`, `LOEKZ`, `LOEVM`) go in the `WHERE` to exclude deleted records
and must **not** appear in the `zIsErrorFlag` CASE. Status fields (`MMSTA`, `PSTAT`, `STATU`)
drive the flag. Never duplicate the same condition in both `WHERE` and `CASE`.

**Why.** A deleted record is not a defect — it is not in the universe at all. Counting it as a
defect inflates the error rate and puts records on a remediation list that nobody can action.
Duplicating the predicate in both places is logically redundant and makes the two copies drift
apart on the next edit.

**Detail:** [[con-deletion-flags-vs-status-fields]] · [[prn-deletion-flags-belong-in-where]] ·
ref-deletion-flag-normalization-in-sql-gen · [[ref-sap-deletion-flags-vs-status-fields]]

> [!note] The one deliberate exception
> Deletion-detection rules — rules whose whole point *is* the deletion flag — are the exception,
> and it is a decided one, not an accident. See prn-adr-007 and prn-adr-008.

## 6. Aliases and naming

**Rule.** `zConcatenatedKey` — one word, no space. Rule names ≤ 100 characters (target ≤ 85). SAP
acronyms are preserved verbatim: PIR, BOM, MRP, PO, SO, GL, AP, AR, UoM, CoA, FI.

**Why.** The spelling and the length cap are ingestion requirements, not taste — a spaced
`zConcatenated Key` is skipped without error on load, and an over-length name fails the tracker
row. Preserving acronyms keeps the client's own vocabulary intact; "Purchasing Info Record"
expanded out of a name the business calls a PIR reads as someone else's document.

**Detail:** [[std-zconcatenatedkey-convention]] · [[prc-write-a-quality-rule-name]] ·
[[std-rule-name-heuristics]] · [[std-view-naming-patterns]]

## 7. Description = Fetch / Check / Return

**Rule.** Every rule's description follows the three-section template, with section 3 built as
Fetch → Check → Return. AI-generated descriptions must match it exactly — the shape is not a
suggestion the model may improve on.

**Why.** The description is read by a business owner deciding whether to sign off the rule and by
a cleanse team deciding what to do with the records. Fetch names the population, Check names the
test, Return names the consequence — three questions every reviewer asks in that order. A free-form
paragraph answers them in an unpredictable order or not at all.

**Detail:** [[prn-fetch-check-return]] · [[std-rule-description-template]] ·
[[std-implication-template]] · [[prc-format-an-implication]]

## 8. AI-derivation parity

**Rule.** The AI path must reach the same structural quality as local derivation: spec and SQL in
sync, all Syniti Technical Fields present, rule type respected throughout.

**Why.** AI is a second route to the same deliverable, not a lower tier of it. The moment the AI
path is allowed to ship thinner output, the audit findings concentrate on AI-derived rules and
the whole pipeline becomes untrustworthy at the point where it is fastest. Parity is what keeps
"use AI Enhance" from being a quality trade-off.

**Detail:** [[ref-ai-derive-and-enhance-internals]] · [[ref-ai-static-validator-gate]] ·
std-req-ai-edit-scope · std-harness-requirements

## How they are enforced

These are not honour-system rules. Each one has machinery behind it:

| Non-negotiable | Enforced by |
|---|---|
| SQL commenting | ref-sql-validator section-header checks; ref-output-section-builders |
| zIsErrorFlag integer | std-req-sql-undefined-error-flag, std-req-sql-literal-flag-fallback |
| OptSel universe / RptSel wrapper | std-req-sql-rptsel-flag-filter, std-req-sql-rptsel-wrapping |
| Logic vs Filters | spec model validation in ref-dqrulespec-data-model |
| Deletion vs status | ref-deletion-flag-normalization-in-sql-gen |
| Aliases and naming | ref-rule-name-scorer, std-req-sql-view-naming-pattern |
| Fetch / Check / Return | ref-markdown-exporter-and-round-trip-contract |
| AI parity | [[ref-ai-static-validator-gate]], std-harness-requirements |

The workflow-level expression of the same doctrine — what the *app* refuses to let a user do — is
[[prn-studio-workflow-guardrails]].
