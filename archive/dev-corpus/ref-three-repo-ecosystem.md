---
id: ref-three-repo-ecosystem
type: reference
title: Three-Repo Ecosystem
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - relates:ref-home-page
  - relates:ref-ports-install-and-versioning
  - relates:ref-repo-workflow-and-ci
  - relates:ref-architecture-context-and-project-yamls
  - relates:ref-markdown-exporter-and-round-trip-contract
  - relates:ref-knowledge-base-file-inventory
  - relates:ref-exporters
  - relates:ref-ai-client-conventions
  - relates:gls-boa
  - relates:gls-evaluation-sheet
  - relates:gls-mcp
  - relates:gls-project-spec
sources:
  - vault:studio-architecture/Studio — Three-Repo Ecosystem.md
tags: [studio, app, architecture, methodology, agent, course]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

The Syniti DQ methodology ships as three companion repos — `syniti-methodology-studio` (the 8501
*design* app), `syniti-dq-pipeline` (the 8502 *run* app), and `syniti-dataquality` (the AI-loadable
knowledge bundle plus a `methodology/` mirror of the vault) — and the Obsidian vault, not any repo,
is the single source of truth for methodology. There are three active repos plus one decommissioned
archive. Each has a distinct job; together they cover *design the rule → run the rule → teach the
rule to humans and AI*.

## The three active repos

| Repo | Role | Port / shape |
|---|---|---|
| **syniti-methodology-studio** | The Studio app — the runtime that DESIGNS and DERIVES rules (single + bulk, profiling, audit, exports) | FastAPI + Jinja, port 8501 |
| **syniti-dq-pipeline** | The DQ data pipeline app — RUNS the views the Studio generates | FastAPI, port 8502 (split off 2026-04-09) |
| **syniti-dataquality** | Knowledge bundle: AI-loadable rules/skills/commands/agents plus a `methodology/` mirror of the vault | No app, no CI |

> [!note] The retired fourth repo
> `syniti-dq-rule-copilot-archive` is the decommissioned single-file HTML companion app (v6.1.8),
> replaced by the unified Studio at v2.0. Kept for reference only — not maintained.

## The 8501 / 8502 split (design vs run)

The Studio (8501) is *rule creation*: it emits view DDL (OptSel/RptSel/InfSel/PrfSel/PrfSum),
markdown specs, trackers and deploy scripts — it has **no live database connections** (schema
comes from DDL/DBML files only). The pipeline (8502) is a **separate app in a separate repo** that
*executes* those views against the data layers. They were one combined app until the 2026-04-09
split.

> [!note] Implementation status — resolved 2026-07-01
> FastAPI, not Streamlit (B10). The Studio's `CLAUDE.md` has been corrected to FastAPI + Jinja,
> matching both active apps (README/HANDOFF/INSTALL agree). The prior "Python + Streamlit /
> Streamlit pages" wording is gone.

## Vault is methodology source of truth; the repo mirrors it

- The Obsidian vault `~/Obsidian/syniti-data-quality-coe/` (specifically `30 Resources/`) is the
  **single source of truth** for methodology prose.
- It is **published** into `syniti-dataquality`'s `methodology/` folder, which is a **mirror**
  refreshed by `bin/sync-methodology.py --apply`.
- The Studio repo **implements** the methodology and **consumes** `knowledge/*.json` — it must
  **not** copy methodology prose; it links to the mirror instead.

```text
Obsidian vault (30 Resources/)   ← single source of truth
        │  bin/sync-methodology.py --apply
        ▼
syniti-dataquality/methodology/  ← mirror (regenerated, do not hand-edit)
syniti-dataquality/applications/…/  ← AI bundle (rules/skills/commands/agents)
        │  symlink as .claude/
        ▼
syniti-methodology-studio  +  syniti-dq-pipeline   ← apps that implement/run it
```

## The `.claude/` symlink wiring

The AI bundle inside `syniti-dataquality` is wired into an app by symlinking it as `.claude/`.
Folder names deliberately use Claude Code's lowercase conventions (`rules/`, `skills/`,
`commands/`, `agents/`) so it symlinks with zero renames:

```bash
ln -s ~/repos/syniti-dataquality/applications/Syniti\ DQ\ Studio\ -\ Application .claude
```

- After symlinking, `rules/` and `skills/` **auto-load** in Claude Code; `CLAUDE.md` pulls extra
  context via `@./` imports.
- `.claude/` is **gitignored — never committed**. The symlink is local wiring, not repo content.

> [!tip] Do / don't (agent)
> - **Do** edit methodology in the vault, then run `bin/sync-methodology.py --apply` to refresh
>   the mirror.
> - **Don't** hand-edit `syniti-dataquality/methodology/` (it is regenerated) and **don't** paste
>   methodology prose into the Studio repo.
> - **Don't** commit `.claude/` — it is a local symlink into the bundle.

## Source

- `README.md:49-65`, `WORKFLOW.md:92-100`, `CLAUDE.md:32-37` — the three-repo table; vault-as-
  source-of-truth; "link to the mirror, don't copy."
- `README.md:59-65`, `CONTRIBUTING.md:91-102` — `.claude/` symlink wiring; gitignored, never
  committed.
- `wiring-into-claude-code.md:5`, bundle `README.md:38` — zero-rename lowercase folder naming.
- `prompts/session-context-2026-06.md` — 4-repo snapshot including archive; the 8502 split on
  2026-04-09.

## Related

- [[ref-home-page]]
- [[ref-ports-install-and-versioning]]
- [[ref-repo-workflow-and-ci]]
- [[ref-architecture-context-and-project-yamls]]
- [[ref-markdown-exporter-and-round-trip-contract]]
- [[ref-knowledge-base-file-inventory]]
- [[ref-exporters]]
- [[ref-ai-client-conventions]]
