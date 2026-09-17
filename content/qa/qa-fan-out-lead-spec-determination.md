---
id: qa-fan-out-lead-spec-determination
type: qa
title: How is the lead spec determined when multiple implementations already exist?
domain: studio
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:prc-fan-out-a-rule-per-system
created: 2026-09-03
updated: 2026-09-03
links:
  - parent:prc-fan-out-a-rule-per-system
  - relates:con-multi-implementation-model
  - relates:gls-sibling-implementation
---

## Question

How is the lead spec determined when multiple implementations already exist for the same SKP_RULE_NNNN? Can the lead be changed manually/selected?

## Answer

The **lead spec** is typically the **first per-system implementation** created (e.g., P02 if you started with SAP ECC). 

When you fan-out a rule across systems, the lead's spec is cloned to create all sibling implementations — so the lead becomes the source of truth for the group.

**Can the lead be changed?** The current Studio does not have a UI option to manually select or change which system is the lead. If you need a different system to be the lead:

1. **Re-derive the entire rule** from scratch with the new system listed first in the fan-out scope
2. **Or** treat the sibling you want as the new lead and manually update its spec, then re-fan-out from that point forward

**Impact:** The lead determines the baseline logic for all siblings. If you change the lead, future fan-out operations will clone from the new lead's spec, potentially overwriting sibling-specific customizations.

**Best practice:** Choose your lead system carefully at the start (usually the most complete or representative system in your data model) and keep it stable throughout the project.

---

### Related

- [[prc-fan-out-a-rule-per-system|Fan Out a Rule Per System]]
- [[con-multi-implementation-model|The Multi-Implementation Model]]
