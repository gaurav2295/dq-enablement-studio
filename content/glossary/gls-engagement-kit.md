---
id: gls-engagement-kit
type: glossary
title: Engagement Kit
domain: delivery
audience: [consultant, lead]
level: practitioner
status: review
links:
  - parent:gls-dq-studio
  - relates:gls-rule-package
  - relates:gls-project-spec
  - relates:gls-iteration-loop
  - relates:con-studio-capabilities
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, deliverable, handover]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

Everything [[gls-dq-studio|dq-studio]] generates for an engagement from an imported
[[gls-project-spec|project spec]] — the rules, their SQL, the specs and the supporting documents
needed to run them.

## Usage

"Kit" is the right word: it is not a report, it is the set of things a delivery team executes with.
The [[gls-rule-package|rule package]] is its SQL-bearing core.

The kit is regenerated, never hand-patched — the Studio owns the only
[[gls-iteration-loop|iteration loop]] in the chain, so a change goes back through derivation rather
than being edited into the output.
