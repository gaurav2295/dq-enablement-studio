---
id: qa-profiling-rules-five-section-structure
type: qa
title: Does the five-section structure apply to profiling rules?
domain: sql-standards
audience: [consultant, developer]
level: foundation
status: review
sources:
  - coe:changeset-6-sql-best-practices
created: 2026-09-02
updated: 2026-09-02
links:
  - relates:std-output-field-sections
  - relates:con-rule-types
---

## Question

Does the five-section structure apply equally to profiling rules, or is it specific to Error/Info (opportunity) rules?

## Answer

**No — the five-section structure is for Error/Info rules only.** Profiling rules have a different output structure.

**Error/Info rules (OptSel/RptSel/InfSel):**
```sql
SELECT
    -- Syniti Technical Fields
    table.zSourceSystemID, ...
    -- Basic Fields
    ...
    -- Organizational Context
    ...
    -- Value Context
    ...
    -- Activity Context
    ...
```

**Profiling rules (PrfSel/PrfSum):**
```sql
-- PrfSel: record-level detail
SELECT
    [zSourceSystemID],
    [Segmentation Field],
    [Profiled Value],
    COUNT(*) AS [Occurrences]
FROM ...
GROUP BY [zSourceSystemID], [Segmentation Field], [Profiled Value]

-- PrfSum: aggregated summary
SELECT
    [zSourceSystemID],
    [Profiled Value],
    COUNT(*) AS [Occurrences],
    CAST(100.0 * COUNT(*) / ... AS DECIMAL(5,1)) AS [Percentage]
FROM ...
GROUP BY [zSourceSystemID], [Profiled Value]
```

Profiling views **do not** use the five-section comment structure because:
- They have no `zIsErrorFlag` (no error concept)
- They segment by value, not organize by context
- The output is "what values exist" and "what % each", not "which record is defective and why"

**Exception:** If a profiling rule happens to include organizational or activity context fields (rare), you can add those sections. But the five-section pattern is **Error/Info only**.

## Related

- [[std-output-field-sections|Output Field Sections]]
- [[con-rule-types|Rule Types — Error, Info, Profiling]]
