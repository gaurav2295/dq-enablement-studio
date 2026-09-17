# Conflicts log

Where sources (or people) disagree about the methodology, the disagreement is recorded here —
never silently resolved. Format per entry: id, topic, positions (one line per source), resolution,
status (`open` | `resolved`), decided-by + date. Status is exactly one of those two words; who
decided (or that a decision is still pending) lives on the **Decided-by** line. Entries are kept in
numeric order. Units on both sides of an open conflict link each other with `contrast:`.

---

## CONFLICT-001 — How many DQ dimensions?

**Positions**
- vault `dq-methodology/DQ Dimensions.md`: **seven** — Accuracy, Completeness, Conformity, Consistency, Integrity, Timeliness, Uniqueness.
- academy v1 `landing.html` (Session 1 + matching quiz): **six** — Accuracy, Completeness, Consistency, Validity, Timeliness, Uniqueness.

**Resolution**: Seven wins. The vault is seed-canonical; Conformity subsumes Validity, and
Integrity stands alone because referential breakage is the dominant SAP failure mode.
Consequence: academy-derived quiz items teaching six dimensions / "Validity" are rewritten
during the Wave 4 assessment migration. Canonical unit: `con-dq-dimensions`.

**Status**: resolved

**Decided-by**: Truwayne (session decision), 2026-08-20.

---

## CONFLICT-002 — Process-area taxonomies overlap unreconciled

**Positions**
- bob-dq (spec §1.3): L3 "process areas" as the middle tier of the L1–L5 outcome hierarchy.
- data-cleanse-canvas (`docs/DATA-MODEL.md`): **12 process areas** ("cleanse atoms") plus **6 Business Process Areas** (Source-to-Contract, Procure-to-Pay, Plan-to-Maintain, Transportation & Logistics, Record-to-Report, …) as aggregation dimensions.

**Resolution**: none yet. Both taxonomies are seeded as separate units linked with `contrast:` —
`con-outcome-hierarchy-l1-l5` (the bob-dq L1–L5 side, seeded in batch w3-bob-method) and
`ref-cleanse-process-areas` (the cleanse side); reconciling them into one canonical process-area
model is a CoE decision.

**Status**: open

**Decided-by**: pending CoE — logged by Claude seed session 2026-08-20.

---

## CONFLICT-003 — Rule-name heuristics total weight: 60.5 or 70.15?

**Positions**
- `ref-rule-name-scorer` (vault-seeded, prose summary): stated total weight of all 19 heuristics as **70.15**.
- dq-studio `knowledge/methodology/heuristics.json` (authoritative, machine-summed): the 19 weights (7, 5, 5, 5, 5, 4, 3.5, 3.5, 3.25, 3, 2.4, 2.25, 2.15, 2, 2, 1.85, 1.5, 1.1, 1) sum to **60.5**.
- `std-rule-name-heuristics` already carried a note flagging 70.15 as an earlier mining-note figure and using 60.5 as authoritative.

**Resolution**: 60.5 wins — dq-studio content (the actual scoring JSON) outranks the vault-seeded
prose summary per the authority order. `ref-rule-name-scorer` corrected in place to state 60.5 and
cross-reference `std-rule-name-heuristics` for the breakdown; `dq-studio:knowledge/methodology/heuristics.json`
added to its sources.

**Corpus note**: `ref-rule-name-scorer` (unit archived to dev-corpus 2026-08-21).

**Status**: resolved

**Decided-by**: batch w2-heuristics, 2026-08-20.

---

## CONFLICT-004 — What database does a generated rule SELECT FROM?

**Positions**
- dq-studio `.claude/skills_canonical/studio-architecture.md` (skill file dated 2026-04-30): **`prep_db`** — "every FROM/JOIN qualifier MUST be `prep_db` (`WRKDQPREP_ALL`). Never `source_db`." Common-bug list names `arch.prep_db or arch.source_db` as the correct generator expression.
- Seeded units `ref-three-database-architecture` / `ref-profiling-view-generation` / `ref-architecture-context-and-project-yamls`: **`working_db`** (`WRKDQ`) — one repository, rules are CREATEd in and SELECT FROM `WRKDQ`; `WRKDQPREP_ALL` is the upstream prep layer whose output is pushed into `WRKDQ` (KNOWN-ISSUES B4, fixed 2026-07-01).

