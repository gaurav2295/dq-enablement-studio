---
id: qa-profile-table-selection-criteria
type: qa
title: What criteria should guide table selection for initial profiling?
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

When starting a discovery exercise, how should you decide which tables to include in the profiling bundle? 
Should you profile everything, or are there criteria for selective profiling?

## Answer

**Selective profiling is the standard.** Profile strategically based on engagement scope and business priority.

### Selection criteria

**1. Engagement scope (foundational)**
- Which modules/processes are in scope? (e.g., Materials, Purchasing, Finance?)
- Profile master tables from those modules only
- Example: If Finance focus, profile BKPF, BSEG, GLPCA, but not MARA (Materials)

**2. Business criticality (importance)**
- Which tables drive decisions or contain financial data?
- High criticality → profile early
- Low criticality (supporting/reference) → profile later (if time allows)

| Priority | Tables | Rationale |
|----------|--------|-----------|
| High | MARA, MARC (master) + MSKU (valuation) | Business decisions depend on these |
| Medium | VBAK, VBAP (sales orders) + LIPS (deliveries) | Transactional; important but derived |
| Low | KNA1, LFA1 (customer/vendor masters) | Reference data; fewer DQ rules |

**3. Data complexity (effort)**
- Simple tables (few custom fields, stable schema) → safe to profile early
- Complex tables (many Z fields, frequently modified) → profile after kickoff alignment
- Example: VBAK (stable structure) vs ZCUSTOM_TABLE (new client-specific table)

**4. Knowledge availability (readiness)**
- Do you have DD% access to extract descriptions?
- Has the client documented Z fields and custom tables?
- No documentation → can't profile effectively; wait until documented

### The profiling roadmap (typical engagement)

**Phase 1 (Weeks 1–2): Core discovery**
- 5–10 high-criticality master tables
- Scope: Materials, Plants, Purchasing, Sales (core)
- Effort: ~1 day per table

**Phase 2 (Weeks 3–4): Transactional & specialty**
- 5–8 transactional tables (orders, invoices, payments)
- Add specialty modules (Finance GL, CO, HR) if in scope
- Effort: ~4–6 hours per table

**Phase 3 (Weeks 5+): Custom & optional**
- Client's custom/Z tables
- Reference/supporting tables
- Effort: ~2–3 hours per table (usually with client support)

### When NOT to profile

**Skip profiling when:**
- Table is purely informational (lookup/reference) with no DQ rules planned
- Schema is completely unknown and not documented
- Table is temporary/staging-only (not deployed)
- Client says "we never use this data"

**Instead:** Gather requirements via interviews; skip the profiling run.

> [!tip]
> Start with 5–8 high-value tables. Profile them deeply, build rules, get client feedback. 
> Expand based on what they ask for, not what you think they need.
