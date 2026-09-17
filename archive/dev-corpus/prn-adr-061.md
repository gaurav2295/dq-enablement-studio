---
id: prn-adr-061
type: principle
kind: decision
title: ADR D-61 — workspace_iterate rows must carry the real validator_findings through the re-derive path
domain: studio
audience: [developer]
level: advanced
status: approved
links:
  - parent:prn-studio-decision-registry
sources:
  - dq-studio:knowledge/harness/decisions.json#D-61
tags: [adr, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Decision

workspace_iterate rows must carry the real validator_findings through the re-derive path.

## Rationale

Fix-review regression: api_derive's response surfaces validator_findings, but _rederive_target_with_enhance has to explicitly copy that onto the re-derived dict too — without both halves of that wiring, every workspace_iterate row silently reported validator_finding_count=0/validator_max_severity=None regardless of the SQL's actual findings, hiding real defects from the bulk-iterate UI.

## Consequence

Any future change to the workspace-iterate re-derive path must keep threading validator_findings from the real /api/derive call through to the row the UI reads, not just from the initial derive. The test forces two deterministic findings (one High, one Medium) through the REAL in-process /api/derive call to prove the full wiring, not a stubbed shortcut.

> [!note] Provenance
> Architecture decision **D-61** in the DQ Studio decision registry, decided 2026-07-27, registry status *active*.
