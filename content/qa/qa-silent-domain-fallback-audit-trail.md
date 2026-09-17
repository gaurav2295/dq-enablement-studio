---
id: qa-silent-domain-fallback-audit-trail
type: qa
title: Does the Studio log failed domain-detection attempts?
domain: studio
audience: [developer, lead]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-04
created: 2026-09-07
updated: 2026-09-07
---

## Question

When users rephrase a rule name after receiving a domain-unknown result, does the Studio retain 
any record of the original failed derivation attempt for troubleshooting or audit purposes?

## Context

A rule submitted as `Profit_Center_Negative_Balance_Check` triggers domain-unknown and returns 
TBD. The user renames it to `FI_Profit_Center_Negative_Balance_Check`, which succeeds. 

From an audit and troubleshooting perspective: Is there a log entry recording the failed 
attempt? If a DBA later needs to trace why version 1 failed, can they find that record?

## Answer

No. The Studio **does not** retain a record of the original failed rule name.

### What actually happens

When a rule submission triggers domain-unknown:

1. The user sees the TBD error in the UI with the covered-domains list
2. The user renames the rule and resubmits
3. **The failed attempt is not logged** — only the successful derivation becomes a tracker record

There is no audit trail linking the failed `Profit_Center_Negative_Balance_Check` to the successful 
`FI_Profit_Center_Negative_Balance_Check`. Once the user renames and resubmits, the original 
attempt is gone.

### Why

This is by design. The Studio's philosophy is **"fail loudly, then fix forward"** — the error 
message is explicit enough to guide the user to a fix, and that's the only concern. Retaining 
failed attempts would add complexity to:

- The derivation pipeline (every failed spec would need storage)
- The tracker schema (new fields for "prior attempts")
- User support (consultants would ask "why do I have 5 failed attempts on this rule?")

Instead, the system assumes: **if the user got the error and fixed the name, they're done. 
The only record that matters is the final, successful rule.**

### Implication for troubleshooting

If a DBA encounters a rule in the tracker and wants to understand the derivation history, they 
**cannot** see prior failed names. They can only see the current rule name, the domain detected, 
and the final spec.

If troubleshooting is needed, the DBA must **ask the rule author** or consult the engagement's 
rule-authoring notes / batches (which may record the user's worksheet with name changes).
