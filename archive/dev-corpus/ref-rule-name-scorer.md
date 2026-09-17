---
id: ref-rule-name-scorer
type: reference
title: Rule-Name Scorer (engine)
domain: studio
audience: [developer]
level: advanced
status: review
links:
  - implements:std-rule-name-heuristics
  - relates:ref-single-rule-designer
  - relates:ref-local-deriver
  - relates:ref-rule-type-detection
  - relates:ref-dqrulespec-data-model
  - relates:ref-profiling-view-generation
  - relates:prc-write-a-quality-rule-name
sources:
  - vault:studio-architecture/Studio — Rule-Name Scorer (engine).md
  - dq-studio:knowledge/methodology/heuristics.json
tags: [studio, engine, methodology, scoring]
created: 2026-08-20
updated: 2026-08-20
---

## Summary

`score_rule_name(name, heuristics=None, rule_type=None)` scores a candidate DQ rule name as
`earned_weight / total_weight` over the data-driven 19-heuristic set loaded from
`heuristics.json`, evaluating each heuristic through a fixed dispatch precedence (structural
pattern → number guard → anti-regex → simple regex) and modulating that scoring per rule type —
fully suspended for Profiling, relaxed for Info.

The heuristics themselves (names, weights, regexes) are enumerated in
[[std-rule-name-heuristics]]; this note documents the *engine* that runs them. It is invoked by
the [[ref-single-rule-designer]] (live scoring as you type) and by [[ref-local-deriver]] when
validating a derived name.

## What it does

- Loads heuristics from `knowledge/methodology/heuristics.json` (default path resolved at
  `rule_name_scorer.py:26-31`). The set is **data-driven**: edit the JSON and restart to change
  scoring — no code change. Total weight of all 19 = **60.5** (see [[std-rule-name-heuristics]]
  for the per-heuristic breakdown — an earlier mining note here cited 70.15; the JSON sums to
  60.5).
- Returns a `ScoringResult` (`rule_name_scorer.py:67-87`): `score` (0.0–1.0, rounded 4 dp),
  `score_pct` (0–100), `total_weight`, `earned_weight`, `passed_count`, `total_count`,
  `passed`/`failed` lists, `suggestions`, `suspended`, `suspended_reason`.
- **Score formula** (`:321`): `score = earned_weight / total_weight` (0.0 if total is 0).
  `score_pct = round(score * 100)` (`:332`); weights rounded 2 dp. A heuristic contributes its
  weight to `total_weight` always, and to `earned_weight` only when it passes.
- `suggestions` are built from the **failed** list — each formatted `"{name} (weight {weight}):
  {description}"` (`:323-328`). All-pass emits `"Perfect score -- all heuristics pass."`.

## Dispatch precedence — `_evaluate_heuristic` (`:146-192`)

Each heuristic is evaluated by trying these branches **in fixed order**; first applicable branch
wins:

1. **Structural / `pattern`** (no regex; recognised by substring of the pattern text):
   - `"!name.includes"` → Single Sentence: pass when `". "` (period-space) NOT in name.
   - `"W.length"` → Must Have Subject: pass when `len(words) >= 3`.
   - `"second word"` / `"plural"` → Singular Subject: 2nd word must not look plural, unless in
     the exception list.
   - **Unknown structural pattern → pass** (graceful degradation for future heuristics;
     `:165-167`).
2. **`number_detect` guard** (Number Context Required only, `:170-176`): if the name has **no
   number → auto-pass**; if a number is present, the main regex must match (verb/preposition near
   the number).
3. **Compound `anti_regex`** (Strong Modal Required only, `:179-182`): pass = `primary_match AND
   NOT anti_match` (e.g. has "must" AND no weak modal should/shall/can/may).
4. **Simple `regex`** (`:185-189`): when `fail_when == "matches"` → pass when it does NOT match
   (the "No …" guards); otherwise pass when it matches.
5. **No criterion → pass by default** (`:192`).

> [!note] JS-flag conversion
> Heuristic logic is authored JS-style in the JSON. Only the `"i"` (IGNORECASE) flag is honoured
> (`_re_flags`, `:138-143`); all other JS regex flags are dropped on the Python side.

The **plural-exception list** (Singular Subject) is verbatim (`:132-135`): `is, has, was, does,
series, status, process, address, gross, business, class, goods` — a 2nd word ending in "s"
passes only if it is one of these (so "status must …" is not penalised as plural).

## Rule-type modulation

- **Profiling → scoring fully SUSPENDED** (`:251-268`). Returns `score=1.0, score_pct=100,
  suspended=True, total_weight=0`, with a `suspended_reason` explaining the 19 heuristics were
  built for Error-rule grammar ("X must have Y") and would mis-fail profiling names like "Profile
  of X on Y by Z" / "Distribution of X by Y" / "Count of X by Y" (usual offenders: *No Stray
  Symbols*, *Must Have Subject*). The UI renders this as a neutral informational message rather
  than a low score. A profiling-specific ruleset is reserved as Future Work.
- **Info → two relaxations** (`:199-209, 291-305`):
  - **Auto-pass set** `_INFO_SKIP_HEURISTICS` = *Modal Phrase Required, Detectable Pattern,
    Strong Modal Required, Must Start with Determiner* — these four are credited full weight
    without evaluation (Info names need no "must" and need not start with a determiner).
  - **Weight override** `_INFO_WEIGHT_OVERRIDES` = *Singular Subject: 0.5* (down from 2.25).
- **Empty name** (`:270-279`) → `score=0.0`, suggestion `"Enter a rule name to begin scoring."`,
  `total_count = len(heuristics)`.
- Default (Error / unspecified) → all 19 run at full weight.

## Inputs & outputs

- **In:** `name` (candidate, stripped before scoring); optional pre-loaded `heuristics`; optional
  `rule_type` (`"Info"` / `"Profiling"` recognised case-insensitively).
- **Out:** `ScoringResult` (above). Consumed by the rule-designer UI (live badge + suggestions)
  and by name-quality checks in derivation.

> [!warning] Name length is NOT scored here
> The ADM rule-name limits (≤100 hard, ≤85 target) are **not enforced in the scorer** — it never
> penalises length. That limit belongs in the rule-name builder / [[ref-local-deriver]] path, not
> the heuristic score. Do not assume a high score implies a compliant length.

## Source

- `core/rule_name_scorer.py:26-340` — path resolution, `_evaluate_heuristic` (`:146-192`), Info
  skip/override sets (`:199-209`), `score_rule_name` (`:212`) incl. profiling suspend
  (`:251-268`) and score formula (`:321-332`).
- `knowledge/methodology/heuristics.json` — the editable 19-heuristic data set (see
  [[std-rule-name-heuristics]]).
- Detail: `knowledge-mining/scoring-profiling.md` §1.

## Related

[[std-rule-name-heuristics]] · [[ref-local-deriver]] · [[ref-single-rule-designer]] ·
[[ref-rule-type-detection]] · [[ref-dqrulespec-data-model]] · [[ref-knowledge-base-file-inventory]] ·
[[ref-multi-impl-fan-out-engine]] · [[ref-profiling-view-generation]]
