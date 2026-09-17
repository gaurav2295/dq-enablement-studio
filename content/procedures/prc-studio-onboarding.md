---
id: prc-studio-onboarding
type: procedure
title: Studio Onboarding — Your First Hour
domain: studio
audience: [consultant]
level: foundation
status: review
sources:
  - academy:index.html#studio-intro
  - academy:index.html#create-account
  - academy:index.html#session-config
  - coe:reconciled against the current app per CONFLICT-020 (no account/org/login layer ships)
tags: [onboarding, first-hour]
created: 2026-08-21
updated: 2026-08-21
links:
  - relates:ref-home-page
  - relates:con-studio-capabilities
  - relates:ref-config-editor
  - relates:con-multi-implementation-model
  - relates:prc-derive-a-dq-rule
---

## Goal

Get from "never opened the Studio" to "systems configured, oriented in the app, ready to derive a
rule" in the first hour. This is setup and orientation only — the actual derivation walkthrough is
[[prc-derive-a-dq-rule|Derive a DQ Rule]].

## When to use

- Onboarding a new consultant before their first derivation
- Standing up a fresh project for a new client engagement
- Re-orienting after time away from the Studio

## Prerequisites

- A running Studio instance — see Ports, Install & Versioning
  for setup
- Read-only access to the client's SAP systems, if you'll point at real data
- An Anthropic API key — only if you want AI Derive / AI Enhance. Local Derive works without one.

> [!note] There is no account to create
> If you're coming from an older training guide that talks about registering an account, verifying
> an email, or creating an "organization" — that describes a different design than what ships
> today. The Studio is a locally-run app, not a hosted multi-tenant product. See CONFLICT-020.

## Steps

### 1. Start the app

No login screen. See Ports, Install & Versioning for the
full install/run reference and port overrides.

### 2. Land on the project hub

The `/` route is the project hub and switcher, not a Dashboard you configure a "Session" from.
The sidebar footer shows the Studio's version — note it; it tells support which behavior to
expect. See [[ref-home-page|Home Page]].

**Home Page — Studio Landing Screen:**

The hub shows the Studio's core pitch: "Describe it — the Studio builds it." It displays recent rules (if any), quick-start templates, and the four DQ assets (Table Profile, Distribution Profile, Data Quality Rules, Attribute Usage) with their live samples. Use the "Open Workspace" button to enter the DQ Rules space.

**Left sidebar navigation:**
- **Home** — Always links back to the project hub
- **Execution Spaces** — Five numbered sections (① DQ Rules, ② Catalog, ③ Profile, ④ Ship, ⑤ Audit)
- **Admin section** — Methodology, Insights, Admin, Session Setup (collapsed menu at bottom)

### 3. Pick or configure your project

The unit of setup is a **project**. Two ship by default: `sap_ecc` (the default) and
`sap_s4hana`. Open the Settings/Config space to:

- Confirm the **source systems** in scope (with their friendly aliases) — this is what every
  generated rule's system filter reads from, and what [[con-multi-implementation-model|the
  fan-out model]] uses to know how many implementations a rule produces.
- Confirm the **databases** (working / prep / source) the project points at.
- Leave anything outside the editable settings alone — Settings can only touch a handful of
  project-level fields; everything else (naming patterns, ERP pack, SKP defaults) is edited by
  hand in the project's configuration file. See [[ref-config-editor|Config Editor]].

**Session Setup — ERP System & Foundation:**

The Session Setup page shows the active ERP knowledge pack (e.g., SAP ECC) and lets you view/edit the source systems and their database mappings. This is the "foundation" all execution spaces build on — once set, DQ Rules, Schema Profile, and Attribute Usage all read from these definitions.

**What you'll see in the UI:**

```
┌──────────────────────────────────────┐
│ Session Setup                        │
├──────────────────────────────────────┤
│ This foundation for the whole        │
│ session — the ERP knowledge pack,    │
│ databases, and source systems that   │
│ every execution space builds on.     │
│ Set it here once; DQ Rules, Schema   │
│ Profile, and Attribute Usage all     │
│ read from it.                        │
│                                      │
│ ERP System           [SAP ECC]       │
│ ├─ ACTIVE ERP KNOWLEDGE PACK         │
│ │  SAP ECC ◇ SAP ECC Central         │
│ │  Component                         │
│                                      │
│ Source Systems and Databases:        │
│ ├─ SRCECC02100 (P02) → WRKDQ        │
│ ├─ SRCECC03100 (P03) → WRKDQ        │
│ └─ [View/Edit Mappings]              │
│                                      │
│ ⓘ Foundation - read-only once set   │
│   (changes require re-import)        │
└──────────────────────────────────────┘
```

