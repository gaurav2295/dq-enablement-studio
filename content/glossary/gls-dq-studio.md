---
id: gls-dq-studio
type: glossary
title: dq-studio
domain: studio
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-vector-studio
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, instruments, studio]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The application that generates rules, SQL and the engagement kit from the imported spec.**

**It owns the only iteration loop.**

One application, two names: the repository is `syniti-methodology-studio`, while the estate and
this knowledge base call the working clone **dq-studio**. Both name the same thing — the
DQ Studio.

## Core Functions

| Function | Input | Output | Related Term |
|---|---|---|---|
| **Derive Rules** | [[gls-project-spec\|Project spec]] | [[gls-optsel\|OptSel]] + [[gls-rptsel\|RptSel]] SQL views | [[prc-derive-a-dq-rule]] |
| **Derive Profiles** | Profiling config | [[gls-prfsel\|PrfSel]] + [[gls-prfsum\|PrfSum]] views | [[con-profiling-concepts]] |
| **Generate Engagement Kit** | Rules + metadata | HTML5 interactive app | [[gls-engagement-kit]] |
| **AI Enhance** | Base rule + AI config | Enhanced rule SQL + suggestions | [[gls-ai-enhance]] |
| **Fan Out** | One rule | N implementations per system | [[gls-fan-out]], [[gls-system-alias]] |
| **Bulk Processor** | CSV rules | Batch derive all rules | [[prc-run-the-bulk-pipeline]] |
| **Audit Engine** | Rules + execution results | Validation report + reconciliation | [[prc-audit-rule-quality]] |

## Key Options & Workflow

### 1. **Rule Authoring Mode**
- **Manual SQL**: Write OptSel/RptSel directly in rule YAML
- **Pattern Library** ([[gls-rule-pattern]]): Pick from standard patterns (completeness, conformity, etc.)
- **AI-Assisted** ([[gls-ai-enhance]]): Let AI generate initial SQL + enhancements
- **Template** ([[std-view-naming-patterns]]): Use system/segment templates

### 2. **Profiling Configuration**
- **Grain**: Choose record-level (PrfSel) or aggregated (PrfSum)
- **Segmentation**: Define how to slice the universe (by plant, by material type)
- **Top-N Analysis**: Distribution counting with occurrence thresholds

### 3. **Multi-System Scope**
- **System Aliases** ([[gls-system-alias]]): Map real codes to view name tokens (SAP → P02, LEGACY → P01)
- **Fan-Out Behavior** ([[gls-fan-out]]): One rule → N implementations (one per system)
- **Profiling Exception**: Profiling rules do NOT fan out; systems become `IN (...)` filter instead

### 4. **Output Field Sections** ([[std-output-field-sections]])
The Studio enforces 5-section structure in every rule:
1. **Identity** ([[gls-basic-fields]]): Who/what is this? (primary key)
2. **Classification** ([[gls-field-classification]]): Type, category, status
3. **Organizational Context** ([[gls-organizational-context]]): BUKRS, WERKS, VKORG (where in org)
4. **Value Context** ([[gls-value-context]]): Monetary amounts, prices, quantities (how much)
5. **Activity Context** ([[gls-activity-context]]): Dates, timestamps, frequency (when)

### 5. **Technical Fields** (Auto-inserted by Studio)
- `zSourceSystemID`: Which system this record came from
- `zConcatenatedKey`: Multi-system unique key
- `zDQOpsID`: Deployment identifier in DQOps
- `zRuleName`: The rule's canonical name
- `zIsErrorFlag`: 0 = pass, 1 = defect (Error rules only)
- `[Implication]`: Business consequence (Info rules only)

### 6. **Validation & Quality Gates**
- **Save Validation**: Syntax, wikilinks, frontmatter, naming conventions
- **Build Validation**: Cross-references, section structure, field cardinality
- **AI Validator** ([[ref-ai-static-validator-gate]]): Logic quality, performance risk, best practices
- **Audit** ([[prc-audit-rule-quality]]): Reconciliation after execution

### 7. **Iteration Loop**
```
1. Import spec → Canvas or YAML
2. Derive rules (Studio)
   ├─ Pick pattern or write SQL
   ├─ Configure fan-out
   └─ Generate OptSel/RptSel
3. Generate views + engagement kit
4. Review (audit engine + manual)
5. Fix issues in YAML
6. Re-derive (loop to step 2)
```

## Usage in the Ecosystem

In the instrument chain dq-studio sits in the middle: 
- **Input from:** [[gls-bob-canvas]] (project spec)
- **Processing:** Derives rules, SQL, engagement kit
- **Output to:** [[gls-vector-studio]] (blueprint deployment)

"Owns the only iteration loop" is the load-bearing clause. Refinement — re-derive, review, fix,
re-derive — happens **here and nowhere else**. The canvas does not iterate rules and
vector-studio does not author them; if a change is needed, it is made in the Studio and flows
outward again.

> [!warning]
> `dq-studio` is an internal tool name and does not appear in a client room. It is also **not**
> the offering — the offering is `#bob-dq`; see [[gls-bob-dq]].
