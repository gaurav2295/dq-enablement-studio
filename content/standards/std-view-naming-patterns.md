---
id: std-view-naming-patterns
type: standard
title: View Naming Patterns
domain: sql-standards
audience: [consultant, developer]
level: practitioner
status: approved
sources:
  - vault:dq-methodology/View Naming Patterns.md
  - dq-studio:.claude/skills_canonical/studio-naming-rules.md
  - dq-studio:docs/DQ_RULE_STANDARDS.md
  - dq-studio:knowledge/methodology/view_conventions.json
tags: [methodology, convention, studio, sap, syniti-dq-emea-methodology]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:con-view-types
  - relates:ref-system-aliases-map
  - relates:con-multi-implementation-model
  - relates:con-data-architecture-layers
  - relates:std-studio-config-shape
  - relates:std-optsel-select-structure
---

## What it is

Every view the Studio generates is a token template
(`DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}`) resolved by plain substitution — the Studio
ships one canonical default pattern set.

Patterns are declared per-project in the `naming:` block of the project YAML. When no YAML
override is present, defaults apply — and every generation path is aligned to the same default set
(see **Implementation reality** below).

## The base standard

The human-authored **DQ Rule Standards** state the format every view name must follow:

```
DQ_[RuleNumber]_[ObjectName]_[Description]_[Suffix]
```

```sql
DQ_0001_MARA_MAT_NOT_EXTENDED_MARC_OptSel
DQ_0001_MARA_MAT_NOT_EXTENDED_MARC_RptSel

DQ_0002_KNA1_CUSTOMER_NO_SALES_AREA_OptSel
DQ_0002_KNA1_CUSTOMER_NO_SALES_AREA_RptSel
```

| Element | Requirement |
|---|---|
| **RuleNumber** | Four digits · zero-padded · sequential · starts at `0001` |
| **ObjectName** | Must represent the **primary SAP table** being validated (e.g. `MARA`, `KNA1`) |
| **Description** | Must be meaningful, concise and business-friendly |
| **Suffix** | `OptSel` (Opportunity View) or `RptSel` (Report View) |

Every **Error** rule produces exactly two views under this format — one `_OptSel`, one `_RptSel` —
so the pair is discoverable from the rule number alone. The standards doc predates the Info and
Profiling model and is silent on the other three suffixes; those follow the same token grammar with
their own view-type tags (see [[con-view-types|View Types]]).

> [!warning] Two live token orders — see CONFLICT-011
> The standards doc places the system token **immediately before the suffix**
> (`DQ_[####]_[Object]_[Description]_{{SYSTEM}}_OptSel`, §3.5); the Studio resolver places it
> **directly after the rule id** (`DQ_{id}_{system}_{table}_{field}_{desc}_OptSel`). Both are in
> production on different generation paths. Do not "fix" one to match the other on a live
> engagement — the parser, the validator's rule-id routing and SKP's query columns all key off
> whichever order that project already deployed.

## The canonical patterns

```yaml
naming:
  optsel_view: DQ_{id}_{system}_{table}_{field}_{desc}_OptSel
  rptsel_view: DQ_{id}_{system}_{table}_{field}_{desc}_RptSel
  infsel_view: DQ_{id}_{system}_{table}_{field}_{desc}_InfSel
  prfsel_view: DQ_{id}_{table}_{field}_PrfSel      # NO {system}, NO {desc}
  prfsum_view: DQ_{id}_{table}_{field}_PrfSum      # NO {system}, NO {desc}
  filter_view: '{system}_{table}_FILT'
  bridge_view: '{table}'
```

> [!note] Canonical target
> The block above is the agreed canonical pattern set. Error/Info views (OptSel/RptSel/InfSel)
> carry `{system}`; profiling views (PrfSel/PrfSum) omit it by default. `{id}` is 4-digit
> zero-padded and MUST equal the `-- Rule ID:` banner (the parser and validator route on it).
> `{system}` is the **production** system ID / agreed alias (e.g. `PD1`) — never the interim QA
> system (e.g. `QA1`). Separator `_`; total name ≤128 (SQL Server). A project YAML may override,
> and the YAML resolver is the production path.

## Token meanings

