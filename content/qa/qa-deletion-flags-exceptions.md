---
id: qa-deletion-flags-exceptions
type: qa
title: Are there exceptions to "deleted records not in universe"?
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: review
sources:
  - coe:feedback-2026-09-07
created: 2026-09-07
updated: 2026-09-07
---

## Question

The principle states "A deleted record is not in the universe the rule applies to." 
Are there any commonly accepted exceptions to this, besides explicit deletion-detection rules?

## Answer

**One exception: audit/compliance rules where deletion history is the data.**

### Standard rule (no deleted records)

```sql
WHERE LVORM <> 'X'  -- Exclude deleted from universe
CASE WHEN <error> THEN 1 ELSE 0 END
```

Active records only. Deleted records don't exist as far as this rule is concerned.

### Exception: Audit trail rules

Some rules exist specifically to track deletions for compliance:

> *"All materials deleted in the last 90 days must have a documented reason (LOEKZ_REASON field populated)"*

Here, **deleted records ARE the universe**:

```sql
WHERE LVORM = 'X'   -- Universe is ONLY deleted records
  AND DATEDIFF(DAY, LOEDT, GETDATE()) <= 90
CASE WHEN LOEKZ_REASON IS NULL THEN 1 ELSE 0 END AS [zIsErrorFlag]
```

**Why?** The rule's purpose is to audit deletion records, not to validate active records.

### Another framing: "Tombstone" records

In some systems, deleted records aren't purged — they're marked with a deletion flag and kept 
for audit/reversion purposes. A rule checking tombstone records isn't an exception to the 
principle; it's applying the principle correctly: **the universe for this rule is "deleted records."**

### The line

**Not an exception:**
- A rule that checks active records but *also* counts deleted records to inflate/deflate the defect rate
- This violates the principle. The universe should exclude deleted records.

**Is an exception:**
- A rule whose **explicit purpose** is to audit, verify, or report on deleted records
- Here, the deletion flag becomes a universe-definition filter (not an error condition)

> [!tip]
> Exceptions are rare and intentional. If you're writing a rule and thinking "maybe I should include deleted records," ask yourself: "Is deletion itself what I'm auditing?" If no, exclude them from WHERE.
