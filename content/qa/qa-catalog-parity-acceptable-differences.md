---
id: qa-catalog-parity-acceptable-differences
type: qa
title: What parity differences are acceptable in catalog audit?
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:prc-audit-rule-quality
  - relates:std-optsel-select-structure
---

## Question

For catalog parity, what kinds of differences are typically acceptable before investigation is required?

## Answer

**< 5% drift is typical and acceptable; > 10% triggers investigation.**

**Parity score measures:** Does the bespoke (edited) rule match the catalog (original) SQL?

**Typical acceptable drift (score 0.95–1.0 = 95–100%):**

| Drift type | Example | Acceptable? |
|---|---|---|
| **Alias addition** | Added `MAKT` for description readability | ✅ Yes (< 1% drift) |
| **Comment edits** | Updated Fetch/Check/Return in Implication | ✅ Yes (comments don't affect score) |
| **Column rename** | `MEINS` → `[Base Unit of Measure]` alias | ✅ Yes (same data, clearer label) |
| **Field reordering within section** | Moved Basic fields around | ✅ Yes (same section) |
| **WHERE clause extension** | Added MTART filter to narrow scope | ⚠️ Maybe — depends on intent |

**Borderline drift (score 0.80–0.95 = 80–95%):**

| Drift type | Example | Action |
|---|---|---|
| **New JOIN** | Added MAKT to catalog's MARA-only rule | ⚠️ **Investigate** — why add a join? |
| **Changed CASE logic** | Modified error condition | ⚠️ **Investigate** — is the catalog wrong or is bespoke custom? |
| **Field moved to different section** | Moved field from Basic to Value | ⚠️ **Investigate** — is the classification right? |
| **System scope change** | Narrowed from 3 systems to 1 | ⚠️ **Investigate** — intentional customization or error? |

**High drift (score < 0.80 = < 80%):**

| Drift type | Example | Action |
|---|---|---|
| **Major logic rewrite** | Completely different CASE, new tables | ❌ **Block and revert** — rule is no longer catalog-based |
| **Silent WHERE filter** | Added system filter that wasn't in catalog | ❌ **Block** — changes the universe without audit trail |
| **Deleted columns** | Removed key fields from output | ❌ **Block** — breaks downstream dependencies |

**Decision framework:**

```
Parity score ≥ 0.95 (≥95%)?
  → Accept — minor edits, safe to deploy

Parity score 0.80–0.95?
  → Audit review — ask: Is this intentional customization or a drift?
  → If intentional → document in tracker as "bespoke" variant
  → If accidental → revert to catalog

Parity score < 0.80?
  → Block — the rule has diverged too far from catalog
  → Options: revert to catalog OR promote to bespoke with full re-audit
```

## Related

- [[prc-audit-rule-quality|Audit Rule Quality]]
- [[std-optsel-select-structure|OptSel SELECT Structure]]
