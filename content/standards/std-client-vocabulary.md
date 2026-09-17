---
id: std-client-vocabulary
type: standard
title: Client Vocabulary — Say/Never-Say
domain: delivery
audience: [consultant, lead]
level: practitioner
status: review
sources:
  - bob-dq:enablement/enablement-guide.md
  - bob-dq:bob-canvas/enablement-notes.md
tags: [bob-dq, client-facing, vocabulary, facilitation]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:gls-key-issue
  - relates:gls-business-data-driver
  - relates:gls-business-rule
  - relates:gls-time-to-value
---

## What it is

The enforceable client-language rules for running a #bob-dq Business Outcomes Canvas session. Get
either translation direction wrong in a live session and you either confuse the client or
embarrass the delivery team. Two internal shorthand terms map to two client-facing ones, and one
list of words is simply banned in front of a client.

## Translation flash-cards

The ten that matter most in a live session — internal shorthand on the left, what to say on the
sheet or out loud on the right:

| Internal | Client-facing |
|---|---|
| `key_issue` | Business data driver |
| `dq_rule` (DQOps rule) | Business rule |
| `adm_rule_name` | The business-readable rule name shown on the sheet |
| `bob-client-project-spec` | "The specification that drives implementation" |
| `priority` (export field) | The order you dragged the outcome cards into |
| L1 (hierarchy level) | Outcomes — C-suite altitude |
| L2 (hierarchy level) | Measures — VP / Director altitude |
| L3 (hierarchy level) | Business data drivers — process owner altitude |
| L5 (hierarchy level) | Business rules — technical altitude, the proof |
| Save working file (action) | Produces the internal spec — not a client leave-behind |

Same entities, two vocabularies: the exported spec carries
`meta.vocabulary = {business_data_driver: "key_issue", business_rule: "dq_rule"}`, so nothing is
lost between the conversation and the build.

> [!warning] Do not explain this translation to the client
> Naming the internal shorthand reads as stage management. If asked whether the work is
> traceable, the honest client-facing answer is already on the sheet: *the exported specification
> carries a technical identifier for every driver and rule.*

## The systems behind the sheet

Our internal system names are **never spoken in the room** — say the neutral phrase, and know what
sits behind it so you can answer a follow-up without inventing anything:

| What you say in the room | What it actually is | What it does |
|---|---|---|
| "The specification that drives implementation" | the exported `bob-client-project-spec` | Carries the outcome selection, priority order, drivers and rules out of [[gls-bob-canvas]] and into delivery |
| *(not named — folded into the same phrase)* | [[gls-dq-studio]] | Imports the spec and generates the rules, tests, deploy scripts and evidence queries |
| "The blueprint you keep" | [[gls-vector-studio]] | Consumes the executed results and elevates them into the blueprint |
| "A secure managed environment" | an ADM-M environment, client- or Syniti-hosted | Where execution runs — identical mechanics either way, because the generated scripts are handed to the implementation team regardless |

## The value lever is invisible to the client

**Money aggregates at the [[gls-value-lever|value lever]] and only at the lever** — but the client
never sees a lever by name. They see the outcome, and they see the
[[gls-value-potential|value potential]] it produces. The lever is how the instrument gets from
evidence to a number without ever putting a number on a rule or a driver, and without the client
needing to know it exists. Naming it in the room invites a debate about our arithmetic instead of
their outcome.

## The say / never-say table

Banned in early client conversations, and why:

| Banned | Why it costs you the room |
|---|---|
| "data quality" | Names the tooling category, not the business problem — pulls the conversation down before it's earned the trip. |
| "governance" | Reads as a programme the client already has an opinion about — usually a scar. |
| "software rules" | Technology-forward; the client hears a system, not a business fact. |
| "cleansing" | Delivery-team language — correct internally, alienating on the sheet. |
| "conservative" | Claims a certainty about the number's direction that an indicative figure cannot carry. |
| "guaranteed" | The offering has no bookable number at this stage — this word promises one. |
| "you'll save" | States a future fact instead of an indicative scale — the single most damaging misreading available to a CFO. |
| "ROI" | The offering's language excludes return ratios entirely (R4) — investment and return only enter after real data is profiled. |
| "payback" | Same family as "you'll save" — attaches a timeline to a figure that hasn't earned one. |
| "timeline" (in the client tier) | The canvas carries no duration by design (A22). The sanctioned frame is **time to value** ([[gls-time-to-value]]), and it lives in Solution Proposal — a *priced* timeline exists only inside the internal workbench's documents. |
| "the tool counted it" (of a promoted measure) | A promote is a **facilitator decision**, narrated. The instrument proposes; a person counts. |

## Sanctioned replacements

What each replacement carries, so it's said with the right weight, not just the right word:

| Say instead | What it carries |
|---|---|
| **business outcome** | The client's own words for what they want to be true — never a technology goal. |
| **business data driver** | The client-facing name for the recognisable, repeating data problem — same thing as a "key issue," said in the room's language. |
| **business rule** | The client-facing name for a DQ rule — a plain statement of what "correct" looks like, testable by a computer. |
| **indicative** | The standing word for every figure in the instrument — computed from stated assumptions the reader can open and change. |
| **value potential** | The scale of the opportunity evidenced in the data — not booked value, not a forecast, not a promised saving. |
| **evidence** | What the figure traces back to — a business rule that will run on the client's own data. |
| **coverage** | Which outcomes *could be evidenced* given scope — never a completeness score. |

## Verification

- No banned word from the say/never-say table appears in a script, slide, or live narration aimed
  at a client.
- Every currency figure spoken to a client is paired with "indicative."
- Internal shorthand (`key_issue`, `dq_rule`, hierarchy level codes) never surfaces on a client
  screen or in client-facing narration.

## Common pitfalls

- Saying "the tool counted it" about a promoted measure — surrenders the honesty discipline that a
  narrated Promote click is built to protect. See [[prc-run-the-blueprint-room|Run the Blueprint Room]].
- Answering "how long?" with a duration on the canvas — the sanctioned answer is voiceover only,
  and on the sheet exclusively as time to value in Solution Proposal.
- Letting "ROI" or "payback" slip in while defending a challenged number — see
  [[prc-handle-the-cold-room|Handle the Cold Room]] for the honest sequence to use instead.

## Related

- [[con-audience-altitude|Audience Altitude]]
- [[prc-run-the-blueprint-room|Run the Blueprint Room]]
- [[prc-handle-the-cold-room|Handle the Cold Room]]
