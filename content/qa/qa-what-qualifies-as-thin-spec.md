---
id: qa-what-qualifies-as-thin-spec
type: qa
title: What Qualifies a Spec as "Thin"?
domain: ai-enhancement
audience: [consultant, developer]
level: practitioner
status: review
links:
  - parent:ref-local-deriver
  - relates:gls-project-spec
  - relates:std-ai-enhance-scope
sources:
  - coe:changeset-7-dq-studio-workflow-2026-08-31
created: 2026-09-02
updated: 2026-09-02
---

## Question

When Local Derive returns a "thin spec", what qualifies a spec as thin? 

Specifically:
- How many fields are missing from a "thin" spec?
- How much metadata (description, examples, sources) can be missing?
- Is a thin spec complete enough to be deployed, or does it require manual enrichment?
- How does a thin spec differ from a "failed" spec (unknown domain)?

## Context

The Local Deriver uses AI to infer rule specifications from field names and table context. When it has insufficient information, it returns a "thin spec" — a partial specification that requires manual completion before derivation.

## Why This Matters

- **Quality Assurance** — Distinguishes between viable-but-incomplete specs and specs that failed entirely
- **Consultant Workflow** — Thin specs require manual enrichment; failed specs require restart
- **Automation Potential** — Understanding thinness helps identify when to accept or reject AI-derived specs
- **Documentation** — "Thin" is a technical term; must be precisely defined

## Related Concepts

- **Project Spec** ([[gls-project-spec]]) — The complete specification format
- **Local Deriver** ([[ref-local-deriver]]) — How specs are inferred
- **AI Enhance Scope** ([[std-ai-enhance-scope]]) — What data AI needs to work effectively

## Expected Answer Should Cover

1. **Thin Spec Definition** — Formal criteria for "thin" status
2. **Thinness Indicators:**
   - Missing sections (e.g., no description)
   - Incomplete metadata (e.g., source system guessed, not confirmed)
   - Partial field coverage (e.g., 70% of expected fields inferred)
3. **Thin vs Failed:** Thin = Partial but viable; Failed = Fundamentally unrecognizable
4. **Deployment Readiness:** What MUST be completed before deployment?
5. **Example:** Table detection → thin spec with 70% fields, missing description

---

**Status:** Awaiting answer  
**Priority:** MEDIUM (AI-derivation workflow)  
**Changeset:** 7
