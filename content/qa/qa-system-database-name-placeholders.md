---
id: qa-system-database-name-placeholders
type: qa
title: What are {{SYSTEM}} and {{DATABASE_NAME}} placeholders?
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

Could we briefly explain what {{SYSTEM}} and {{DATABASE_NAME}} represent and why placeholders are used instead of actual values in the examples?

## Answer

**Template tokens that are substituted once per system during deployment** — allowing one authored rule to fan out into per-system implementations.

| Placeholder | What it is | Example substitution |
|---|---|---|
| `{{SYSTEM}}` | The system code to be deployed to | `SRCECCZ02`, `SRCS4SG2`, `P06` |
| `{{DATABASE_NAME}}` | The target working database | `WRKDQ`, `WRKDQ_PROD`, `working_db` |

**Why placeholders instead of hardcoded values:**

A rule lives in the **repository as a template**, not a deployable artifact. When you author a rule, you don't know which systems it will eventually fan out to. So you use placeholders:

```sql
-- Template form (in repository)
CREATE VIEW [{{DATABASE_NAME}}].[dbo].[DQ_0042_{{SYSTEM}}_MARA_MEINS_OptSel] AS
SELECT
  MARA.zSourceSystemID,
  ...
FROM [{{DATABASE_NAME}}].[dbo].[MARA] AS MARA
WHERE MARA.zSourceSystemID = '{{SYSTEM}}'
```

**During deployment, the generator substitutes:**

```sql
-- Deployed to Z02 (first system)
CREATE VIEW [WRKDQ].[dbo].[DQ_0042_SRCECCZ02_MARA_MEINS_OptSel] AS
SELECT
  MARA.zSourceSystemID,
  ...
FROM [WRKDQ].[dbo].[MARA] AS MARA
WHERE MARA.zSourceSystemID = 'SRCECCZ02'

-- Deployed to Z06 (second system)
CREATE VIEW [WRKDQ].[dbo].[DQ_0042_SRCECCZ06_MARA_MEINS_OptSel] AS
SELECT
  MARA.zSourceSystemID,
  ...
FROM [WRKDQ].[dbo].[MARA] AS MARA
WHERE MARA.zSourceSystemID = 'SRCECCZ06'

-- Deployed to Z09 (third system)
CREATE VIEW [WRKDQ].[dbo].[DQ_0042_SRCECCZ09_MARA_MEINS_OptSel] AS
SELECT
  MARA.zSourceSystemID,
  ...
FROM [WRKDQ].[dbo].[MARA] AS MARA
WHERE MARA.zSourceSystemID = 'SRCECCZ09'
```

**Same rule logic, different system IDs — one template generates three views.**

**Why not hardcode?**

If you wrote:
```sql
CREATE VIEW [WRKDQ].[dbo].[DQ_0042_SRCECCZ02_MARA_MEINS_OptSel] AS
...
WHERE MARA.zSourceSystemID = 'SRCECCZ02'
```

Then deploying to Z06 would be wrong — the view would still filter to Z02 only. Placeholders make the template portable: one rule → many systems → same logic, right filters.

## Related

- [[std-view-naming-patterns|View Naming Patterns]]
- [[con-multi-implementation-model|Multi-Implementation Model]]