**Resolution**: `working_db` wins. Verified against current dq-studio code, which post-dates the
skill file: `core/sql_generator.py:188-195` (`from_db = arch.working_db or arch.source_db`, with
the comment "FROM target = working_db (WRKDQ), the ONE rule repository"), `:281-283` (InfSel) and
`:1416-1418` (RptSel JOIN qualification). The skill captured the pre-B4 state. Both sources agree
on the parts that still hold and are kept: **never** `source_db` in a FROM/JOIN, CREATE VIEW
qualifier is `working_db`, and catalog `{datastore}` substitution genuinely does target `prep_db`
(`core/catalog_deriver.py:232`) — that is a real asymmetry, not a bug. See also `prn-adr-048`,
which states the prep-DB position and is now narrower than the code.

**Corpus note**: `ref-three-database-architecture`, `ref-profiling-view-generation`,
`ref-architecture-context-and-project-yamls` and `prn-adr-048` (units archived to dev-corpus
2026-08-21).

**Status**: resolved

**Decided-by**: code verification, 2026-08-20.

---

## CONFLICT-005 — Which YAML key is the authoritative fan-out scope?

**Positions**
- dq-studio `.claude/skills_canonical/studio-config-shape.md` + `studio-multi-impl.md`: **`source_systems`** is authoritative; `system_aliases.keys()` is "the SOFT-MIGRATION fallback for legacy YAMLs" and using it as fan-out scope is listed as a bug.
- Seeded units `ref-architecture-context-and-project-yamls` / `ref-multi-impl-fan-out-engine` / `con-multi-implementation-model`: **`system_aliases` keys** are authoritative; `source_systems` is the legacy fallback, and a one-time WARNING logs when both are set and disagree.

