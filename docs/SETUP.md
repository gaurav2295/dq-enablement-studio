# Deployment & setup

The deliverable is **one file**: `dist/enablement-master.html`. No server, no dependencies, no
build step for consumers.

## Give it to people

| Channel | How |
|---|---|
| File share / intranet | Copy `dist/enablement-master.html` anywhere reachable; users double-click it. |
| Web server | Drop the file in any static web root (Apache/nginx/IIS/SharePoint doc library). |
| Repo clone | `git pull`, open `dist/enablement-master.html`. |
| Email | The file is ~4 MB and self-contained; attaching it works when nothing else does. |

Progress and draft changesets live in the reader's browser `localStorage` — they survive
reloads on the same machine + path, and are lost if the file is opened from a different
location (documented in the app; a progress export/import is on the roadmap).

## Collect feedback

Readers use **Review mode** (✍) and export a JSON changeset. Collect those files (email,
Teams, share folder) and drop them into `feedback/inbox/`, then:

```bash
python3 build/merge_changesets.py --stage   # see what arrived
python3 build/merge_changesets.py --apply   # apply hash-safe edits, stage the rest for triage
python3 build/build.py                      # rebuild the app
```

Questions and flagged issues stay pending for a Claude session (or a human) to triage —
questions typically become new Q&A units, so asking improves the base for everyone.

## Rebuild after content changes

```bash
python3 build/build.py
```

Python 3.9+ standard library only. The build fails loudly on any validation error and writes
`dist/validation-report.md` either way. Commit `content/`, `taxonomy/` and `dist/` together.

## Requirements

- Consumers: any modern browser (Chrome/Edge 90+, Firefox 88+, Safari 14+). Offline fine.
- Maintainers: Python 3.9+, a clone of this repo, and the authoring rules in `CLAUDE.md`.
