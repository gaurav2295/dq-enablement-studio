# Enablement-Master — Reimagined DQ Enablement Studio

## Context

The DQ CoE's methodology knowledge is scattered across five repos and an Obsidian vault only Truwayne uses: a 113-note vault mirror in the estate hub (read-only, overwritten by sync), dq-studio's operational standards docs + machine-readable knowledge (36 requirement contracts, 68 ADRs, heuristics, view conventions), bob-dq's glossary/value-chain/enablement guide, data-cleanse-canvas's execution model docs, and rule-repo's catalogue semantics. The current `dq-enablement-studio` (3 standalone training HTML files, content welded into markup) is neither searchable nor enrichable, and its training content conflicts with the methodology source (six vs seven DQ dimensions).

Goal: rebuild `dq-enablement-studio` (in the CoE monorepo `syniti-dq-coe-projects`) as **enablement-master** — the centralized, canonical, searchable, enrichable DQ methodology knowledge base, seeded from all sources, branded with syniti-brand-kit, usable by Gaurav and the team going forward, and RAG-ready for a later chatbot.

## Decisions made with the user (brainstorming, 2026-08-20)

1. **Access model:** files/intranet, NO server. Single-file offline HTML app shared via repo clone / file share.
2. **Edit model:** in-browser edit/enrich/cross-reference + JSON changeset export, merged into canonical files by build/Claude. Major baselining and deep research happens via Claude sessions on the markdown.
3. **Source of truth:** enablement-master becomes canonical for the CoE. The vault mirror is SEED ONLY; Truwayne's personal Obsidian vault stays untouched for now.
4. **V1 scope:** everything — knowledge base + search, learning paths/academy rebuilt on the KB, consultant feedback loop, RAG-ready data model, well-thought-out UI, structure the team can build on.
5. **Architecture (option A):** canonical content = typed, frontmattered markdown knowledge units + registry JSON in git; Python build compiles ONE branded single-file HTML app + `chunks.jsonl` for future RAG.
6. **Taxonomy (trimmed, 7 types + paths):** concepts, principles (incl. `kind: decision` for ADRs), standards (incl. `kind: pattern`), procedures, reference, glossary, qa. Learning Paths = curated sequences over units (Sessions 1–3 become paths). Assessments = quiz items attached to units/paths, not a browse type. Facets: domain, audience, level.
7. **Seed depth:** FULL corpus seed (~200+ units from all sources).

## Seed source inventory (from exploration)

| Source | Assets |
|---|---|
| estate-hub `knowledge/methodology/` | 113 frontmattered .md notes: dq-methodology (21), studio-architecture (46), sap-knowledge (15), sops (12), thought-leadership (9), templates (6), ai-related (3), syniti-platform (1) |
| dq-studio | `docs/DQ_RULE_STANDARDS.md`, `RULE_PATTERNS.md`, `ai_enhance_instructions.md`, `Studio_Overview.md`, `CLAUDE.md` non-negotiables, `.claude/skills_canonical/*.md` (7), `knowledge/harness/requirements.json` (36) + `decisions.json` (68 ADRs), `knowledge/methodology/*.json` (view_conventions, heuristics, rule_patterns, capabilities, methodology_graph) |
| bob-dq | `CONTEXT.md` glossary, `enablement/enablement-guide.md` (8 modules), spec §1.3 (L1–L5) + §1.4b (value model), ADRs, resourcing rubric |
| data-cleanse-canvas | `docs/DATA-MODEL.md`, `PLAN-operational-layer.md`, `CONTEXT.md` glossary, `DECISIONS.md` |
| syniti-dq-rule-repo | `data/catalogue.json._meta` (field/provenance semantics, 69-entry key-issue vocabulary), `README.md` schema, ADR 0002 |
| existing dq-enablement-studio | ~3200 lines pedagogy + 27 quiz items (landing.html answers are inline function args — parse job; sql-pre-assessment.html has clean answers{}/feedback{}), `docs/FAQ.md` + `INSTRUCTORS.md` portable |
| syniti-brand-kit | `tokens/tokens.css` + `tokens.js` (SYNITI{}), `patterns/patterns.css` (aurora underlay MANDATORY before glass), icons inlined individually, `starter.html` scaffold |

**Known content conflicts to log + resolve during seed:** seven dimensions (vault: Accuracy, Completeness, Conformity, Consistency, Integrity, Timeliness, Uniqueness) vs six in academy HTML (Validity, no Conformity/Integrity) — vault wins as seed-canonical, academy quiz items updated. bob-dq L3 process areas vs cleanse-canvas 12 process areas / 6 BPAs — record in conflicts log, reconcile as CoE decision.

## Design

### Repo layout (inside `syniti-dq-coe-projects/dq-enablement-studio/`)

