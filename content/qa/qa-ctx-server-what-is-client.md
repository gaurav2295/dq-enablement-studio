---
id: qa-ctx-server-what-is-client
type: qa
title: In ctx-server, does "client" refer to SAP clients (DEV-100/110/120)?
domain: delivery
audience: [consultant, lead]
level: foundation
status: review
sources:
  - coe:gls-ctx-server
created: 2026-09-03
updated: 2026-09-03
links:
  - parent:gls-ctx-server
  - relates:gls-rule-repository
  - relates:gls-dq-studio
---

## Question

Is client here referring to the different clients which are within SAP System for e.g. DEV-100/110/120?

## Answer

**No — "client" in ctx-server refers to different business clients (companies/customers), not SAP clients (100/110/120).**

### Clarification

| Term | Meaning | Example |
|------|---------|---------|
| **SAP Client** | A separate instance/database within one SAP system | DEV-100, DEV-110, PROD-100 |
| **Business Client** (ctx-server) | A different customer/company using the tool | Acme Corp, TechCorp, MegaCorp |

### What ctx-server Does

**ctx-server** isolates **different business clients' data** so they cannot accidentally see each other's DQ results or rules.

**Design principle:** "One client root per session, so cross-client queries are impossible by construction"

```
┌─────────────────────────────────┐
│ ctx-server (Per-Client Context) │
├─────────────────────────────────┤
│ Session 1                       │
│ └─ Root: Acme Corp              │
│    └─ All queries/rules for     │
│       Acme only                 │
│                                 │
│ Session 2                       │
│ └─ Root: TechCorp               │
│    └─ All queries/rules for     │
│       TechCorp only             │
│                                 │
│ (No cross-client visibility)    │
└─────────────────────────────────┘
```

### Real Example

**Acme Corp DQ Engagement:**
- Running DQ rules on Acme's data (SAP client DEV-100 and PROD-100)
- ctx-server ensures Acme's rules/results stay isolated

**TechCorp DQ Engagement:**
- Running DQ rules on TechCorp's data (SAP client DEV-110 and PROD-110)
- ctx-server ensures TechCorp's rules/results stay isolated
- **TechCorp cannot access Acme's data**, even though they might share the same SAP infrastructure

### Why "By Construction"

Instead of checking permissions at **query time** (which could be misconfigured), ctx-server makes isolation **impossible to bypass**:

```
✅ SAFE BY CONSTRUCTION:
- One client root per session
- No second client is mounted
- No query can reach a different client (it doesn't exist in that session)

❌ NOT SAFE (permission-based):
- If the permission check is misconfigured, data leaks
```

### Important Note

**ctx-server is planned, not yet built.** The unit explicitly states:

> "Designed, not yet built. Do not write material that implies it exists, and do not commit an engagement to capability that depends on it."

So this is a **future security architecture** for multi-tenant deployment, not something currently available in the Studio.

---

### Related

- [[gls-ctx-server|ctx-server (per-client context server)]]
- [[gls-rule-repository|Rule Repository]]
- [[gls-dq-studio|DQ Studio]]
