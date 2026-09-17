---
id: gls-rule-pattern
type: glossary
title: Rule Pattern
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:std-rule-pattern-library
  - relates:ref-local-deriver
  - relates:gls-correlated-subquery
sources:
  - dq-studio:docs/RULE_PATTERNS.md
  - dq-studio:knowledge/methodology/rule_patterns.json
tags: [rule-pattern, derivation]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

A parameterised **rule shape** the standard keyword-based derivation cannot express — one that
needs a [[gls-correlated-subquery|correlated subquery]] or a curated knowledge-base lookup rather
than "does this row's own field satisfy a condition".

## The Four Patterns

| Pattern | Question | SQL Shape | Example |
|---|---|---|---|
| **Hierarchy Membership** | Does the parent exist? | `EXISTS (SELECT 1 FROM parent WHERE ...)` | Material → Plant, Customer → Company Code |
| **Partner Cardinality** | Are there enough related rows? | `COUNT(...) OVER (...) >= threshold` | Order → Order Lines, Vendor → Purchase Orders |
| **Org-to-Central Parity** | Do org values match the central record? | `WHERE org_value <> central_value` | Plant Material attrs vs. Central MARA |
| **Status-Field Check** | Is the status valid for this state? | `CASE WHEN status NOT IN (...) THEN 1` | Material locked status, Vendor approval status |

## Concrete Examples

### Pattern 1: Hierarchy Membership
```sql
-- Question: Does every material have a valid plant assignment?
-- SQL: EXISTS to check parent
SELECT MaterialID, Plant, zSourceSystemID,
  CASE
    WHEN NOT EXISTS (
      SELECT 1 FROM WERKS_Stage W
      WHERE W.Plant = MARC.Plant
        AND W.zSourceSystemID = MARC.zSourceSystemID
    ) THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM MARC_Stage MARC;
```

### Pattern 2: Partner Cardinality
```sql
-- Question: Does every order have at least one line item?
-- SQL: COUNT check on related rows
SELECT OrderID, zSourceSystemID,
  CASE
    WHEN (SELECT COUNT(*) FROM OrderLines OL
          WHERE OL.OrderID = O.OrderID
            AND OL.zSourceSystemID = O.zSourceSystemID) = 0 THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM Orders O;
```

### Pattern 3: Org-to-Central Parity
```sql
-- Question: Do plant-level material attributes match central master?
-- SQL: Compare org record against central
SELECT MARC.MaterialID, MARC.Plant, MARC.zSourceSystemID,
  CASE
    WHEN MARC.UnitOfMeasure <> MARA.BaseUnitOfMeasure THEN 1
    ELSE 0
  END AS zIsErrorFlag
FROM MARC_Stage MARC
JOIN MARA_Stage MARA
  ON MARC.MaterialID = MARA.MaterialID
  AND MARC.zSourceSystemID = MARA.zSourceSystemID;
```

### Pattern 4: Status-Field Check
```sql
-- Question: Is the material status valid?
-- SQL: Domain value check (often a CASE)
SELECT MaterialID, Status, zSourceSystemID,
  CASE
    WHEN Status NOT IN ('A', 'B', 'D') THEN 1  -- Active, Blocked, Deleted only
    ELSE 0
  END AS zIsErrorFlag
FROM MARA_Stage;
```

## Usage

Every pattern flows through the same steps: 
1. **Detect intent** from the rule name (keyword regex)
2. **Fill slots** from the knowledge base (parent table, cardinality threshold, etc.)
3. **Build output fields** (identity, context, activity, value sections)
4. **Build the SQL** (correlated subquery or domain check)

Downstream, a pattern-derived spec is **indistinguishable** from a keyword-matched one — it goes
through the same export, validation and audit process as every other rule.
