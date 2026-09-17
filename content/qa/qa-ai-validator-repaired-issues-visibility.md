---
id: qa-ai-validator-repaired-issues-visibility
type: qa
title: Visibility of Automatically Repaired Issues
domain: rule-design
audience: [developer, lead]
level: practitioner
status: review
links:
  - parent:ref-ai-static-validator-gate
  - relates:ref-ai-derive-and-enhance-internals
  - relates:prc-audit-rule-quality
sources:
  - coe:changeset-7-dq-studio-workflow-2026-08-31
created: 2026-09-02
updated: 2026-09-02
---

## Question

When the AI Validator automatically repairs issues (without human review), are those repairs visible to the user?

- Where can repairs be reviewed?
- Is there a change log showing before/after?
- Can a user reject an auto-repair and require manual review instead?
- What categories of issues are auto-repaired vs. escalated?

## Context

The AI Static Validator Gate can automatically fix certain issues (syntax errors, formatting, minor logic gaps). Users need visibility into what was changed and why.

## Why This Matters

- **Audit Trail** — Must document what AI fixed automatically
- **Trust** — Consultants need to understand/accept fixes before deployment
- **Control** — Users should be able to reject problematic auto-repairs
- **Learning** — Seeing repairs helps consultants avoid similar issues in future

## Related Concepts

- **AI Validator Gate** ([[ref-ai-static-validator-gate]]) — Quality gate mechanism
- **AI Enhance** ([[ref-ai-derive-and-enhance-internals]]) — AI repair process
- **Audit Quality** ([[prc-audit-rule-quality]]) — Verification after auto-repair

## Expected Answer Should Cover

1. **Repair Visibility:**
   - UI location to review auto-repairs
   - Log format (diff, summary, detailed)
   - Timing (immediate, batch, end-of-run)

2. **Repair Categories:**
   - Auto-repaired (syntax, formatting, minor logic)
   - Escalated for review (structural changes, semantic issues)

3. **User Controls:**
   - Can user reject and require manual review?
   - Override options?
   - Re-run validator with different settings?

4. **Audit Trail:**
   - What's logged (original vs repaired SQL)
   - Who approved the auto-repair (AI timestamp)
   - Ability to revert repairs

5. **Example:**
   - Before: Syntax error (missing comma)
   - After: Corrected syntax
   - Visibility: Shown in [location] with diff

---

**Status:** Awaiting answer  
**Priority:** HIGH (audit and control)  
**Changeset:** 7
