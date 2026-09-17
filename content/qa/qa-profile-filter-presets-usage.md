---
id: qa-profile-filter-presets-usage
type: qa
title: When should auto_active, custom, and no_filter presets be used?
domain: studio
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

The profiler has three filter presets (auto_active, custom, no_filter). When should each one be used, 
and what are typical scenarios?

## Answer

**Pick based on your knowledge of the table's deletion/status strategy.**

### The three presets

| Preset | What it does | Use when |
|--------|--------------|----------|
| **auto_active** | Automatically excludes deletion flags (LVORM, LOEKZ, etc.) | You know the table has standard SAP deletion flags |
| **custom** | You specify exactly which WHERE conditions to apply | Table has non-standard deletion or status logic |
| **no_filter** | Returns all records including deleted | You want to see everything (rare) |

### Scenario examples

**Scenario 1: MARA (Materials master)**
- Standard SAP table with LVORM (delete flag)
- No custom status logic
- **Use:** `auto_active`
- **Result:** Profiles only non-deleted materials (LVORM <> 'X')

```yaml
profiling:
  tables:
    MARA:
      filter_preset: auto_active
```

**Scenario 2: MARC (Plant-specific material data)**
- Has LOEKZ (deletion flag) AND MMSTA (plant-specific status)
- Status codes 01, 02, 03 = active; others = blocked
- **Use:** `custom` (standard auto_active won't filter by MMSTA)
- **Specification:**
```yaml
profiling:
  tables:
    MARC:
      filter_preset: custom
      where_filters:
        - LOEKZ <> 'X'         # deletion flag
        - MMSTA IN ('01','02','03')  # active status
```

**Scenario 3: ZCUSTOM_TABLE (Client-specific custom table)**
- No deletion flag (client never marks records deleted)
- Has a Z_STATUS field with custom meanings
- **Use:** `no_filter` (or custom if you know Z_STATUS codes)
- **If unsure:** Use `no_filter`; review the profiling output, then add filters

```yaml
profiling:
  tables:
    ZCUSTOM_TABLE:
      filter_preset: no_filter  # See all records, then decide what to filter
```

**Scenario 4: KNA1 (Customer masters)**
- Standard deletion (LOEVM) exists
- Also has PSTAT (account status) with client-specific codes
- **Use:** `custom` (combine auto_active's LOEVM with custom PSTAT logic)

```yaml
profiling:
  tables:
    KNA1:
      filter_preset: custom
      where_filters:
        - LOEVM <> 'X'         # Standard SAP deletion
        - PSTAT IS NULL        # Fully set up (not in setup/approval)
```

### Decision tree

```
Do you know the table's deletion flag strategy?

├─ YES, it's standard SAP (LVORM, LOEKZ, LOEVM)
│  └─ Does it also have status codes (MMSTA, PSTAT) I need to filter?
│     ├─ NO → Use auto_active
│     └─ YES → Use custom (deletion flag + status codes)
│
└─ NO, or it's custom (Z-fields, no deletion flag)
   └─ Use no_filter; review output; add filters in next run if needed
```

> [!tip]
> **Start conservative:** auto_active or no_filter first. Once you see the data, 
> tighten with custom filters. Don't over-specify before you understand the data.
