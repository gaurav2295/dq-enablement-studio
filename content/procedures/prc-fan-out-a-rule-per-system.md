---
id: prc-fan-out-a-rule-per-system
type: procedure
title: Fan Out a Rule Per System
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:sops/SOP — Fan Out a Rule Per System.md
tags: [sop]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:con-multi-implementation-model
  - relates:ref-system-aliases-map
  - relates:std-skp-rule-identifier-convention
  - relates:prc-audit-rule-quality
  - relates:prc-run-the-bulk-pipeline
  - relates:std-view-naming-patterns
  - relates:std-zsourcesystemid-convention
  - relates:qa-fan-out-lead-spec-determination
  - relates:qa-fan-out-zsourcesystemid-validation
---

## Goal

How to take one conceptual rule and produce N per-system implementations (e.g. P02, P03, P06,
PG3) that all share an SKP_RULE_NNNN but each carry their own DQOps `rule_id`, view names, and
`zSourceSystemID` inclusion filter.

## When to use

- After authoring a fresh rule that needs to deploy to multiple systems
- After importing a catalog rule that hasn't been fanned out yet
- After amending an existing rule on the lead system — siblings need to be re-derived from the
  changes

## Prerequisites

- Project YAML with `system_aliases` correctly populated for every target system
- The lead spec saved in the bulk session
- An SKP_RULE_NNNN already assigned (or you're letting auto-counter assign one)

## Steps

### 1. Pick the lead spec

In the `/workspace` page, identify which row is the **lead** (typically the first per-system
implementation, e.g. P02). The lead's spec is what gets cloned to siblings.

**Lead Rule → Siblings Relationship:**

```
LEAD RULE (P02):
├─ SKP_RULE_NNNN: SKP_RULE_0089          (shared across all siblings)
├─ DQOps ID: 0001                        (lead's unique ID)
├─ zSourceSystemID: 'SRCECCZ02100'
├─ View: DQ_0001_P02_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_OptSel
└─ View: DQ_0001_P02_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_RptSel

          │ (Fan-out clones the spec 3 times)
          ├─ SIBLING 1 (P03)
          │  ├─ SKP_RULE_NNNN: SKP_RULE_0089          (same as lead)
          │  ├─ DQOps ID: 0002                        (new ID per system)
          │  ├─ zSourceSystemID: 'SRCECCZ03100'       (different system code)
          │  ├─ View: DQ_0002_P03_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_OptSel
          │  └─ View: DQ_0002_P03_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_RptSel
          │
          ├─ SIBLING 2 (P06)
          │  ├─ SKP_RULE_NNNN: SKP_RULE_0089          (same as lead)
          │  ├─ DQOps ID: 0003                        (new ID per system)
          │  ├─ zSourceSystemID: 'SRCECCZ06100'       (different system code)
          │  ├─ View: DQ_0003_P06_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_OptSel
          │  └─ View: DQ_0003_P06_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_RptSel
          │
          └─ SIBLING 3 (PG3)
             ├─ SKP_RULE_NNNN: SKP_RULE_0089          (same as lead)
             ├─ DQOps ID: 0004                        (new ID per system)
             ├─ zSourceSystemID: 'SRCS4SG2100'        (different system code)
             ├─ View: DQ_0004_PG3_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_OptSel
             └─ View: DQ_0004_PG3_MARA_ACTIVITY_DATE_Material_Activity_Last_Two_Years_RptSel
```

**Key Points:**
- ✅ **All siblings share the same SKP_RULE_NNNN** — they're logically one rule across systems
- ✅ **Each sibling gets a unique DQOps ID** — for deployment and audit tracking per system
- ✅ **View names include the system alias** — DQ_000X_P02_, DQ_000X_P03_, etc.
- ✅ **zSourceSystemID filter differs** — constrains each sibling to its own system's data

### 2. Identify the sibling systems

From the project YAML's `system_aliases`:

```yaml
SRCECCZ02100: P02
SRCECCZ03100: P03
SRCECCZ06100: P06
SRCS4SG2100:  PG3
```

Siblings = every alias key except the lead's.

### 3. For each sibling system

The Studio's bulk pipeline does this automatically when:

- **Two tracker rows share a ClientRef** — automatic fan-out during bulk run
- **OR you click "AI: Replicate from Sibling"** — manual replication of a single sibling

**When to use each approach:**

| Approach | When to Use | How |
|----------|---|---|
| **Shared ClientRef** | Bulk pipeline run (multiple rules at once) | Tracker has same SKP_RULE_ID on rows for P02, P03, P06, PG3 → Bulk pipeline auto-fans them out |
| **"AI: Replicate from Sibling"** | Need to replicate one sibling in the single-rule designer | Click button on the sibling row in workspace → Studio clones from lead, updates system filter + view names |
| **After new system added** | A system was added to the project after initial fan-out | Re-derive the entire rule; the new system will be included automatically |

For each sibling, the Studio clones the lead spec, sets the sibling's `zSourceSystemID` filter
and alias, assigns a new DQOps `rule_id`, and re-resolves the view names using the
[[std-view-naming-patterns|View Naming Patterns]].

**Detecting fan-out issues early:** Don't wait until bulk pipeline reconciliation to find missing siblings. Before running bulk:
- Check the tracker: do you have rows for all systems in `system_aliases`?
- Open the lead rule in the designer: does the config show all expected systems?
- If a system is in the alias map but no tracker row exists, add it manually before bulk run — it's faster than fixing after reconciliation

### 4. Verify each sibling

Open each sibling's spec markdown. Confirm:

- Rule Identity table: same SKP_RULE_NNNN as the lead, **different** DQOps ID
- View names: `_P03_` (or whichever alias) in the slot, not `_P02_`
- Filter literal: `zSourceSystemID = 'SRCECCZ03100'`
- WHERE comment: `Limit to source system P03` — matches the literal, NOT lingering as `P02`
  (a known stale-comment issue; see [[prc-audit-rule-quality|Audit Rule Quality]])

### 5. (Optional) Repair stale-comment SQL

If you're loading already-generated SQL and find sibling WHERE comments lying about the system
(lead's label leaked across), see [[prc-audit-rule-quality|Audit Rule Quality]] for the repair
flow.

## Verification

- Bulk reconciliation Excel shows N rows per ClientRef (one per system)
- Each row has a distinct DQOps ID
- Each row's view name slot carries the correct alias
- Each row's `zSourceSystemID = '<code>'` literal matches the alias map

## Common pitfalls

- **Alias map missing a system** — siblings for that system never get generated. Add to
  `system_aliases` and re-fan-out
- **Sibling-replicate shows stale comment labels** — if your Studio session is out of date,
  refresh the browser so the fix is loaded
- **Filter literal is alias instead of source code** — `zSourceSystemID = 'P02'` will return
  zero rows if WRKDQ stores `SRCECCZ02100`. Always check the actual data values once before
  bulk fan-out. See [[qa-fan-out-zsourcesystemid-validation|Does the Studio validate zSourceSystemID filters?]] for required manual validation steps

## Related

- [[con-multi-implementation-model|Multi-Implementation Model]]
- [[ref-system-aliases-map|System Aliases Map]]
- [[std-skp-rule-identifier-convention|SKP_RULE Identifier Convention]]
- [[prc-run-the-bulk-pipeline|Run the Bulk Pipeline]]
- Studio — Multi-Impl Fan-out Engine
