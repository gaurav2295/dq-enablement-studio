# HANDOFF — DQ Enablement Studio (enablement-master)

**Last session:** overnight autonomous build, 2026-08-20 → 2026-08-21 (Claude, per approved
plan `docs/specs/2026-08-20-enablement-master-design.md`), followed by the 2026-08-21
methodology-enablement prune and reconcile (app design/dev material archived out of `content/`).
**Branch:** `feat/enablement-master` — pushed, PR open for review. **Not merged.**

## What exists this morning

The reimagined DQ Enablement Studio: the CoE's **canonical methodology knowledge base**,
fully seeded and working.

| Fact | Value |
|---|---|
| Knowledge units | **251** (concepts 24 · principles 14 · standards 27 · procedures 16 · reference 28 · glossary 142 · qa 0) — after the 2026-08-21 methodology-only prune |
| Learning paths | **6** — Session 1 Fundamentals · SQL Readiness Check · Session 2 SQL · Session 3 Studio Workflow · Delivering a Blueprint Engagement · From Rules to Business Value |
| Assessment items | 35 mcq (29 migrated from academy v1 with seven-dimension rewrites, 6 new for Session 3) |
| App | `dist/enablement-master.html` — 2.69 MB single file, offline, brand-kit (aurora/glass) |
| RAG chunks | `dist/chunks.jsonl` — 1,060 stable-ID chunks, embedding-ready |
| Build | `python3 build/build.py` — **0 errors, 0 warnings**, byte-stable, stdlib-only |
| Verification | 15/15 Playwright checks pass post-prune (search, routing, quizzes, reinforce checks, paths, filtered graph, review mode, clean console) |
| UI (2026-08-21 cleanups) | Syniti logo in header; brand-kit icons only (no emoji); graph defaults to the methodology skeleton with type + domain filters and domain clustering; knowledge checks redesigned as per-unit Reinforce sections (step completes when all checks pass); light/dark theme (follows system, header toggle, persisted) |
| Feedback loop | Review mode → JSON changeset → `feedback/inbox/` → `merge_changesets.py` (round-trip tested: hash-safe edit applied, stale edit rejected, question staged) |
| Conflicts log | `docs/CONFLICTS.md` — 20 governed entries, numerically ordered, statuses normalised |

Seeded from (commits pinned in `taxonomy/seed-map.json`; these are now **history — this repo
is master**): estate-hub vault mirror (111 notes), dq-studio (standards docs, 7 canonical
skills, 68 ADRs and 36 requirement contracts — **since archived out of `content/`**, see open
items — methodology JSONs), bob-dq (glossary, value
methodology, enablement guide, delivery spine), data-cleanse-canvas (execution model),
syniti-dq-rule-repo (schema + governance), academy v1 (pedagogy + quizzes; HTML archived in
`archive/academy-v1/`).

## First 30 minutes for a reviewer (you or Gaurav)

1. Open `dist/enablement-master.html`. Search something you know cold (e.g. "zSourceSystemID"),
   read the unit, follow its cross-refs — judge the register.
2. Walk a learning path end-to-end (Session 1 is the most polished).
3. Read `docs/CONFLICTS.md` — the open entries are the decisions only the CoE can make.
4. Review + merge the PR when satisfied; then announce to the consultant test group with
   `docs/SETUP.md`'s distribution guidance.

## Open items (ranked; from the overnight completeness critique)

**CoE decisions needed (open conflicts — don't let these linger):**
- CONFLICT-002 process-area taxonomies (bob-dq L3 vs cleanse-canvas 12+6) — one model or a mapped pair?
- CONFLICT-007 zConcatenatedKey argument order (re-keys deployed views if changed).
- CONFLICT-011 view-name token order (three variants live; picking one implies a migration).
- CONFLICT-013 `{{SYSTEM}}` literal vs column reference in templates.
- CONFLICT-017 provenance vocabulary (needs the rule-repo owner).
- CONFLICT-018 "coverage" homonym · CONFLICT-019 technical-field membership (3 vs 4 vs 5) ·
  CONFLICT-020 academy's SaaS onboarding narrative vs the shipped local app.

**Content work for next sessions:**

- App-internal corpus (ADRs, requirement contracts, engine internals) archived to
  `archive/dev-corpus/` — candidate seed for a future developer KB. 161 units moved out on
  2026-08-21 under the methodology-enablement policy; they are intact and could seed a
  developer-facing companion if the CoE wants one.

1. **Review-queue triage** — 242 units are `status: review`, and *every* unit in the
   consultant-facing domains (delivery, value-outcomes, cleanse, sap, ai-enhancement,
   platform) is unapproved. Suggested: bulk-approve the 141 single-source glossary stubs, then
   work the 101 substantive units. (Deliberately NOT auto-approved overnight — sign-off is yours.)
2. **Domain skew** — after the prune the corpus leans SQL and rule design (sql-standards 49 ·
   rule-design 44 · delivery 38 · value-outcomes 34 · sap 27 · studio 24 · ai-enhancement 12 ·
   dq-fundamentals 10 · cleanse 9 · platform 4). Consider a `profiling` domain, whether
   ai-enhancement/sap need concepts+principles (currently reference/glossary-heavy), and whether
   `platform` still earns its own domain at four units.
3. **Un-mined riches** — bob-dq spec §1.6/§2.3 (security pack, commercial model),
   `enablement/scenarios.md` role-plays, `handover/g4-sample-blueprint.md` (worked example), and
   deeper `archive/academy-v1/index.html` fundamentals.
4. **Q&A is empty** — it fills from the consultant feedback loop; seed it with the first
   incoming questions.
5. **Glossary gaps** — governance, remediation, reconciliation, master data, golden record,
   survivorship, cutover, data steward, DQA are used but undefined.
6. **App v1.1** — progress export/import JSON (file:// localStorage caveat), edit diff
   preview, tighter orphan warnings in build.py (zero-inbound units of any type).
7. **SQL practice integration** (sql-practice.online-style) — the `sql_practice` hook field
   and assessment kind exist; no items authored yet.
8. **Team distribution** — after merge: put `dist/enablement-master.html` on the share,
   brief the consultant group, and register the estate-hub knowledge sync decision (the
   vault mirror is now non-canonical; decide whether `bin/sync-methodology.py` should stop
   or reverse).

## How to work on this (rules)

`CLAUDE.md` is the authoring contract: strict flat-YAML frontmatter, markdown subset, closed
vocabularies (`taxonomy/taxonomy.json`), conflicts to `docs/CONFLICTS.md`, never delete —
deprecate + supersede, rebuild + commit `content/` and `dist/` together, always
`python3 build/build.py` clean before commit.
