---
id: qa-fan-out-zsourcesystemid-validation
type: qa
title: Does the Studio validate that zSourceSystemID filters match the alias mapping before deployment?
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
  - relates:std-zsourcesystemid-convention
  - relates:ref-system-aliases-map
  - relates:prc-audit-rule-quality
---

## Question

Does the Studio perform any validation to confirm that the generated zSourceSystemID filter matches the correct alias mapping before deployment?

## Answer

**No — validation is manual, not automated.** The Studio generates and applies the zSourceSystemID filter based on the project's `system_aliases` configuration, but does not validate that:
1. The generated code actually exists in your target database
2. The code matches your data values
3. The filter is syntactically correct for your specific SAP environment

### What the Studio Does (Automatic)

When you fan-out a rule across systems:

1. ✅ **Reads** the `system_aliases` from project YAML (e.g., `SRCECCZ03100: P03`)
2. ✅ **Generates** the filter literal for each sibling (e.g., `zSourceSystemID = 'SRCECCZ03100'`)
3. ✅ **Inserts** it into the sibling's WHERE clause and join conditions

### What the Studio Does NOT Do (Manual Verification Required)

1. ❌ **Does not check** if `'SRCECCZ03100'` exists in your WRKDQ database
2. ❌ **Does not validate** the code against actual data values
3. ❌ **Does not verify** that the alias map is complete for all target systems
4. ❌ **Does not warn** if you accidentally use an alias (e.g., `'P03'`) instead of a code (e.g., `'SRCECCZ03100'`)

### Critical Pitfall

The most common mistake is **using the alias instead of the source-system code:**

```sql
-- ❌ WRONG — If WRKDQ stores 'SRCECCZ03100', this will return zero rows
WHERE zSourceSystemID = 'P03'

-- ✅ CORRECT — Matches actual data in WRKDQ
WHERE zSourceSystemID = 'SRCECCZ03100'
```

**This can be silently wrong** — the query will execute without errors, but return no defects because no records match the filter.

### Required Manual Validation

After fan-out, before bulk deployment:

1. **Verify the alias map is complete**
   ```yaml
   system_aliases:
     SRCECCZ02100: P02  ✅
     SRCECCZ03100: P03  ✅
     SRCECCZ06100: P06  ✅
     # Any missing systems?
   ```

2. **Check each sibling's filter matches the map**
   - Open each sibling's spec markdown
   - Confirm: `zSourceSystemID = 'SRCECCZ03100'` (matches P03 in alias map)
   - Not: `zSourceSystemID = 'P03'` (using the alias, not the code)

3. **Query your database to verify the code exists**
   ```sql
   SELECT DISTINCT zSourceSystemID 
   FROM [WRKDQ].[dbo].[MARA]
   ```
   
   The result should include:
   - `SRCECCZ02100` ✅
   - `SRCECCZ03100` ✅
   - `SRCECCZ06100` ✅
   - (whatever codes are in your actual data)

4. **Test one sibling before bulk deployment**
   - Deploy just P03's rule and run it
   - Verify it finds defects (not zero rows)
   - Verify the defects are from system P03's data only

### Why Manual, Not Automated?

The alias map is **project-specific metadata** — the Studio can enforce format but cannot validate business meaning:

- **The alias map could be wrong** — if your config says P03 = SRCECCZ03100 but your data actually uses SRCECCZ03200, the Studio cannot know which is correct
- **Different environments have different codes** — DEV might use Z02100, PROD might use Z02500; the Studio cannot validate across environments
- **Cross-system contamination is silent** — if the code is wrong, the query returns zero rows (not an error), so only testing would catch it

**Better to make it visible and manual:** You review before deployment, not relying on a gate that might give false confidence.

### Related

- [[prc-fan-out-a-rule-per-system|Fan Out a Rule Per System]]
- [[std-zsourcesystemid-convention|zSourceSystemID Convention]]
- [[ref-system-aliases-map|System Aliases Map]]
- [[prc-audit-rule-quality|Audit Rule Quality]]