**Key elements:**
- **ACTIVE ERP KNOWLEDGE PACK** — Dropdown showing the ERP system in scope (SAP ECC, S/4HANA, etc.)
- **Foundation banner** — Info note explaining this is read-only once set
- **System badge** — Quick indicator like "SAP ECC" showing which pack is active
- **Source systems list** — Read-only view of configured systems and their aliases

**Project Configuration — Settings/Config Space:**

The Project Configuration form displays all editable project-level settings in a single scrollable interface:

**Form Layout (What you'll see):**

```
┌─────────────────────────────────────────────────┐
│ PROJECT NAME                                    │
│ ┌───────────────────────────────────────────┐  │
│ │ SAP ECC Default                           │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
│ ERP SYSTEM                                      │
│ ┌───────────────────────────────────────────┐  │
│ │ sap_ecc                                   │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
│ SOURCE DATABASE (PROVENANCE ONLY)              │
│ ┌───────────────────────────────────────────┐  │
│ │ SRCECC_DA                                 │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
│ PREP DATABASE (SELECT FROM)                    │
│ ┌───────────────────────────────────────────┐  │
│ │ WRKDQ                                     │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
│ WORKING DATABASE (CREATE VIEW)                 │
│ ┌───────────────────────────────────────────┐  │
│ │ WRKDQTEST                                 │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
│ DEFAULT SOURCE SYSTEM ID                       │
│ ┌───────────────────────────────────────────┐  │
│ │ ECCP80100_DQ                              │  │
│ └───────────────────────────────────────────┘  │
│                                                 │
│ SOURCE SYSTEMS & ALIASES                       │
│ ┌─────────────────┬──────────┬───────────────┐ │
│ │ CODE (zSrcSys)  │ ALIAS    │ INCLUDE FAN-O │ │
│ ├─────────────────┼──────────┼───────────────┤ │
│ │ SRCECCZ02100    │ P02      │ ☑             │ │
│ │ SRCECCZ03100    │ P03      │ ☑             │ │
│ ├─────────────────┼──────────┼───────────────┤ │
│ │ + Add System                                 │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ ⚠️ Saving rewrites config/projects/sap_ecc.   │
│    yaml. Comments are not preserved on save.  │
│                                                 │
│ [Save Project Settings]  [Reset]              │
└─────────────────────────────────────────────────┘
```

**Fields Explained:**

| Field | Type | Purpose |
|-------|------|---------|
| **Project Name** | Text | Display name (e.g., "SAP ECC Default") |
| **ERP System** | Dropdown | Read-only; set from Session Setup (e.g., `sap_ecc`) |
| **Source Database** | Text | Raw source system database (PROVENANCE ONLY — rules don't write here). Example: `SRCECC_DA` |
| **Prep Database** | Text | Pre-merged staging layer where rules execute. Example: `WRKDQ` |
| **Working Database** | Text | Where generated rule VIEW definitions live. Example: `WRKDQTEST` |
| **Default Source System ID** | Text | Fallback zSourceSystemID when a rule doesn't specify one. Example: `ECCP80100_DQ` |
| **Source Systems & Aliases** | Table | Multi-row section: Code (zSourceSystemID) + Alias + Include in fan-out checkbox |

**Key visual indicators:**
- ⚠️ **Yellow warning banner** — appears before saving; reminds you that comments will be lost
- **Save Project Settings button** (blue) — persists all changes
- **Reset button** — reverts to last saved state

**Adding source systems:**

Source systems are **free-text input** — there is no fixed list. Define the systems your engagement covers:

1. In the **Source Systems & Aliases** section, click **+ Add System**
2. Enter the system **Code** (zSourceSystemID value, e.g., `SRCECC02100`, `SRCS4H01`, or any custom identifier)
3. Enter the **Alias** (short label for view names, e.g., `P02`, `PR`)
4. Check **Include in fan-out** if this system should receive its own rule implementations when rules are fanned out across multiple systems
5. Click Save

Once added, all rules will be able to filter on this system, and [[prc-fan-out-a-rule-per-system|fan-out]] will generate system-specific implementations if enabled.

After any configuration change, click "Save Project Settings" — but note the warning: saving rewrites the whole YAML file and does **not preserve comments**. If teammates left explanatory notes in the config file, hand-edit instead.

> [!warning] Saving from the UI strips comments
> The Settings page rewrites the whole configuration file, which does not preserve explanatory
> comments. If a teammate left explanatory comments in the project configuration, don't "just
> save" from the UI to make a small change — hand-edit the file instead, or you'll silently erase
> them.

### 4. Set your API key, if you want AI Derive / AI Enhance

**AI Integration — Settings/Config Space:**

The AI Integration section (also in Settings/Config) allows you to configure one or more LLM providers for AI Convert Name, AI Enhance, SQL Review, and other AI-assisted workflows. Each provider is its own endpoint (Anthropic, OpenAI, or any OpenAI-compatible custom gateway) with its own key and model — mark one as "Active" to use it.

**What you'll see in the UI:**

```
┌──────────────────────────────────────┐
│ AI Integration  [Not configured]     │
├──────────────────────────────────────┤
│ Configure one or more LLM providers  │
│ for AI Convert Name, AI Enhance,     │
│ SQL Review, and other AI workflows.  │
│ Each provider is its own endpoint    │
│ (Anthropic, OpenAI, or custom) with  │
│ its own key and model — mark one as  │
│ "Active" to use it.                  │
│ No providers configured yet.         │
│                                      │
│        + Add provider                │
└──────────────────────────────────────┘
```

**Key resolution order** (if you want AI paths):
1. **Session-level key** (set in Settings/Config) — **highest priority** ⭐
2. **Environment variable** (`ANTHROPIC_API_KEY`) — fallback
3. **No key** → Error: "API key required"

Local Derive needs no key at all — it's the deterministic, no-API-call path. Set whichever level makes sense for you; if none resolves, the app returns a clear "API key required" error rather than silently making an empty call. See AI Client Conventions.

### 5. Find your way around: the five spaces

The current navigation is five execution spaces, not a page list to memorize by URL. Each space in the left sidebar has a dedicated number (1–5) for easy reference. When you open **DQ Rules** (① Space 1), you'll see:

**DQ Rules Workspace Layout:**
- **Left sidebar** — Five numbered execution spaces, plus Admin menu
- **Main panel** — "Add Rules to the Workspace" form on top, with tabs for "Single rule" and "Add many"
- **Rules list** — Below the form, a table showing staged rules with:
  - Rule ID and name (truncated with `...`)
  - Status badge (e.g., "Error", score indicator)
  - SQL state (e.g., "SQL Generated")
  - Implementation count
  - Individual action buttons (X to remove)
- **Bulk actions** — "Clear all", "AI Enhance All", "Ship →" buttons to manage all staged rules

| Space | Number | Purpose | Engagement-Dependent? |
|---|---|---|---|
| DQ Rules | 1 | Describe, derive, score, and refine rules — one at a time or in bulk | ✅ Required for rule-writing |
| Catalog | 2 | Browse reusable rule templates and governance standards | Optional — reference only |
| Profile | 3 | Run Schema Profile + Attribute Usage — the per-field census before rule work | Recommended; optional if profiling out-of-scope |
| Ship | 4 | Package the tracker + deploy SQL + specs + tests for handoff | ✅ Required for deployment |
| Audit | 5 | Review rule quality, parity checks, and compliance audit logs | Optional — quality gate |

**The Five Execution Spaces:**

**DQ Studio Navigation — Left Sidebar:**

```
┌─────────────────────────┐
│      DQ STUDIO          │
├─────────────────────────┤
│ 🏠 Home                 │
├─────────────────────────┤
│ EXECUTION SPACES        │
│                         │
│ ① 📋 DQ Rules      (20) │
│ ② 📚 Catalog           │
│ ③ 📊 Profile           │
│    └─ Schema Profile    │
│    └─ Attribute Usage   │
│ ④ 📦 Ship              │
│ ⑤ ✓  Audit             │
└─────────────────────────┘
```

**Space meanings:**
- **①  DQ Rules** — Describe and derive rules (primary workspace)
- **② Catalog** — Browse rule templates and governance standards
- **③ Profile** — Run schema & attribute profiling (sub-menu expanded)
- **④ Ship** — Package and deploy rule assets
- **⑤ Audit** — Review rule quality and compliance

### Which spaces do I actually need?

Usage depends on **engagement scope**. See [[qa-optional-studio-spaces-per-engagement|Which Studio spaces are required for my engagement?]] for detailed scenarios.

**Real-world examples:**

- **Profiling-only engagement** (client baseline assessment): Profile only → skip DQ Rules, Catalog, Ship, Audit
- **Rule development + testing** (client wants rules reviewed before deployment): DQ Rules + Profile + Audit → Ship later
- **Rule migration & deployment** (client has existing rules): DQ Rules + Ship → Profile/Catalog/Audit optional
- **Full end-to-end** (greenfield engagement): All 5 spaces — Profile first, then DQ Rules, Catalog reference, Audit throughout, Ship at close

See
[[con-studio-capabilities|The Four Studio Capabilities]] for the full purpose/benefit/impact brief
on the client-facing four (Table Profile, Distribution Profile, Data Quality Rules, Attribute
Usage) — that is the capability framing, not the full space list. If you land on an old link like
`/single`, `/bulk`, `/profiler`, `/skp`, or
`/config`, don't worry — those still work, they just redirect into the space above that replaced
them.

### 6. Take a look before you derive anything

Open DQ Rules and read one existing rule's spec end to end — output fields (5 sections), logic,
joins, filters — before writing your own. It's faster to recognize the shape than to learn it from
a blank form. When you're ready to write one, move to
[[prc-derive-a-dq-rule|Derive a DQ Rule (single rule)]].

## Verification

- The app is running and reachable in your browser, with no errors in the console
- Session Setup shows the source systems and databases you expect for this engagement
- If you configured an API key, a Local→AI Derive round trip on a throwaway rule name succeeds
  without an "API key required" error

## Common pitfalls

### 1. Looking for a signup/login flow

**The mistake:** You open the Studio and expect to see a login screen, create an account, or set up an "organization" — like you would with any SaaS product.

**What actually happens:** There is no login screen. The Studio is a **locally-run application**, not a hosted multi-tenant product. You open it, and you're in. No account creation, no email verification, no organization setup.

**Why this matters:** If an older training guide, a colleague, or documentation describes signup/login/organizations, they're describing a different design that **is not in the shipped app** — see `CONFLICT-020`. You won't find it, no matter how hard you look. Don't waste time hunting for it.

**What to do instead:** Start the Studio locally (see Ports, Install & Versioning), and you're immediately ready to configure your project in Session Setup.

---

### 2. Editing the project YAML by hand, then also saving from Settings

**The mistake:** You edit `project.yaml` directly in your editor to add a comment or fix a field, then later (or simultaneously) click "Save Project Settings" in the Studio's Settings/Config page.

**What goes wrong:** The Settings save **rewrites the entire YAML file** without preserving your comments. Any explanatory notes you added are silently erased. If you edited a field by hand and then click Save in Settings, the Settings panel's value wins — your hand edit disappears.

**Why this matters:** Comments are how teammates document *why* a system code is what it is, or remind the next person about a data model quirk. Losing comments creates knowledge gaps.

**What to do instead:** Pick **one editing path per change**:
- Use **hand-edit only** if you want to preserve comments
- Use **Settings UI only** if the change is simple and comments aren't critical
- Never mix both for the same file in the same session

---

### 3. Assuming the environment variable always wins for the API key

**The mistake:** You set `ANTHROPIC_API_KEY` as an environment variable and assume it will be used for all AI Derive/Enhance calls, no matter what.

**What actually happens:** The API key resolution is **not** "environment variable always wins." The priority order is:
1. **Session-level key** (set in the Studio's Settings/Config) — **highest priority**
2. **Environment variable** (`ANTHROPIC_API_KEY`) — fallback
3. **No key** — error ("API key required")

**The problem:** If you (or someone else) set an API key in a previous Studio session and forgot to clear it, that key **silently overrides** your environment variable. You think you're using your environment key, but the stale session key is being used instead.

**Why this matters:** This can cause:
- Wrong API account charged (if using different org keys)
- Unexpected rate limits (if using a key with lower quota)
- Silent failures (if the session key is invalid)

**What to do instead:**
1. Always check the **Settings/Config page** to see what API key is currently active
2. If you see a key set at the session level, decide: clear it (use env variable) or keep it (use session key)
3. Be explicit: only rely on the environment variable if you've explicitly cleared the session-level key

---

### 4. Bookmarking the old page URLs and being confused when they redirect

**The mistake:** You bookmark URLs like `/single`, `/bulk`, `/profiler`, `/skp`, or `/config` from an older Studio version, then navigate to one of your bookmarks in a newer version.

**What happens:** The URL still works, but you don't land on a dedicated page called "Single Rule Designer" or "Profiler" — you land in the **current space layout** (Space 1: DQ Rules, Space 3: Profile, etc.). The UI looks different from what you remembered, and you're confused.

**Why this matters:** The page layout changed from a URL-based navigation model (one page per feature) to a space-based navigation model (five execution spaces). Old bookmarks are honoured for backward compatibility, but they redirect to the new location, which can feel disorienting.

**What to do instead:**
1. **Bookmark the space layouts instead** of the old page URLs
2. **Use the sidebar numbers** (1–5) to navigate, not URLs
3. If you find yourself at a URL like `/single?rule=...`, know it's equivalent to Space 1 (DQ Rules) — you're in the right place, just the layout is different

## Related

- [[ref-home-page|Studio — Home Page]]
- Studio — Ports, Install & Versioning
- [[con-studio-capabilities|The Four Studio Capabilities]]
- [[ref-config-editor|Studio — Config Editor]]
- Studio — AI Client Conventions
- [[prc-derive-a-dq-rule|Derive a DQ Rule (single rule)]]
