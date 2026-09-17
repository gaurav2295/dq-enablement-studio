# Feedback Summary — DQ Enablement Studio
**Period:** August 26–27, 2026  
**Total feedback items:** 34  
**Reviewed by:** 4 people

---

## Feedback by Reviewer

| Reviewer | Notes | Questions | Units Touched | Total |
|----------|-------|-----------|----------------|-------|
| **Keshav** | 16 | 0 | 8 units | **16** |
| **Karatam Sai Venkata Durga Madhu** | 7 | 1 | 5 units | **8** |
| **Shruthi Gunne** | 2 | 5 | 4 units | **7** |
| **Chappavarapu Rajasekar Reddy** | 0 | 3 | 3 units | **3** |
| **TOTAL** | **25** | **9** | **14 unique units** | **34** |

---

## Feedback by Reviewer — Detailed Unit Breakdown

### Keshav (16 items across 8 units)
| Unit ID | Type | Count | Items |
|---------|------|-------|-------|
| `con-dq-dimensions` | Concept | 3 | Change capitalization, remove CONFLICT ref, add DAMA-DMBOK explanation |
| `con-view-types` | Concept | 1 | Need example for PrfSel ↔ PrfSum pair |
| `prn-fetch-check-return` | Principle | 2 | Fix bullet numbering (1,1,1→1,2,3), remove irrelevant HTML note |
| `prn-optsel-is-the-universe` | Principle | 1 | Fix bullet numbering (1,1,1→1,2,3) |
| `std-cte-rules` | Standard | 1 | Fix bullet numbering under CTE Rules |
| `std-sql-comment-standards` | Standard | 1 | Highlight material-specific table/field flags |
| `std-rule-name-heuristics` | Standard | 2 | Remove ref to docs, restructure Criteria section with pattern details |
| `prc-write-a-quality-rule-name` | Procedure | 2 | Remove CONFLICTS.md ref, fix step numbering |
| `std-output-field-sections` | Standard | 1 | Clarify conflict references |
| `std-optsel-select-structure` | Standard | 1 | Clarify checked field mapping |
| `prn-sql-comments-must-match-local-derive-quality` | Principle | 1 | Re-number bullet points (canonical rule section) |

### Karatam Sai Venkata Durga Madhu (8 items across 5 units)
| Unit ID | Type | Count | Items |
|---------|------|-------|-------|
| `con-what-is-data-quality` | Concept | 2 | Add sources for statistics, add real-life example |
| `prn-fetch-check-return` | Principle | 1 | Add before/after example (paragraph vs Fetch/Check/Return) |
| `prn-optsel-is-the-universe` | Principle | 1 | Add visual flow diagram (OptSel → RptSel) |
| `std-rule-name-heuristics` | Standard | 1 | "Criteria, Verbatim" section too technical and lengthy |
| `prc-write-a-quality-rule-name` | Procedure | 1 | Add comparison (checklist vs scorer output) |
| `std-view-naming-patterns` | Standard | 1 | Add end-to-end example (rule name → OptSel/RptSel) |
| `prn-sql-comments-must-match-local-derive-quality` | Principle | 1 | **Q:** Is commenting standard for DQ views only? |

### Shruthi Gunne (7 items across 4 units)
| Unit ID | Type | Count | Items |
|---------|------|-------|-------|
| `con-what-is-data-quality` | Concept | 2 | Add example for "Fitness", add context for acronyms (GDPR, HIPAA, SOX) |
| `con-dq-dimensions` | Concept | 4 | **Q:** Distinguish Accuracy vs Conformity (e.g., year 1905)? **Q:** Priority always Accuracy/Integrity? **Q:** Why Completeness more tolerable? **Q:** Why "consistent format" maps to Accuracy vs Conformity? |
| `notes` | Other | 1 | **Q:** Explain DAMA-DMBOK and relevance to DQ |

### Chappavarapu Rajasekar Reddy (3 items across 3 units)
| Unit ID | Type | Count | Items |
|---------|------|-------|-------|
| `con-view-types` | Concept | 2 | **Q:** Why PrfSel/PrfSum vs OptSel/RptSel for profiling? **Q:** Why InfSel vs RptSel for informational? |
| `con-dq-dimensions` | Concept | 1 | **Q:** What is DAMA-DMBOK and its role in DQ? |

---

## Feedback by Unit/Section

### Concepts (14 items across 3 units)

**con-what-is-data-quality** (4 items)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Karatam | 2 | Add sources for statistics; Add real-life example |
| Shruthi | 2 | Add example for "Fitness"; Add context for acronyms (GDPR, HIPAA, SOX) |

**con-dq-dimensions** (8 items)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 3 | Change "data current" → "Current data"; Remove CONFLICT-001 ref; Add DAMA-DMBOK explanation |
| Shruthi | 4 | **Q:** Accuracy vs Conformity distinction?; **Q:** Priority always Accuracy/Integrity?; **Q:** Why Completeness more tolerable?; **Q:** Why "consistent format" → Accuracy vs Conformity? |
| Chappavarapu | 1 | **Q:** What is DAMA-DMBOK and its role? |

**con-view-types** (2 items)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 1 | Need good example for "PrfSel ↔ PrfSum pair" |
| Chappavarapu | 2 | **Q:** Why PrfSel/PrfSum vs OptSel/RptSel?; **Q:** Why InfSel vs RptSel? |

---

### Principles (6 items across 3 units)

**prn-fetch-check-return** (3 items)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 2 | Fix bullet numbering (1,1,1→1,2,3); Remove irrelevant HTML note |
| Karatam | 1 | Add before/after example (paragraph vs Fetch/Check/Return) |

