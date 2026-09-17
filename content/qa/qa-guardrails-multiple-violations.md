---
id: qa-guardrails-multiple-violations
type: qa
title: If multiple guardrails are violated, how does the Studio prioritize findings?
domain: studio
audience: [developer]
level: advanced
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

If a rule violates guardrails #1, #3, and #6 simultaneously, how does the Studio 
prioritize and report those violations? Is there a specific order or grouping?

## Answer

**Violations are grouped by severity, then reported in priority order.**

### Severity tiers

**Tier 1 (Blocks deployment):**
- Guardrail 1: Missing mandatory tech fields
- Guardrail 2: zIsErrorFlag is not INTEGER
- Guardrail 3: OptSel is pre-filtered (WHERE is used for logic)

**Tier 2 (Warns, can still deploy with flag):**
- Guardrail 4: RptSel wrapper is non-standard
- Guardrail 5: User intent ignored (catalog downgraded to InfSel when user said Error)
- Guardrail 6: Fan-out sibling IDs don't match tracker
- Guardrail 7: Catalog SQL was re-derived (should be verbatim)
- Guardrail 8: Section comments are incomplete

**Tier 3 (Documents, doesn't block):**
- Guardrail 9: Description template doesn't follow Fetch/Check/Return

### Reporting order

**Tier 1 violations reported first** (largest impact):
```
❌ CRITICAL (rule is un-deployable):
  - Guardrail 1: Missing zSourceSystemID
  - Guardrail 2: zIsErrorFlag is VARCHAR
  [STOP: user must fix these before rule can deploy]
```

**Tier 2 violations reported if Tier 1 passes:**
```
⚠ WARNING (rule deployable but flagged):
  - Guardrail 5: User intended Error; rule is InfSel
  - Guardrail 7: Catalog SQL was modified
  [Rule deploys, but with caution markers]
```

**Tier 3 violations reported if Tier 1 and Tier 2 pass:**
```
ℹ INFO (style/documentation):
  - Guardrail 9: Description missing "Check" section
  [Doesn't affect deployment; FYI only]
```

### Example: Three simultaneous violations

Rule has:
- Missing zSourceSystemID (Guardrail 1, Tier 1)
- RptSel wrapper uses INNER JOIN instead of SELECT * (Guardrail 4, Tier 2)
- Description is missing Check section (Guardrail 9, Tier 3)

**Reported as:**
```
❌ CRITICAL (report Tier 1 first, stop):
  - Guardrail 1: zSourceSystemID is missing
  
[Tier 2 and Tier 3 not reported; user must fix Tier 1 first]
```

User fixes, revalidates:

```
⚠ WARNING (now report Tier 2):
  - Guardrail 4: RptSel should be SELECT * FROM OptSel WHERE [zIsErrorFlag] = 1
  
ℹ INFO (then Tier 3):
  - Guardrail 9: Description template incomplete
```

### Why group by severity?

**Signal-to-noise ratio:** If you report all 27 findings at once, users are overwhelmed. 
Grouping by severity lets them focus on blocking issues first, then warnings, then documentation.

> [!tip]
> Fix Tier 1, revalidate. Then fix Tier 2, revalidate. Then Tier 3. 
> This iterative approach is faster than trying to fix everything at once.
