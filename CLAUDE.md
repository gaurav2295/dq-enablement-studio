# DQ Enablement Studio — authoring rules for Claude sessions

This folder is the **canonical home of the CoE's DQ methodology knowledge** ("enablement-master").
Content lives as typed markdown knowledge units in `content/`; `build/build.py` compiles the
single-file app `dist/enablement-master.html` plus RAG-ready `dist/chunks.jsonl`. The Obsidian
vault mirror in the estate hub was **seed only** — do not sync from it; this repo is the master.

## The one command

```bash
python3 build/build.py
```

Stdlib-only, deterministic, byte-stable output. It fails (nonzero) on any validation error and
writes `dist/validation-report.md`. **Never commit content that doesn't build clean.**

## Authoring a knowledge unit

- One unit = one `.md` file in `content/<folder>/<id>.md`. The `id` frontmatter, the filename,
  and the folder must agree (`con-*` in `concepts/`, `prn-*` in `principles/`, `std-*` in
  `standards/`, `prc-*` in `procedures/`, `ref-*` in `reference/`, `gls-*` in `glossary/`,
  `qa-*` in `qa/`). IDs are stable forever — never rename; use `supersedes:` instead.
- Frontmatter is **strict flat YAML**: `key: value`, `key: [a, b]`, or indented `- item` lists
  only. Required: `id, type, title, domain, audience, level, status, sources, created, updated`.
  Optional: `kind` (decision on principles, pattern on standards), `links` (`rel:target-id`),
  `supersedes`, `sql_practice`, `tags`. All vocabularies are closed — see
  `taxonomy/taxonomy.json`.
- Body markdown subset: `##`/`###` headings, bold/italic/inline-code, fenced code blocks
  (```sql gets highlighting), pipe tables, lists (one nesting level), blockquotes and Obsidian
  callouts (`> [!note]`, `> [!warning]`, `> [!tip]`, `> [!important]`, `> [!info]`,
  `> [!example]`, `> [!success]`), wikilinks `[[unit-id]]` /
  `[[unit-id|label]]`, external `[text](url)`. **Raw HTML is a build error.**
- `sources:` records provenance as `repo-key:relative/path` (repo keys in taxonomy.json).
  Every unit has at least one source; units authored fresh use `coe:<context>`.
- Status: new/AI-transformed content starts `review`; a human (or an explicit CoE decision)
  moves it to `approved`. Never delete an obsolete unit — set `status: deprecated` and add
  `supersedes:` on its replacement.

## Duties that come with editing content

1. **Conflicts** — if two sources (or a consultant and a source) disagree, do not silently pick
   one. Record it in `docs/CONFLICTS.md` (`CONFLICT-NNN` format), link the units with
   `contrast:`, and leave resolution to a logged decision.
2. **Cross-references** — when you touch a unit, check its `links` still make sense and add the
   obvious missing ones. The graph is a first-class deliverable.
3. **Seed map** — bulk transformations from external sources must append to
   `taxonomy/seed-map.json` (source path → unit ids).
4. **Rebuild + commit dist/** — `dist/` is committed on purpose (consultants open the app from
   a file share without Python). After content changes: build, verify zero errors, commit
   content + dist together.

## Consultant feedback

Exported changeset JSON (`em-changeset/1`) lands in `feedback/inbox/`. Run
`python3 build/merge_changesets.py --stage` to triage; `--apply` auto-applies only hash-safe
`edit` ops. Questions become `qa/` draft units; notes and flags are handled in a Claude session
and the changeset file moves to `feedback/applied/`.

## Never

- Never hand-edit `dist/` (build output only).
- Never introduce a dependency (build is stdlib-only; app is a single offline HTML file).
- Never copy client-confidential material into `content/` (same rule as every CoE repo).
- Never reorganise `taxonomy/taxonomy.json` vocabularies casually — closed vocab changes are
  CoE decisions with a commit message explaining why.
