---
id: prc-estimate-blueprint-effort
type: procedure
title: Estimate Blueprint Delivery Effort — The Resourcing Rubric
domain: delivery
audience: [lead]
level: practitioner
status: deprecated
sources:
  - bob-dq:docs/resourcing-rubric.md
links:
  - relates:con-value-chain
  - relates:con-outcome-hierarchy-l1-l5
  - relates:gls-work-lanes
  - relates:gls-capacity-check
  - relates:gls-gdc
  - relates:gls-internal-workbench
  - relates:gls-time-to-value
tags: [bob-dq, resourcing, delivery]
created: 2026-08-20
updated: 2026-08-20
---

## Goal

Size the GDC team and duration needed to execute a selected #bob-dq rule set, from a rules-per-
person-week throughput ladder, a per-object complexity factor and a per-rule complexity factor —
with the SQL test kit and acceleration assumed as given.

This is **rubric v1**, owner-ratified 2026-08-05. It is not a black box: the constants and
formulas below are the justification artefact, the #bob-dq canvas app implements exactly them,
and a gate suite pins the outputs. The [[gls-work-lanes|quantitative lane]] (GDC rule execution)
is what it sizes; the qualitative lane is costed separately.

## When to use

- Sizing an engagement's rule-execution phase from a working rule cart (selected rules + objects
  in scope)
- Checking whether a proposed duration is actually staffable before it is quoted
- Explaining, to Delivery or Finance, why a given team shape produces a given capacity

## 1. Constants

**Throughput ladder** — rules per person per week, with the SQL test kit and acceleration
provided. Ranges are shown to the room; the conservative (committed) end prices every commitment.

| Grade | Range | Committed | Elastic-shape role |
|---|---|---|---|
| C2 | 15–20 | 15 | Floor / extension staffing only — not in the default shape |
| C3 | 25–30 | 25 | GDC Consultant(s) |
| C4 | 35–40 | 35 | GDC Senior Consultant |

**Person-week assumption:** 40 hours.

**Object-class factor** — derived from the intake's existing complexity badge (master data →
low/medium · transactional → medium/high · EAM → high/extra-high). It slows throughput for
volume-heavy and specialist objects.

| Badge | Factor | Reading |
|---|---|---|
| L | ×1.00 | master-data pace (Customer, Supplier) |
| M | ×0.90 | Material, Finance master, open items |
| H | ×0.75 | transactional volume (POs, PRs, equipment) |
| XH | ×0.60 | EAM structures (functional locations) |

**Rule-complexity factor** — placeholder tiers until per-rule complexity is available from the
rule repository: L ×1.15 · M ×1.00 (every rule, currently) · H ×0.80.

**Specialised input (SME)** — finance-flagged objects (the object name matches *finance* or *open
AR/AP items*) reserve hours *outside* the GDC ladder: **8 hours fixed + 4 hours per finance
object**, role Finance SME (specialist input). This capacity never competes with rule-execution
capacity.

**Minimum staffing floor** — the plan never staffs below: Data Quality Lead (oversight, part
allocation) + 1 × GDC Consultant (C3). It is rendered in every generated Resource Plan.

## 2. Formulas

```
objFactor      = mean(object_factor[badge] over objects in scope)          (1.0 if none)
rate(role)     = grades[grade(role)].lo × objFactor × ruleFactor           (committed end)
capacityRules  = floor( sum over GDC roles: (hours(role, selected weeks) / 40) × rate(role) )
weeklyRules    = sum over GDC shape: (realistic_hours / 7 / 40) × rate(role)
weeksRequired  = max(4, ceil(nRules / weeklyRules))     — shown even beyond the corridor
smeHours       = 8 + 4 × (# finance objects)            (0 if none)
```

**Verdict:** the file *fits* when `nRules <= capacityRules` (and the qualitative lane fits — its
constants, 12 hours/outcome + 1.5 hours/driver, are separate working assumptions).
`weeksRequired > 7` does not refuse silently: it renders honestly as beyond the 4–7-week corridor
— T&M-trigger territory under the elastic engagement model's fallback terms.

## 3. Worked example

Default working file: 24 rules · 6 objects — Customer master (L), Vendor master (L), Open AR items
(M) and Open AP items (M), the last two finance-flagged, plus two further objects (the source
names one of them M-class) → `objFactor` = 0.95.

- **7-week shape:** GDC Senior 120 h (3 person-weeks C4) + GDC Consultant 240 h (6 person-weeks
  C3) → floor((3×35 + 6×25) × 0.95) = **242 rules capacity** → 24 rules fit.
- **4-week shape:** 80 h + 80 h (2 person-weeks each) → floor((2×35 + 2×25) × 0.95) = **114** →
  fits.
- **Derived duration:** `weeklyRules` ≈ (120/7/40)×33.25 + (240/7/40)×23.75 ≈ 34.6 →
  ceil(24/34.6) = 1 → clamped to the 4-week floor → **4 weeks**.
- **SME:** 8 + 4×2 = **16 hours** reserved (Open AR items, Open AP items).
- **Over-capacity proof:** a 424-rule cart → capacity 242 → refuses; derived 13 weeks, beyond
  corridor → T&M framing. Do not quote a duration the capacity check refuses.

## 4. The 16 hours/rule retirement

16 hours/rule was measured end-to-end, pre-acceleration, on a live engagement — extraction +
execution + SME validation loops, where SME validation was the binding cap. The ladder above
(which assumes the SQL test kit and acceleration) replaces it for sizing. It is retained as the
historical record — do not resurrect it for sizing. The finding it originally produced (the
default 24-rule package running over budget at every duration) is superseded with it: under the
ladder, the default package fits at 4–7 weeks.

> [!warning]
> The per-object mini-estimator (a separate tool) still cross-checks in hours-per-object; this
> rubric sizes in rules. The two can disagree on unusual scopes — this is a known, unresolved
> seam, not a bug in either tool.

## 5. Change process

Owner ruling → bump the rubric version → update the source document → re-observe and re-pin any
literal test fixtures → changelog entry. Per-rule complexity tiers arrive once the rule
repository can supply per-rule complexity directly; the ladder and qualitative constants are
calibrated with Delivery.
