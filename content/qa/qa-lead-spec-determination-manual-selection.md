---
id: qa-lead-spec-determination-manual-selection
type: qa
title: Determining Lead Spec and Manual Selection in Fan-Out
domain: rule-design
audience: [developer, lead]
level: practitioner
status: review
links:
  - parent:prc-fan-out-a-rule-per-system
  - relates:gls-fan-out
  - relates:gls-sibling-implementation
  - relates:gls-dqops-id
sources:
  - coe:changeset-7-dq-studio-workflow-2026-08-31
created: 2026-09-02
updated: 2026-09-02
---

## Question

How is the lead spec determined when multiple implementations already exist for the same SKP_RULE_NNNN?

- Is lead spec automatic (first created? most recent? best quality)?
- Can the lead be manually selected or changed?
- What happens to non-lead siblings if lead is changed?
- Do all siblings share the same SKP_RULE_NNNN?

## Context

When re-fanning-out an existing rule across systems, the system must choose which implementation is the "lead" (source of truth for re-derivation). This choice affects how sibling updates propagate.

## Why This Matters

- **Governance** — Lead selection impacts which system version is authoritative
- **Consistency** — All siblings should derive from same lead
- **Flexibility** — Users may need to change lead if quality improves in one sibling
- **DQOps Tracking** — Lead/sibling relationship must be clear in audit

## Related Concepts

- **Fan-Out** ([[gls-fan-out]]) — Splitting rule per system
- **Sibling Implementation** ([[gls-sibling-implementation]]) — Variants of same rule
- **DQOps ID** ([[gls-dqops-id]]) — Deployment identifier per implementation

## Expected Answer Should Cover

1. **Lead Determination:**
   - Automatic logic: What criteria (first created? least divergent? user-specified?)
   - Manual override: Can users select lead explicitly?
   - UI/CLI to view/change lead

2. **SKP_RULE_NNNN Relationship:**
   - All siblings share single SKP_RULE_NNNN? YES/NO
   - Each system gets unique SKP_RULE_NNNN? (and DQOps ID per sibling)
   - Example with numbers

3. **Lead Change Implications:**
   - What happens if lead is changed mid-project?
   - Are non-lead siblings updated?
   - Audit trail of lead changes

4. **Example Scenario:**
   - Initial: Lead = SAP sibling
   - Later: Lead changed to LEGACY because quality improved
   - Impact on SAP, LEGACY siblings

5. **Best Practice:**
   - Recommended approach to lead selection
   - When to override automatic lead

---

**Status:** Awaiting answer  
**Priority:** HIGH (fan-out workflow)  
**Changeset:** 7
