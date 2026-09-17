---
id: qa-regex-heuristics-understanding
type: qa
title: Should consultants understand the regex patterns in rule-name heuristics?
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-rule-name-heuristics
---

## Question

Is it expected that users understand the regex patterns, or is this section intended primarily as a reference?

## Answer

**No — the regex section is a reference for tool builders, not consultants.**

Consultants use the **Studio's inline scorer**, which evaluates all 19 heuristics automatically. You write a rule name, the scorer shows you which heuristics passed and which failed, with **plain-English suggestions**:

```
❌ KNA1 records >= 1 entry

Scoring: 42.5 / 60.5 (70%)

Failed heuristics:
- No Technical Names: KNA1 is a SAP table name (−5)
- No Logic Symbols: >= is not allowed (−3.5)
- Modal Phrase Required: missing "must" (−5)

Suggestions:
→ Replace "KNA1" with "customer"
→ Use "greater than" instead of ">="
→ Rewrite: "A customer must have at least one entry"
```

You **never need to read the regex**. The scorer translates it into actionable feedback.

**When would you read the regex?**
- You're building a tool that integrates with rule naming (not typical consultant work)
- You're debugging why the scorer rejected a specific name (rare)
- You're implementing the scoring engine in a different language

For those rare cases, the "Criteria, verbatim" section provides the exact patterns — but most consultants will never need it.

**The human-facing section is "The 19 heuristics, with weight"** — the table with plain English descriptions like "no `". "` anywhere in the name". Read that, not the regex.

## Related

- [[std-rule-name-heuristics|Rule-Name Heuristics (the 19, enumerated)]]
