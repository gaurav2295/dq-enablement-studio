# DQ Enablement Studio

The **canonical knowledge base of the Syniti DQ methodology** — every concept, principle,
standard, procedure, reference fact, glossary term and Q&A the CoE works by, in one
searchable, cross-referenced, enrichable place. Seeded from the methodology vault, the DQ
DQ Studio, the Business Outcomes Blueprint (bob-dq), the Data Cleanse Canvas and the
rule repository; from here forward **this repo is the source of truth** and those sources are
history.

## Use it (no install)

Open **[`dist/enablement-master.html`](dist/enablement-master.html)** in any modern browser —
one self-contained file, works offline, from a file share, or from a repo clone. Inside:

- **Search** (`/` to focus) across titles, tags and full text.
- **Browse** by type — Concepts · Principles · Standards · Procedures · Reference · Glossary ·
  Q&A — with domain/audience/level filters.
- **Learning paths** — six: Session 1 (DQ Fundamentals), the SQL Readiness Check, Session 2
  (SQL Best Practices), Session 3 (Studio Workflow), Delivering a Blueprint Engagement, and
  From Rules to Business Value — with progress tracking and knowledge checks. These replace
  the old academy pages (now in `archive/academy-v1/`). Facilitation guidance for all six is
  in [docs/INSTRUCTORS.md](docs/INSTRUCTORS.md).
- **Graph** — the whole methodology and its typed cross-references, clickable.
- **Review mode** (✍ button) — propose edits, add notes, ask questions, flag issues; export
  your changeset as JSON and send it to the CoE (or drop it in `feedback/inbox/`).

## How it's built

```
content/     one markdown file per knowledge unit (typed, frontmattered — the canon)
taxonomy/    closed vocabularies, learning paths, assessment items, seed provenance
build/       build.py + mdlite.py + template.html + merge_changesets.py (stdlib only)
dist/        committed output: the app, chunks.jsonl (RAG-ready), validation-report.md
feedback/    inbox/ for exported changesets · applied/ once processed
docs/        CONFLICTS.md (governed disagreements), FAQ, instructor guide, specs
```

```bash
python3 build/build.py                     # validate + compile app + chunks + report
python3 build/merge_changesets.py --stage  # triage feedback inbox
python3 build/merge_changesets.py --apply  # apply hash-safe edits, stage the rest
```

The build is deterministic (byte-identical rebuilds) and **fails on any validation error** —
schema, closed vocabularies, link integrity, duplicate ids. `dist/` is committed so consumers
never need Python.

## Contribute knowledge

- **Small edits / questions** — use Review mode in the app and export the changeset.
- **Authoring / enrichment** — edit `content/` directly (rules in [CLAUDE.md](CLAUDE.md):
  strict frontmatter, markdown subset, closed vocabularies, conflicts go to
  `docs/CONFLICTS.md`, never delete — deprecate). Then rebuild and commit content + dist
  together.
- **Disagreements are logged, not overwritten** — see [docs/CONFLICTS.md](docs/CONFLICTS.md).

## RAG-ready by design

`dist/chunks.jsonl` carries the whole corpus as stable-ID chunks (`unit_id#NN`) with type,
domain, audience, level, links, sources and a content hash — a future chatbot or in-app
assistant (in dq-studio or standalone) embeds these directly; no re-chunking needed.

## Provenance

`taxonomy/seed-map.json` records which source file produced which unit(s) and the commit each
source repo was at when seeded (2026-08-20). Units carry their own `sources:` frontmatter.

---

Internal use only — Syniti DQ CoE. Brand per [syniti-brand-kit](../../syniti-brand-kit/).
