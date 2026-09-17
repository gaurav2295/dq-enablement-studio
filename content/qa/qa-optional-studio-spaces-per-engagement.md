---
id: qa-optional-studio-spaces-per-engagement
type: qa
title: Which Studio spaces are required for my engagement?
domain: studio
audience: [consultant]
level: foundation
status: approved
sources:
  - coe:deduced from prc-studio-onboarding
created: 2026-09-02
updated: 2026-09-02
links:
  - parent:prc-studio-onboarding
  - relates:con-studio-capabilities
  - relates:gls-dq-studio
  - relates:ref-deliverables-inventory
---

## Question

Are all five spaces expected to be used during every engagement, or are some optional depending on the project's objectives?

## Answer

**Not all five spaces are required for every engagement.** Usage depends entirely on your engagement scope and deliverables. Session Setup (Settings) is always needed — it's the foundation — but the five execution spaces vary.

### Required vs. Optional by Engagement Type

### Profiling-Only Engagement
**Scope:** Baseline data quality assessment; client wants to understand what they have (no rules yet).

- ✅ **Profile** (required) — Run schema profiling + attribute usage to capture per-field distributions, nulls, cardinality, values by system/org
- ❌ **DQ Rules** — Skip (no rules to write)
- ❌ **Catalog** — Skip (reference only)
- ❌ **Ship** — Skip (nothing to deploy)
- ❌ **Audit** — Skip (no rules to review)

**Deliverable:** Profile reports showing data patterns, anomalies, and readiness for rule definition.

---

### Rule Development + Testing (No Deployment Yet)
**Scope:** Write and test rules locally; client reviews before handoff; deployment happens later or in a separate engagement.

- ✅ **Profile** (recommended) — Run first to understand data before writing rules
- ✅ **DQ Rules** (required) — Describe, derive, and refine rules
- ❌ **Catalog** — Optional; use only if reviewing reusable patterns
- ❌ **Ship** — Skip (not deploying yet)
- ⚠️ **Audit** (optional) — Use if client wants quality/parity review before sign-off

**Deliverable:** Rule specs, test results, quality scores; ready for handoff when client approves.

---

### Rule Migration & Multi-System Deployment
**Scope:** Client has existing rules (from legacy system or prior engagement); need to fan-out to multiple source systems and deploy.

- ✅ **DQ Rules** (required) — Import/adapt existing rules, fan-out to each system
- ⚠️ **Profile** (optional) — Skip if systems are already well-understood; use if migrating between ERP versions
- ❌ **Catalog** — Skip (migration-specific, not template-focused)
- ✅ **Ship** (required) — Deploy rules to each system's databases
- ⚠️ **Audit** (optional) — Use to verify parity across fan-out implementations

**Deliverable:** Deployed rules across all source systems; deployment artifacts and verification log.

---

### Full End-to-End Engagement (Greenfield)
**Scope:** Complete DQ program build from assessment through deployment; client is new to DQ rules or this ERP system.

- ✅ **Profile** (required first) — Baseline assessment; understand data before designing rules
- ✅ **DQ Rules** (required) — Design, derive, and refine all rules in scope
- ⚠️ **Catalog** (optional) — Reference existing rule patterns; promote reusable rules to Catalog if creating a shared library
- ✅ **Ship** (required) — Package and deploy to production
- ✅ **Audit** (required) — Continuous quality review throughout; final parity/compliance audit before close

**Deliverable:** Complete ruleset, deployment package, quality attestation, production monitoring setup.

---

### Catalog Governance / Template Library Build
**Scope:** Client wants to create or update a shared rule library (Catalog); not writing project-specific rules.

- ❌ **Profile** — Skip (assessment not in scope)
- ❌ **DQ Rules** — Skip (project rules not in scope)
- ✅ **Catalog** (required) — Create and organize reusable rule templates with governance metadata
- ❌ **Ship** — Skip (no deployment in this phase)
- ⚠️ **Audit** (optional) — Review Catalog for completeness and consistency

**Deliverable:** Documented Catalog with standardized rule templates, governance tags, and usage guides.

---

### Quick Decision Table

| Engagement Type | Profile | DQ Rules | Catalog | Ship | Audit |
|---|---|---|---|---|---|
| Profiling-only | ✅ | ❌ | ❌ | ❌ | ❌ |
| Rule dev + test | ✅ | ✅ | ⚠️ | ❌ | ⚠️ |
| Migration + deploy | ⚠️ | ✅ | ❌ | ✅ | ⚠️ |
| Full end-to-end | ✅ | ✅ | ⚠️ | ✅ | ✅ |
| Catalog build | ❌ | ❌ | ✅ | ❌ | ⚠️ |

**Legend:** ✅ = required, ⚠️ = optional (recommended for quality), ❌ = skip

---

### How to Determine Your Path

1. **Ask the client:** What does success look like at close?
   - "Show us what's broken" → Profile-only
   - "Write and test rules for us" → Rule dev + test
   - "We have rules; deploy them everywhere" → Migration + deploy
   - "Build a complete DQ program" → Full end-to-end

2. **Check the Statement of Work:** What deliverables are committed?
   - Baseline reports → Profile
   - Rule specs + tests → DQ Rules + Audit
   - Deployed rules + monitoring → Ship
   - Reusable templates → Catalog

3. **Plan your first hour:** Once you know which spaces you need, follow [[prc-studio-onboarding|Studio Onboarding]] for just those spaces.

---

### Related

- [[prc-studio-onboarding|Studio Onboarding — Your First Hour]]
- [[con-studio-capabilities|The Four Studio Capabilities]]
