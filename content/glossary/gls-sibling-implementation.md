---
id: gls-sibling-implementation
type: glossary
title: Sibling Implementation
domain: rule-design
audience: [consultant, developer]
level: practitioner
status: review
links:
  - relates:con-multi-implementation-model
  - relates:gls-fan-out
  - relates:gls-parent-group
sources:
  - vault:studio-architecture/Studio — Bulk Processor & DQOps ID Invariants.md
tags: [multi-system, bulk]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

One of the per-system implementations produced by [[gls-fan-out|fan-out]] — same rule, same
intent, different system. Siblings share a [[gls-parent-group|parent group]].

## Usage

Siblings are meant to stay identical apart from their system token and filter, so the Studio
propagates one AI enhancement across the group rather than paying for N calls. Two collision rules
protect that:

- a sibling already enhanced independently is **skipped by default** (reported, overridable);
- a sibling whose content has **diverged** from the group's shared pattern is **always** skipped,
  never silently overwritten.

Drift between siblings is a validator finding in its own right.