```
dq-enablement-studio/
├── README.md                # rewritten: what enablement-master is, build/consume how-to
├── CLAUDE.md                # NEW: authoring rules for Claude sessions (schema, IDs, build cmd, conflicts duty)
├── content/                 # canonical units, one .md per unit, foldered by type
│   ├── concepts/  con-*.md      ├── principles/ prn-*.md  (kind: decision = ADRs)
│   ├── standards/ std-*.md  (kind: pattern)   ├── procedures/ prc-*.md
│   ├── reference/ ref-*.md      ├── glossary/  gls-*.md (one term per unit)
│   └── qa/        qa-*.md   (consultant questions land here after triage)
├── taxonomy/
│   ├── taxonomy.json        # closed vocabularies: types, kinds, domains, audiences, levels, statuses, link rels
│   ├── paths.json           # learning paths (ordered unit/assessment sequences)
│   ├── assessments.json     # quiz + sql_practice items (attached data, not a browse type)
│   └── seed-map.json        # provenance: source file → unit id(s) + seed commit hash per source repo
├── build/
│   ├── build.py             # single entry point, stdlib only (pattern: syniti-consultant-eval/build/build.py)
│   ├── mdlite.py            # markdown-subset → HTML renderer (~250 lines)
│   ├── merge_changesets.py  # --stage (triage report) / --apply (hash-safe edits) for feedback/inbox/*.json
│   └── template.html        # app shell with __PLACEHOLDERS__ (brand CSS inlined, all UI JS)
├── feedback/  inbox/  applied/
├── dist/                    # COMMITTED output: enablement-master.html, chunks.jsonl, validation-report.md
├── docs/                    # FAQ.md + INSTRUCTORS.md ported; SETUP.md rewritten; CONFLICTS.md (conflict log)
└── archive/academy-v1/      # old 3 HTML files moved verbatim after extraction
```

`dist/` is committed so consultants open `enablement-master.html` from a share with no Python. Build uses `newline=""` byte-stable I/O (consultant-eval pattern) so rebuilds are diffable.

### Knowledge unit schema

Strict flat YAML frontmatter (custom ~60-line stdlib parser; `key: value`, `key: [a, b]`, `- item` lists only; anything else = build error):

- `id` (REQUIRED, `{prefix}-{kebab-slug}`, prefixes con|prn|std|prc|ref|gls|qa; must match filename + folder; stable forever), `type`, `title`, `domain` (single, from taxonomy), `audience` (1+), `level` (foundation|practitioner|advanced), `status` (draft|review|approved|deprecated), `created`, `updated` — all required; `sources` (REQUIRED, min 1, `repo-key:relative/path[#anchor]`).
- Optional: `kind` (decision|pattern), `links` (typed edges `rel:target-id`; closed rel set: prereq, relates, parent, contrast, implements), `supersedes` (drives redirect map), `sql_practice` (assessment item hook), `tags` (search boost only).
- Inbound "referenced by" edges computed at build, never authored.
- Body = markdown subset: ##/### headings, bold/italic/code, fenced code (SQL keyword highlighting), pipe tables, lists (1 nesting level), blockquotes + Obsidian callouts `> [!note]`, wikilinks `[[unit-id]]`/`[[unit-id|label]]` (validated), external links. Raw HTML = build error; unsupported md = warning. Nothing degrades silently.
- Status lifecycle: seeded units start `review` unless verbatim from already-approved sources (skills_canonical, ADRs) → `approved`. `deprecated` stays in corpus (grayed, excluded from paths/default search) so links never dangle.
- Assessments (`assessments.json`): `{id: "as-…", unit_id, path_id?, kind: mcq|sql_practice, question, options{}, answer, feedback_correct, feedback_incorrect{}, source}`; sql_practice items carry `prompt`, `starter_sql`, `expected_notes`.

### Build pipeline (`build/build.py`, deterministic, stdlib only)

