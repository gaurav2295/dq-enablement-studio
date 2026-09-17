---
id: qa-format-accuracy-vs-conformity
type: qa
title: Why is 'consistent format' mapped to Accuracy instead of Conformity in the Studio section?
domain: dq-fundamentals
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:qa
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:con-dq-dimensions
---

## Question

Under the 'In Studio' section — Why is "consistent format" mapped to Accuracy instead of Conformity, since Conformity is defined as adherence to a required format, range, or standard?

## Answer

This is an excellent catch — the distinction is genuinely ambiguous in rule names. The keyword-mapping is a *starting point only*; the final call depends on the rule's **actual intent**, not just its name.

**The principle:**
- **Accuracy:** Does the recorded value match the real-world fact? (Is a postal code 12345 *correct for that address*?)
- **Conformity:** Does the recorded value follow the system's defined format/range/standard? (Is 12345 in the *correct format* for a US postal code — 5 digits?)

**Why the keyword mapping is confusing:**
- "*Properly formatted*" in the keyword list suggests the value *is* in the right format (which should be Conformity)
- "*Conforms to format*" is an explicit Conformity trigger
- Yet both can appear in the same rule name

**The real decision:**

Consult the **rule's implication** (not just the name). Ask: what is the defect saying?

- If the rule says *"Postal code is invalid for this address"* → **Accuracy** (real-world fact: this code doesn't match this location)
- If the rule says *"Postal code doesn't match US 5-digit format"* → **Conformity** (system standard: must be 5 digits)

**Example — same rule name, different intents:**

| Rule Name | Implication | Dimension |
|-----------|-------------|-----------|
| "A customer's postal code must be properly formatted" | "Must match country's postal code format (e.g., US: 5 digits, UK: postcode pattern)" | Conformity |
| "A customer's postal code must be properly formatted" | "Must correspond to the customer's actual physical address" | Accuracy |

The name is identical; the dimension depends on what the rule actually checks.

**The guidance:** When ambiguous between Accuracy and Conformity, the name is the trigger; consult the rule's implication to determine the actual dimension. The keyword mapping is a shortcut, not a hard rule.

See [[con-dq-dimensions|The Seven DQ Dimensions]] for the full keyword-mapping guidance in the "In the Studio" section.
