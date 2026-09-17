---
id: ref-ai-static-validator-gate
type: reference
title: The AI SQL Quality Gate
domain: ai-enhancement
audience: [consultant, lead]
level: practitioner
status: review
links:
  - relates:ref-ai-derive-and-enhance-internals
  - relates:std-ai-enhance-guardrails
  - relates:std-ai-enhance-scope
  - relates:prc-audit-rule-quality
  - relates:prc-run-the-bulk-pipeline
  - relates:qa-ai-quality-gate-serious-findings
  - relates:qa-profiling-rules-quality-gate-exclusion
  - implements:prn-sql-comments-must-match-local-derive-quality
  - implements:prn-no-silent-domain-fallback
  - relates:gls-ai-sql-review
sources:
  - vault:ai-related/AI Static-Validator Gate.md
  - coe:usage rewrite for consultants
tags: [studio, agent, course, sql, methodology]
created: 2026-08-20
updated: 2026-08-21
---

## What it is

Whenever the AI rewrites a rule's SQL, the Studio checks that rewrite against the same standards it
applies to its own deterministic output — before you ever see it. That check is the **quality
gate**. It exists so AI-assisted rules cannot quietly ship at a lower standard than hand-derived
ones.

You do not switch it on or configure it. It runs on every AI SQL review. What matters to you is
what it catches, when it stops you, and what it leaves for you to judge.

## What happens on an AI rewrite

1. The AI's SQL is checked against the standards catalogue.
2. If anything **serious** is found — something that will not run, or a critical logic flaw — the
   Studio asks the AI once more, telling it exactly what was wrong.
3. Whatever comes back is recorded with its findings attached, and shown to you.

There is exactly **one** retry. No loop, no escalation. If the second attempt still has findings,
the rule is not thrown away — it carries its findings forward, visibly, for a human to resolve.

Lesser findings are recorded but do not trigger a retry; they show up as warnings for you to read.

## Auto-repairs: What Gets Fixed Silently

Before the gate blocks you, the Studio silently repairs a short list of issues that can be fixed with no ambiguity:

- A hardcoded system ID (e.g., `'Z01'`) swapped back to a column reference (e.g., `zSourceSystemID`)
- A wrongly delimited concatenated key
- Verbose performance commentary stripped out of the SQL

**Where to find auto-repaired changes:** When you accept an AI enhancement, the auto-repairs are recorded in the **Reconciliation** sheet (after bulk export) with a note: "Auto-repaired: [description]". You can review what was changed before exporting to production.

---

## When it actually blocks you

The retry behaviour above never blocks. There is a second, narrower check that **does**: when you
accept an AI enhancement, a short list of non-negotiable violations stops the save outright with an
error, and nothing is written.

Typical hard stops:

- A hardcoded client number or a hardcoded source-system value written as a literal (that could not be auto-repaired)
- A wrongly delimited concatenated key (that could not be auto-repaired)
- A join between systems missing its source-system pairing
- zIsErrorFlag logic that inverts the error condition

The same enforcement runs on the fan-out path, per sibling — a violation fails that one target
rather than the whole batch.

An ordinary hand-edit save is unaffected. You can still stage an intentionally incomplete rule and
come back to it.

## What to expect

- **Profiling rules skip the gate.** The checks are shaped for Error rules — they expect an error
  flag and a query pair that profiling does not have. Running them on profiling would only produce
  noise. See [[std-ai-enhance-guardrails]] and [[qa-profiling-rules-quality-gate-exclusion|Why profiling rules are excluded]].
- **Findings travel with the batch.** Anything the gate recorded appears on the bulk
  **Reconciliation** sheet and, for rules that did not make it, the **Failed Rules** sheet. That is
  where you look after a bulk run — see [[prc-run-the-bulk-pipeline]].

### Quality Gate vs. Audit Rule Quality

**Two different validation mechanisms for different purposes:**

| Aspect | Quality Gate | Audit Rule Quality |
|--------|---|---|
| **When it runs** | During AI Enhance (single rule) | After bulk pipeline (batch of rules) |
| **What it checks** | AI-rewritten SQL against standards | All rule fields: spec, SQL, logic consistency, parity |
| **Scope** | Error-rule syntax + logic | Error + Profiling + system-level issues |
| **Automation** | Automated (gate blocks you; AI retries once) | Partly automated (Audit screen flags issues; human reviews) |
| **Coverage** | Catches AI mistakes on rewrites | Catches structural issues, convergence, client-specific drift |
| **Output** | Pass/Fail or warnings | Parity scores, defect counts, per-rule status |

**Use together, not as alternatives:**
1. **Quality Gate** — stops you from shipping broken AI output
2. **Audit Rule Quality** — confirms the whole batch meets standards before production

See [[prc-audit-rule-quality|Audit Rule Quality]] for the full batch-wide review process.

---

- **Deterministic wins.** Where the Studio has already resolved a table from real metadata, the AI
  does not get to override it.
- **You are the final gate.** A recorded finding means "a human decides", not "the machine
  approved it".

## Common mistakes

- **Reading a clean save as a clean rule.** Only the hard-stop list blocks; everything else is a
  warning you are expected to read.
- **Ignoring the warning banner** after applying corrected SQL.
- **Exporting a batch without opening the Reconciliation sheet.** Findings are there and nowhere
  else once the session closes.
- **Re-pressing AI Enhance to make a finding go away.** The retry already happened. A finding that
  survives it needs a person, usually a better rule name or an explicit table choice.

## Related

[[ref-ai-derive-and-enhance-internals]] · [[std-ai-enhance-guardrails]] · [[std-ai-enhance-scope]] ·
[[prc-audit-rule-quality]] · [[prc-run-the-bulk-pipeline]] ·
[[prn-sql-comments-must-match-local-derive-quality]] · [[prn-no-silent-domain-fallback]] ·
[[gls-ai-sql-review]]
