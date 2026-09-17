---
id: prn-optsel-is-the-universe
type: principle
title: OptSel Is the Universe, RptSel Is the Wrapper
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: approved
links:
  - prereq:gls-optsel
  - prereq:con-view-types
  - relates:con-dq-dimensions
  - relates:std-ziserrorflag-convention
  - relates:prn-ziserrorflag-is-integer
  - relates:prn-deletion-flags-belong-in-where
  - relates:gls-defect-rate
  - relates:gls-opportunity-count
  - relates:gls-opportunity-universe
sources:
  - vault:thought-leadership/Why OptSel is the Universe and RptSel is the Wrapper.md
tags: [views, doctrine]
created: 2026-08-20
updated: 2026-08-20
---

## The principle

All rule logic — joins, filters, the error condition, every computed column — lives in the
OptSel. The RptSel does exactly one thing: `SELECT` from the OptSel `WHERE zIsErrorFlag = 1`.

## Why

1. **One place to trust.** When a client challenges a number, there is exactly one view to
   read. Logic split across two views cannot be audited in one sitting.

2. **The denominator is free.** Because the OptSel holds the whole universe with a flag, the
   error *rate* (flagged ÷ universe) needs no second query and can never disagree with the
   error *list*.

3. **Remediation reuse.** Cleanse teams work from the same OptSel the report came from — no
   re-derivation, no drift between "what we reported" and "what we fixed".

## The pattern

```sql
-- OptSel: every candidate, with a flag
CREATE VIEW DQ_0042_..._OptSel AS
SELECT
    ...,
    CASE WHEN <error> THEN 1 ELSE 0 END AS [zIsErrorFlag]
FROM ...
WHERE <universe restrictions only — never the error condition>;

-- RptSel: defects only — the canonical wrapper, and nothing else
CREATE VIEW DQ_0042_..._RptSel AS
SELECT *
FROM DQ_0042_..._OptSel
WHERE [zIsErrorFlag] = 1;
```

### Data flow: OptSel → RptSel

```
┌─────────────────────────────┐
│     OptSel (universe)       │
│  All candidates + flag      │
│  zIsErrorFlag: 0 or 1       │
│  Row count: N (all records) │
└──────────────┬──────────────┘
               │
               │ WHERE zIsErrorFlag = 1
               │ (filter to errors only)
               ▼
┌─────────────────────────────┐
│     RptSel (report)         │
│  Defects only               │
│  zIsErrorFlag: 1            │
│  Row count: M (errors)      │
└─────────────────────────────┘

Defect rate = M / N  (RptSel count / OptSel count)
```

> [!warning]
> A `WHERE` clause in a RptSel beyond the flag filter means some of the universe is being
> silently excluded from reporting — the number on the slide no longer matches the OptSel.

## ADM needs both counts

ADM computes defect rate as `defects / opportunities`. That ratio needs both numbers at once:
the opportunity count (every candidate record — the OptSel row count) and the defect count
(records that failed — the RptSel row count, since RptSel is just OptSel filtered to
`zIsErrorFlag = 1`).

If OptSel pre-filtered to defects only, the denominator would vanish and every rule would
report a meaningless 100% defect rate. If RptSel returned everything unfiltered, it would lose
its purpose — reviewers could no longer tell at a glance which records are defective. The split
is strict on both sides for this reason.

## Resisting drift

Over time, it's tempting to customize RptSel — add a column here, skip a column there, add a filter for performance. **Don't.** Each customization creates **drift**: a gap between what OptSel defines as the universe and what RptSel reports. Drift breaks auditing, breaks reuse, and hides defects.

RptSel is intentionally dumb — a filter wrapper, nothing more. Its only job is `SELECT * FROM OptSel WHERE zIsErrorFlag = 1`. Variations get tempting; resist all of them:

- *"What if I rename columns in RptSel for the report?"* — adds drift; `SELECT *` means RptSel
  and OptSel always have the same shape.
- *"What if I add a few formatted columns to RptSel that aren't in OptSel?"* — breaks ADM's
  join-back-to-OptSel for context.
- *"What if I add a second filter to RptSel for performance?"* — makes OptSel's universe
  definition diverge from RptSel's report definition.

## Where the error condition lives

Inside the `CASE` inside the OptSel `SELECT` — never in the `WHERE`.

```sql
-- ✅ CORRECT
SELECT
    CASE WHEN MEINS IS NULL OR MEINS = '' THEN 1 ELSE 0 END AS [zIsErrorFlag]
FROM MARA
WHERE LVORM <> 'X';                  -- universe: not deleted

-- ❌ WRONG
SELECT 1 AS [zIsErrorFlag]
FROM MARA
WHERE LVORM <> 'X'
  AND (MEINS IS NULL OR MEINS = '');  -- pre-filters to defects only
```

The wrong shape returns zero records on a clean dataset — there are no defects to return. ADM
then reports the rule as "no opportunities" and it is silently dropped from reporting. The
defect was hidden by being caught too well upstream.

## When the universe is debatable

Sometimes the line between "universe restriction" (belongs in `WHERE`) and "error condition"
(belongs in the `CASE`) is a judgment call.

*Example*: "A material must have a base UoM" — does the universe include FERT (finished goods)
only, or all material types?

- Scope the universe to "FERT only" and a HALB material missing a UoM never shows as a defect —
  it isn't in the universe.
- Scope the universe to "all material types" with the error condition checking `MEINS`, and
  every material type's UoM gets evaluated.

The right answer depends on business intent. Document the choice in the Implication's Scope
section so the next reviewer knows which way the call went.

## The profiling counterpart

PrfSel / PrfSum follow the same shape philosophy: PrfSel is record-level detail (the "universe
of records in scope"), PrfSum is the aggregated summary. PrfSum isn't a defect filter — it's a
roll-up. But the separation of concerns, one view per granularity, mirrors the OptSel/RptSel
philosophy.
