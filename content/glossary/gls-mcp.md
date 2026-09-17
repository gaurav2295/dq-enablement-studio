---
id: gls-mcp
type: glossary
title: MCP (Model Context Protocol)
domain: delivery
audience: [developer, lead]
level: foundation
status: review
links:
  - relates:gls-rule-repository
  - relates:gls-ctx-server
  - relates:gls-snapshot
sources:
  - rule-repo:README.md
  - rule-repo:docs/mcp-usage.md
tags: [integration, tooling]
created: 2026-08-20
updated: 2026-08-20
---

## Definition

The protocol over which the [[gls-rule-repository|rule repository]] serves its catalogue to other
tools — dq-studio and the bob-canvas explorer connect as MCP clients rather than reading the
catalogue file directly.

## Usage

The reason consumers go through a server rather than the data file is governance: one loader, one
index, one place where provenance and linkage semantics are applied. A consumer that reads
`catalogue.json` off disk bypasses that and will drift.

Two surfaces exist side by side — MCP (stdio) for tool clients, and a read-only HTTP surface for a
local explorer page. The [[gls-ctx-server|per-client context server]] is designed as an MCP server
too, with one client root per session so cross-client queries are impossible by construction.