| Token | Resolves to |
|---|---|
| `{id}` | DQOps rule ID, 4-digit zero-padded — e.g. `0042`; must equal the `-- Rule ID:` banner |
| `{system}` | System alias from `system_aliases` map — e.g. `P02`, `P06`, `PG3`; production ID, not QA |
| `{table}` | Primary table of the rule (uppercased) — e.g. `MARA`, `KNA1`, `CEPC` |
| `{field}` | Key field of the rule — e.g. `MEINS`, `KUNNR`, `PRCTR` |
| `{desc}` | ≤50-char Title_Case keyword slug — part of the canonical Error/Info pattern (see below) |
| `{ViewType}` | Literal suffix tag — `OptSel` / `RptSel` / `InfSel` / `PrfSel` / `PrfSum`, baked into the pattern string |

## Example resolutions

| Rule | Resolved name |
|---|---|
| Rule 0042 / P02 / MARA.MEINS OptSel | `DQ_0042_P02_MARA_MEINS_OptSel` |
| Rule 0042 / P02 / MARA.MEINS RptSel | `DQ_0042_P02_MARA_MEINS_RptSel` |
| Rule 0001 / CEPC.PRCTR PrfSel | `DQ_0001_CEPC_PRCTR_PrfSel` |
| Rule 0001 / CEPC.PRCTR PrfSum | `DQ_0001_CEPC_PRCTR_PrfSum` |

The Error/Info rows above are shown **without** the `{desc}` slug for readability; a real generated
name carries it — `DQ_0042_P02_MARA_MEINS_Valid_Base_Unit_Measure_OptSel`. Short-form names appear
in worked examples across this knowledge base for the same reason.

## Scenario: Reviewing a colleague's CTE for naming compliance

**The CTE they submitted:**

```sql
WITH material_orders AS (
  SELECT
    vbap.zSourceSystemID,
    vbap.MATNR,
    COUNT(*) AS order_count
  FROM [WRKDQ].[dbo].[VBAP] AS vbap
  WHERE vbap.zSourceSystemID = 'Z01'
  GROUP BY vbap.zSourceSystemID, vbap.MATNR
)
SELECT
  mara.zSourceSystemID,
  CONCAT(mara.zSourceSystemID, '_', mara.MATNR) AS zConcatenatedKey,
  CASE WHEN order_summary.MATNR IS NULL THEN 1 ELSE 0 END AS zIsErrorFlag,
  mara.MATNR,
  mara.MAKTX
FROM [WRKDQ].[dbo].[MARA] AS mara
LEFT JOIN material_orders
  ON mara.zSourceSystemID = material_orders.zSourceSystemID
  AND mara.MATNR = material_orders.MATNR
WHERE mara.zSourceSystemID = 'Z01'
```

**Questions to ask in review:**

1. ✅ **CTE is named clearly?** Yes — `material_orders` says what it calculates.
2. ✅ **CTE outputs `zSourceSystemID`?** Yes — it's in the SELECT.
3. ✅ **CTE filters on `zSourceSystemID`?** Yes — `WHERE vbap.zSourceSystemID = 'Z01'`.
4. ✅ **JOIN includes `zSourceSystemID` equality?** Yes — both ON conditions present.
5. ✅ **CTE is actually used?** Yes — it's joined in the outer query.
6. ⚠️ **System hardcoded as 'Z01'?** Yes — this is a **second review point**. For a per-system deployment, the 'Z01' should be a placeholder or parameter, not hardcoded.

**The verdict:** The CTE structure is correct. However, **watch for hardcoding** — if this rule fans out to Z02, Z06, the CTE's WHERE clause needs to be parameterized or the rule is unmigrable.

## End-to-end example: Rule name → View names

Starting with a rule authored in the Studio:

| Step | Input/Output |
|---|---|
| **1. Rule name** | *A material must have a valid base unit of measure* |
| **2. Rule ID** | `0042` (assigned by Studio) |
| **3. SAP table** | `MARA` (material master) |
| **4. Field** | `MEINS` (base unit of measure) |
| **5. System** | `P02` (production system alias) |
| **6. Desc slug (auto-derived)** | `Valid_Base_Unit_Measure` (from rule name via keyword extraction) |
| **7. OptSel view name** | `DQ_0042_P02_MARA_MEINS_Valid_Base_Unit_Measure_OptSel` |
| **8. RptSel view name** | `DQ_0042_P02_MARA_MEINS_Valid_Base_Unit_Measure_RptSel` |
| **9. OptSel SQL** | `CREATE VIEW DQ_0042_P02_MARA_MEINS_Valid_Base_Unit_Measure_OptSel AS SELECT ... FROM MARA WHERE zSourceSystemID = 'Z06' ...` |
| **10. RptSel SQL** | `CREATE VIEW DQ_0042_P02_MARA_MEINS_Valid_Base_Unit_Measure_RptSel AS SELECT * FROM DQ_0042_P02_MARA_MEINS_Valid_Base_Unit_Measure_OptSel WHERE zIsErrorFlag = 1` |

