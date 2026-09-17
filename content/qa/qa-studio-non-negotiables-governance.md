---
id: qa-studio-non-negotiables-governance
type: qa
title: Who owns the Studio non-negotiables and approves exceptions?
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

The [[prn-studio-non-negotiables|non-negotiables]] are listed as immutable — "a change that 
violates one of them is a bug, not a variation." But what if an engagement has a legitimate 
reason to break a rule? Who decides whether an exception is allowed? Can exceptions be approved?

## Answer

**The short answer:** No exceptions. The non-negotiables are not waivable.

### Why they're called "non-negotiable"

The eight standards (mandatory tech fields, zIsErrorFlag = INTEGER, OptSel is the universe, etc.) 
exist because they encode **interoperability requirements.** Breaking one of them breaks:

- **Downstream scoring** — if zIsErrorFlag is VARCHAR, the SUM() breaks
- **Audit integrity** — if OptSel pre-filters to defects, the universe size vanishes
- **Deployment predictability** — if section comments are optional, the DBA loses context

These are not style preferences. They are **load-bearing**: every component that consumes a rule 
assumes these eight standards hold. Violating one breaks the contract for all downstream consumers.

### When you think you need an exception

**Case 1: "This engagement has a different business model"**
- **Response:** The non-negotiables apply *regardless of business model.* They are encoding integrity, 
  not a particular methodology flavor. Rephrase the rule to fit the standard, don't violate the standard.

**Case 2: "The catalog rule doesn't follow the standard"**
- **Response:** Catalog rules are *promoted* through the wrapper, which *adds* the standard fields 
  (guardrail #7). The catalog SQL is preserved as-is; the Studio ensures the *output* is compliant.
  If the output doesn't comply, that's a bug in the promoter, not a reason to waive the standard.

**Case 3: "Our DBA says we can skip this check"**
- **Response:** The DBA is the implementer, not the standard-setter. If the DBA encounters a 
  technical barrier to implementing a standard (e.g., "our T-SQL doesn't support CONCAT()"), 
  that's a tooling problem to solve, not a standard to waive. Escalate to the CoE.

### Who decides the standards?

The **CoE Architecture Board** owns the eight non-negotiables. Changes to them require:

1. **Documented rationale** — why is the change needed?
2. **Impact assessment** — which downstream components would it affect?
3. **Migration plan** — how would we re-validate existing rules deployed under the old standard?
4. **Board approval** — consensus from leads across engagements

This happens rarely (typically at major SAP version upgrades or after a live incident). 
It is not a per-engagement decision.

### The escalation path

If an engagement discovers a genuine conflict with the standards:

1. **Document it** — what's the conflict? Include engagement context and business justification.
2. **Open a CONFLICT ticket** — add to `docs/CONFLICTS.md` (see CLAUDE.md)
3. **Escalate to CoE lead** — don't proceed until resolved
4. **DO NOT WAIVE** — the rule must be authored to fit the standard, or the engagement is blocked

> [!important]
> The non-negotiables are called that because they are non-negotiable. An exception would 
> mean they're negotiable, which defeats the purpose.
