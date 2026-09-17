---
id: con-catalog-vs-bespoke-rules
type: concept
title: Catalog vs Bespoke Rules
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-skp-rule-identifier-convention
  - relates:prc-run-the-bulk-pipeline
  - relates:qa-catalog-to-bespoke-rule-conversion
  - relates:qa-bespoke-to-catalog-promotion
sources:
  - vault:dq-methodology/Catalog vs Bespoke Rules.md
tags: [methodology]
created: 2026-08-20
updated: 2026-08-20
---

## The two provenance categories

Every rule's origin is one of two categories. The tracker carries the distinction in the
`RuleOrigin` column.

## Catalog

Rules sourced from the **Syniti AI Generated Rule Catalog 2025** — a curated, version-pinned set
of pre-defined DQ rules with verbatim SQL.

- Catalog ID anchors the rule (`DQ_0028`, `DQ_0152`, etc.).
- OpQuerySQL + ReportQuerySQL come straight from the catalog with `{datastore}` placeholder
  substitution.
- The catalog's original SQL is preserved on the spec so the Audit screen can compute a parity
  score against it.
- Profiling rules are **out of scope** of the catalog — all profiling rules are Bespoke.

**Use Catalog when** the rule already exists in the catalog and matches the client's intent.
Faster to deliver, peer-reviewed, parity-tested.

## Bespoke

Rules authored fresh for a specific engagement, either via:

- **Local Derive** — knowledge-driven from a rule name (uses the Studio knowledge base).
- **AI Derive** — Claude-driven from a rule name + AI table hint.
- **Adapted Catalog rule** — a Catalog rule customized for client-specific scope, data model, or business logic (see [[qa-catalog-to-bespoke-rule-conversion|Can a Catalog rule be converted to Bespoke?]]).

No catalog ID. The [[prc-run-the-bulk-pipeline|bulk pipeline]] auto-assigns DQOps `rule_id`s and
`SKP_RULE_NNNN` identifiers via the auto-counter.

**Use Bespoke when** the rule is client-specific, the catalog doesn't cover it, the client's
environment requires a custom data model the catalog doesn't speak to, or a Catalog rule needs
client-specific modifications.

## Quick Decision Guide: Catalog vs. Bespoke

**Use this flowchart to quickly decide which approach is right for your scenario:**

```
START: Do you have a rule requirement?
│
├─ YES, and it matches a Catalog rule exactly?
│  └─ YES ──→ ✅ USE CATALOG
│     └─ Faster, peer-reviewed, parity guarantee
│  └─ NO (needs modifications)
│     ├─ Small modifications (different filters, custom field)?
│     │  └─→ ✅ ADAPT CATALOG RULE AS BESPOKE
│     │     └─ Use as template, modify, mark as Bespoke
│     └─ Large changes (different tables, different logic)?
│        └─→ ✅ CREATE BESPOKE RULE
│           └─ Via Local Derive or AI Derive
│
├─ NO, or Catalog doesn't cover this domain?
│  └─ ✅ CREATE BESPOKE RULE
│     ├─ Use Local Derive (knowledge-driven)
│     └─ Or use AI Derive (Claude-driven with hints)
│
└─ Profiling rule?
   └─ ✅ ALWAYS BESPOKE
      └─ Profiling rules are out of scope for Catalog
```

**Decision Table (When in Doubt):**

| Scenario | Choice | Why | Tradeoff |
|----------|--------|-----|----------|
| Rule exists in catalog exactly as needed | **Catalog** | Faster, peer-reviewed, parity guarantee | No customization possible |
| Rule exists but needs minor tweaks (field mappings, filters) | **Bespoke (adapted)** | Reuses solid foundation, documents lineage | Loses parity guarantee after modification |
| Rule doesn't exist in catalog or needs major changes | **Bespoke (new)** | Client-specific, fully customizable | Needs internal review and validation |
| Profiling rule (distribution, counts, grouping) | **Bespoke** | Profiling out of scope for Catalog | No catalog baseline to compare against |
| Rule for unusual/custom domain (client-specific tables) | **Bespoke** | Catalog assumes standard SAP; custom domains need custom rules | More development effort upfront |

## Converting a Catalog rule to Bespoke

**Can you take a Catalog rule and adapt it?** Yes. When a Catalog rule matches the business intent but needs client-specific modifications (different tables, additional filters, custom logic), adapt it as a Bespoke rule.

**Process:**
1. Start with the Catalog rule's SQL as a template
2. Modify it for the client's data model, scope, or requirements
3. **Mark it as Bespoke** in `RuleOrigin` — it's no longer the authoritative Catalog version
4. **Document the lineage** — in the spec's Description or a comment, note: "Based on Catalog rule `DQ_NNNN`, adapted for [client-specific reason: custom table mapping / additional filters / data model variation]"
5. The [[prc-run-the-bulk-pipeline|bulk pipeline]] auto-assigns its own identifiers (DQOps ID and SKP_RULE_NNNN)

**Why Bespoke?** Once modified, the rule no longer matches the authoritative Catalog SQL, so it cannot carry the Catalog parity guarantee. Marking it as Bespoke is honest about that loss and enables proper auditing.

**Promotion path:** If the adapted rule proves valuable across multiple engagements, it can be promoted back into the Catalog with the modification as a standard variant (e.g., "DQ_0028_variant: Custom vendor table mapping"). See [[qa-bespoke-to-catalog-promotion|When should a Bespoke rule be promoted to Catalog?]] for promotion criteria.

## Why preserve the distinction

- **Audit defensibility** — catalog rules carry the parity guarantee against Syniti's
  authoritative SQL. Bespoke rules need their own validation evidence. Adapted rules explicitly declare they're no longer authoritative.
- **Promotion path** — when a Bespoke rule (adapted or original) proves useful across engagements, it can be promoted up into the catalog. Tracking provenance and adaptation notes lets that pipeline work.
- **Estimate accuracy** — Catalog rules deliver fast; Bespoke rules need more rule-name scoring,
  AI derive review, audit. Knowing the mix at the start of a sprint sizes the work correctly.

## Promoting a Bespoke rule to Catalog

A Bespoke rule can be elevated into the Catalog if it meets promotion criteria. See [[qa-bespoke-to-catalog-promotion|When should a Bespoke rule be promoted to Catalog?]] for the full decision framework.

**High-level criteria:**
- **Proven reuse** — successfully used across 2+ distinct engagements without modification (or with documented, stable variations)
- **Quality attestation** — passed all audits, client sign-off, and production deployment with no defect escalations
- **General applicability** — solves a common DQ problem across multiple clients / industries / ERP scenarios
- **SQL standards compliance** — follows all mandatory rules (CTE structure, zSourceSystemID alignment, 5-section output, OptSel/RptSel pattern)
- **Stable logic** — the rule's condition and intent haven't drifted between engagements

**Outcome:** Once promoted, the rule becomes a Catalog entry with a fixed Catalog ID, versioning, and parity guarantee.

## In the tracker

| Column | Value |
|---|---|
| `RuleOrigin` | `Catalog` or `Bespoke` |
| `DQOPSID` | Sequential per implementation (4-digit zero-padded) |
| `ClientRef` | `SKP_RULE_NNNN` (see [[std-skp-rule-identifier-convention]]) |

The Audit screen pivots on `RuleOrigin` — bespoke rules surface a "no catalog reference" status;
catalog rules get parity-scored against the catalog SQL.
