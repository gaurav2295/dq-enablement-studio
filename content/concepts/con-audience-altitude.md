---
id: con-audience-altitude
type: concept
title: Audience Altitude
domain: delivery
audience: [consultant, lead]
level: practitioner
status: deprecated
sources:
  - bob-dq:enablement/enablement-guide.md
  - bob-dq:bob-canvas/enablement-notes.md
tags: [bob-dq, client-facing, vocabulary, facilitation]
created: 2026-08-20
updated: 2026-08-20
links:
  - relates:prc-run-the-blueprint-room
  - relates:std-client-vocabulary
  - relates:prc-handle-the-cold-room
  - parent:con-outcome-hierarchy-l1-l5
  - relates:gls-business-outcome
  - relates:gls-business-data-driver
  - relates:gls-business-rule
  - relates:gls-mode
  - relates:gls-variant
---

## What it is

**Audience altitude** is the discipline of matching what you say to who in the room owns the
number. The same fact — a broken material master field, an overdue invoice — reads as a different
sentence depending on whether the listener is a C-suite executive, a VP who owns a KPI, a process
owner who runs the workaround, or a technical audience that has to trust the check. Get the
altitude wrong and you either bore the executive with a field name or lose the technical audience
by hand-waving past the proof.

This concept underpins the #bob-dq Business Outcomes Canvas method — same content, four sheets, no
sheet prints the audience label. You hold the mapping in your head and narrate accordingly.

## The four altitudes (client tier)

| Level on the sheet | Who it's for | What you say |
|---|---|---|
| Outcomes ([[gls-business-outcome]]) | C-suite | Board language — working capital, spend, revenue. Start here. |
| Measures | VP / Director / head of department | The empirical number that person personally owns (DSO, overdue AR, duplicate-vendor spend). This is where funding decisions are made. |
| Business data drivers ([[gls-business-data-driver]]) | Process owner / programme lead | Where the effort is focused — the patterns a business owner can act on. |
| Business rules ([[gls-business-rule]]) | Data / technical audience | The proof. Reusable across clients; implementation bespoke to this one. |

The framing to hold onto: same chain, two directions — **down to sell, up to prove**. Client-facing
version, said out loud: *"down to the evidence, and back up to the value."*

## The L1→L5 hierarchy

The same four altitudes extend to a five-level organisational map used across the method (canvas,
proposal, and the handoff into delivery). The hierarchy itself — the register per level, the
inclusion criterion and the published outcome catalogue — is stated canonically in
[[con-outcome-hierarchy-l1-l5]]; the table below is the facilitation view of it.

| Level | Audience | What is expressed |
|---|---|---|
| L1 | C-suite | The business outcome, named — e.g. *working capital* |
| L2 | VP · Director · Head of Department | The same outcome, quantified — the empirical number the role owns |
| L3 | Process owner · Programme director | The process area where the number is made or lost |
| L4 | — | The data objects involved |
| L5 | — | The DQ rules that measure them |

## Persona-to-outcome mapping

Which outcome, which measure, which opening line, for which buyer. Each of the three buyer
personas below has a **worked opening line** — the sentence that lands cold. What is *not* yet
settled is the warm-versus-skeptical variation on that opening: only the CFO is scripted for room
temperature, and [[prc-handle-the-cold-room|Handle the Cold Room]] marks the other two as planned
rather than faking them.

### CFO / Finance

- **Hierarchy level:** L1 → L2 (outcome down to the measure they own).
- **Outcomes that land:** working capital; revenue leakage & assurance; procurement & spend.
- **Measures that land:** DSO, overdue AR, unapplied cash, DPO & payables accuracy,
  duplicate-vendor spend, credit-control exposure, billing hygiene.
- **What they fear:** being handed a soft number they can't defend upward — to their board, to a
  cost-programme review — and getting caught out on it.
