---
id: con-solution-components
type: concept
title: The Five Solution Components
domain: delivery
audience: [consultant, lead]
level: foundation
status: deprecated
sources:
  - bob-dq:bob-dq-solution-spec.md (§1.4 Solution components)
  - bob-dq:bob-dq-solution-spec.md (§1.2 Architecture — the accelerator chain)
  - bob-dq:business-outcomes-blueprint-solution-overview.md (§4 Architecture — Components & Data Flow)
links:
  - prereq:con-value-chain
  - relates:con-engagement-phases
  - relates:con-outcome-hierarchy-l1-l5
  - relates:prc-assess-and-discover
  - relates:ref-deliverables-inventory
  - relates:gls-bob-dq
  - relates:gls-bob-canvas
  - relates:gls-dq-studio
  - relates:gls-vector-studio
  - relates:gls-ctx-server
  - relates:gls-project-spec
  - relates:gls-evaluation-sheet
  - relates:gls-iteration-loop
  - relates:gls-adm
tags: [bob-dq, delivery, architecture, components]
created: 2026-08-20
updated: 2026-08-20
---

## What it is

A #bob-dq engagement is assembled from **five named components**. They are `#sc`-tagged and
leveraged by the implementation plan (see [[con-engagement-phases]]) — the number in the tag is the
**conceptual level** at which the component lives, **zero being the top level**.

| Tag | Component | What it produces |
|---|---|---|
| `#0-sc-engage` | **Engage** | The client's outcome selection, captured as an exportable project spec |
| `#1-d3p` | **Data Provisioning, Preparation, Profiling** | Extracted, prepared, profiled source data on the engagement environment |
| `#2-rules` | **Rules** | The outcome-linked rule set, generated as deployable SQL with tests |
| `#3-validate-improve` | **Validate & improve** | A stable rule set and an accepted evidence base |
| `#4-present-vector-studio` | **Present** | The published blueprint |

Three applications carry them, deliberately **not consolidated** — separation of concerns with
explicit connections, one direction of data flow, one mid-engagement iteration loop, two contracts.

| App | Verb | Role |
|---|---|---|
| **bob-canvas** | **DEFINE** (+ revise pre-signature) | GTM instrument, accelerator, implementation connect. Builds the opportunity; emits the project spec. |
| **dq-studio** | **GENERATE** (+ regenerate) | The implementation engine — owns ALL generation: extraction lists, prep, profiling, rule SQL, unit tests, deploys, results export, evidence queries. Owns the only iteration loop, under its harness/guardrails. Reusable beyond #bob-dq. |
| **vector-studio** | **ELEVATE** | Pure consumer of the evaluation sheet. Assessment + elevation into the blueprint; flags weak evidence but never fixes it locally. The common vocabulary. |

The two contracts between them are the [[gls-project-spec|bob-client-project-spec]] (canvas →
dq-studio: outcomes, key issues, rule scope, financial-impact types, levers, phases, ROM
assumptions) and the 38-column [[gls-evaluation-sheet|evaluation sheet]] (dq-studio →
vector-studio). The project-spec exit is the implementation phase — **a one-way door**; after
handover the scope door closes by default, and only fringe cases reopen it deliberately.

## `#0-sc-engage` — Engage

Facilitate engagement with client teams to increase **efficiency, knowledge transfer, consistency
and end result**. Parent of three sub-components.

- **bob-canvas** — the [[gls-client-instrument|opportunity-start instrument]], operated at L1/L2
  altitude. It opens at *"what business outcomes do we want to drive — and how can we use data to
  get there"* and **sells the finish**: the conversation starts from what the finished blueprint
  looks like. It walks the outcomes journey L1→L5, computes
  [[gls-value-potential|value potential]] from editable labelled assumptions, shows a click-through
  mock-up of how execution works, and **exports the project spec**. Facilitation SOP:
  [[prc-run-the-blueprint-room]].
- **Info-gathering** — a prompt-based, interactive and flexible mechanism derived from the
  Project-QA engagement type. It gathers **information about the business process today versus its
  value** — the L3 layer, captured in the client's own terms — and replaces unstructured workshops
  with structured capture. Its real job is removing expectation-debt workshops.