**Resolution**: `system_aliases` keys win. Verified against current dq-studio code:
`core/architecture.py:200-231` ("`system_aliases` keys are the …" / "`source_systems` is the legacy
fallback", plus the disagreement WARNING naming "system_aliases keys win … source_systems list
IGNORED"), `_EDITABLE_PROJECT_KEYS` line 47 comments `source_systems` as "legacy fan-out scope
(kept for back-compat)", and `pipeline/bulk_processor.py::_expand_implementations`, whose
precedence tier 3 is "Project's `system_aliases` keys". The skills' *independence* rule survives
intact and is the substantive point: display alias values must never affect deployment scope, and
editing aliases must never silently change it — what the skills got wrong is only which key is the
legacy one.

**Corpus note**: `ref-architecture-context-and-project-yamls` and `ref-multi-impl-fan-out-engine`
(units archived to dev-corpus 2026-08-21).

**Status**: resolved

**Decided-by**: code verification, 2026-08-20.

---

## CONFLICT-006 — How many implementations does one profiling rule produce?

**Positions**
- Seeded units `con-multi-implementation-model` / `con-profiling-concepts` / `ref-multi-impl-fan-out-engine` (summary line): **two** implementations per profiling rule — PrfSel and PrfSum as sibling view-type impls sharing one `SKP_RULE_NNNN`.
- dq-studio `.claude/skills_canonical/studio-multi-impl.md` + `studio-profiling.md`: **one** — one profiling row → one `DQRuleSpec` carrying two SQL views (`sql_optsel` = PrfSel, `sql_rptsel` = PrfSum) under a single DQOps ID, `view_type` left blank. The two-spec model is named explicitly as the OLD model that was replaced.

**Resolution**: one spec, two views. The skill wins and is code-confirmed —
`pipeline/bulk_processor.py::_expand_implementations` early-returns `[impl]` for
`rule_type == "profiling"` with `view_type = ""` and `system_filter = ""`, one DQOps ID locked to
the SKP numeric portion. Consequence: one tracker row per profiling rule, ViewType rendered as the
paired literal `"PrfSel + PrfSum"`. Note the docstring header in that same function still
describes "always 2 implementations" — stale prose above correct code, worth a dq-studio cleanup.

**Corpus note**: `ref-multi-impl-fan-out-engine` (unit archived to dev-corpus 2026-08-21).

**Status**: resolved

**Decided-by**: dq-studio skill + code verification, 2026-08-20.

---

## CONFLICT-007 — Which element comes first in zConcatenatedKey?

**Positions**
- dq-studio `docs/DQ_RULE_STANDARDS.md` (via `std-zconcatenatedkey-convention`) and `docs/Studio_Overview.md` §2.1: `zSourceSystemID` is **always the first element** — `CONCAT(zSourceSystemID, '_', <pk1>, '_', <pk2>, …)`. Code-confirmed on the local-derive path: `core/sql_generator.py::_collect_concat_key_fields` comments "zSourceSystemID always goes first" and inserts it at position 0.
- dq-studio `core/catalog_promotion.py:262` and `:796` (via `ref-catalog-promotion`): the catalog/promotion path emits **key first, system last** — `CONCAT(src.<key_field>, '_', src.zSourceSystemID) AS [zConcatenatedKey]`.

**Resolution**: none yet — this is a live code inconsistency inside dq-studio, not a documentation
disagreement. Separator (`_`) and NULL-safety are already identical across both paths; only
argument order differs, so the same business record derived via the catalog route and via the local
route produces two different `zConcatenatedKey` values, which breaks any cross-route comparison or
join on that key. The standard (system-first) is the stated methodology and should win, but
changing the promoter's order silently re-keys every already-deployed catalog-derived view — so the
fix needs a migration decision, not just an edit. Units linked with `contrast:`.

**Corpus note**: `ref-catalog-promotion` (unit archived to dev-corpus 2026-08-21) — the
`contrast:` edge on this side no longer has a unit to point at.

**Status**: open

**Decided-by**: pending CoE — raised from `dq-studio:docs/Studio_Overview.md` §2.1 + code read,
2026-08-20.

---

## CONFLICT-008 — What belongs in Value Context and Activity Context?

**Positions**
- vault `dq-methodology/Output Field Sections.md` (seed): **Value Context = "the field(s) under check + supporting values"** — a UoM rule files `MEINS` there, a date-comparison rule files its dates there; **Activity Context = "dates, status flags, posting indicators"**.
- dq-studio `docs/ai_enhance_instructions.md` (the live rule-fulfilment prompt): **Value Context = ONLY money, amounts and financial values** (`NETWR`, `STPRS`, `VERPR`, `DMBTR`, prices, costs, rates, percentages, `WAERS`) — "NEVER put dates here, NEVER put organizational fields here"; **Activity Context = ONLY dates, times and temporal fields** — "NEVER put monetary values here". Type/descriptive fields that identify the master record go to **Basic Fields**.

**Resolution**: dq-studio wins (authority order: dq-studio content > vault-seeded units). The
section is decided by *what kind of field it is*, not by whether the rule happens to be checking
it. `std-output-field-sections` is updated: the five-section table now carries the one-question
test per section, the exact prompt definitions are reproduced, and the worked example moves
`MTART`/`MEINS` from Value Context into Basic Fields with monetary fields (`STPRS`/`WAERS`) taking
their place. Tie-breaker for any individual field remains the per-field `classification` lookup in
`SAP_ECC_Complete.json` — a lookup, not a judgement call.

**Consequence — applied**: `std-optsel-select-structure`'s worked example showed `MARA.MEINS`
under Value Context and `MARA.MTART` under Organizational Context (a third placement again). Both
moved into Basic Fields, the Organizational and Value headers left deliberately empty, and the
skeleton's Value Context placeholder changed from `<CheckedField>` to
`<AmountOrCurrencyField>`. Applied during the review of batch w2-ai, 2026-08-20.

> [!note] Scope of this entry
> This entry once carried a secondary, unresolved nuance about whether the Syniti Technical Fields
> are "ALWAYS these three" when the Studio also emits `zDomainSegment`. That question is not about
> Value/Activity Context at all and has been struck from here — it lives in **CONFLICT-019**
> (technical-field membership, open). This entry is closed on its primary question.

**Status**: resolved

**Decided-by**: authority order (dq-studio prompt over vault seed) — raised from
`dq-studio:docs/ai_enhance_instructions.md`, 2026-08-20; nuance split out to CONFLICT-019
2026-08-20.

---

## CONFLICT-009 — Which spelling do the SELECT-section headers use?

**Positions**
- dq-studio `docs/DQ_RULE_STANDARDS.md` §3.4: headers are `-- Syniti Technical Fields`, `-- Basic Fields`, `-- Organizational Context Fields`, `-- Value Context Fields`, `-- Activity Fields`.
- dq-studio `CLAUDE.md` non-negotiables + `core/sql_generator.py` (via `ref-sql-comment-and-formatting-standard`): headers are `-- Organizational Context`, `-- Value Context`, `-- Activity Context` — no trailing "Fields" — and the parser switches `current_section` on these exact strings.

**Resolution**: neither spelling is wrong; the disagreement is cosmetic and the standing
instruction closes it. Section **order** and **membership** are identical across both sources and
the order is the part that is validated (`std-req-sql-section-header-order`), so: match the
spelling a project's existing rules already use, and never mix both inside one package. Both
spellings are documented in `std-output-field-sections`, which carries the instruction. Units on
the two sides are linked with `contrast:` — `std-output-field-sections` and
`ref-sql-comment-and-formatting-standard`.

**Corpus note**: `ref-sql-comment-and-formatting-standard` and `std-req-sql-section-header-order`
(units archived to dev-corpus 2026-08-21) — the `contrast:` pair named above no longer exists;
`std-output-field-sections` carries both spellings on its own.

> [!note] Split
> This entry originally bundled two questions: header spelling (this one, now resolved) and what
> counts as a Syniti Technical Field. The membership question was never settled by the resolution
> above and is now tracked separately as **CONFLICT-019** (open), which also absorbs the secondary
> nuance struck from CONFLICT-008.

**Status**: resolved

**Decided-by**: standing instruction recorded during batch w2-standards from
`dq-studio:docs/DQ_RULE_STANDARDS.md`, 2026-08-20; membership half split out 2026-08-20.

---

## CONFLICT-010 — Is zConcatenatedKey trimmed and null-substituted?

**Positions**
- dq-studio `docs/DQ_RULE_STANDARDS.md` §3.1: every element is wrapped — `CONCAT(COALESCE(TRIM(zSourceSystemID),'NA'), '_', COALESCE(TRIM(KUNNR),'NA'), …)`. The stated requirements are uniqueness, `zSourceSystemID` included, all relevant PK fields included, null values handled safely, built with `CONCAT`.
- Seeded unit `std-zconcatenatedkey-convention` (vault): "Underscores between fields. **No padding. No trimming. No type coercion**", with a bare `CONCAT(zSourceSystemID, '_', <pk1>, …)` template.

**Resolution**: the standards doc wins — dq-studio content outranks the vault seed per the
authority order, and the mechanism is load-bearing rather than cosmetic. `TRIM` matters because SAP
CHAR columns carry trailing blanks, so an untrimmed key gives the same record two different key
values depending on which table it was read from; `COALESCE(...,'NA')` matters because a NULL
element would otherwise degrade the whole key. This also aligns the unit with
`std-req-sql-null-unsafe-key-concat` and with the NULL-safe-CONCAT position already recorded in
`ref-output-section-builders` (KNOWN-ISSUES B3, fixed 2026-07-01). `std-zconcatenatedkey-convention`
corrected in place; the "no trimming, no padding" sentence is removed and the doc added to its
sources. Argument **order** is a separate, still-open question — see CONFLICT-007.

**Corpus note**: `std-req-sql-null-unsafe-key-concat` and `ref-output-section-builders` (units
archived to dev-corpus 2026-08-21).

**Status**: resolved

**Decided-by**: authority order (dq-studio doc over vault seed), batch w2-standards, 2026-08-20.

---

## CONFLICT-011 — Where does the system token sit in a view name?

**Positions**
- dq-studio `docs/DQ_RULE_STANDARDS.md` §2 + §3.5 (the human-authored standard): the base format is `DQ_[RuleNumber]_[ObjectName]_[Description]_[Suffix]`, and the multi-system token goes **immediately before the suffix** — `DQ_[####]_[Object]_[Description]_{{SYSTEM}}_OptSel`. Tokens are double-brace (`{{SYSTEM}}`, `{{DATABASE_NAME}}`) and substituted by the repository generator (`generate-dq-rules.js`); there is no `{field}` slot.
- Seeded unit `std-view-naming-patterns` (from vault + Studio code): `DQ_{id}_{system}_{table}_{field}_{desc}_{ViewType}` — the system token sits **directly after the rule id**, tokens are single-brace, and a `{field}` slot sits between table and desc. Code-confirmed: `core/architecture.py::resolve_view_name` plus the aligned dataclass / `from_dict` / YAML-resolver defaults (KNOWN-ISSUES B2 + B6, fixed 2026-07-01).

**Resolution**: none yet — both are in production, on different generation paths. The standards
doc describes the repository-template path; `std-view-naming-patterns` describes the Studio
resolver, and the Studio's SQL parser, its `view-name-rule-id-mismatch` check and SKP's
Opportunity/Error Query columns all key off whichever order a project already deployed. Renaming
deployed views to converge is a migration, not an edit. Both orders are documented in
`std-view-naming-patterns` with the warning that they must not be mixed within a project.
Converging on one canonical order is a CoE decision.

> [!note] No `contrast:` unit pair exists for this conflict
> The competing side is a **document**, not a knowledge unit: the token order lives only in
> `dq-studio:docs/DQ_RULE_STANDARDS.md` §2/§3.5, and no unit in this corpus carries it as its own
> position. `std-view-naming-patterns` documents **both** orders inside one unit (see its "Two live
> token orders" warning), and `std-req-sql-view-naming-pattern` states the Studio order only. So
> the log's "both sides link each other with `contrast:`" rule has nothing to link here — if the
> repository-template path is ever seeded as its own unit, add the edge then.

**Corpus note**: `std-req-sql-view-naming-pattern` (unit archived to dev-corpus 2026-08-21).

**Status**: open

**Decided-by**: pending CoE — raised from `dq-studio:docs/DQ_RULE_STANDARDS.md` during batch
w2-standards, 2026-08-20.

---

## CONFLICT-012 — Which list is "the 19 rule-name heuristics"?

**Positions**
- dq-studio `knowledge/methodology/heuristics.json` (the file the scorer actually loads): 19 grammar/symbol heuristics with numeric weights summing to 60.5 — *Single Sentence, Modal Phrase Required, Detectable Pattern, Number Context Required, No Technical Names, No SQL Keywords, …*. Enumerated in `std-rule-name-heuristics`.
- vault `sops/SOP — Write a Quality Rule Name.md`, seeded into `prc-write-a-quality-rule-name`: a *different* 19-item list with High/Medium/Low weights — *Length ≤ 100, Length ≤ 85, Starts with an article, Preserves SAP acronyms, No version/sprint numbers, No client name, Plain ASCII, No trailing punctuation, …* — introduced with the claim that "the Studio's rule-name scorer (`core/rule_name_scorer.py`) runs each rule name through these checks".

**Resolution**: both lists are real, but only one is the scorer's. `heuristics.json` wins as the
description of what the scorer computes — verified against `core/rule_name_scorer.py:146-192`,
which has no length, ASCII, acronym, punctuation or client-name check of any kind. The SOP's list
is a **human authoring checklist**: it captures naming conventions (the ≤100/≤85 ADM limit, acronym
preservation, timelessness) that are enforced elsewhere — the length cap in the rule-name builder /
local-deriver path, the rest by the consultant. The two units already carry the caveat that name
length is not scored (`std-rule-name-heuristics`, `ref-rule-name-scorer`). Fixed in place:
`prc-write-a-quality-rule-name`'s introductory sentence no longer attributes its list to the
scorer, and **both** units now carry a short note stating that the two 19-item lists are unrelated
and that the shared count of 19 is a coincidence. Still open: the coincidence itself will keep
misleading readers — the CoE should either renumber the SOP list or fold its scorable items into
`heuristics.json`.

Both units are already linked (`prc-write-a-quality-rule-name --implements--> std-rule-name-heuristics`,
plus `relates:ref-rule-name-scorer`), so no additional `contrast:` edge was added.

**Corpus note**: `ref-rule-name-scorer` (unit archived to dev-corpus 2026-08-21) — the caveat it
carried now lives only in `std-rule-name-heuristics` and `prc-write-a-quality-rule-name`.

**Status**: open

**Decided-by**: pending CoE — raised during the review of batch w2-heuristics, 2026-08-20.

---

## CONFLICT-013 — Is `'<code>' AS [zSourceSystemID]` a template or a blocking violation?

**Positions**
- dq-studio `docs/DQ_RULE_STANDARDS.md` §3.5 (the human-authored repository standard): the
  `zSourceSystemID` literal is written as `'{{SYSTEM}}'` — a double-brace placeholder token
  substituted per source system by the repository generator (`generate-dq-rules.js`), alongside
  `{{DATABASE_NAME}}`. The rendered file therefore ships `'ECC' AS [zSourceSystemID]` (§3.3's own
  worked example). The template is not deployed directly.
- dq-studio `docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md` §4/§6 + `docs/ai_enhance_instructions.md`
  (the Studio path): `'<code>' AS [zSourceSystemID]` is **never valid anywhere in generated SQL** —
  `_check_hardcoded_system_id_literal`, High severity, on `AI_ENHANCE_BLOCKING_CHECKS`, and
  auto-repaired to a column reference by `attempt_ai_enhance_autorepair`. The value must always be
  a live column reference off the driving table.

**Resolution**: none yet — two generation paths, same as CONFLICT-011. The repository-template path
predates the Studio and treats the literal as a pre-substitution token; the Studio derives against
`WRKDQ`, where `zSourceSystemID` is a real column on every table, so a literal there fabricates
provenance and silently survives a system change. For anything the Studio generates or enhances,
the column reference is mandatory and the literal blocks the save. Whether the repository template
should converge on the column reference (it could — the substituted views read the same
Syniti-loaded tables) is a CoE decision, because re-rendering the repository re-keys nothing but
does touch every deployed template file. Both positions are documented in
`std-output-field-sections` (the `{{SYSTEM}}` worked example) and `std-ai-enhance-guardrails`, and
those two units are linked with `contrast:`.

**Status**: open

**Decided-by**: pending CoE — raised from `dq-studio:docs/AI_ENHANCE_GUARDRAILS_AND_HARNESS_RULES.md`
during the review of batch w2-ai, 2026-08-20.

---

## CONFLICT-014 — Which navigation does the Studio actually have: seven task pages, or four spaces?

**Positions**
- Seeded page units `ref-home-page` / `ref-single-rule-designer` / `ref-bulk-pipeline` /
  `ref-profiler-and-audit-pages` / `ref-config-editor` / `ref-skp-assetupload-and-tracker-flow`
  (from the vault mirror): **seven page routes** — `/`, `/single`, `/bulk`, `/profiler`, `/audit`,
  `/skp`, `/config` — each rendering its own Jinja template (`single.html`, `bulk.html`,
  `profiler.html`, `skp.html`, `config.html`), with a sidebar grouped Design / Integrate.
- dq-studio `knowledge/methodology/capabilities.json` (via `con-studio-capabilities`): named
  **spaces** — Session Setup, Schema Profile, DQ Rules / Workspace, Attribute Usage, Ship — with
  `execute.href` values `/profile#schema`, `/workspace`, `/profile#aua`.

**Resolution**: the spaces model is current; the seven-page model is the superseded UI. Verified at
the pinned seed commit `c6d6f9d`: `app.py` declares `/`, `/workspace`, `/profile`, `/ship`,
`/audit`, `/settings`, `/methodology`, and `ui/templates/` contains only `home.html`,
`workspace.html`, `profile.html`, `ship.html`, `audit.html`, `settings.html`, `methodology.html` —
there is no `single.html`, `bulk.html`, `profiler.html`, `skp.html` or `config.html`. The old paths
survive only as a legacy redirect map (`app.py:229-233`): `/single` → `/workspace`,
`/bulk` → `/workspace`, `/profiler` → `/profile`, `/config` → `/settings`, `/skp` → `/ship#skp`.

Consequence: the page units' *engine* content is unaffected and remains accurate — what was stale
was their route/template/nav framing and the `app.py` line citations that go with it.

**Sweep done**: 15 units reconciled onto the spaces model across the corpus, 2026-08-21, using the
mapping `/single` → `/workspace`, `/bulk` → `/workspace`, `/profiler` → `/profile`,
`/config` → `/settings`, `/skp` → `/ship` (SKP tab). The six page units named above — being *about*
the pages themselves — keep the legacy path noted parenthetically (e.g. "`/workspace` (formerly
`/single`)") so a consultant following an old link is not lost. The other nine
(`con-studio-capabilities`, `con-attribute-usage-analysis`, `prc-fan-out-a-rule-per-system`,
`prc-generate-a-profile-bundle`, `prc-generate-the-skp-assetupload`,
`prc-ingest-a-client-dd-dictionary`, `prc-run-an-attribute-usage-analysis`,
`prc-run-the-bulk-pipeline`, `ref-building-a-per-client-dd-dictionary`) only instruct the user where
to click, so their mentions were rewritten straight to the current route with no parenthetical.

**Status**: resolved

**Decided-by**: mechanical sweep per CONFLICT-014's own resolution note, 2026-08-21.

---

## CONFLICT-015 — Is "Reduce unplanned downtime" a live candidate outcome, or cut?

**Positions**
- bob-dq `CONTEXT.md` (via `gls-business-outcome`): a **candidate** outcome, pending confirmation
  that the chain walks down to rules for it (R3, 2026-08-04).
- bob-dq `bob-dq-solution-spec.md` §1.3 (via `con-outcome-hierarchy-l1-l5`): **CUT 2026-08-06** on
  the walkability test — 6 rules across 2 drivers, 16 of 18 EAM drivers empty. The published v1
  catalogue is six outcomes.

**Resolution**: the spec wins — it is canonical in bob-dq ("if they diverge, the spec wins") and
its ruling is two days later than the CONTEXT.md line, so this is staleness rather than a real
methodological disagreement. `gls-business-outcome` corrected in place: the candidate line now
records the cut, that it is held as a re-propose candidate once manufacturing rules land, and
links to `con-outcome-hierarchy-l1-l5` for the six-outcome catalogue.

**Status**: resolved

**Decided-by**: canonicity + date, during the review of batch w3-bob-method, 2026-08-20.

---

## CONFLICT-016 — "Directional" or "indicative"?

**Positions**
- bob-dq `business-outcomes-blueprint-solution-overview.md` §7 (via `prn-value-discipline`):
  "**directional vs audited** — explicitly labelled, never blurred".
- bob-dq `CONTEXT.md` + `bob-dq-solution-spec.md` changelog A7 (via `gls-indicative`):
  **"indicative" is the standing word for every figure**; *directional* and *projected* are banned
  — "directional" implies a trend the data does not support.

**Positions are about the same discipline, not different ones**: both want a figure's epistemic
status labelled; they disagree on the word.

**Resolution**: *indicative* wins. A7 explicitly retires "directional" → "indicative" throughout,
and the overview is marked reference-only and superseded for #bob-dq by the spec. The labelling
requirement survives intact — `prn-value-discipline` now reads "indicative vs audited", records
the overview's original wording and why it was retired, and links `gls-indicative`.

**Status**: resolved

**Decided-by**: authority order (spec over the superseded overview), during the review of batch
w3-bob-method, 2026-08-20.

---

## CONFLICT-017 — How many provenance values does a rule-repo record have?

**Positions**
- rule-repo `README.md` ("Provenance model"): **three** — `field_proven` | `ai_generated` |
  `template_compliant`, with `field_proven` vs `ai_generated` as the operative distinction and an
  optional `agent_decided: true` flag alongside.
- rule-repo `data/catalogue.json` `_meta.provenance_values` (the metadata that ships with the
  data): **two** — `field_proven` and `derived`. `derived` matches none of the README's three
  names; `ai_generated` and `template_compliant` appear nowhere in `_meta`.
- Same file, `_meta.provenance_semantics`: stricter still — "every entry carries
  provenance='field_proven' (Fable ruling F1)", i.e. the served catalogue instantiates **one**
  value, while `_meta.composition` still labels 113 of the 497 pipeline rules
  `derived_for_lever_coverage`.

**Resolution**: none yet. The catalogue's own `_meta` is the runtime authority (it loads with the
data, so it travels with it), and `field_proven` | `derived` is the vocabulary the corpus uses —
`gls-provenance` and `con-rule-provenance-model` both define that pair, and
`con-rule-provenance-model` carries the drift callout. What is unresolved is whether
`ai_generated` / `template_compliant` are dead schema lineage that the README should drop, or a
fuller vocabulary the data has simply not reached yet — and whether `derived` is meant as a
rename of `ai_generated` or as a distinct third thing. Only the rule-repo owner can settle that;
until then no unit here presents the three-value set as current. The two units carrying the
positions — `gls-provenance` (the two served values) and `con-rule-provenance-model` (the drift
against the README's three) — are linked with `contrast:`.

**Status**: open

**Decided-by**: pending rule-repo owner — raised from `rule-repo:README.md` +
`rule-repo:data/catalogue.json` (`_meta`) during the review of batch w3-rulerepo, 2026-08-20.

---

## CONFLICT-018 — "Coverage" names two different things, one of which forbids the other's form

**Positions**
- bob-dq `CONTEXT.md` + `CLAUDE.md`: **coverage = which outcomes *could be evidenced*** given the
  scope in play. Explicitly **not a completeness score**, and explicitly never expressed as a
  percentage — a percentage invites the reader to hear completeness or quality.
- dq-studio (audit engine `_check_coverage`; Attribute Usage `qualifies_for_deep_dive`):
  **coverage = a computed ratio** — whether a rule family spans every expected source system, and
  the share of a column's rows captured by its top-K values (thresholded at 0.80).

**Resolution**: none yet. Both are correct in their own lens and neither is wrong internally; the
collision is the *word*, and it is load-bearing because one lens forbids exactly the form the other
lens produces. Interim rule, applied in the units: `gls-coverage` carries the client-facing
definition plus an explicit "second, unrelated sense" section, and links `contrast:ref-audit-engine`;
Studio units keep the technical usage but should say **system coverage** or **coverage qualifier**
rather than bare "coverage". A CoE decision could either rename the Studio-side measures or accept
the homonym formally.

**Corpus note**: `ref-audit-engine` (unit archived to dev-corpus 2026-08-21) — `gls-coverage` no
longer carries the `contrast:` edge named above.

**Status**: open

**Decided-by**: pending CoE — raised during the glossary consolidation pass, 2026-08-20.

---

## CONFLICT-019 — What counts as a Syniti Technical Field?

Split out of CONFLICT-009 (whose header-spelling half is resolved), and absorbing the secondary
nuance struck from CONFLICT-008. Four sources give four different technical-field lists.

**Positions**
- dq-studio `docs/DQ_RULE_STANDARDS.md` §3.4: **three** — the technical section is "always exactly `zSourceSystemID`, `zConcatenatedKey`, `zIsErrorFlag`, in that order".
- dq-studio `docs/ai_enhance_instructions.md` (the live rule-fulfilment prompt): the same **three**, stated as a closed list — "ALWAYS these three".
- Seeded unit `std-output-field-sections`: **four** — the three above plus `zDomainSegment`, which the Studio's generated views emit in that same section (conditionally, on Customer/Vendor/Material master tables).
- dq-studio `knowledge/methodology/view_conventions.json`: OptSel `tech_fields` lists **five** — `zDQOpsID`, `zRuleName`, `zSourceSystemID`, `zConcatenatedKey`, `zIsErrorFlag`.

**Resolution**: none yet. The standards doc's three are the mandatory core and nothing disputes
them. `zDomainSegment` is a live Studio addition, best read as minimum-vs-maximum rather than a
contradiction — the prompt's "ALWAYS these three" states a floor, and the generator emits a fourth
field above it. `view_conventions.json`'s `zDQOpsID` / `zRuleName` are the genuinely unexplained
pair: they appear in neither the seeded units nor the standards doc, and need verifying against
emitted SQL before either list is called canonical. Until then `std-output-field-sections`
documents the three-plus-`zDomainSegment` reading and flags the rest. Units on the two sides are
linked with `contrast:` — `std-output-field-sections` and `ref-sql-comment-and-formatting-standard`.

**Corpus note**: `ref-sql-comment-and-formatting-standard` (unit archived to dev-corpus
2026-08-21) — the `contrast:` pair named above no longer exists.

**Status**: open

**Decided-by**: pending CoE — raised from `dq-studio:docs/DQ_RULE_STANDARDS.md` +
`knowledge/methodology/view_conventions.json` during batch w2-standards, 2026-08-20; split out of
CONFLICT-009 and merged with the CONFLICT-008 nuance, 2026-08-20.

---

## CONFLICT-020 — Does the Studio have user accounts, organizations, and a login flow?

**Positions**
- academy v1 Session 3 (`archive/academy-v1/index.html#create-account`, `#session-config`):
  describes a cloud-style onboarding — "Create New Account", email verification, per-user
  timezone/language settings, an auto-created "organization" you invite colleagues into, a
  "Session" as a named container you create from a Dashboard holding system connections plus a
  stored (encrypted) Claude API key, and an "Export Format" choice of SQL/T-SQL/Snowflake dialect.
- Verified corpus (`ref-home-page`, `ref-ports-install-and-versioning`, `ref-config-editor`,
  `ref-ai-client-conventions`): the shipped Studio is a **locally-run FastAPI app**
  (`python app.py` → `http://localhost:8501`), with **no accounts, no login, no organizations**.
  The unit of configuration is a **project** (`config/projects/<id>.yaml`, e.g. `sap_ecc`,
  `sap_s4hana`), edited on the Settings/Config page — not created from a Dashboard. There *is* a
  real per-session API key override (`_resolve_ai_key`: request > session > env
  `ANTHROPIC_API_KEY`), which is the one part of the academy narrative that holds up; "encrypted
  storage" and an "Export Format" dialect choice are not attested anywhere else in the corpus.

**Resolution**: the verified corpus wins for anything a consultant would act on.
`prc-studio-onboarding` is written against the real app — launch locally, pick/configure a
project, optionally set a session-level API key, orient via the current capability spaces — and
does not carry forward the account/organization/login framing. The academy content is preserved
here as a paper trail (it may describe an earlier design intent, or a hosted variant that was
never shipped); no unit should present accounts, organizations, or a login flow as current
behavior.

**Corpus note**: `ref-ports-install-and-versioning` and `ref-ai-client-conventions` (units archived
to dev-corpus 2026-08-21) — of the verified-corpus side, `ref-home-page` and `ref-config-editor`
remain in `content/`.

**Status**: open

**Decided-by**: pending CoE — raised while mining academy Session 3
(`archive/academy-v1/index.html`) into `prc-studio-onboarding`, 2026-08-21. Only a CoE decision
(or someone who can date-check the original design) can say whether an account layer was ever
real and got removed, or was never built.
