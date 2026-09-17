---
id: ref-repo-workflow-and-ci
type: reference
title: Repo Workflow & CI
domain: studio
audience: [developer]
level: practitioner
status: review
links:
  - relates:ref-ports-install-and-versioning
  - relates:ref-three-repo-ecosystem
sources:
  - vault:studio-architecture/Studio — Repo Workflow & CI.md
tags: [studio, ops, git, ci, course, agent]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

Work the Studio repo with a typed branch prefix and Conventional Commits, send quick one-liners
straight to `main` but everything non-trivial through a feature branch + PR, run
`python -m pytest` green before every commit (CI re-runs it on Python 3.11 and blocks merge on
failure), and remember the two-machine rule — the Dev machine pushes, the Run machine pulls.

This is the day-to-day contributor workflow for `syniti-methodology-studio`. For the release
ritual (version bump + CHANGELOG + tag) see [[ref-ports-install-and-versioning]]; for how this
repo relates to the pipeline and knowledge-bundle repos see [[ref-three-repo-ecosystem]].

## Branches & commits

| Element | Convention | Source |
|---|---|---|
| Branch prefix | `feat/`, `fix/`, `chore/`, `docs/`, `refactor/`, `test/` + short-kebab | `CONTRIBUTING.md:43` |
| Commit message | **Conventional Commits**; first line ≤72 chars; body explains the *why* | `CONTRIBUTING.md:44` |

- **Quick fix** (typo, one-liner) → commit straight to `main`.
- **Anything non-trivial** → feature branch + PR (`CLAUDE.md:78-79`, `CONTRIBUTING.md:17-39`).

## Tests before every commit (non-negotiable)

Run `python -m pytest` and get it **green before you commit** (`CLAUDE.md:13,80`,
`CONTRIBUTING.md:22`). A PR **cannot merge if CI fails** (`CONTRIBUTING.md:64`). Current suite:
**1148 passed, 0 failed, 2 skipped** (`HANDOFF.md:45`).

> [!note] Test-count drift — Resolved 2026-07-01
> `WORKFLOW.md` / `CONTRIBUTING.md` previously quoted a hardcoded **113 tests**; the dev replaced
> it with non-drifting wording ("full suite") so it can't go stale again (KNOWN-ISSUES B11, fixed
> 2026-07-01). The suite runs **1148** passing (`HANDOFF.md:45`).

## The CI (GitHub Actions)

Two workflows live in `.github/workflows/`:

- **`test.yml`** — the real gate. **Python 3.11**, install `requirements.txt`, then
  `python -m pytest -v --tb=short`. Triggers on **push + PR to `main`**. Runs with
  `STUDIO_ENV=ci` (CI has no client data).
- **`slack-notifications.yml`** — runs on every push: `cd slack-bot && npm install && npm test`
  then a Slack "code modified and committed" notify. The `slack-bot/` is a trivial
  commit-notification stub (its `test` just runs `node index.js`, which logs "Tests running") —
  **not** a quality gate.

> [!note] 3.11 is the CI target, not the installer floor
> `setup.sh` *accepts* Python 3.9 as a bare floor, but CI gates on **3.11**, and README +
> CONTRIBUTING agree. Develop and test on **3.11** so you match what CI runs. See
> [[ref-ports-install-and-versioning]].

## The two-machine model (Dev pushes, Run pulls)

GitHub is the middle. The **Dev machine pushes**; the **Run machine pulls**
(`HANDOFF.md:265-278`).

- Always `git pull` before starting work on **either** machine.
- `.venv/` and API keys are **per-machine and gitignored** — they never sync.

## Never commit

Client data, secrets, generated artefacts, and `.claude/` stay out of git
(`CONTRIBUTING.md:69-79`, `.gitignore`):

- **Client data** — `knowledge/clients/*/` is gitignored; deliverables live only in
  `~/Downloads` (DECISION D-5).
- **Secrets** — `.env`, anything matching `*api*key*`.
- **Generated artefacts** and the **`.claude/`** bundle symlink.

## Do / Don't (agent)

- **Do** prefix branches and write Conventional Commit messages.
- **Do** run `python -m pytest` green *before* committing; never push a red suite.
- **Do** push from Dev, pull on Run; `git pull` before starting on either.
- **Don't** send non-trivial work straight to `main` — branch + PR.
- **Don't** commit client data, secrets, generated files, or `.claude/`.
- **Don't** rely on `slack-notifications.yml` as a test gate — `test.yml` is the gate.

## Inputs & outputs

- **In:** a checkout of `syniti-methodology-studio`; Python 3.11; a clean `python -m pytest` run.
- **Out:** a commit/PR on `main` that passes the `test.yml` CI gate; the same tree pulled onto the
  Run machine.

## Source

- `CONTRIBUTING.md:17-39,43,44,64,69-79` — branches, Conventional Commits, PR-merge gate,
  never-commit list.
- `CLAUDE.md:13,78-80` — quick-fix-to-main vs branch+PR; tests before commit.
- `.github/workflows/test.yml` — Python 3.11, `pytest -v --tb=short`, push+PR to `main`,
  `STUDIO_ENV=ci`.
- `.github/workflows/slack-notifications.yml` — `slack-bot/` commit-notify stub.
- `HANDOFF.md:45,265-278` — 1148 passing; two-machine Dev-pushes/Run-pulls; per-machine
  `.venv`/keys.
- `.gitignore` / `HANDOFF.md:157-162` — client data out of git (D-5).
- Detail: `knowledge-mining/app-arch-ops.md` §8 (and §6, §7).

## Related

[[ref-ports-install-and-versioning]] · [[ref-three-repo-ecosystem]]
