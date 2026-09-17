---
id: qa-attribute-skipped-table-remediation
type: qa
title: When a table is skipped, what's recorded and how do you remediate?
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

When the attribute usage analysis skips a table (no spec, no knowledge file, no profile results), 
what information is recorded in the manifest, and what's the remediation path?

## Answer

**Skipped tables are logged with a clear reason. Remediation depends on which source is missing.**

### What gets recorded in the manifest

When a table is skipped, the manifest entry looks like:

```json
{
  "table": "ZCUSTOM_TABLE",
  "status": "SKIPPED",
  "reason": "no_spec_and_no_knowledge_and_no_profile",
  "available_sources": {
    "spec_file": false,
    "knowledge_file": false,
    "profile_results": false
  },
  "skip_timestamp": "2026-09-07T08:00:00Z",
  "remediation": "See recommendations below"
}
```

### Why tables are skipped

**Scenario 1: No spec file**
- No `.xlsx` spec defining attributes for this table
- **Remediation:** Create a spec file listing attributes you need

**Scenario 2: No knowledge file entry**
- Spec file exists but doesn't list this table
- **Remediation:** Add table to the knowledge file

**Scenario 3: No profile results**
- Spec and knowledge exist but the table wasn't profiled
- **Remediation:** Run the profiler and upload results

**Scenario 4: All three missing**
- Most common for new/custom tables
- **Remediation:** Do all three (spec → knowledge → profile)

### The remediation workflow

```
Table is skipped
    ↓
Check the manifest "reason" field
    ├─ no_spec → Create spec file (xlsx)
    ├─ no_knowledge → Add table to knowledge file
    ├─ no_profile → Run profiler, upload results
    └─ no_spec_and_no_knowledge_and_no_profile → Do all three
    ↓
Re-run attribute usage analysis
    ↓
Table is now included (if spec has attributes, knowledge has entry, profile has results)
```

### Typical fix timeline

**Quick fix (1 day):** Table is already profiled; just add spec + knowledge
**Medium fix (2–3 days):** Need to profile the table first
**Slow fix (1+ week):** Need to meet with client to understand attributes, then profile

### Avoiding skips upfront

**In the project kickoff:**
- Identify all tables needing attributes (spec)
- Map them to the knowledge base (knowledge file)
- Schedule profiling for all of them (profile run)

**Result:** No skipped tables when you run attribute analysis.

> [!tip]
> Skipped tables are a sign that something is incomplete in your pre-work. 
> Don't ignore them; fix the root cause (missing spec, knowledge, or profile).
