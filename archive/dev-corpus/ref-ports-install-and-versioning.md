---
id: ref-ports-install-and-versioning
type: reference
title: Ports, Install & Versioning
domain: studio
audience: [developer]
level: practitioner
status: review
links:
  - relates:ref-home-page
  - relates:ref-three-repo-ecosystem
  - relates:ref-repo-workflow-and-ci
sources:
  - vault:studio-architecture/Studio — Ports, Install & Versioning.md
tags: [studio, app, ops, install, versioning, course]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

The Studio is a FastAPI + Jinja app that runs on port 8501 (the separate DQ Data Pipeline repo
owns 8502); you install it with `setup.sh` on macOS/Linux or a manual venv on Windows, and every
release bumps the single-source-of-truth `version.py` plus a matching `CHANGELOG.md` entry under
SemVer.

This note is the operator's view: how to start it, on which port, how to install it, and the
release ritual. For what each page does see [[ref-home-page|Home Page]]; for the wider repo story
see [[ref-three-repo-ecosystem|Three-Repo Ecosystem]].

## Ports

| Port | App | Repo |
|---|---|---|
| 8501 | The Studio — rule creation / design / derive (this app) | `syniti-methodology-studio` |
| 8502 | DQ Data Pipeline — *runs* the views the Studio generates | `syniti-dq-pipeline` (separate) |

- **8501 is the default** (`app.py:82`, `PORT=8501` env default; `WORKFLOW.md:16`). The Studio repo
  only documents 8501 for itself.
- **8502 is a different repo.** Per the App Split decision, Rule Creation (8501) and DQ Data
  Pipeline (8502) are two separate apps; the Studio does not serve 8502. Teach them as a paired
  story but distinct binaries.
- Override the port with `--port` (e.g. `--port 8001`, `9000`) or the `PORT` env var.

## Run commands

```bash
python app.py                                  # → http://localhost:8501 (uvicorn, reload=True, host 127.0.0.1)
uvicorn app:app --reload --port 8501           # explicit
python -m uvicorn app:app --host 127.0.0.1 --port 8501 --loop asyncio   # Windows / manual paths
```

Note the Windows incantation needs `--loop asyncio` (`INSTALL-WINDOWS.md:159`).

## Install

- **macOS / Linux** — `./setup.sh` creates `.venv/` and installs deps. Flags: `--venv`,
  `--venv --start`, `--check-only`, `--no-test`, `--port N` (`setup.sh:8-11,49-53`). It prefers
  `python3` (then 3.12/3.11/3.10/3.9), and **requires Python 3.9+** or it fails
  (`setup.sh:99,113`).
- **Windows** — no `setup.sh`; follow `INSTALL-WINDOWS.md` for a manual venv, or use the one-click
  `start_studio.bat` (`START-STUDIO-WINDOWS.md`).
- **Smoke test** after install: `curl /` → 200; `GET /api/profiler/filter-presets` → 5 presets;
  `pytest tests/ -q --ignore=tests/correctness --ignore=tests/golden` → 1000+ tests in ~25s
  (`INSTALL.md:160-175`).

> [!note] Python version — resolved 2026-07-01 (B7, floor standardized on 3.11)
> The Python floor is now standardized on **3.11** across the board (KNOWN-ISSUES B7, fixed
> 2026-07-01) — no more 3.9-floor-vs-3.11-target split. That is what CI gates on
> (`.github/workflows/test.yml`), and README/CONTRIBUTING/HANDOFF agree. Use 3.11.

Key dependency gotcha: **`python-multipart≥0.0.9`** is required for *all* file-upload endpoints —
without it FastAPI raises "Form data requires 'python-multipart'" (`requirements.txt`).

## Versioning (single source of truth)

`version.py` is the **single source of truth**:

```python
__version__      = "2.2.0"
__version_date__ = "2026-06-30"
```

Both the API metadata (`app.py:27`) and the on-screen sidebar badge `Studio v{{ app_version }}`
(`base.html:18`, injected as the Jinja global `templates.env.globals["app_version"]` in
`app.py:34-36`) read from `version.py` — so the API version and the UI version **can never drift**.
This was the fix for the "API said 1.0.0, sidebar said v2.0" bug (DECISION D-6).

> [!tip] Don't confuse the cache-buster with the app version
> Static CSS/JS are cache-busted with `?v=3.0.0` query strings (`base.html:7,105`). That `3.0.0` is
> a cache-buster, **not** the app version. The real version lives only in `version.py`.

### SemVer policy

MAJOR.MINOR.PATCH (`version.py:9-14`):

- **MAJOR** — a structural shift in what the product *is* (v2.0 = the unified Studio replacing the
  HTML companion).
- **MINOR** — a new backwards-compatible capability (e.g. 2.1.0 added the PIR domain + coverage
  transparency).
- **PATCH** — bug fixes (e.g. the 2.0.x DQOps-dup fix).

### Release ritual (do this every release)

1. Bump `version.py` (`__version__` and `__version_date__`).
2. Add a matching `CHANGELOG.md` entry — format is *Keep a Changelog + SemVer* (`CHANGELOG.md:7`).
3. Run tests green (`python -m pytest` — currently 1148 passing).
4. Tag and release: `git tag -a vX.Y.Z` → `git push --tags` → `gh release create`
   (`WORKFLOW.md:76-80`).

> [!warning] Both, every release
> Bumping `version.py` without a CHANGELOG entry (or vice versa) is incomplete. The rule is **both,
> every release** (`version.py:3-4`, `CLAUDE.md:29,77`, `HANDOFF.md:50`). Never hardcode a version
> anywhere in markup — that is exactly the drift D-6 outlawed.

## Inputs & outputs

- **In:** a checkout of `syniti-methodology-studio`; Python 3.11; `setup.sh` (or manual venv).
- **Out:** a running FastAPI server on `http://localhost:8501`, version self-reported (API +
  sidebar) from `version.py`.

> [!note] Implementation status — resolved 2026-07-01 (B10, FastAPI, not Streamlit)
> `CLAUDE.md` has been corrected to describe the app as **FastAPI + Jinja** (KNOWN-ISSUES B10, fixed
> 2026-07-01) — the prior "Python + Streamlit" / "Streamlit pages" wording is gone. The shipped app
> is FastAPI + Jinja (`app.py` + `ui/templates/*.html`); CLAUDE.md, README, HANDOFF and INSTALL all
> now agree. Teach FastAPI + Jinja.

## Source

- `app.py:79-83` — uvicorn run block (`PORT=8501` default, `127.0.0.1`, `reload=True`).
- `app.py:27`, `app.py:34-36` — version read into API metadata + Jinja global.
- `version.py:1-18` — single-source version, date, and the SemVer policy comments.
- `setup.sh:8-11,49-53,99,113` — installer flags + Python 3.9 floor.
- `INSTALL.md`, `INSTALL-WINDOWS.md`, `START-STUDIO-WINDOWS.md`, `WORKFLOW.md:16-17,76-80` —
  install/run/release docs.
- `CHANGELOG.md:7,11-92` — Keep-a-Changelog format + version history.
- Detail: `knowledge-mining/app-arch-ops.md` §6, §7, §10.

## Related

[[ref-home-page]] · [[ref-three-repo-ecosystem]] · [[ref-repo-workflow-and-ci]]
