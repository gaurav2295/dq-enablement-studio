---
id: prn-adr-048
type: principle
kind: decision
title: ADR D-48 — Every generated DQ rule SELECTs from the consolidated prep DB, never the raw source DB
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
  - relates:ref-three-database-architecture
sources:
  - dq-studio:knowledge/harness/decisions.json#D-48
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

Every generated DQ rule SELECTs from the consolidated prep DB, never the raw source DB.

## Rationale

Per the architecture diagram (knowledge/architecture/syniti_dq_data_flow.md), every generated DQ rule must read from the consolidated prep DB (WRKDQ) — NEVER the raw source DB (SRCECC_DA). This is an architectural contract, not an implementation detail, and it applies across all three rule shapes the Studio emits: Error (OptSel + RptSel), Info (InfSel), and Catalog (verbatim catalog SQL with a substituted {datastore} placeholder).

## Consequence

Any new rule shape or code-generation path must target the prep DB exclusively; a generated rule that references the raw source DB directly is an architecture violation, not a stylistic choice. The test strips provenance-header comments first so a source_db mention in a comment doesn't false-positive the check.

> [!warning] Read "prep DB" here as `WRKDQ`, not `WRKDQPREP_ALL`
> This ADR's own rationale names the target as "the consolidated prep DB (**WRKDQ**)", which is the
> `working_db` in the vocabulary [[ref-three-database-architecture]] uses — there, "prep DB" means
> `WRKDQPREP_ALL`, the upstream layer rules do **not** read. The decision is intact (rules never
> touch `SRCECC_DA`), but its wording predates that split and reads as the opposite of the code. The
> ADR registry owner should restate the title against current terminology; see CONFLICT-004.

> [!note] Provenance
> Architecture decision **D-48** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
