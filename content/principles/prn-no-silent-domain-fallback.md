---
id: prn-no-silent-domain-fallback
type: principle
title: Why No Silent Domain Fallback
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-local-deriver
  - relates:prn-catalog-promotion-wraps-instead-of-injecting
  - relates:prn-sql-comments-must-match-local-derive-quality
  - relates:gls-tbd-placeholder
sources:
  - vault:thought-leadership/Why No Silent Domain Fallback.md
tags: [thought-leadership, methodology, engine, studio, sap]
created: 2026-08-20
updated: 2026-08-20
---

## The rule

When the deriver can't recognise a rule's domain, it emits an un-deployable TBD spec on
purpose — because silently falling back to the Material domain produced confidently-wrong
MARA/MARC SQL for every FI, intercompany, banking, project, and SD rule whose name didn't trip a
domain detector.

This is the decision rationale behind ref-no-silent-material-fallback. That reference
documents *what the code does*; this note documents *why we chose failure over a guess*.

## The temptation

The [[ref-local-deriver]] starts every derivation by trying to detect the rule's domain.
Material is the richest, most-tested domain. The lazy default is obvious: if nothing matches,
assume material, point `mainTable` at MARA, and generate something.

Something always renders. That is the trap. The generated SQL is **syntactically valid and
semantically wrong** — it joins MARA/MARC and checks material fields for a rule that was
actually about a profit centre, a tax category, or a field status group.

## The burn — the "Bacardi" rules

The verbatim code comment names the incident: silent material fallback "produced
confidently-wrong MARA/MARC SQL for every FI / intercompany / banking / project / SD rule whose
name didn't trigger any domain detector." The profiling path's comment is even more specific — it
cites the Bacardi Profit Center / Tax Category / Field Status Group rules as the rules that
motivated the change.

These rules have nothing to do with materials. But "Profit Center distribution" doesn't
substring-match a material field, so detection returned nothing, the old code fell back to
material, and out came MARA SQL with a straight face. A reviewer skimming for syntax errors
finds none — the defect is invisible until someone who knows FI reads it.

## The canonical rule

> [!warning]
> Unknown domain → un-deployable TBD spec. Never a guessed domain.

When domain detection finds no match the deriver:

1. Marks the domain as unknown and builds an empty shell — no main table, fields, joins, or
   deletion flags.
2. Short-circuits to a deliberately broken placeholder spec — zero confidence, zero fields
   matched, a warning recorded — and returns early rather than continuing.
3. The SQL generator renders `SELECT * FROM /* TBD */;` — which fails at parse time, so a stale
   guess can never sneak into a deployment.
4. The description lists the covered domains so the user can rephrase the rule into a name the
   detector recognises.

The profiling narrative path makes the identical choice: unknown domain → empty main table and a
domain-unknown flag, never a material guess.

## The principle: loud failure beats quiet wrongness

A spec that won't deploy stops the line. The author sees the warning, sees the covered-domain
list, and either renames the rule or extends the knowledge base. A spec that deploys with wrong
SQL ships a lie — it reports a defect rate for the wrong table, and nobody notices until a
downstream audit or an unhappy client does.

Cost of the TBD spec: one rephrase. Cost of the silent guess: a wrong rule in production, found
late, traced to the deriver, eroding trust in every other rule it generated.

This is the same instinct as "uncovered domains highlight, never silently blank." The system
would rather be visibly incomplete than invisibly wrong.

## Worked example: From domain-unknown to successful derivation

Here's what happens when you hit the domain detector, then fix it.

**Step 1: User submits a rule with an unrecognized name**

Rule name: `Profit_Center_Negative_Balance_Check`

The domain detector scans the name for keywords (MARA, MATERIAL, FI, SALES, CO, etc.). 
It finds nothing. No domain matched.

**Step 2: Studio returns a TBD spec**

```
⚠ Domain unknown. Studio cannot derive SQL.

Covered domains: [MATERIAL, PLANT, PURCHASING, SALES, PRODUCTION, FI, HR, CO, ...]

Fix: Rename the rule to include a recognized domain keyword.
Example: "FI_Profit_Center_Negative_Balance_Check" (prefix "FI")
```