- **[[gls-ctx-server|ctx-server]]** — the customer-context layer: an MCP server holding the
  per-opportunity customer-information repository (public research, info-gathering output,
  conversation briefings, AE notes), exposed to the AI surfaces of the chain. **Connectivity
  without consolidation** — the apps stay separate, the context is shared. Internal-only; contains
  no customer system data.

> [!important]
> Neither investment nor timeline sits in the always-on canvas console. Time-to-value belongs in
> the Solution Proposal; investment enters in the internal workbench, in the commercial annex.

## `#1-d3p` — Data Provisioning, Preparation, Profiling

Get the data in and understood. ABAP extractor reuse, direct source extraction, **bespoke
SQL-based data profiling** (generated as a schema-profiler bundle), and SQL-based data preparation.
Execution happens on the engagement's [[gls-adm|ADM]]-M environment — client-hosted or
Syniti-hosted, the mechanics are identical because dq-studio generates the scripts and they are
handed to the implementation team. Hosting is a single variable in the project spec, not a fork in
the method. Method: [[prc-assess-and-discover]].

> [!warning]
> **Critical scheduling property:** the timeline of #bob-dq **does not start until this component is
> complete.** Deliberate — it insulates the promised timeline from provisioning drag.

## `#2-rules` — Rules

The foundation of the implementation is the DQ rule set, **derived from the business outcomes** —
imported as scope via the project spec, generated as implementations by dq-studio.

- The rule catalog **exists as a seed, not a fixed baseline** in early stages; dq-studio converts
  existing rules from rule repositories.
- dq-studio carries the outcome linkage per rule (`outcome_links`, `outcome_category`,
  `key_issue_id`, `value_lever`).
- **No rule without an outcome pulling it** — import-enforced.
- Data-readiness rules are in scope, **gated by outcome**: they enter the seed only when the
  *digital transformation readiness* outcome is selected.
- Rules are built in SQL and deployed in SQL; validation, testing and adjustments are
  **programmatically generated** (unit tests plus deploy scripts). Output bar: **trusted,
  implementation-ready tools.**

Rule lifecycle is **hyper-DQOps**: instead of the enterprise five-step process (define → specify →
build → validate-improve → publish) with its overhead, execution on source data follows a
compressed process in which the generated specs, tests, deploys and tracker are the control
surface. Structure and control without enterprise-grade ceremony.

## `#3-validate-improve` — Validate & improve

Reports identify **potential points for clarification**, produced from generated scripts. A
**bounded** [[gls-iteration-loop|iteration loop]] runs with the client data team — findings →
clarification → rule adjustment → re-execution — **without a change-request cycle**.

**Exit condition:** the rule set is stable and results are accepted as the evidence base.

## `#4-present-vector-studio` — Present

Elevate the DQ results and the Business Outcomes Summary into the published blueprint. The
component ingests the 38-column evaluation sheet — the existing contract — and is where **weak
evidence is identified**: the flag goes back to dq-studio for regeneration. *Vector-studio never
authors SQL.*

Method rules that hold inside it: addressable populations not gross counts · anchoring to the
client's own financials where available · assumptions sheet separate and consultant-owned ·
distinct lenses never summed · **pull the levers you have** · sequencing is what makes the output a
Blueprint rather than an Assessment. The arithmetic behind those rules is
[[prn-value-discipline]]; what ships is [[ref-deliverables-inventory]].

**"Start where you finish":** the blueprint form, sanitised, is also a canvas asset — the opening
conversation shows the finish, which is what closes the loop back to `#0-sc-engage`.

## What never happens

The #bob-dq applications **never touch customer data or customer systems**. The canvas holds
opportunity and context material; dq-studio holds scope, metadata and generated scripts; execution
happens on the engagement's ADM-M environment by the implementation team; the apps ingest **result
sheets only**. Nothing is deployed into the client estate — the client runs SQL they can read and
receives an HTML file they can open.
