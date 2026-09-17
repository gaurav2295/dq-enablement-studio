---
id: qa-domain-kb-extension
type: qa
title: How do you extend the knowledge base when a domain keeps returning unknown?
domain: studio
audience: [developer, lead]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

If a rule repeatedly falls into the "unknown domain" path, what's the process for adding 
support for a new domain or extending the domain detector to recognize new rule-name patterns?

## Answer

**Two paths: extend the detector (fast), or add a new domain (slower).**

### Path 1: Extend the domain detector (90% of cases)

**When:** The domain exists, but the detector doesn't recognize the rule name pattern.

**Example:** Rules starting with "CO_" (Controlling) should map to domain CO, 
but the detector only recognizes "COPC_" (cost center).

**How to extend:**

1. **File a CONFLICT ticket** in `docs/CONFLICTS.md`:
   ```
   CONFLICT-NNN: Domain detector misses CO_ prefix
   
   Rule name: "CO_CostCenter_Missing_Assignment"
   Expected domain: Controlling (CO)
   Actual detector result: Unknown
   
   Proposed fix: Add "CO_" to the CO domain's pattern list
   ```

2. **Add the pattern to taxonomy.json** (ref-domain-detector-patterns):
   ```json
   {
     "domain_id": "CO",
     "patterns": [
       "copc_", "coki_", "co_",  -- Add this
       "profit", "cost"
     ]
   }
   ```

3. **Test:** Rerun the deriver with a rule matching the new pattern
4. **Commit** the taxonomy update

**Effort:** 30 minutes (identify pattern, update taxonomy, test, commit).

### Path 2: Add a new domain (rare, requires architecture board)

**When:** A domain doesn't exist in the Studio at all (e.g., new module, client-specific domain).

**Example:** A new client has a CUSTOM domain (ZCUSTOM tables, ZCUSTOM logic) 
not in the standard SAP/Syniti taxonomy.

**How to add:**

1. **Document the domain:**
   - What tables does it cover? (ZCUSTOM1, ZCUSTOM2, ZCUSTOM3?)
   - What are the table relationships? (master, transactional, config?)
   - What are the key fields? (PK, deletion flags, status fields?)

2. **Create domain artifacts:**
   - Domain registration in taxonomy.json
   - Field mappings in table_metadata.json
   - Example rules (to test the detector)

3. **Extend the deriver:** Add ZCUSTOM to [[ref-local-deriver]]'s domain-detection logic

4. **Escalate to CoE:** File a CONFLICT and ask the Architecture Board to review. 
   New domains require board approval (they affect all future engagements).

5. **Merge after approval** (typically 2–4 weeks turnaround for board review)

**Effort:** 40–80 hours (design, implementation, testing, board review).

### Decision tree

```
Rule returns "unknown domain"

├─ Do you know which domain it SHOULD be?
│  └─ YES
│     ├─ Does the domain exist in the Studio?
│     │  ├─ YES → Extend the detector (Path 1, 30 min)
│     │  └─ NO → Add the domain (Path 2, months)
│     
└─ NO
   └─ Escalate to domain expert / SME
      Ask: "What domain should this rule belong to?"
      Then follow the tree again
```

### Engagement impact

**Path 1 extension:** Ship now, detector improves for next engagement
**Path 2 new domain:** Block current engagement; wait for board approval; resume after merge

To minimize delays, **clarify domain scope in the kickoff** — don't discover new domains 
mid-engagement.

> [!tip]
> Most "unknown" domains are caught by extending the detector (Path 1). 
> New domains (Path 2) are rare and require governance. Plan ahead.