The spec is deliberately broken — `SELECT * FROM /* TBD */;` — so it won't deploy. The error stops the line.

**Step 3: User renames the rule**

Rule name: `FI_Profit_Center_Negative_Balance_Check`

The prefix "FI" now matches the Financial domain detector.

**Step 4: Studio derives FI-specific SQL, then AI Enhancement cleans it up**

Domain matched → FI tables and fields are available → SQL derives. If any `/* TBD */` markers remain in the spec (e.g., missing error predicate), the **AI Enhancement guardrail** detects them and resolves them. AI Enhancement ensures the final output has **zero TBD placeholders** — it fills in gaps with confident SQL or flags the rule for manual review if it cannot.

Result: Deployable FI-specific SQL with no TBD markers:

```sql
CREATE VIEW [dbo].[DQ_0087_SAP_GLPCA_NegBalance_OptSel] AS

SELECT
    -- Syniti Technical Fields
    bukrs AS [zSourceSystemID],
    CONCAT(bukrs, '|', prctr, '|', bukrs) AS [zConcatenatedKey],
    CASE WHEN dmbtr < 0 THEN 1 ELSE 0 END AS [zIsErrorFlag],
    
    -- Basic Fields
    bukrs AS CompanyCode,
    prctr AS ProfitCenter,
    dmbtr AS DebitAmount
    
FROM GLPCA_Stage
WHERE bukrs = 'SAP'
;
```

> [!tip]
> **TBD handling:** If a TBD survives initial derivation, AI Enhancement catches it. The final rule shipped to the tracker carries zero TBDs — either they're resolved by AI, or the rule is flagged for DBA review before deployment.

## A sibling guard — empty-match field injection

The same philosophy fires one layer deeper. Even when a domain *is* detected, if field-matching
produces no confident match the value-section builder does **not** inject a random field to fill
the gap — the reasoning is blunt: doing so "causes hallucinated SQL." A domain match
with zero field matches sets `_review_required` and the generator emits a NULL `zIsErrorFlag`
with a `/* TBD */` marker rather than inventing a check. Same rule, smaller scope: don't
manufacture a confident answer from no evidence.

## User-visible output example

When domain detection fails, here's what the user sees:

```
⚠ DOMAIN UNKNOWN

Rule name: "Profit_Center_Negative_Balance_Check"

The Studio could not recognize a known domain from the rule name.
To fix this, prepend a domain keyword:

  ✓ FI_Profit_Center_Negative_Balance_Check    (Financial)
  ✓ CO_Profit_Center_Negative_Balance_Check    (Controlling)

Covered domains: [MATERIAL, PLANT, PURCHASING, SALES, PRODUCTION, FI, HR, CO, ...]

Spec generated: UN-DEPLOYABLE (TBD placeholder)
SELECT * FROM /* TBD */;
```

The placeholder spec fails at parse time, preventing deployment. This forces the user to rephrase and retry.

## Rephrase vs extend the knowledge base

When you encounter domain-unknown, decide:

| Scenario | Action |
|----------|--------|
| You know which domain the rule belongs to, but the detector didn't recognize the name | **Rephrase:** Add a domain prefix ("FI_", "CO_", etc.) and resubmit |
| The rule's domain is new (not in the covered list) | **Escalate:** File a CONFLICT; ask the CoE to extend domain support (2–4 weeks) |
| You're unsure which domain applies | **Ask:** Contact the CoE or a domain expert before resubmitting |

Rephrasing is instant (1 minute). Extending the knowledge base takes weeks (board approval). 
Prefer rephrasing unless the domain truly doesn't exist.

## Related

- ref-no-silent-material-fallback — the engine-level implementation
- [[ref-local-deriver]] — the derivation pipeline this guard lives in
- ref-field-matching — the field-matching step the sibling guard protects
- ref-rule-type-detection
- [[prn-catalog-promotion-wraps-instead-of-injecting]] — same "don't re-derive a guess" instinct
- [[prn-sql-comments-must-match-local-derive-quality]]
