---
id: qa-studio-configuration-file-location
type: qa
title: Where Can We Find the Project's Configuration File?
domain: studio
audience: [consultant, developer]
level: practitioner
status: review
links:
  - parent:prc-studio-onboarding
  - relates:gls-project-spec
  - relates:gls-project-spec
sources:
  - coe:changeset-7-dq-studio-workflow-2026-08-31
created: 2026-09-02
updated: 2026-09-02
---

## Question

Where can we find the project's configuration file in the DQ Studio environment? Is it:
- Located in a specific directory within the Studio workspace?
- Available through the Project Hub interface?
- Stored in a version control repository (e.g., Git)?
- Accessible through settings or configuration menu?

## Context

New users starting with prc-studio-onboarding need to understand where project configuration is stored and how to access it for editing system aliases, database connections, and engagement scope parameters.

## Why This Matters

- **Setup and Onboarding** — Consultants need to locate config early in project setup
- **Troubleshooting** — Common issues (missing systems, wrong aliases) require config inspection
- **Reproducibility** — Project config version control is critical for team collaboration
- **Documentation** — Clear path to config file reduces support requests

## Related Concepts

- **Project Spec** ([[gls-project-spec]]) — What the config contains
- **System Alias** ([[gls-system-alias]]) — How systems are registered in config
- **YAML Structure** (project specification) — Config file format
- **Studio Onboarding** ([[prc-studio-onboarding]]) — Where this fits in setup

## Expected Answer Should Cover

1. **File location:** Absolute path or relative to Studio root (e.g., `.claude/project.yaml` or `config/project-config.json`)
2. **Access methods:** CLI commands, UI navigation, or direct file editing
3. **Version control:** Whether config is committed to Git, how to track changes
4. **Permissions:** Who can edit, backup/recovery procedures
5. **Format:** YAML, JSON, or custom format; pointer to schema/docs
6. **Example:** A real config snippet showing system aliases, database connections

## Suggested Answer Structure

```markdown
## Answer

The project's configuration file is typically located at:
[Path/location details]

### Accessing the Configuration

**Via Studio UI:** [Navigation steps]
**Via CLI:** [Command example]
**Via File System:** [Direct file location]

### File Structure

[YAML/JSON example with comments]

### Key Sections

- System Aliases
- Database Connections  
- Engagement Scope
- Settings

### Version Control

[How to track/commit config changes]

### Common Tasks

1. Add a new system
2. Update database connection
3. Reset to defaults
```

---

**Status:** Awaiting answer  
**Priority:** HIGH (foundational for studio onboarding)  
**Changeset:** 7 (DQ Studio Workflow)
