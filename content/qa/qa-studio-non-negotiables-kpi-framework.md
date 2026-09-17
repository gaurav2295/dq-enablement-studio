---
id: qa-studio-non-negotiables-kpi-framework
type: qa
title: How do we measure adherence to the non-negotiables?
domain: studio
audience: [lead, developer]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-04
created: 2026-09-07
updated: 2026-09-07
---

## Question

The [[prn-studio-non-negotiables|eight non-negotiables]] are the foundation of the Studio. 
But how do we measure whether they're being followed? What are the KPIs for adherence to 
the standards themselves?

## Answer

**Two levels of measurement:** automated validation (compliance), and audit metrics (quality).

### Automated validation (0% tolerance)

These checks run on every rule before deployment:

| Standard | Check | Pass/Fail |
|----------|-------|-----------|
| 1. SQL commenting | Every OptSel/InfSel has five section headers + comments on JOINs/CASE | Fail → un-deployable |
| 2. zIsErrorFlag = INTEGER | Data type is NUMERIC, not VARCHAR | Fail → un-deployable |
| 3. OptSel is universe | RptSel is exactly `SELECT * FROM OptSel WHERE zIsErrorFlag = 1` | Fail → un-deployable |
| 4. Logic vs filters | Error condition in CASE, not WHERE. WHERE only for scope/deletion. | Fail → review_required |
| 5. Deletion flags in WHERE | LVORM/LOEKZ/LOEVM not in CASE (no duplicates) | Fail → audit flag |
| 6. Tech fields mandatory | zSourceSystemID, zConcatenatedKey, zIsErrorFlag present | Fail → un-deployable |
| 7. Catalog SQL preserved | Wrapper doesn't re-derive; catalog SQL verbatim | Fail → audit flag |
| 8. Section comments | `-- Syniti Technical Fields` header present | Fail → audit flag |

**Result:** Every rule published to the tracker has passed all 8 checks. **Automated compliance = 100%.**

### Audit metrics (tracking quality)

Beyond automated checks, we track:

**Monthly audit report:**
- Total rules authored: 247
- Rules that passed first-pass audit: 241 (97.6%)
- Rules requiring rework for standard violations: 6 (2.4%)
- Common violation types:
  - "Status field in WHERE instead of CASE" (2 rules)
  - "Deletion flag in both WHERE and CASE" (3 rules)
  - "Missing activity-context comments" (1 rule)

**Trend tracking:**
- If violation rate > 5%, investigate why (new team? new domain? old patterns resurging?)
- Per-consultant: which authors have high violation rates? Provide coaching.
- Per-domain: which domains have the most rework? (FI vs MM vs SD)

**Engagement-level KPI:**
- "Rules deployed in this engagement that passed first-pass audit" (target: > 95%)
- If below 95%, flag it: either the consultant needs coaching, or the scope is unclear.

### How violations are caught

1. **Automated validator** (Studio) — fails the rule outright
2. **DBA audit** (prc-audit-rule-quality) — finds logic/comment gaps, marks `_review_required`
3. **Monthly metrics** — trends across all rules; identifies patterns

### What "adherence" means

✅ **100% automated compliance** — all rules pass the 8 validator checks before deployment.

✅ **90%+ first-pass audit** — 9 out of 10 rules pass DBA audit without rework.

⚠️ **Trend is stable or improving** — violation rates are not climbing; common mistakes are being caught and patterns are improving.

### If adherence drops

1. **Investigate the root cause**
   - New junior consultant? Provide training.
   - New domain the standards weren't written for? Update the standards (via CONFLICT escalation).
   - Studio validator bug? File a bug report.

2. **Don't lower the standard** — increase the support (coaching, docs, examples).

> [!tip]
> The non-negotiables have automated teeth (the validator). The audit metrics tell us 
> how well the automated checks are catching edge cases the validator misses. Together, 
> they keep the system honest.