1. Load taxonomy → closed vocabularies.
2. Parse all `content/**/*.md` (no PyYAML — precedent: consultant-eval + cleanse-canvas builders).
3. Validate (errors fail build): required fields, id/filename/folder agreement, vocab membership, duplicate ids, link + wikilink integrity, assessments/paths reference real units, orphan warnings, raw-HTML check.
4. Pre-render bodies via `mdlite.py`; embed BOTH raw md (edit mode needs it) and rendered HTML per unit. Size est. ~3MB at ~300 units; build warns at 6MB (escape hatch: drop embedded HTML, render client-side).
5. Search index: per-unit lowercased blob (title|tags|term|plaintext); client does scored linear scan (title 10 / tag 5 / body 1 + phrase bonus) — <10ms at 300 units; inverted index deferred until >1000 units.
6. Graph data: `{nodes:[{id,type,title,domain,status}], edges:[{s,t,rel}]}` incl. computed inbound edges.
7. Compile `template.html`: substitute `__TOKENS_CSS__`, `__PATTERNS_CSS__`, `__DATA_JSON__` (in `<script type="application/json">`, JSON.parse'd), `__BUILD_META__` (date + content hash); guard leftover `__[A-Z_]+__` placeholders, exit nonzero (consultant-eval `render()` pattern).
8. Emit `dist/chunks.jsonl` + `dist/validation-report.md`; nonzero exit on any error.

`merge_changesets.py`: `--stage` = triage report of inbox; `--apply` = apply `edit` ops whose `base_hash` (sha256 of raw body at build time) matches current body, bump `updated`, move changeset to `applied/`; hash mismatches + note/question/flag ops stay in triage for Claude (questions typically become qa/ draft units). Never auto-forces a conflicting edit.

### App UI (single file, brand kit, hash routing)

Brand-kit `starter.html` scaffold; aurora `body::before` underlay BEFORE glass (mandatory); `.card` glass; violet #5B31EE accent only; `system-ui` stack (Work Sans is PPTX-only per brand-identity.md); tabular-nums on counts. Routes: `#/`, `#/browse/<type>`, `#/unit/<id>`, `#/path/<id>`, `#/search?q=`, `#/graph`.

- **Home**: hero, counts by type, learning-path cards with progress rings, recently-updated, search box.
- **Browse**: type tabs + facet chips (domain/audience/level; deprecated hidden by default).
- **Unit page**: metadata bar, rendered body, cross-refs grouped by relation, computed "Referenced by", sources badges, inline quiz items, prev/next within a path.
- **Search**: `/` shortcut, live scored results with type badges.
- **Learning paths**: ordered steps + assessment checkpoints, progress in `localStorage["em.progress.v1"]`, instant quiz feedback (answers visible in source — accepted for internal tool, documented).
- **Review mode** (header toggle): Propose edit (textarea preloaded with raw md) / Add note / Ask question / Flag (outdated|wrong|conflict|unclear); accumulates in `localStorage["em.changeset.v1"]` with badge; Export downloads changeset JSON via Blob (works on file://). Review-loop pattern applied to knowledge units.
- **Graph view** (Phase 6): no-library SVG force layout ported from dq-studio `ui/static/js/explorer.js` (585-line precedent), color by type, domain filter; per-unit 1-hop mini-graph.
- **Print**: `@media print`, current unit or whole path.
- v1.1+ (after this plan): progress export/import JSON, edit diff preview. Deferred indefinitely: spaced repetition, dark mode, images.

### Seeding pipeline (Claude-driven, one wave per source, parallel subagents within a wave)

Granularity: one vault note = one unit unless >~400 lines or mixed types. Every transformation records `seed-map.json` entries + source repo commit hashes (vault becomes seed-only from that hash).

- **Wave 1 — vault mirror (113 notes)**: sops/→procedures; dq-methodology/→concepts+standards (per-note call); studio-architecture/→reference + principles(decision); sap-knowledge/→reference/concepts (domain sap); thought-leadership/→concepts (audience lead); templates/, ai-related/, syniti-platform/→reference. Tags migrate; wikilinks rewritten to unit ids.
- **Wave 2 — dq-studio**: DQ_RULE_STANDARDS + RULE_PATTERNS → standards(kind:pattern); skills_canonical (7) → standards/reference, `approved`; decisions.json 68 ADRs → batch `prn-adr-NNNN` (mechanical); requirements.json 36 + methodology JSONs → reference; CLAUDE.md non-negotiables → one principles unit.
- **Wave 3 — bob-dq + cleanse-canvas + rule-repo**: ADRs → principles(decision); DATA-MODEL/spec sections → reference; resourcing rubric → procedure. Glossary consolidation: union of bob CONTEXT.md + cleanse CONTEXT.md + rule-repo `_meta` vocab → one gls-* per term with all origins in sources[]; conflicting definitions keep both statements + CONFLICTS.md entry. Process-area overlap seeded as two reference units + contrast links + CONFLICT-002 (open).
- **Wave 4 — academy extraction**: regex-parse `checkAnswer('qN','x','…')` (landing.html) + `answers{}/feedback{}` (sql-pre-assessment.html) → 27 items in assessments.json; Sessions 1–3 → 3 paths in paths.json; uncovered pedagogy prose → new concept units; then move all 3 HTML files to `archive/academy-v1/`.

**Dedup authority order**: dq-studio skills_canonical > vault > academy — most authoritative is the base unit, deltas merged, all origins in sources[], unmergeable disagreements → CONFLICTS.md.

**CONFLICTS.md format**: `CONFLICT-NNN | topic | positions | resolution | status | decided-by, date`. Pre-seeded CONFLICT-001 (seven vs six dimensions): resolved, seven wins; academy quiz items rewritten in Wave 4.

### Changeset JSON (`em-changeset/1`)

`{schema, exported_at, author (self-identified free text), app_build, ops[]}` with ops: `edit` (unit_id, base_hash, new_body), `note` (unit_id, anchor, text), `question` (unit_id nullable for corpus-level, text), `flag` (unit_id, reason, text).

### chunks.jsonl (RAG-ready)

One object per line; split at `##` boundaries, >~500-word sections split at paragraphs; stable ids `unit_id#NN`. Fields: chunk_id, unit_id, seq, type, kind, title, section, domain, audience, level, status, text (plain, wikilinks resolved to titles), links, sources, hash, updated. Embedding caches invalidate on `hash`; later RAG needs zero re-chunking.

## Phasing & verification

| Phase | Work | Done means |
|---|---|---|
| 0. Scaffold | Layout, archive academy HTML, taxonomy.json, CLAUDE.md, 3 sample units | Sample units parse |
| 1. Build + core app | build.py + mdlite.py + template.html; home/browse/unit/search | Build exits 0, zero errors; opens from file:// in Chrome+Edge; rebuild byte-identical |
| 2. Seed wave 1 | Vault → ~113 units, seed-map, CONFLICTS.md | Zero validation errors; spot-check 10 units for render fidelity |
| 3. Seed waves 2–3 | dq-studio, bob, cleanse, rule-repo; glossary; ADR batch; dedup | Link integrity clean; CONFLICT-001/002 logged |
| 4. Paths + assessments | Wave 4; 3 paths; quiz UI + progress | 3 paths playable end-to-end; 27 items migrated (6-dim items rewritten) |
| 5. Feedback loop | Review mode + export; merge_changesets.py | Round-trip demonstrated: edit → export → inbox → --apply → rebuild shows edit |
| 6. Graph + polish | explorer.js port, chunks.jsonl validation, print, docs rewrite | Graph <2s @ ~300 nodes; chunks.jsonl all json.loads clean; README/SETUP/FAQ updated |

Gate throughout: validation report zero errors. Playwright smoke (playwright-skill) at phases 1/4/6: open dist app from file://, search "dimensions", open a unit, complete a quiz step.

## Risks

1. Single-file size ~3MB (fine); warn at 6MB, escape hatch = client-side render from md only.
2. Obsidian-flavor md edge cases → mdlite warnings name file+line, seeding normalizes.
3. Quiz answers in page source → accepted, documented.
4. Changeset conflicts → base_hash never auto-forces; Claude triage.
5. Vault drift after seed → seed commit hash in seed-map.json enables later diff.
6. file:// localStorage origin quirks → documented; progress export/import in v1.1.

## Overnight execution strategy (user-directed, 2026-08-20)

Locked-in answers: **feature branch** `feat/enablement-master` in syniti-dq-coe-projects, commit at each phase gate, push overnight, **PR at end** (not merged). **Quality-first** multi-agent processing. App title: **"DQ Enablement Studio"** (folder/registry name unchanged; "enablement-master" remains the artifact name `enablement-master.html`). Morning bar: **all 6 phases** + morning HANDOFF (state, conflicts, open review items). Run fully autonomously — no user interruption after approval; errors are handled and retried, never waited on.

Orchestration (user opted into multi-agent workflows explicitly):
- **Phases 0–1 (scaffold, build.py, mdlite.py, template.html, core UI)**: engineered directly by the main session (single coherent artifact set; fan-out would fragment it). Verified with build runs + Playwright smoke before any seeding starts.
- **Phases 2–3 (seeding, ~200+ units)**: Workflow-orchestrated pipeline per wave — Sonnet agents transform source notes → units (one agent per note batch), Opus agents review every batch (schema fidelity, taxonomy fit, cross-link quality, dedup collisions), an Opus corpus-level pass at wave end (glossary consolidation, authority-order dedup, CONFLICTS.md entries, link enrichment). Build validation gate after every wave; a failing build blocks the next wave until fixed.
- **Phase 4 (paths + assessments)**: main session (parse job + paths.json authoring), with one Opus review of the 27 migrated items incl. six→seven-dimension rewrites.
- **Phase 5–6 (feedback loop, graph, polish, docs)**: main session; final Opus completeness critic over the whole corpus ("what's missing, unlinked, inconsistent") whose findings become the morning HANDOFF's open-items list.
- Checkpoints: git commit + push at each phase gate; validation-report.md committed each time; morning HANDOFF.md written last, plus updated .vala registry entry.

## Also in scope at close

- Write the design doc (this plan's Design section) to `docs/superpowers/specs/2026-08-20-enablement-master-design.md` in the project and commit per brainstorming skill.
- Update `.vala/projects.json` entry for dq-enablement-studio (handoffRepo → new HANDOFF.md or README, primaryDoc → dist/enablement-master.html, notes rewritten).
- Commit via /vala at session close (per session-flow rules).

