---
id: std-rule-name-heuristics
type: standard
title: Rule-Name Heuristics (the 19, enumerated)
domain: rule-design
audience: [consultant]
level: practitioner
status: review
sources:
  - vault:dq-methodology/Rule-Name Heuristics (the 19, enumerated).md
  - dq-studio:knowledge/methodology/heuristics.json
tags: [methodology, engine, studio, sap, course]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:con-rule-types
  - relates:prc-write-a-quality-rule-name
  - relates:std-view-naming-patterns
  - relates:std-skp-rule-identifier-convention
  - relates:ref-local-deriver
---

## The standard

A DQ rule name is scored against 19 weighted, data-driven heuristics (total weight 60.5) that
enforce a single, grammatical "A `<singular subject>` must `<modal verb>` …" sentence free of
SAP table/field names, SQL keywords, and symbols. The score is `earned_weight / total_weight`,
evaluated by the Rule-Name Scorer.

## Why it exists

A good rule name reads as one plain-English business assertion ("A customer must have a valid
country code"), not a technical fragment. Consistent grammar makes names sortable,
deduplicable, and exportable to SKP without per-name cleanup. The 19 heuristics codify that
house style and turn it into a 0–100 quality score, so a name can be graded and improved before
it ships.

## The 19 heuristics, with weight

Weights are summed at runtime; **total = 60.5** for an Error rule. `failWhen: matches`
heuristics are negative checks (the name passes when the pattern is *absent*); all flags shown
are `i` (case-insensitive) unless noted. The table states each pass condition in words; the
exact regexes follow it verbatim.

| # | Name | Weight | Pass condition |
|---|------|--------|----------------|
| 1 | Single Sentence | **7** | no `". "` (period-space) anywhere in the name |
| 2 | Modal Phrase Required | **5** | the word `must` appears |
| 3 | Detectable Pattern | **5** | `must` is followed by one of `have, be, not, equal, contain, match, include, exceed` |
| 4 | Number Context Required | **5** | auto-pass if the name carries no number (a digit, or `one…ten, twenty, thirty`); otherwise a context word must be present — `equal, greater, less, within, over, under, at least, at most, be, have, exceed` |
| 5 | No Technical Names | **5** | no SAP table/field token matches (see list below) |
| 6 | No SQL Keywords | **4** | none of `SELECT WHERE NULL JOIN FROM INSERT UPDATE DELETE TABLE VIEW` |
| 7 | No Possessive on Subject | **3.5** | does not start with `my, our, your, its, their` |
| 8 | No Logic Symbols | **3.5** | no `>= <= == > < != ~=` (regex `[><=!~]{1,2}`, case-sensitive) |
| 9 | No Stray Symbols | **3.25** | none of backslash, forward slash, pipe, plus, tilde, backtick, caret, ampersand, asterisk, double quote, parentheses, square brackets, braces (case-sensitive) |
| 10 | Must Have Subject | **3** | ≥ 3 words |
| 11 | No Indef. Possessive Pronouns | **2.4** | none of `everyone's, someone's, nobody's, anybody's, everybody's` |
| 12 | Singular Subject | **2.25** | 2nd word is not plural (see exceptions below) |
| 13 | No Subject Pronouns | **2.15** | does not start with `it, you, he, she, they, we` |
| 14 | No Conditional Statements | **2** | no `if … then` construction |
| 15 | No Possessive Nouns | **2** | no `\w's\b` (e.g. `customer's`), case-sensitive |
| 16 | No Vague Subjects | **1.85** | none of `everyone, everybody, someone, somebody, anyone, nobody` |
| 17 | Strong Modal Required | **1.5** | `must` appears **AND** no weak modal (`should, shall, can, may, could, would`) |
| 18 | Must Start with Determiner | **1.1** | first word is `a, an, the, this` |
| 19 | Single Determiner Only | **1** | does not start with `all the` or `half of the` |

> [!note] 60.5, not 70.15
> Earlier mining notes cited a total weight of 70.15. The authoritative scoring definition sums
> to **60.5** (19 weights, top to bottom: 7, 5, 5, 5, 5, 4, 3.5, 3.5, 3.25, 3, 2.4, 2.25, 2.15,
> 2, 2, 1.85, 1.5, 1.1, 1). Use 60.5.

> [!warning] Two unrelated lists of 19 — the count is a coincidence
> These 19 heuristics are the scoring rules. A separate 19-item SOP checklist exists for human
> authoring. The shared count of 19 is coincidence, not correspondence.

## The criteria, verbatim

The table below shows the exact implementation of each heuristic — the regex patterns or structural checks the scorer runs. **You do not need to memorize or understand these patterns.** The Studio's inline scorer evaluates all 19 automatically and flags any that didn't pass with targeted suggestions. Read this section if you're curious about how the scorer works, or if you're building tools that integrate with the naming standard.

Three heuristics (1, 10, 12) carry a `pattern` string instead of a regex and are evaluated
structurally; the rest are regexes. `i` = case-insensitive.

| # | Heuristic | Type | Definition | Flags | Pass Condition |
|---|-----------|------|------------|-------|---|
| 1 | Single Sentence | Pattern | `!name.includes('. ')` | — | No period-space in the name |
| 2 | Modal Phrase Required | Regex | `\bmust\b` | `i` | "must" appears |
| 3 | Detectable Pattern | Regex | `\bmust\s+(have\|be\|not\|equal\|contain\|match\|include\|exceed)\b` | `i` | "must" followed by one of the listed verbs |
| 4 | Number Context Required | Regex + Pattern | `\b(equal\|greater\|less\|within\|over\|under\|at least\|at most\|be\|have\|exceed)\b` | `i` | If name has a number, a context word must be present |
| 5 | No Technical Names | Regex | `\b(KNA1\|KNB1\|KNVV\|...\|KZAUS)\b` | `i` | Fails if SAP table/field names match |
| 6 | No SQL Keywords | Regex | `\b(SELECT\|WHERE\|NULL\|...\|VIEW)\b` | `i` | Fails if SQL keywords present |
| 7 | No Possessive on Subject | Regex | `^(my\|our\|your\|its\|their)\b` | `i` | Does not start with possessives |
| 8 | No Logic Symbols | Regex | `[><=!~]{1,2}` | — | Fails if `>= <= == > < != ~=` present |
| 9 | No Stray Symbols | Regex | `[\\\/\|+~\`^&*"()\[\]{}]` | — | Fails if special symbols present |
| 10 | Must Have Subject | Pattern | `W.length >= 3` | — | Name has ≥ 3 words |
| 11 | No Indef. Possessive Pronouns | Regex | `(everyone's\|someone's\|nobody's\|anybody's\|everybody's)` | `i` | Fails if indefinite possessives present |
| 12 | Singular Subject | Pattern | 2nd word not plural (see exceptions below) | — | Subject noun does not end in 's' (unless whitelisted) |
| 13 | No Subject Pronouns | Regex | `^(it\|you\|he\|she\|they\|we)\b` | `i` | Does not start with pronouns |
| 14 | No Conditional Statements | Regex | `\bif\b.*\bthen\b` | `i` | Fails if "if...then" construction present |
| 15 | No Possessive Nouns | Regex | `\w's\b` | — | Fails if possessive nouns (e.g., `customer's`) present |
| 16 | No Vague Subjects | Regex | `\b(everyone\|everybody\|someone\|somebody\|anyone\|nobody)\b` | `i` | Fails if vague subjects present |
| 17 | Strong Modal Required | Regex + AntiRegex | `\bmust\b` AND NOT `\b(should\|shall\|can\|may\|could\|would)\b` | `i` | "must" present AND no weak modals |
| 18 | Must Start with Determiner | Regex | `^(a\|an\|the\|this)\b` | `i` | First word is a determiner |
| 19 | Single Determiner Only | Regex | `^(all the\|half of the)\b` | `i` | Fails if starts with "all the" or "half of the" |

> [!note] One description overshoots its regex
> *No Vague Subjects*' JSON description also lists "nothing" among the banned vague subjects, but
> the regex does not include it — a name containing "nothing" is not actually caught. Read the
> regex, not the description, when predicting a score.

## No Technical Names — the banned-token list (verbatim)

Heuristic #5 fails the name if any of these appear as a whole word (case-insensitive). Tables
and fields are mixed in one list:

```
KNA1  KNB1  KNVV  MARA  MARC  MAKT  MBEW  LFA1  LFB1  BSEG  BKPF
VBAK  VBAP  EKKO  EKPO  LOEVM  BRGEW  DMBTR  MATNR  KUNNR  LIFNR
BUKRS  WERKS  SAKNR  MHDHB  XCHPF  KZAUS
```

Use business terms instead: "customer" not `KNA1`, "gross weight" not `BRGEW`, "deletion flag"
not `LOEVM`. The list is illustrative, not exhaustive — keep all SAP physical names out of rule
names.

## Singular Subject — the plural exceptions (verbatim)

Heuristic #12 looks at the **second word** (the subject noun, after the determiner). A 2nd word
ending in `s` fails *unless* it is one of these whitelisted words (word-boundary,
case-insensitive):

```
is  has  was  does  series  status  process  address  gross  business  class  goods
```

So "A customer**s** must …" fails, but "A **status** must …" and "A **business** must …" pass.
The whitelist covers verbs ("A material **has** …"), mass nouns ("goods"), and singular nouns
that merely end in `s`.

## Rule-type modulation (how the 19 shift)

- **Error rules** — all 19 apply at full weight (total 60.5).
- **Info rules** — four grammar heuristics auto-pass (full credit, no check): *Modal Phrase
  Required, Detectable Pattern, Strong Modal Required, Must Start with Determiner*. *Singular
  Subject* is re-weighted **2.25 → 0.5**. (Info names read "Count of X by Y", not "X must have
  Y".)
- **Profiling rules** — scoring is **fully suspended**, returns score 1.0 / 100%. Profiling
  names ("Profile of X on Y by Z") follow different grammar; the 19 would mis-fail them.
- **Empty name** → score 0.0, suggestion "Enter a rule name to begin scoring."

See [[con-rule-types|Rule Types — Error, Info, Profiling]] for what distinguishes Error, Info,
and Profiling rules.

## A concrete example

> **A customer must have a valid country code** — passes all 19. Determiner ("A"), singular
> subject ("customer"), strong modal ("must"), no symbols, no SAP names, ≥ 3 words → earned
> 60.5 of 60.5 → **score 1.0 / 100%**.

> **KNA1 records >= 1 entry** — fails *No Technical Names* (`KNA1`, −5), *No Logic Symbols*
> (`>=`, −3.5), *Modal Phrase Required* (no "must", −5), and more → low score with targeted
> suggestions.

> [!warning] Implementation status
> The ≤100-char hard limit / ≤85-char target (ADM requirement) is **not** enforced by the
> scorer — none of the 19 heuristics penalise length. That limit lives in the rule-name builder /
> [[ref-local-deriver|Studio — Local Deriver]] path, not here.

## Questions from consultants

- [[qa-regex-heuristics-understanding|Should consultants understand the regex patterns?]]

## Related

- Studio — Rule-Name Scorer (engine) — the evaluator that runs these 19
- [[con-rule-types|Rule Types — Error, Info, Profiling]] — drives the per-type modulation above
- [[con-deletion-flags-vs-status-fields|Deletion Flags vs Status Fields]] — source of the SAP
  field names banned in #5
- [[std-view-naming-patterns|View Naming Patterns]] — the other place rule identity is encoded
- [[std-skp-rule-identifier-convention|SKP_RULE Identifier Convention]]