The **OptSel** (opportunity view) contains all candidates plus a flag; the **RptSel** filters to
defects only. Both view names are derived deterministically from the rule name, so reverse-routing
and rule-to-deployment mappings always work — the name is the contract.

## Why profiling omits {system}

Profiling rules are **cross-system aggregations** — they segment by `zSourceSystemID` rather than
filter by it. A per-system qualifier in the name would mislead reviewers into thinking the view
restricts to one system; it doesn't.

So `DQ_0001_CEPC_PRCTR_PrfSel` (no `{system}` slot) represents the entire cross-system
distribution. Compare with the Error counterpart `DQ_0042_P02_MARA_MEINS_OptSel`, where `_P02_`
makes the scope explicit.

## Implementation reality

Token substitution always considers all five tokens (`{id}`, `{system}`, `{table}`, `{field}`,
`{desc}`) but only fills in the ones literally present in a given pattern string — any token not
used in the pattern is simply skipped.

### One canonical default pattern set

Whether `{system}` appears in OptSel/RptSel/InfSel names is **consistent across every generation
path** — every path agrees `{system}` is present on Error/Info views, and every path agrees
profiling views (`prfsel_view`/`prfsum_view` = `DQ_{id}_{table}_{field}_Prf…`) and the filter view
(`{system}_{table}_FILT`) omit it.

So the same rule deploys under one consistent view name regardless of which path generated it.

> [!tip] Canonical rule
> Error/Info views include `{system}`; profiling views omit it. `{system}` resolves to the
> *production* ID / agreed alias (e.g. `PD1`), never the interim QA system (e.g. `QA1`). Name-based
> routing in the SQL parser and the validator's rule-id/view-name check both depend on this staying
> consistent.

### The literal suffix is baked, not generated

The view-type tag (`_OptSel`, `_RptSel`, `_InfSel`, `_PrfSel`, `_PrfSum`) is the literal text at
the end of each pattern string — mixed case, hard-coded into the pattern, not generated. The `DQ_`
prefix and `_` separator are likewise literal. Table names are uppercased, per SAP convention.

### {desc} is computed and appears in the canonical name

