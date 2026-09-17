---
id: qa-system-token-fallback-logic
type: qa
title: What problem does the {system} token fallback logic solve?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-view-naming-patterns
  - relates:con-multi-implementation-model
---

## Question

In the {system} token resolution order, what business problem is the fallback-to-raw-code and fallback-to-"SYS" logic solving?

## Answer

**Handling systems that haven't been mapped to an alias** — ensuring view names never break even when a system code is unmapped.

**The fallback chain (in order):**

1. **Explicit alias on the rule** (e.g., rule config says `alias: P06`)
   - Use that alias directly → `DQ_0042_P06_MARA_…`

2. **Alias mapped in project config** (e.g., `Z06 → P06` in system_aliases)
   - Use the mapped alias → `DQ_0042_P06_MARA_…`

3. **No mapping, use raw code** (e.g., system is `Z06`, no alias entry)
   - Use the code directly → `DQ_0042_Z06_MARA_…`
   - (Less friendly, but still works)

4. **Last resort: literal "SYS"** (e.g., system ID is unknown or null)
   - Placeholder to prevent blank view names → `DQ_0042_SYS_MARA_…`
   - (Should rarely happen; signals misconfiguration)

**Why this matters:**

- **Teams grow and systems change.** A new SAP system (Z09) arrives before anyone updates the alias map. Without the fallback, view generation would fail. With it, views are named `DQ_0042_Z09_…` and still work.
- **Audit trail.** The raw code in the name matches the raw code in the SQL WHERE clause — reviewers can trace name ↔ SQL ↔ system without confusion.
- **Flexibility.** Projects with 5 systems can use aliases (`P01–P05`); projects with 50 systems can use codes (`Z01–Z50`). The fallback works either way.

**Real scenario:**

```yaml
# Project YAML
systems:
  - code: SRCECCZ02
    alias: P02
  - code: SRCECCZ06
    alias: P06
  # Z09 is new, not yet in this map

# When Z09 rule is generated:
# Step 1: Is there an explicit alias on the rule? No.
# Step 2: Is Z09 in the system_aliases map? No.
# Step 3: Use the raw code.
# Result: DQ_0042_Z09_MARA_MEINS_OptSel (fallback to raw code)
#
# When Z09 is added to the map:
# Next rule regeneration will use the new alias automatically.
```

The fallback ensures **generation doesn't break while you update config**.

## Related

- [[std-view-naming-patterns|View Naming Patterns]]
- [[con-multi-implementation-model|Multi-Implementation Model]]
