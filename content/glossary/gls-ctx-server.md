---
id: gls-ctx-server
type: glossary
title: ctx-server (per-client context server)
domain: delivery
audience: [consultant, lead]
level: foundation
status: review
links:
  - relates:gls-rule-repository
  - relates:gls-dq-studio
  - relates:qa-ctx-server-what-is-client
sources:
  - bob-dq:CONTEXT.md
tags: [bob-dq, instruments, security, planned]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

**The per-client context server.** One client root per session, **so cross-client queries are
impossible by construction**.

**Designed, not yet built.**

## Usage

The design point is the phrase *by construction*: client isolation is not a permission check
that could be misconfigured but a property of the server having exactly one root per session.
There is no query that reaches a second client because there is no second client mounted.

> [!important]
> This term describes a **planned** component. Do not write material that implies it exists,
> and do not commit an engagement to capability that depends on it.

Referred to as `#ctx-server` in bob-dq material; like every instrument name it is internal and
stays out of the client room.