The Studio derives a ≤50-char Title_Case slug from the rule name (e.g. "A material must have a
valid base unit of measure" → `Valid_Base_Unit_Measure`) and uses it to fill `{desc}`. The
`{desc}` token is part of the canonical pattern — `DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}`
— so the slug reaches the view name.

> [!tip] Canonical rule
> The canonical view name includes `{desc}`, so the keyword slug reaches the view name. The slug
> length is capped and total name kept ≤128 while preserving name-stability for reverse-import
> routing. The `{desc}` slug, once assigned, is FIXED.

### How {desc} is derived — the keyword-extraction algorithm

The canonical specification converts a rule *name* into a view-name-safe *description* in nine
ordered steps:

1. Remove leading articles — `^(A|An|The|This)\s+`
2. Remove modal phrases — `must be`, `must have`, `must include`, `must contain`, `must equal`, `must match`, `must not …`
3. Remove auxiliary verbs — `shall`, `should`, `can`, `cannot`, `will`, `would`
4. Remove prepositions — `in`, `on`, `at`, `to`, `for`, `with`, `from`, `by`, `of`, `within`, `across`, `between`, `among`
5. Split into words and filter stop words
6. Take up to `max_words` significant words, each longer than `min_word_length` characters
7. Capitalize each word and join with the separator
8. Strip any non-word / non-underscore characters
9. Truncate to `max_chars`

| Parameter | Value |
|---|---|
| `max_words` | 6 |
| `min_word_length` | 3 |
| `max_chars` | 50 |
| `separator` | `_` |
| `capitalize` | true |
| `fallback` | `Rule_Description` |

Stop words: `a, an, the, and, or, but, is, are, was, were, be, been, being, in, on, at, to, for,
with, from, by, of, as, than`.

Worked example — "A material must have a valid base unit of measure" loses the article, the modal
`must have`, the preposition `of` and the stop words, leaving `Valid_Base_Unit_Measure`.

> [!important] The slug is fixed once assigned
> The `{desc}` slug is name-stable: reverse-import routing and the deployed view name both depend
> on it. Re-deriving a slug after deployment renames the view and orphans the SKP asset row.

### Naming elements and file names

| Element | Meaning | Example |
|---|---|---|
| `id` | DQOpsID — the unique rule identifier | `0001` |
| `table` | Primary SAP source table name | `MARA` |
| `field` | Target field being validated (from the logic entry or key field) | `MEINS` |
| `desc` | Shortened rule description from keyword extraction | `Valid_Base_Unit_Measure` |

SQL files are saved under the view name itself: `DQ_{id}_{table}_{field}_{desc}_OptSel.sql` and
`DQ_{id}_{table}_{field}_{desc}_RptSel.sql`.

## Template tokens — {{SYSTEM}} and {{DATABASE_NAME}}

A rule stored in the repository is a **template**, not a deployable artefact. Two double-brace
tokens are substituted per system by the generation tooling before deployment:

- `{{SYSTEM}}` — sits immediately before the `_OptSel` / `_RptSel` suffix in the view name, and is
  also the literal written into `zSourceSystemID`. Never hard-code a system name in either place.
- `{{DATABASE_NAME}}` — the target database the view is created in.

```sql
-- template form, as stored in the repository
CREATE VIEW DQ_0002_KNA1_CUSTOMER_NO_SALES_AREA_{{SYSTEM}}_OptSel AS
SELECT
    -- Syniti Technical Fields
    '{{SYSTEM}}' AS [zSourceSystemID],
    ...
FROM {{DATABASE_NAME}}.dbo.KNA1 AS KNA1
```

The raw template is **not deployed directly** — the generator substitutes both tokens once per
source system, which is how one authored rule fans out into a per-system implementation set. See
[[con-multi-implementation-model|Multi-Implementation Model]].

## Where the pattern resolves

Token substitution is **strict** — no fallback, no inference. If a project YAML changes `{table}`
to `{tbl}`, the substitution stops working until both sides agree.

## Per-project overrides

The default patterns above are sensible for Bacardi-style projects. Other engagements may
override — for example, prefixing with a tenant code:

```yaml
naming:
  optsel_view: BAC_DQ_{id}_{system}_{table}_{field}_OptSel
```

The Studio supports this transparently — patterns are loaded from the active project's YAML at
runtime.

## Filter and bridge views

`filter_view` and `bridge_view` are a different shape — they're not rule views but Layer-2 /
Layer-4 helpers in the [[con-data-architecture-layers|data flow]]. Default patterns:

- `filter_view`: `{system}_{table}_FILT` — per-system filtered view (e.g. `P02_MARA_FILT`)
- `bridge_view`: `{table}` — consolidated cross-system bridge

When you see a view called `WRKDQ.dbo.MARA` (no DQ prefix, no suffix) — that's a bridge view, not
raw SAP.

## Questions from consultants

- [[qa-system-token-fallback-logic|What problem does the {system} token fallback logic solve?]]
- [[qa-system-database-name-placeholders|What are {{SYSTEM}} and {{DATABASE_NAME}} placeholders?]]

## System Alias vs Source-System Code — when and why

These two are **different concepts**, stored in different places, serving different purposes:

| Aspect | System Alias | Source-System Code |
|---|---|---|
| **What it is** | Friendly name for display | The actual value stored in the data |
| **Example** | `P02`, `P06`, `PG3` | `SRCECCZ02100`, `SRCS4SG2100`, `Z06` |
| **Where it lives** | `system_aliases` map in project config | `zSourceSystemID` column in database tables |
| **Used in** | View **names** (display) | SQL **WHERE clauses** (filtering) |
| **Who reads it** | Consultants, dashboards, SKP | The database engine, the SQL |
| **Can it change?** | Yes, rename alias for reporting | No, renaming breaks all deployed views |

**Real example:**

```yaml
# Project YAML - system_aliases map
systems:
  - code: SRCECCZ02100
    alias: P02
    label: "Production ECC System"
  - code: SRCS4SG2100
    alias: P06
    label: "Production S/4 HANA"
```

**How they flow through a rule:**

```
Rule authored in Studio:
├─ Rule name: "A material must have valid UoM"
├─ System chosen: P02 (the alias)
│
Generated view name:
└─ DQ_0042_P02_MARA_MEINS_OptSel  ← uses the ALIAS (P02)
   
Generated SQL:
└─ WHERE MARA.zSourceSystemID = 'SRCECCZ02100'  ← uses the CODE
```

**Why both?**

1. **Alias makes names readable** — `DQ_0042_P02_…` is shorter and friendlier than `DQ_0042_SRCECCZ02100_…`
2. **Code makes SQL correct** — the database only recognizes `'SRCECCZ02100'`, not `'P02'`
3. **They're independent** — you can rename the alias for display without touching the deployed SQL (the code stays the same)

**Common mistakes:**

❌ Using the **alias in the WHERE clause:**
```sql
WHERE MARA.zSourceSystemID = 'P02'  -- WRONG: P02 doesn't exist in the data
```

✅ Using the **code in the WHERE clause:**
```sql
WHERE MARA.zSourceSystemID = 'SRCECCZ02100'  -- CORRECT
```

❌ Using the **code in the view name:**
```sql
CREATE VIEW DQ_0042_SRCECCZ02100_MARA_MEINS_OptSel  -- too long, not user-friendly
```

✅ Using the **alias in the view name:**
```sql
CREATE VIEW DQ_0042_P02_MARA_MEINS_OptSel  -- short, readable
```

## The {system} token value

The `{system}` token is resolved in order of preference: (1) an explicit friendly alias set on the
rule (e.g. `P06`); (2) the alias mapped from the implementation's system filter, falling through to
the raw code itself when unmapped; (3) a legacy source-system fallback; (4) the literal `"SYS"` so
the slot is never empty. A `Z06` implementation with an alias mapping `Z06 → P06` resolves to
`DQ_0042_P06_KNA1_…` instead of `DQ_0042_SRCECCZ06_…`. See
Studio — View Name Token Resolution and
[[ref-system-aliases-map|System Aliases Map]].

### The alias is for the name only — SQL semantics use the raw code

This is the rule the token resolver exists to keep straight, and the most commonly broken one:

- The **view name** carries the alias: `DQ_0042_P06_KNA1_…`
- The **WHERE clause** carries the raw `zSourceSystemID` code: `WHERE KNA1.zSourceSystemID = 'Z06'`

If you ever see `WHERE zSourceSystemID = 'P06'` in generated SQL, that is a defect — the alias is a
display map and no source system is actually stored under that value. The two never swap, which is
why a name and its filter cannot drift apart.

### Naming independence from fan-out scope

The alias map and the fan-out scope are independent (see
[[std-studio-config-shape|Project Config Shape]]):

- A deployed code with **no alias entry** → the view name uses the raw code, e.g. `…_SG3_…`.
- An alias entry for a code that is **not deployed** → dead decoration; it never produces a view.
- Editing an alias changes names and UI cells, never which systems get deployed to.

## Common bugs to avoid

- **Adding `{system}` to profiling patterns.** Removed deliberately; profiling views are
  cross-system aggregations and a system token in the name misleads reviewers about the scope.
- **Using the alias as the WHERE-clause value** (see above).
- **Hardcoding a view-name pattern instead of using the project YAML.** Patterns live in the
  project configuration, not in individual rules — change the YAML to change the pattern.
- **Treating `{system}` substitution as required.** If a pattern does not contain the token, it is
  simply skipped. That is by design, not a missed substitution.

## Related

- [[con-view-types|View Types — OptSel RptSel InfSel PrfSel PrfSum]]
- [[con-data-architecture-layers|Data Architecture Layers]]
- [[ref-system-aliases-map|System Aliases Map]]
- [[con-multi-implementation-model|Multi-Implementation Model]]
- Studio — View Name Token Resolution
- Studio — Architecture Context & Project YAMLs
- Studio — DQRuleSpec Data Model
- Studio — Layer-2/Layer-4 Datastore Views
- Studio — SQL Parser (reverse-engineer specs)
- [[std-optsel-select-structure|OptSel SELECT Structure]]
