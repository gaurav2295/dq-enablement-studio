---
id: std-req-sql-header-comment-incomplete
type: standard
title: REQ-SQL-HEADER-COMMENT-INCOMPLETE — Header comment block should carry Rule Name/Author/Creation Date/View Type
domain: studio
audience: [developer, consultant]
level: practitioner
status: approved
links:
  - parent:std-harness-requirements
sources:
  - dq-studio:knowledge/harness/requirements.json#REQ-SQL-HEADER-COMMENT-INCOMPLETE
tags: [requirement, harness]
created: 2026-08-20
updated: 2026-08-20
---

## Contract

Header comment block should carry Rule Name/Author/Creation Date/View Type.

## Rationale

The DQ Rule Standards require these four labels in the header comment. Deliberately Info/advisory and disabled by default (shell_guardrails.yaml: header_comment_enabled=false) until core/sql_generator.py's header is deliberately updated to emit them — that's a separate, owner-reviewed change requiring a golden re-bless (D-6 goldens discipline), not something this check should silently force today.

## Enforcement

| Aspect | Value |
|---|---|
| Artifact | sql |
| Severity | Info |
| Posture | advisory |
| Enforced by | sql-validator |
| Codes | sql-validator.header-comment-incomplete |
| Since | v3 (v1) |
