---
id: qa-domain-error-message-detail
type: qa
title: Does the error message show which parts of the rule name failed to match?
domain: studio
audience: [consultant]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

When a rule returns domain-unknown, the error message lists the covered domains. 
But does it also explain *why* the detection failed? Does it show which parts of 
the rule name didn't match any known domain terminology?

## Answer

**Not in the current version.** The error message lists covered domains, 
but does not show substring-matching results.

### Current error message

```
⚠ Domain unknown. Studio cannot derive SQL.

Covered domains: [MATERIAL, PLANT, PURCHASING, SALES, PRODUCTION, FI, HR, CO, ...]

Fix: Rename the rule to include a recognized domain keyword.
Example: "FI_Profit_Center_Negative_Balance_Check" (prefix "FI")
```

### What would be helpful

A more detailed message showing substring attempts:

```
Rule name: "Profit_Center_Negative_Balance_Check"

Substring matching attempts:
  ✗ PROFIT does not match MATERIAL, PLANT, PURCHASING, FI, ...
  ✗ CENTER does not match any domain keyword
  ✗ NEGATIVE does not match any domain keyword
  ✗ BALANCE does not match any domain keyword

Suggestion: Prepend a domain prefix. Examples:
  - "FI_Profit_Center_Negative_Balance_Check" (for Controlling)
  - "CO_..." (for Cost Controlling)

Covered domains: [MATERIAL, PLANT, PURCHASING, SALES, PRODUCTION, FI, HR, CO, ...]
```

### Workaround (current)

If the error message is unclear:

1. **Check the domain list** — look for domains related to your rule's business area
2. **Experiment with prefixes:** "FI_", "CO_", "HR_", etc.
3. **Ask the CoE:** If still unclear, escalate with the rule name; we can guide you to the right domain

### Future improvement

This diagnostic detail (substring-matching results) is planned for a future Studio update.
Until then, the generic "covered domains" list is your starting point.

> [!tip]
> If the error message feels vague, don't hesitate to ask for help. The detector's internal 
> logic is deterministic; we can trace through it manually and guide you to the right domain.