**prn-optsel-is-the-universe** (2 items)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 1 | Fix bullet numbering (1,1,1→1,2,3) |
| Karatam | 1 | Add visual flow/diagram (OptSel → RptSel) |

**prn-sql-comments-must-match-local-derive-quality** (2 items)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 1 | Re-number bullet points (canonical rule section) |
| Karatam | 1 | **Q:** Applicable only to DQ views or all Syniti SQL? |

---

### Standards (7 items across 5 units)

**std-cte-rules** (1 item)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 1 | Fix bullet numbering (1,1,1→1,2,3) |

**std-sql-comment-standards** (1 item)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 1 | Highlight material-specific table/field flags |

**std-rule-name-heuristics** (3 items)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 2 | Remove docs ref; Restructure "Criteria, Verbatim" with pattern details |
| Karatam | 1 | "Criteria, Verbatim" too technical and lengthy |

**std-output-field-sections** (1 item)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 1 | Clarify conflict references |

**std-optsel-select-structure** (1 item)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 1 | Clarify checked field mapping |

**std-view-naming-patterns** (1 item)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Karatam | 1 | Add end-to-end example (rule name → OptSel/RptSel) |

---

### Procedures (3 items across 1 unit)

**prc-write-a-quality-rule-name** (3 items)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Keshav | 2 | Remove CONFLICTS.md ref; Fix step numbering |
| Karatam | 1 | Add comparison (checklist vs scorer output) |

---

### Other (1 item across 1 unit)

**notes** (1 item)
| Reviewer | Count | Feedback |
|----------|-------|----------|
| Shruthi | 1 | **Q:** Explain DAMA-DMBOK and relevance to DQ |

---

## Units Touched by Reviewer (Heatmap)

| Unit ID | Keshav | Karatam | Shruthi | Chappavarapu | Total |
|---------|:------:|:-------:|:-------:|:------------:|:-----:|
| con-what-is-data-quality | — | 2 | 2 | — | 4 |
| con-dq-dimensions | 3 | — | 4 | 1 | 8 |
| con-view-types | 1 | — | — | 2 | 3 |
| prn-fetch-check-return | 2 | 1 | — | — | 3 |
| prn-optsel-is-the-universe | 1 | 1 | — | — | 2 |
| prn-sql-comments-must-match-local-derive-quality | 1 | 1 | — | — | 2 |
| std-cte-rules | 1 | — | — | — | 1 |
| std-sql-comment-standards | 1 | — | — | — | 1 |
| std-rule-name-heuristics | 2 | 1 | — | — | 3 |
| std-output-field-sections | 1 | — | — | — | 1 |
| std-optsel-select-structure | 1 | — | — | — | 1 |
| std-view-naming-patterns | — | 1 | — | — | 1 |
| prc-write-a-quality-rule-name | 2 | 1 | — | — | 3 |
| notes | — | — | 1 | — | 1 |
| **TOTAL** | **16** | **8** | **7** | **3** | **34** |

---

## Key Themes

### 1. **Formatting & Numbering Issues** (Keshav-heavy: 11 items)
- Multiple bullet-point numbering errors (1,1,1 instead of 1,2,3) across 5 units
- Several conflict references that feel out-of-place or unclear (3 references)
- **Units:** prn-fetch-check-return, prn-optsel-is-the-universe, std-cte-rules, std-rule-name-heuristics, prc-write-a-quality-rule-name

### 2. **Clarity & Context Gaps** (Karatam + Shruthi: 9 items)
- Statistics and examples need sources/context (2 items)
- Acronyms (GDPR, HIPAA, SOX, DAMA, DMBOK) need explanation (2 items)
- Technical sections too dense (1 item)
- **Units:** con-what-is-data-quality, std-rule-name-heuristics

### 3. **Visual Aids & Examples** (Karatam + Chappavarapu: 5 items)
- Diagrams/flow charts requested for concept relationships (1 item)
- Before/after and end-to-end examples needed (3 items)
- Mapping examples (rule name → view names, PrfSel/RptSel behavior)
- **Units:** prn-fetch-check-return, prn-optsel-is-the-universe, std-view-naming-patterns

### 4. **Conceptual Clarity** (Shruthi + Chappavarapu: 9 items)
- Questions about dimension priorities and distinctions (4 items)
- Questions about view selection patterns and when to use each (2 items)
- Need clearer guidance on when different approaches apply (3 items)
- **Units:** con-dq-dimensions, con-view-types, prn-sql-comments-must-match-local-derive-quality

---

## Recommended Triage Order

| Priority | Category | Units | Items | Lead Issues |
|----------|----------|-------|-------|-------------|
| **1** | Critical formatting fixes | `prn-fetch-check-return`, `prn-optsel-is-the-universe`, `std-cte-rules`, `std-rule-name-heuristics`, `prc-write-a-quality-rule-name` | 5 units, 6 items | Bullet numbering (1,1,1→1,2,3) |
| **2** | Conflict references cleanup | `con-dq-dimensions`, `std-output-field-sections`, `std-optsel-select-structure` | 3 units, 4 items | Remove or clarify "See CONFLICT-..." refs |
| **3** | High-impact examples | `con-what-is-data-quality`, `prn-optsel-is-the-universe`, `std-view-naming-patterns` | 3 units, 4 items | Sources, before/after, end-to-end flow |
| **4** | Contextual additions | `con-dq-dimensions`, `con-what-is-data-quality` | 2 units, 4 items | DAMA-DMBOK, acronym explanations (GDPR, HIPAA, SOX) |
| **5** | Conceptual clarifications | `con-dq-dimensions`, `con-view-types`, `prn-sql-comments-must-match-local-derive-quality` | 3 units, 9 Q's | Dimension priorities, view selection patterns |
