# Instructor Guide

How to facilitate the DQ Enablement Studio with a team. The material is
`dist/enablement-master.html` — one offline HTML file with search, browse, the graph, six
learning paths and Review mode. Nothing else to install or host (see `SETUP.md`).

## What you are actually facilitating

The app is the content. Your job is not to re-present it — it is to **pace it, pressure-test it,
and connect it to the client's data**. Three things the file gives you that a slide deck does not:

- **Learning paths** — ordered sequences over the knowledge units, with progress tracking and
  knowledge checks interleaved as checkpoints.
- **The graph and cross-links** — every unit links to its prerequisites and relations, so a
  learner's tangent is a feature, not a derailment. Follow it, then come back.
- **Review mode** (the ✍ button) — learners propose edits, leave notes, ask questions and flag
  problems, then export a changeset. This is how the corpus improves. See
  [Reviewing with consultants](#reviewing-with-consultants) below.

### The six learning paths

| Path | Audience | Self-paced | Facilitated | Checkpoints |
|---|---|---|---|---|
| Session 1 — Data Quality Fundamentals | Consultant, lead | ~60 min | 90 min | 12 |
| SQL Readiness Check | Consultant | ~10 min | 15 min (debrief) | 14 |
| Session 2 — SQL Best Practices | Consultant | ~60 min | 90 min | 3 |
| Session 3 — DQ Studio Workflow | Consultant | ~60 min | 90 min | 6 |
| Delivering a Blueprint Engagement | Consultant, lead | ~75 min | 90 min | none yet |
| From Rules to Business Value | Consultant, lead | ~60 min | 75 min | none yet |

Facilitated timings assume discussion, live demo and client examples. Self-paced timings are the
reading estimates in each path's blurb.

---

## Before you facilitate

**1. Walk the paths yourself.** Not just the units — take every checkpoint. The multiple-choice
distractors are chosen from real consultant mistakes; knowing why each wrong answer is tempting
is most of your discussion material.

**2. Take the SQL Readiness Check cold.** It calibrates you to the difficulty your learners
will feel, and it is the fastest way to find the units you are shaky on.

**3. Do not fork the content.** The old guide told you to edit HTML files to localise examples.
Don't — `dist/` is build output and hand-edits are lost on the next build. Localise in the room
instead: keep a one-page crib of the client's system IDs, tables and domains, and swap them in
verbally. If a change belongs in the canon, raise it through Review mode.

**4. Know your escape hatches.** Search (`/`), the graph, and `docs/FAQ.md`. If a question lands
that the corpus cannot answer, that is a Review-mode question, not a failure — say so out loud.
It models the behaviour you want.

**5. Set expectations with learners:**

- **Time:** 3–4 hours of paths for a consultant track; 5–6 hours if delivery and value are in scope.
- **Prerequisites:** Session 1 → Readiness Check → Session 2 → Session 3. Delivery and value paths
  need Session 1 only.
- **Progress is local.** Path progress lives in browser storage on their machine. Same file,
  different browser, no progress. Tell them up front.

---

## Facilitating each path

### Session 1 — Data Quality Fundamentals

**Audience:** everyone, day one. **Facilitated: 90 min.** 8 units, 12 checkpoints.

**Shape of the session**

- **Intro (5 min)** — a real data failure from this client or a recent engagement.
- **What DQ is + the seven dimensions (30 min)** — includes the five dimension-matching checkpoints.
- **Lifecycle (15 min)**
- **Rule types, fetch-check-return, view types (25 min)** — OptSel/RptSel lives here.
- **Deletion flags vs status fields (10 min)**
- **Wrap (5 min)**

**Checkpoints to stop on**

- The four `as-fund-match-*` items (tax ID, name sync, status code, duplicate IDs) run back to
  back. Do them as a round — one learner answers, another has to justify it. Four rapid reps is
  what makes the dimension vocabulary stick.
- `as-fund-dimension-scenario` and `as-fund-status-scope` are the paired scenario at the end.
  Treat them as the session's exit ticket: if the room fumbles the second one, deletion flags
  need another pass before Session 2.

**Discussion points**

- **"Why seven, not six."** Most learners arrive with a six-dimension model that used *Validity*.
  The unit explains the change (Conformity absorbs Validity; Integrity earns its own dimension)
  and CONFLICT-001 logs it. Expect pushback from anyone trained on DAMA — the answer is *map their
  vocabulary to ours in the engagement glossary, don't adopt theirs mid-delivery*.
- **OptSel vs RptSel is THE concept.** Whiteboard it: OptSel is the universe with a flag,
  RptSel is the error rows only. Say it at least three times across the session. Learners who
  only hear it once will invert it in Session 2.
- **"Which dimension matters most here?"** Different teams answer differently, and that is the
  point — it surfaces what the client actually cares about.

**Common misconceptions**

| Misconception | Correction |
|---|---|
| "All bad data should be deleted" | Classify it, understand why, then remediate |
| "Perfect data is the goal" | Acceptable quality for the business purpose is the goal |
| "DQ rules only catch typos" | They catch logic errors, broken references, inconsistency |
| "One rule per table is enough" | Quality is multidimensional — several rules per table |
| "Validity is a dimension" | Conformity covers it; see CONFLICT-001 |

---

### SQL Readiness Check

**Audience:** anyone about to start Session 2. **Facilitated: 15 min debrief.** 14 questions, no units.

Have learners take it asynchronously before the workshop, then debrief the misses live. It is a
diagnostic, not an exam — say that, or people bluff their answers and you lose the signal.

**Reading the score (out of 14)**

| Score | What to do |
|---|---|
| 13–14 | Straight into Session 2 |
| 11–12 | Review the missed questions' units, then Session 2 |
| 9–10 | 30 minutes back on Session 1 view types and deletion flags first |
| < 9 | Redo Session 1 before Session 2 |

The questions are attached to their source units, so a miss points straight at what to re-read.
`as-pre-multi-system` and `as-pre-literal-system-id` are the two worth debriefing even when the
room gets them right — they are the mistakes that survive into production SQL.

---

### Session 2 — SQL Best Practices

**Audience:** consultants who will write or review rule SQL. **Facilitated: 90 min.**
10 units, 3 checkpoints.

**Shape of the session**

- **Why standards exist (10 min)** — auditability, consistency, safety, AI compatibility.
- **CTE rules (15 min)** — checkpoint `as-sql-unused-cte`.
- **zSourceSystemID (20 min)** — checkpoint `as-sql-zsource-statement`. Spend the time.
- **Comments and naming (20 min)** — includes writing a rule name against the heuristics.
- **Field sections, OptSel structure, view naming (15 min)**
- **Review drill (10 min)** — checkpoint `as-sql-cte-review`, then the audit procedure.

**Checkpoints to stop on**

- `as-sql-cte-review` is a code-review scenario. Do not let learners answer alone — put the SQL
  on screen and have the room find the fault before anyone picks an option.

**Discussion points**

- **The four places zSourceSystemID must appear** — main table WHERE, every join's ON, every CTE's
  internal WHERE, every join to a CTE's output. Say all four, five separate times, in different
  orders. This is the single highest-value repetition in the whole curriculum.
- **The leakage scenario.** A rule joins MARA (production) to a quality-system copy of T006.
  Without zSourceSystemID paired in the ON clause the join matches a production material against
  a quality-system UoM. The rule *runs*. It returns *wrong answers*. Nothing errors. That is what
  the standard prevents, and no abstract argument lands as hard as this example.
- **Comments: what not to write.** No line-by-line narration of SQL syntax, no performance advice
  inline, no mention of AI or generation.
- **Run a bad rule through the audit checklist live.** Business correctness → structural
  correctness → documentation correctness. Ask "what's wrong?" and let them use the checklist
  rather than their instincts.

**Common mistakes**

| Mistake | Why it's wrong | Fix |
|---|---|---|
| Missing zSourceSystemID in a join | Silent cross-system leakage | Pair it in every ON clause |
| zSourceSystemID as a literal `'Z01'` | Breaks fan-out; defeats filtering | Always a column reference |
| Deletion flag inside CASE | Turns scope into an error condition | Deletion flags belong in WHERE |
| Wrong field order | Inconsistent, unreviewable output | Technical → Basic → Org → Value → Activity |
| Unused CTE | Signals unfinished logic | Every CTE is joined or selected from |

---

### Session 3 — DQ Studio Workflow

**Audience:** consultants who will use the Studio. **Facilitated: 90 min, hands-on.**
12 units, 6 checkpoints.

Have the Studio open. This path does not survive being read aloud — it needs a live derivation.

**Shape of the session**

- **Onboarding (10 min)** — `prc-studio-onboarding`, then checkpoint `as-studio-06`.
- **Derive a rule (20 min)** — Local Derive, catalog vs bespoke; checkpoint `as-studio-01`.
- **Implications and AI enhancement (20 min)** — what AI Enhance does for you and the AI SQL
  quality gate; checkpoint `as-studio-02`.
- **Multi-implementation and fan-out (20 min)** — checkpoints `as-studio-03`, `as-studio-05`.
- **Bulk pipeline (10 min)** — checkpoint `as-studio-04`.
- **Audit and export (10 min)**

**Checkpoints to stop on**

- `as-studio-06` (API key precedence) comes first for a reason — a room that is confused about
  which key the session is using will misread everything that happens after.
- `as-studio-02` — the AI SQL quality gate. The teaching point is that the gate retries **once**
  and then hands the rule back with its findings attached: a finding is a decision for the
  consultant, not something the Studio has already cleared. Only the short hard-stop list blocks
  a save outright.

**Discussion points**

- **Live demo is non-negotiable.** Derive something small in front of them — "material must have a
  valid unit of measure" — and narrate what the generated SQL contains: header block, field
  sections, zSourceSystemID in all four places, the comment standard. Session 2 suddenly makes sense.
- **Deterministic derivation vs AI enhancement.** Same input, same output, always — that is what
  makes the deterministic path auditable. AI is the optional layer on top, gated by the AI SQL
  quality gate, and the consultant decides.
- **Fan-out is mechanical, on purpose.** One enhancement on the lead implementation, substituted
  across siblings. No AI re-run per system — that is what keeps siblings identical.

**Common questions**

| Q | A |
|---|---|
| "Will AI always improve my rule?" | No. Often the deterministic rule is already right. |
| "Can I skip AI entirely?" | Yes. Deterministic derivation alone is production-ready. |
| "How do I judge an AI suggestion?" | Against the Session 2 checklist and the validator, then sample data. |
| "Can siblings span different rules?" | No — siblings are one rule across systems. |
| "How often do we run bulk?" | Baseline once, then on a cadence that matches the remediation cycle. |

---

### Delivering a Blueprint Engagement

**Audience:** consultants and leads going client-facing. **Facilitated: 90 min.**
11 units, no checkpoints yet.

The delivery spine in teaching order: the three phases → the five solution components → assess and
discover → team shape → effort estimation → the room craft (altitude, vocabulary, running the
room, cold rooms) → QA before it ships → the deliverables inventory.

This path has **no knowledge checks yet**, so the facilitation has to supply the pressure. Use
rehearsal instead of quizzing.

**Shape of the session**

- **Phases and components (20 min)** — anchor everything else on this. If people cannot name the
  five components, the rest of the path is a list of unrelated procedures.
- **Assess and discover (15 min)**
- **Team shape and effort (15 min)** — leads run this part; consultants should still hear it,
  because scope arguments are won or lost on the rubric.
- **Room craft (25 min)** — audience altitude, the say/never-say vocabulary, running the room,
  and the cold room.
- **QA and deliverables (15 min)**

**Facilitation substitutes for the missing checkpoints**

- **Altitude drill.** Take one finding and have each person state it three times: to an analyst,
  to a process owner, to the CFO. Then have the room name which altitude each version was pitched at.
- **Vocabulary drill.** Read out ten phrases, half of them from the never-say list. Thumbs up or
  down, fast. Then ask *why* each banned phrase is banned — the reasons matter more than the list.
- **Cold-room roleplay.** You play the sceptical stakeholder. Ten minutes, no rescuing. Debrief on
  what actually moved the room, not on what sounded clever.
- **QA pass.** Hand the room a real (sanitised) blueprint extract and run the QA procedure against
  it out loud.

**Discussion points**

- **Estimation is a conversation about scope, not effort.** The rubric only works if the value
  levers and key issues are agreed first. Leads should be able to say what a number *assumes*.
- **The deliverables inventory is the contract.** Walk it as "what the client is holding after we
  leave" — it stops the engagement being sold as a slide deck.

**Common misconceptions**

| Misconception | Correction |
|---|---|
| "Discovery is just profiling" | Profiling is one input; discovery is estate, process and value |
| "We estimate from table counts" | Effort follows lanes and key issues, not raw table volume |
| "Speak the client's language" means adopt their terms | Map their terms to ours; adopting theirs mid-delivery loses the method |
| "QA is a proofread" | QA tests walkability and whether the claims survive challenge |

---

### From Rules to Business Value

**Audience:** consultants and leads who present findings to a business audience.
**Facilitated: 75 min.** 8 units, no checkpoints yet.

The chain from a rule result to a number a CFO will accept: value chain → the L1–L5 outcome
hierarchy → value levers → valuation discipline → key issues as the primary tier → the rule
provenance model → the key issue vocabulary → the rule record schema. It deliberately does **not**
re-teach what data quality is — Session 1 covers that.

**Shape of the session**

- **Value chain and the L1–L5 hierarchy (25 min)** — draw the whole chain on one board and keep it
  up for the rest of the session. Every later unit is a segment of it.
- **Levers and valuation discipline (20 min)**
- **Key issues as the primary tier (10 min)**
- **Provenance, vocabulary and schema (20 min)** — the audit trail that keeps the number defensible.

**Facilitation substitutes for the missing checkpoints**

- **Trace one rule end to end.** Pick a real rule and walk it up the chain: finding → key issue →
  lever → outcome → the money claim. Then walk it back down and ask what evidence supports each hop.
- **Break the claim.** Present a value number with a deliberately weak link — a lever with no
  evidenced volume, or aggregation at the wrong level — and have the room find it.

**Discussion points**

- **Money aggregates at the lever only.** This is the discipline that keeps a blueprint honest and
  the most common thing consultants get wrong under pressure to produce a big number. Expect
  resistance; the reason it holds is double-counting.
- **Provenance is existence vs text.** Knowing a rule exists is a different claim from knowing what
  its SQL says. Value statements must be clear about which one they rest on.
- **Key issues are the primary tier** — not dimensions, not tables. It changes what the client's
  report is organised around.

**Common misconceptions**

| Misconception | Correction |
|---|---|
| "More findings means more value" | Value comes from levers with evidenced volume, not error counts |
| "Every rule maps to money" | Many rules are enablers; only levers carry the number |
| "The hierarchy is a taxonomy" | It is a chain of evidence — each level must be earned from the one below |

---

## The three delivery models

Retimed for the app rather than the retired academy pages.

### Model 1 — Self-paced with a check-in

**Best for:** experienced consultants, distributed teams, rolling onboarding.

- Send the file (or the share path) with the path order and a completion date two weeks out.
- Ask everyone to take the SQL Readiness Check and send you their score.
- Hold one 45-minute Q&A at the end — agenda built from the Readiness Check misses and any
  Review-mode questions that came back.

**Your prep:** ~45 minutes. **Learner time:** 3–4 hours.

### Model 2 — Instructor-led

**Best for:** new joiners, a team starting an engagement together, anywhere the room needs to
build shared vocabulary fast.

| Day | Content | Length |
|---|---|---|
| 1 | Session 1 + Readiness Check taken live at the end | 105 min |
| 2 | Session 2 (Readiness debrief first) | 105 min |
| 3 | Session 3, hands-on with the Studio | 90 min |
| 4 (optional) | Delivering a Blueprint Engagement | 90 min |
| 5 (optional) | From Rules to Business Value | 75 min |

**Core track: 5 hours over three days. Full track: ~7.75 hours over five.** Don't compress days 1–2
into one sitting; the Readiness Check needs to sit overnight to be worth anything.

**Your prep:** 3–4 hours including a Studio dry run.

### Model 3 — Blended

**Best for:** most teams. Reading is async; the room is for pressure-testing.

| Week | Async | Facilitated |
|---|---|---|
| 1 | Session 1 (~60 min) | Workshop A (60 min) — dimensions and OptSel/RptSel |
| 2 | Readiness Check + Session 2 (~70 min) | Workshop B (75 min) — Readiness debrief, live rule review |
| 3 | Session 3 (~60 min) | Workshop C (75 min) — Studio derivation, hands-on |
| 4 | Delivery + value paths (~2 hr) | Workshop D (75 min) — room-craft roleplay and value chain drill |
| 5 | — | Review-mode triage session (45 min) |

**Your prep:** 4–5 hours total, spread across the five weeks.

The week 5 slot is the one people cut and shouldn't. It is where the corpus improves — see below.

---

## Reviewing with consultants

Review mode is the feedback loop, and it works best when it is a facilitated activity rather than
an invitation nobody takes up.

**What the ✍ button gives a learner**

| Op | What it is | Where it goes |
|---|---|---|
| **edit** | Edit the unit's markdown directly | Auto-applies if the unit hasn't changed since their build (hash-checked); otherwise triage |
| **note** | A comment for the CoE, optionally anchored to a section | Triage in a Claude session |
| **question** | Something the material couldn't answer | Usually becomes a new `qa/` unit |
| **flag** | Outdated / factually wrong / conflicts / unclear, plus a reason | Triage; conflicts may become a `CONFLICT-NNN` entry |

Ops accumulate locally with a badge count. **Export** prompts for a name and downloads
`em-changeset-<name>-<date>.json` (schema `em-changeset/1`, stamped with the app build id).

**Running a review session (45 min)**

1. **Frame it (5 min).** "You have used this on a real engagement. Where was it wrong, thin, or
   missing?" Disagreement is the deliverable — the corpus logs conflicts rather than overwriting them.
2. **Silent pass (20 min).** Everyone walks the units they actually used and logs ops. Notes and
   flags are cheap; encourage volume.
3. **Round the room (15 min).** Each person reads out one flag or question. Others say whether they
   hit the same thing. Agreement across two consultants is a strong signal for the CoE.
4. **Export (5 min).** Everyone exports and sends you the JSON.

**What you do with the changesets**

Drop them in `feedback/inbox/`, then:

```bash
python3 build/merge_changesets.py --stage   # triage report, nothing changed
python3 build/merge_changesets.py --apply   # apply hash-safe edits, stage the rest
```

An `edit` is auto-applied only when its `base_hash` still matches the unit body — a conflicting
edit is never forced. Everything else needs a Claude session: questions become `qa/` drafts, flags
get investigated, genuine disagreements go to `docs/CONFLICTS.md`. Processed files move to
`feedback/applied/`. Then rebuild and commit content and `dist/` together.

**Tell learners what happened.** A changeset that disappears kills the loop. Send round a note
naming whose feedback landed, in one line each.

---

## Facilitator craft

**Pacing**

- Pause every 2–3 minutes. A 15-minute uninterrupted stretch loses the room.
- Session 1 is foundational — don't rush OptSel/RptSel to make time later.
- Session 2's zSourceSystemID block is where you should feel repetitive. Be repetitive.
- Session 3 without a live demo is a waste of 90 minutes.
- The delivery and value paths need rehearsal, not lecture. If nobody has spoken a finding out
  loud, you facilitated the wrong session.

**Handling the usual objections**

| They say | You say |
|---|---|
| "This is too technical for me" | The SQL is generated. You define the rule; your job is judging whether it's a good one. |
| "When will I use this?" | Be specific and dated — name the engagement and the month. |
| "We don't use the Studio yet" | The method holds either way; the Studio just makes it fast and consistent. |
| "I already know SQL" | DQ SQL is a dialect with a compliance surface. Take the Readiness Check. |
| "The client uses different DQ terms" | Map theirs onto our seven in the engagement glossary; don't switch models mid-delivery. |

**Building confidence**

- Start with simple rules (material UoM, customer email), build to multi-table with CTEs.
- Celebrate the first derived rule — that is the hardest step psychologically.
- Treat wrong checkpoint answers as content: "why is that distractor tempting?" is a better
  question than "who got it right?"

---

## Feedback on the teaching

After each cohort, collect:

1. Which path was hardest, and where exactly?
2. What did you expect to find in the app and couldn't?
3. Do you feel ready to derive a rule / run a room unaided? (yes / no / partly)
4. What would you change about the pacing?

Bring the answers back as Review-mode notes on the units concerned, so the next facilitator
inherits them rather than re-discovering them.

---

## Quick reference

| Term | Definition |
|---|---|
| **OptSel** | The universe view — all in-scope rows with `zIsErrorFlag` 1 or 0 |
| **RptSel** | The report view — a wrapper returning only error rows |
| **zSourceSystemID** | Column identifying which source system a row belongs to |
| **zIsErrorFlag** | INTEGER 1 (error) or 0 (clean) |
| **CTE** | Common Table Expression — a `WITH … AS` block for pre-filtering or aggregating |
| **Sibling implementation** | The same conceptual rule scoped to another system |
| **Deterministic derivation** | Same input, same output, always — the auditable path |
| **AI enhancement** | An optional layer over derived SQL, gated by the AI SQL quality gate |
| **Key issue** | The primary tier findings are organised around |
| **Value lever** | Where money aggregates in the value chain — and only there |
| **Changeset** | An exported `em-changeset/1` JSON of a reviewer's edits, notes, questions and flags |

**Also read:** `README.md` (what the corpus is) · `SETUP.md` (distributing the file) ·
`FAQ.md` (learner questions) · `CONFLICTS.md` (governed disagreements) · `CLAUDE.md` (authoring rules).

---

**Last updated:** 2026-08-21 — rewritten against the six learning paths in
`dist/enablement-master.html`, then reconciled after the app-internal corpus was archived to
`archive/dev-corpus/`. Path unit and checkpoint counts above match `taxonomy/paths.json` as built.
The retired academy HTML is in `archive/academy-v1/`.
