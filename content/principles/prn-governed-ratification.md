---
id: prn-governed-ratification
type: principle
kind: decision
title: ADR 0002 — Principle-Governed Ratification of Bulk Review Queues
domain: value-outcomes
audience: [lead]
level: advanced
status: deprecated
sources:
  - rule-repo:docs/adr/0002-principle-governed-ratification.md
tags: [rule-repo, adr, governance, decision]
created: 2026-08-20
updated: 2026-08-20
links:
  - prereq:prn-key-issues-primary-tier
  - relates:gls-business-data-driver
  - relates:gls-key-issue
  - relates:ref-key-issue-vocabulary
  - relates:ref-rule-record-schema
  - relates:con-rule-provenance-model
  - relates:gls-bulk-ratification
---

## Status

Accepted — ratified by the estate owner, 2026-08-05. Governs `syniti-dq-rule-repo`'s bulk
review queues (in `review/`): rule→driver linkage, `adm_rule_name` recovery, and future queues
of the same kind.

**Relation to ADR 0001.** This decision extends, never overrides,
[[prn-key-issues-primary-tier|ADR 0001]] — key issues remain owner-governed vocabulary. Creating
or renaming a driver still requires an explicit owner ruling under ADR 0001; this ADR only
governs how *bulk per-row decisions* against already-governed vocabulary get made.

## The decision

Per-row ratification of bulk queues does not scale to the owner walking every row. Instead:

1. The owner ratifies a **principle set** once per queue *kind*.
2. A session applies the principles deterministically, recording the deciding principle id,
   method and date on every row and on every catalogue edge it writes.
3. Verification is **measured, not self-reported**: programmatic invariants plus an independent
   re-check; agent self-reports are not evidence.
4. The owner receives a **short exception list** (rows the principles could not decide, or
   decided against the proposal) plus a **random sample of 12 applied decisions** with their
   evidence. Systematic error found in the sample voids the batch.
5. Rows failing the bar are resolved **honestly** — to the gap pool or a named repair queue,
   never force-linked, never silently dropped.

## The ratified principles

### Linkage (rule → driver)

| # | Principle |
|---|---|
| L1 · Two signals | A link is accepted only when the rule matches the driver on **both** its object and its defect theme. Object evidence may come from `primary_data_object`, `tables`, the rule text, or the ADM/view identity. Lexical overlap alone is insufficient. |
| L2 · Boilerplate evidences nothing | A rule whose text is generic ("must meet data quality requirements"…) links to nothing until repaired — unless its embedded view identity carries the concrete check, in which case the link stands and the *text* goes to repair. |
| L3 · Honest failure | Rows failing the bar return to the unlinked pool (the gap tray) or the repair queue; they stay eligible after repair. |
| L4 · One best fit | A rule links to its single closest driver — re-routing away from a proposed driver is allowed and recorded; a second driver only when the rule genuinely tests two distinct defects. |
| L5 · Provenance | Every applied link carries `method`, principle id and date in `linkage.edges[]`. |

Principles outrank a prior agent main-loop rejection — one bar for every row, owner-ruled
2026-08-05.

### Renames (`adm_rule_name` recovery)

| # | Principle |
|---|---|
| R1 · View identity governs | The name states what the view decomposition says the view checks (the documented `naming_basis` method). The original name is preserved. |
| R2 · Form | Declarative must-form (or "Profile of …" for informational); within the length limit. Off-form proposals are held, not fixed silently. |
| R3 · No re-collision | A proposed name equal to an existing catalogue name is held — collision was the original defect. |
| R4 · No ghost renames | Records not present in the catalogue (quarantined or unlocated) hold until recovered; a rename there is a no-op. |

Where the applied view-identity name shares fewer than two significant words with the record's
`rule` text, the record is flagged to a divergence queue rather than diverging further in
silence.

### Driver gaps discovered during application

A cluster of two or more same-defect rules with no existing driver is **not** linked to a
near-miss driver — it is recorded as a candidate for the next driver-proposal round under ADR
0001. First instance (2026-08-05): "Vendor master incomplete", 4 rules.

## What the first application measured (2026-08-05)

The ADR records its own first run, which is what makes the principles auditable rather than
aspirational:

| Queue | Outcome |
|---|---|
| 80 linkage rows | 56 accepted (L1) · 5 re-routed (L4) · 14 to the gap pool (L1/L3) · 2 to repair (L2) · 2 already applied · 1 declined as already better-linked |
| 128 renames | 97 applied (R1) · 5 held for re-collision (R3) · 3 held off-form (R2) · 23 held absent (R4) |

Catalogue driver coverage moved from 230 to 291 of 497 rules in that single application.

## Amendment 1 — the bounded night-run authority grant

For the night of 2026-08-05→06 the owner granted **one night of full authority, including driver
creation and key-issue → lever mapping** — a bounded amendment of ADR 0001's owner-only
vocabulary rule. Its conditions, all honoured: everything the night created or ruled was marked
**PROVISIONAL** in its provenance (library `lever_provenance.status`, catalogue edge methods,
driver `source` fields); a morning **ratify-or-revert pack** enumerated every provisional item;
and rules that could not be linked honestly went to a named exception list rather than being
force-linked.

**Closure (2026-08-06 morning sitting).** The owner walked the pack and ratified it in full — the
4 overrides, the 7 conflict resolutions, all 36 best-fit mappings, the 11 night-created drivers
and the P2P-008 object widening — and ruled the disposition of the 50 exceptions (quarantined to a
backlog file, tracked as a bob-dq backlog item). No provisional vocabulary remains and the grant
is closed; ADR 0001's owner-only rule stands for everything after it.

> [!important]
> The amendment is the pattern worth copying, not the exception: a time-boxed grant, every
> artefact of it labelled provisional at the moment of creation, and a scheduled sitting where a
> human ratifies or reverts item by item. Authority was widened for one night with the revert
> path built in first.

## Why this matters beyond the rule-repo

This is the governing pattern for every bulk AI-assisted decision queue that touches owner-ruled
vocabulary, not just this one repository's linkage/rename queues: ratify the principle once,
apply it deterministically at scale, verify by independent measurement rather than self-report,
and route anything the principle can't honestly decide to a named queue instead of forcing it.

## Related

- [[prn-key-issues-primary-tier]] — ADR 0001, the vocabulary-governance decision this one
  extends.
- [[ref-key-issue-vocabulary]] / [[ref-rule-record-schema]] — the data this ADR governs the
  bulk-decisioning of.
- [[gls-business-data-driver]] — the client-facing name for the "driver" this ADR's linkage
  principles resolve rules against.
