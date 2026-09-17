---
id: qa-profile-ddic-tables-required
type: qa
title: What does "DD% reachable" mean? Which DDIC tables are required?
domain: studio
audience: [developer, consultant]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

The profiling bundle mentions that "DD% reachability" is critical. What exactly is "DD% reachable," 
and which SAP DDIC tables does the profiler need access to?

## Answer

**"DD% reachable" means the profiler can query SAP's Data Dictionary tables to extract field descriptions.**

### What DD% is

DD% (Data Dictionary in SAP terms, formally DDIC) is the repository of table and field metadata. 
When the profiler runs, it needs to access these tables to populate the **Tier 1 (snapshot)** descriptions 
for the profiler dashboard.

### Required DDIC tables

The profiler needs SELECT access to:

| Table | Content | Used for |
|-------|---------|----------|
| **DD03L** | Field definitions (all fields in all tables) | Column names, data types, descriptions |
| **DD02T** | Table titles (short descriptions) | Table labels in the profiler |
| **DD04T** | Domain values (field domains, code lists) | Understanding field types (code table, numeric, etc.) |

**Minimum access:** DD03L (absolutely required). DD02T and DD04T are nice-to-have; if blocked, the profiler still works.

### Who can access DD%?

In SAP, DDIC access is role-based:

- **Developers:** Full access (typically via SE11 transaction)
- **Basis team:** Full access (they manage DDIC)
- **Business users:** Usually no direct access
- **Service accounts (profiler user):** Depends on role assignment

### "DD% not reachable" scenarios

**Scenario 1: Role restriction**
- The profiler service account doesn't have DDIC roles
- **Fix:** Ask Basis to grant SE11 / DDIC select permissions to the profiler user

**Scenario 2: Network/firewall blocking**
- The profiler user can't reach the SAP system's DDIC (e.g., sandbox isolated from prod)
- **Fix:** Open network path from profiler host to SAP DDIC tables

**Scenario 3: SAP system down**
- DD% tables are temporarily unavailable
- **Fix:** Wait for system to recover; retry profiling

### What happens when DD% is not reachable?

Profiler still runs, but:
- Tier 1 (snapshot) descriptions are empty
- Falls back to Tier 2 (client dictionary) or Tier 3 (internal SAP)
- Provenance badge shows 0% snapshot

**Result:** Dashboard labels are generic or stale. Less useful for discovery.

### How to verify DD% access

Before running the profiler, test:

```sql
SELECT TABNAME, FIELDNAME, DDTEXT 
FROM DD03L 
WHERE TABNAME = 'MARA' 
  AND FIELDNAME = 'MATNR';
```

If this query succeeds, DD% is reachable. If it fails, escalate to Basis.

> [!tip]
> DD% access is a prerequisite for rich profiling. If the profiler user can't access it, 
> ask your SAP Basis team to grant the role. It's a one-time setup.