- **What they demand as evidence:** a defensible number with a visible basis. Not certainty —
  traceability. They test whether you can show your working, not whether the number is big.
- **Opening line:** *"This is the size of the case your data is already making — evidenced rule by
  rule. What you'd take to the budget is what we build from it, with your own figures."*
- **Trigger that gets you the meeting:** business case scrutiny, a cost programme underway.

### COO

- **Hierarchy level:** L1 → L3 (outcome down to the process owner's territory).
- **Outcomes that land:** inventory & supply reliability; process & compliance exposure — plus
  *reduce unplanned downtime* where the client is manufacturing/EAM. Downtime is **not in the
  published L1 catalogue**: it was cut on walkability grounds and is held as a re-propose
  candidate, so raise it as framing, never as a scoped outcome. See
  [[con-outcome-hierarchy-l1-l5]] for its exact status.
- **Measures that land:** dead & no-movement stock, planning-data completeness, open-PO
  commitments, catalog hygiene.
- **What they fear:** operational consequence — a failed go-live, a process breaking in
  production — traced back to data nobody owned.
- **What they demand as evidence:** the operational chain. Not "your data is bad" — *what*
  breaks, *where*, and what changes it.
- **Opening line:** *"Here's what breaks operationally when this data goes uncorrected — and
  exactly where it breaks."*
- **Trigger that gets you the meeting:** a failed go-live, a process breakdown already in the
  room's memory.

### CDO / CIO / CTO (data leadership)

- **Hierarchy level:** L2 → L5 (measure down through to the rule — the full traceable chain).
- **Outcomes that land:** digital transformation readiness; process & compliance exposure — plus a
  mandate view across all outcomes, since this persona owns the data programme, not one P&L line.
- **What they fear:** losing the funding argument for the data programme itself — a board
  challenge on why data investment deserves budget at all.
- **What they demand as evidence:** end-to-end traceability, L2 through L5, and
  [[gls-coverage|coverage]] — which outcomes could be evidenced given the scope in play (never
  presented as a completeness score).
- **Opening line:** *"This gives your data programme the funding case and the mandate it doesn't
  have today — traceable from the board's language down to the rule that proves it."*
- **Trigger that gets you the meeting:** a budget cycle, or a board challenge on the value of data
  investment.

> [!note] Reading note
> VP/Head of Dept (L2, "the number they own, moved") and Process owner/Programme director (L3,
> "what to change, where") sit *inside* these three conversations — they are who the CFO and COO
> bring into the room, not separate openings you plan for.

## Altitude sort — worked drill

Who is a given sentence pitched at? The practice: sort each statement into C-suite / VP-Director /
Process owner / Technical before checking the answer.

| Statement | Altitude |
|---|---|
| "Working capital is trapped in receivables, payables and unapplied cash." | C-suite |
| "DSO is running higher than it should — that's the number I personally own." | VP / Director |
| "Duplicate vendor records are splitting our purchasing volume across the catalog." | Process owner |
| "This rule checks whether a credit limit was breached before the sales order posted." | Technical |
| "Overdue AR is sitting behind bad addresses and cancelled orders nobody chased." | VP / Director |
| "The board wants to see spend and revenue move, not a defect count." | C-suite |
| "Show me where the effort is focused — which patterns can I action." | Process owner |
| "Is this reusable across clients, and how is it tested on ours specifically?" | Technical |

## Common pitfalls

- Naming a data problem first instead of the outcome — it drops the conversation's altitude before
  it has earned the trip down.
- Showing the business-rules column (or explaining the technical proof) to an executive audience
  before they've asked for it.
- Treating a VP's measure and a process owner's driver as interchangeable — they own different
  numbers and want different evidence.

## Related

- [[prc-run-the-blueprint-room|Run the Blueprint Room]]
- [[std-client-vocabulary|Client Vocabulary — Say/Never-Say]]
- [[prc-handle-the-cold-room|Handle the Cold Room]]
