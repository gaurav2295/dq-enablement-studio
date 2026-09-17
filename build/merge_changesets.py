#!/usr/bin/env python3
"""merge_changesets.py — triage and apply consultant changesets (em-changeset/1).

Modes:
  python3 build/merge_changesets.py --stage   # report everything in feedback/inbox/
  python3 build/merge_changesets.py --apply   # apply hash-safe edit ops, move processed
                                              # changesets to feedback/applied/

Safety: an `edit` op is auto-applied ONLY if its base_hash matches the sha256 of
the target unit's current raw body (i.e. the unit hasn't changed since the build
the consultant was reading). Everything else — hash mismatches, notes, questions,
flags — is left for a Claude session to triage (questions typically become qa/
draft units). A conflicting edit is never forced.
"""

import hashlib
import json
import os
import re
import sys
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INBOX = os.path.join(ROOT, "feedback", "inbox")
APPLIED = os.path.join(ROOT, "feedback", "applied")
CONTENT = os.path.join(ROOT, "content")


def read(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


def find_unit(uid):
    for folder in sorted(os.listdir(CONTENT)):
        p = os.path.join(CONTENT, folder, uid + ".md")
        if os.path.isfile(p):
            return p
    return None


def split_unit(raw):
    end = raw.find("\n---", 4)
    return raw[: end + 4], raw[end + 4:].lstrip("\n")


def body_hash(body):
    return hashlib.sha256(body.encode("utf-8")).hexdigest()[:16]


def main():
    mode = sys.argv[1] if len(sys.argv) > 1 else "--stage"
    if mode not in ("--stage", "--apply"):
        print(__doc__)
        return 2
    files = sorted(f for f in os.listdir(INBOX) if f.endswith(".json")) if os.path.isdir(INBOX) else []
    if not files:
        print("Inbox empty — nothing to do.")
        return 0

    triage = []
    for fname in files:
        path = os.path.join(INBOX, fname)
        try:
            cs = json.loads(read(path))
        except ValueError as e:
            print("SKIP %s — not valid JSON (%s)" % (fname, e))
            continue
        if cs.get("schema") != "em-changeset/1":
            print("SKIP %s — unknown schema %r" % (fname, cs.get("schema")))
            continue
        author = cs.get("author", "anonymous")
        applied_ops, pending_ops = [], []
        for op in cs.get("ops", []):
            kind = op.get("op")
            uid = op.get("unit_id")
            if kind == "edit":
                upath = find_unit(uid or "")
                if not upath:
                    pending_ops.append((op, "unit %r not found" % uid))
                    continue
                fm, body = split_unit(read(upath))
                if body_hash(body) != op.get("base_hash"):
                    pending_ops.append((op, "hash mismatch — unit changed since export; needs manual merge"))
                    continue
                if mode == "--apply":
                    new_fm = re.sub(r"(?m)^updated:\s*.*$", "updated: " + date.today().isoformat(), fm)
                    write(upath, new_fm + "\n\n" + op["new_body"].rstrip("\n") + "\n")
                    applied_ops.append((op, "edit applied to " + os.path.relpath(upath, ROOT)))
                else:
                    applied_ops.append((op, "edit is hash-safe, would apply"))
            else:
                pending_ops.append((op, kind + " — needs Claude triage"))
        triage.append((fname, author, applied_ops, pending_ops))
        if mode == "--apply":
            os.makedirs(APPLIED, exist_ok=True)
            base = date.today().isoformat() + "-" + re.sub(r"[^a-z0-9]+", "-", author.lower()).strip("-")
            n, dest = 1, None
            while dest is None or os.path.exists(dest):
                dest = os.path.join(APPLIED, "%s-%d.json" % (base, n))
                n += 1
            os.rename(path, dest)

    print("# Changeset triage (%s)\n" % ("applied" if mode == "--apply" else "staged"))
    for fname, author, applied_ops, pending_ops in triage:
        print("## %s — %s" % (fname, author))
        for op, msg in applied_ops:
            print("  APPLIED  %-22s %s" % (op.get("unit_id") or "(corpus)", msg))
        for op, msg in pending_ops:
            text = (op.get("text") or op.get("new_body") or "")[:80].replace("\n", " ")
            print("  PENDING  %-22s %s :: %s" % (op.get("unit_id") or "(corpus)", msg, text))
        print()
    pending_total = sum(len(p) for _, _, _, p in triage)
    if mode == "--apply":
        print("Applied edits: %d · pending for triage: %d (changesets moved to feedback/applied/)" % (
            sum(len(a) for _, _, a, _ in triage), pending_total))
        if pending_total:
            print("Triage the PENDING ops in a Claude session (see CLAUDE.md), then rebuild.")
        print("Remember: python3 build/build.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
