#!/usr/bin/env python3
"""build.py — compiles the DQ Enablement Studio knowledge corpus into
dist/enablement-master.html (single-file offline app), dist/chunks.jsonl
(RAG-ready chunks) and dist/validation-report.md.

Stdlib only. Deterministic: same content -> byte-identical output (all file
I/O uses newline=""; iteration orders are sorted). Exits nonzero on any
validation ERROR; warnings are listed in the report but do not fail the build.

Search index: no inverted index at this scale (~300 units). Each unit carries a
lowercased search blob; the client does a scored linear scan (title 10 / tags 5
/ term 5 / body 1 + phrase bonus). Revisit only past ~1000 units.

Usage: python3 build/build.py            (from the project root or anywhere)
"""

import hashlib
import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import mdlite  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTENT = os.path.join(ROOT, "content")
TAXONOMY = os.path.join(ROOT, "taxonomy")
DIST = os.path.join(ROOT, "dist")
BRAND_KIT = os.path.expanduser("~/repos/syniti-brand-kit")

SIZE_WARN_BYTES = 6 * 1024 * 1024
CHUNK_SPLIT_WORDS = 500

DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
ID_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)+$")


class Reporter:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def error(self, where, msg):
        self.errors.append((where, msg))

    def warn(self, where, msg):
        self.warnings.append((where, msg))


def read(path):
    with open(path, "r", encoding="utf-8", newline="") as f:
        return f.read()


def write(path, text):
    with open(path, "w", encoding="utf-8", newline="") as f:
        f.write(text)


# ---------------------------------------------------------------- frontmatter
def parse_frontmatter(raw, where, rep):
    """Strict flat YAML: `key: value`, `key: [a, b]`, and indented `- item` lists."""
    if not raw.startswith("---\n"):
        rep.error(where, "missing frontmatter (file must start with ---)")
        return None, raw
    end = raw.find("\n---", 4)
    if end == -1:
        rep.error(where, "unterminated frontmatter")
        return None, raw
    block = raw[4:end]
    body = raw[end + 4:]
    if body.startswith("\n"):
        body = body[1:]
    meta = {}
    current_list_key = None
    for ln, line in enumerate(block.split("\n"), start=2):
        if not line.strip() or line.strip().startswith("#"):
            continue
        if re.match(r"^\s+-\s+", line):
            if current_list_key is None:
                rep.error(where, "line %d: list item without a key" % ln)
                continue
            meta[current_list_key].append(line.split("-", 1)[1].strip())
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_]*):\s*(.*)$", line)
        if not m:
            rep.error(where, "line %d: not flat YAML: %r" % (ln, line.strip()))
            continue
        key, val = m.group(1), m.group(2).strip()
        current_list_key = None
        if val == "":
            meta[key] = []
            current_list_key = key
        elif val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            meta[key] = [v.strip() for v in inner.split(",") if v.strip()] if inner else []
        else:
            if (val.startswith('"') and val.endswith('"')) or (val.startswith("'") and val.endswith("'")):
                val = val[1:-1]
            meta[key] = val
    return meta, body


# ---------------------------------------------------------------- validation
def load_units(taxonomy, rep):
    types = taxonomy["types"]
    folder_to_type = {v["folder"]: k for k, v in types.items()}
    prefix_by_type = {k: v["prefix"] for k, v in types.items()}
    units = {}
    for folder in sorted(os.listdir(CONTENT)):
        fdir = os.path.join(CONTENT, folder)
        if not os.path.isdir(fdir):
            continue
        if folder not in folder_to_type:
            rep.error("content/" + folder, "folder is not a known type folder")
            continue
        ftype = folder_to_type[folder]
        for fname in sorted(os.listdir(fdir)):
            if not fname.endswith(".md"):
                continue
            where = "content/%s/%s" % (folder, fname)
            meta, body = parse_frontmatter(read(os.path.join(fdir, fname)), where, rep)
            if meta is None:
                continue
            uid = meta.get("id", "")
            if not uid:
                rep.error(where, "missing id")
                continue
            if uid in units:
                rep.error(where, "duplicate id %r (also in %s)" % (uid, units[uid]["where"]))
                continue
            if fname != uid + ".md":
                rep.error(where, "filename must be %s.md" % uid)
            if not ID_RE.match(uid):
                rep.error(where, "id %r is not kebab-case" % uid)
            elif not uid.startswith(prefix_by_type[ftype] + "-"):
                rep.error(where, "id prefix must be %r for type %s" % (prefix_by_type[ftype], ftype))
            for req in ("type", "title", "domain", "level", "status", "created", "updated"):
                if not meta.get(req):
                    rep.error(where, "missing required field %r" % req)
            for req_list in ("audience", "sources"):
                v = meta.get(req_list)
                if not isinstance(v, list) or not v:
                    rep.error(where, "field %r must be a non-empty list" % req_list)
            if meta.get("type") and meta["type"] != ftype:
                rep.error(where, "type %r does not match folder %r" % (meta.get("type"), folder))
            units[uid] = {"meta": meta, "body": body, "where": where, "type": ftype}
    return units


def validate_vocab(units, taxonomy, rep):
    domains = set(taxonomy["domains"])
    audiences = set(taxonomy["audiences"])
    levels = set(taxonomy["levels"])
    statuses = set(taxonomy["statuses"])
    kinds = set(taxonomy["kinds"])
    rels = set(taxonomy["link_relations"])
    repo_keys = set(taxonomy["source_repos"])
    kind_valid_on = {"decision": "principle", "pattern": "standard"}
    for uid in sorted(units):
        u, meta, where = units[uid], units[uid]["meta"], units[uid]["where"]
        if meta.get("domain") and meta["domain"] not in domains:
            rep.error(where, "unknown domain %r" % meta["domain"])
        for a in meta.get("audience", []):
            if a not in audiences:
                rep.error(where, "unknown audience %r" % a)
        if meta.get("level") and meta["level"] not in levels:
            rep.error(where, "unknown level %r" % meta["level"])
        if meta.get("status") and meta["status"] not in statuses:
            rep.error(where, "unknown status %r" % meta["status"])
        kind = meta.get("kind")
        if kind:
            if kind not in kinds:
                rep.error(where, "unknown kind %r" % kind)
            elif u["type"] != kind_valid_on.get(kind):
                rep.error(where, "kind %r not valid on type %r" % (kind, u["type"]))
        for field in ("created", "updated"):
            v = meta.get(field)
            if v and not DATE_RE.match(v):
                rep.error(where, "%s must be YYYY-MM-DD, got %r" % (field, v))
        for link in meta.get("links", []):
            if ":" not in link:
                rep.error(where, "link %r must be rel:target-id" % link)
                continue
            rel, target = link.split(":", 1)
            if rel not in rels:
                rep.error(where, "unknown link relation %r" % rel)
            if target not in units:
                rep.error(where, "link target %r does not exist" % target)
            if target == uid:
                rep.warn(where, "self-link ignored")
        sup = meta.get("supersedes")
        if sup and sup not in units:
            rep.error(where, "supersedes target %r does not exist" % sup)
        for src in meta.get("sources", []):
            if ":" not in src:
                rep.error(where, "source %r must be repo-key:path" % src)
            elif src.split(":", 1)[0] not in repo_keys:
                rep.error(where, "unknown source repo key %r" % src.split(":", 1)[0])


def validate_registries(units, paths_data, assess_data, rep):
    item_ids = set()
    for item in assess_data.get("items", []):
        where = "taxonomy/assessments.json#" + item.get("id", "?")
        iid = item.get("id")
        if not iid or not iid.startswith("as-"):
            rep.error(where, "assessment id must start with as-")
            continue
        if iid in item_ids:
            rep.error(where, "duplicate assessment id")
        item_ids.add(iid)
        if item.get("unit_id") and item["unit_id"] not in units:
            rep.error(where, "unit_id %r does not exist" % item["unit_id"])
        kind = item.get("kind")
        if kind == "mcq":
            for req in ("question", "options", "answer"):
                if not item.get(req):
                    rep.error(where, "mcq item missing %r" % req)
            if item.get("options") and item.get("answer") not in item["options"]:
                rep.error(where, "answer %r not in options" % item.get("answer"))
        elif kind == "sql_practice":
            if not item.get("prompt"):
                rep.error(where, "sql_practice item missing prompt")
        else:
            rep.error(where, "unknown assessment kind %r" % kind)
    for p in paths_data.get("paths", []):
        where = "taxonomy/paths.json#" + p.get("id", "?")
        if not p.get("id") or not p.get("title") or not isinstance(p.get("steps"), list):
            rep.error(where, "path needs id, title, steps[]")
            continue
        for step in p["steps"]:
            if "unit" in step:
                if step["unit"] not in units:
                    rep.error(where, "step unit %r does not exist" % step["unit"])
                for chk in step.get("checks", []):
                    if chk not in item_ids:
                        rep.error(where, "step check %r does not exist" % chk)
            elif "assessment" in step:
                if step["assessment"] not in item_ids:
                    rep.error(where, "step assessment %r does not exist" % step["assessment"])
            else:
                rep.error(where, "step must have unit or assessment")
    # sql_practice hooks on units
    for uid in sorted(units):
        hook = units[uid]["meta"].get("sql_practice")
        if hook and hook not in item_ids:
            rep.error(units[uid]["where"], "sql_practice %r does not exist" % hook)
    return item_ids


# ---------------------------------------------------------------- assembly
def build_corpus(units, taxonomy, paths_data, assess_data, rep):
    titles = {uid: units[uid]["meta"].get("title", uid) for uid in units}

    def resolve(uid):
        return titles.get(uid)

    inbound = {uid: [] for uid in units}
    compiled = {}
    for uid in sorted(units):
        u, meta, where = units[uid], units[uid]["meta"], units[uid]["where"]
        rendered = mdlite.render(u["body"], resolve)
        for iss in rendered["issues"]:
            (rep.error if iss["kind"] == "error" else rep.warn)(where, "line %s: %s" % (iss.get("line", "?"), iss["msg"]))
        for wl in rendered["wikilinks"]:
            if not wl["resolved"]:
                rep.error(where, "wikilink [[%s]] does not resolve" % wl["id"])
        links = []
        for link in meta.get("links", []):
            if ":" in link:
                rel, target = link.split(":", 1)
                if target in units and target != uid:
                    links.append({"rel": rel, "to": target})
                    inbound[target].append({"rel": rel, "from": uid})
        for wl in rendered["wikilinks"]:
            if wl["resolved"] and wl["id"] != uid:
                if not any(l["to"] == wl["id"] for l in links):
                    links.append({"rel": "relates", "to": wl["id"], "via": "wikilink"})
                    inbound[wl["id"]].append({"rel": "relates", "from": uid})
        body_hash = hashlib.sha256(u["body"].encode("utf-8")).hexdigest()[:16]
        search_blob = " | ".join([
            meta.get("title", "").lower(),
            " ".join(meta.get("tags", [])).lower(),
            rendered["text"].lower(),
        ])
        compiled[uid] = {
            "id": uid,
            "type": u["type"],
            "kind": meta.get("kind"),
            "title": meta.get("title", uid),
            "domain": meta.get("domain"),
            "audience": meta.get("audience", []),
            "level": meta.get("level"),
            "status": meta.get("status"),
            "links": links,
            "supersedes": meta.get("supersedes"),
            "sources": meta.get("sources", []),
            "sql_practice": meta.get("sql_practice"),
            "tags": meta.get("tags", []),
            "created": meta.get("created"),
            "updated": meta.get("updated"),
            "md": u["body"],
            "html": rendered["html"],
            "search": search_blob,
            "hash": body_hash,
            "sections": rendered["sections"],
        }
    for uid in compiled:
        compiled[uid]["inbound"] = sorted(inbound[uid], key=lambda e: (e["from"], e["rel"]))

    # Orphans: no in/out edges and in no path
    in_path = set()
    for p in paths_data.get("paths", []):
        for step in p.get("steps", []):
            if "unit" in step:
                in_path.add(step["unit"])
    for uid in sorted(compiled):
        c = compiled[uid]
        if not c["links"] and not c["inbound"] and uid not in in_path:
            rep.warn(c["id"], "orphan: no links in or out and not in any path")
    return compiled


def build_graph(compiled):
    nodes = [
        {"id": c["id"], "type": c["type"], "title": c["title"], "domain": c["domain"], "status": c["status"]}
        for c in (compiled[u] for u in sorted(compiled))
    ]
    edges = []
    for uid in sorted(compiled):
        for l in compiled[uid]["links"]:
            edges.append({"s": uid, "t": l["to"], "rel": l["rel"]})
    return {"nodes": nodes, "edges": edges}


def build_chunks(compiled):
    lines = []
    for uid in sorted(compiled):
        c = compiled[uid]
        raw_chunks = []
        for sec in c["sections"]:
            words = sec["text"].split()
            if len(words) > CHUNK_SPLIT_WORDS:
                paras = [p for p in sec["text"].split("\n\n") if p.strip()]
                buf, count = [], 0
                for p in paras:
                    buf.append(p)
                    count += len(p.split())
                    if count >= CHUNK_SPLIT_WORDS:
                        raw_chunks.append((sec["heading"], "\n\n".join(buf)))
                        buf, count = [], 0
                if buf:
                    raw_chunks.append((sec["heading"], "\n\n".join(buf)))
            elif sec["text"]:
                raw_chunks.append((sec["heading"], sec["text"]))
        if not raw_chunks:
            raw_chunks = [(None, c["title"])]
        for seq, (heading, text) in enumerate(raw_chunks, start=1):
            lines.append(json.dumps({
                "chunk_id": "%s#%02d" % (uid, seq),
                "unit_id": uid,
                "seq": seq,
                "type": c["type"],
                "kind": c["kind"],
                "title": c["title"],
                "section": heading,
                "domain": c["domain"],
                "audience": c["audience"],
                "level": c["level"],
                "status": c["status"],
                "text": text,
                "links": [l["rel"] + ":" + l["to"] for l in c["links"]],
                "sources": c["sources"],
                "hash": hashlib.sha256(text.encode("utf-8")).hexdigest()[:16],
                "updated": c["updated"],
            }, ensure_ascii=False, sort_keys=True))
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------- report + html
def write_report(rep, compiled, out_size):
    by_type, by_status, by_domain = {}, {}, {}
    for c in compiled.values():
        by_type[c["type"]] = by_type.get(c["type"], 0) + 1
        by_status[c["status"]] = by_status.get(c["status"], 0) + 1
        by_domain[c["domain"]] = by_domain.get(c["domain"], 0) + 1
    L = ["# Build validation report", ""]
    L.append("- Units: **%d** · app size: **%.2f MB** · errors: **%d** · warnings: **%d**" % (
        len(compiled), out_size / 1048576.0, len(rep.errors), len(rep.warnings)))
    L.append("")
    for label, d in (("By type", by_type), ("By status", by_status), ("By domain", by_domain)):
        L.append("**%s**: " % label + ", ".join("%s %d" % (k, d[k]) for k in sorted(d)))
    L.append("")
    if rep.errors:
        L.append("## Errors")
        L.extend("- `%s` — %s" % e for e in rep.errors)
        L.append("")
    if rep.warnings:
        L.append("## Warnings")
        L.extend("- `%s` — %s" % w for w in rep.warnings)
        L.append("")
    if not rep.errors and not rep.warnings:
        L.append("Clean build — no errors, no warnings.")
        L.append("")
    write(os.path.join(DIST, "validation-report.md"), "\n".join(L))


def main():
    rep = Reporter()
    taxonomy = json.loads(read(os.path.join(TAXONOMY, "taxonomy.json")))
    paths_data = json.loads(read(os.path.join(TAXONOMY, "paths.json")))
    assess_data = json.loads(read(os.path.join(TAXONOMY, "assessments.json")))

    units = load_units(taxonomy, rep)
    validate_vocab(units, taxonomy, rep)
    validate_registries(units, paths_data, assess_data, rep)
    compiled = build_corpus(units, taxonomy, paths_data, assess_data, rep)

    # Redirect map from supersedes
    redirects = {}
    for uid in sorted(compiled):
        sup = compiled[uid]["supersedes"]
        if sup:
            redirects[sup] = uid

    # Filter out deprecated units from published output
    published = {uid: u for uid, u in compiled.items() if u["status"] != "deprecated"}

    graph = build_graph(published)
    corpus_hash = hashlib.sha256(
        "".join(published[u]["hash"] for u in sorted(published)).encode("utf-8")
    ).hexdigest()[:8]
    newest = max((c["updated"] or "" for c in published.values()), default="")
    build_id = "%s-%s" % (newest or "unbuilt", corpus_hash)

    data = {
        "build": {"id": build_id, "content_date": newest, "units": len(published)},
        "taxonomy": {
            "types": {k: {"label": v["label"], "blurb": v["blurb"], "prefix": v["prefix"]} for k, v in taxonomy["types"].items()},
            "kinds": taxonomy["kinds"],
            "domains": taxonomy["domains"],
            "audiences": taxonomy["audiences"],
            "levels": taxonomy["levels"],
            "statuses": taxonomy["statuses"],
            "link_relations": taxonomy["link_relations"],
            "source_repos": taxonomy["source_repos"],
        },
        "units": {uid: {k: v for k, v in published[uid].items() if k != "sections"} for uid in sorted(published)},
        "paths": [p for p in paths_data.get("paths", []) if not p.get("hidden")],
        "assessments": {i["id"]: i for i in assess_data.get("items", [])},
        "graph": graph,
        "redirects": redirects,
    }

    template = read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "template.html"))
    tokens_css = read(os.path.join(BRAND_KIT, "tokens", "tokens.css"))
    patterns_css = read(os.path.join(BRAND_KIT, "patterns", "patterns.css"))
    logo_datauri = read(os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "syniti-logo-datauri.txt")).strip()

    def brand_icon(name):
        """Inline a brand-kit icon: strip xml header, namespace ids, force currentColor."""
        svg = read(os.path.join(BRAND_KIT, "icons", "sets", "white", name + ".svg"))
        svg = re.sub(r"<\?xml[^>]*\?>\s*", "", svg)
        prefix = "ic" + name.lower().replace("-", "")
        svg = re.sub(r'id="([^"]+)"', lambda m: 'id="%s-%s"' % (prefix, m.group(1)), svg)
        svg = re.sub(r'(url\(#|xlink:href="#)([^)"]+)', lambda m: m.group(1) + prefix + "-" + m.group(2), svg)
        # the white set paints every shape in one near-white; any hex fill IS the icon colour
        svg = re.sub(r'fill:\s*#[0-9a-fA-F]{3,8}', "fill:currentColor", svg)
        svg = re.sub(r'fill="#[0-9a-fA-F]{3,8}"', 'fill="currentColor"', svg)
        svg = re.sub(r'stroke:\s*#[0-9a-fA-F]{3,8}', "stroke:currentColor", svg)
        svg = svg.replace("<svg ", '<svg class="bi" fill="currentColor" aria-hidden="true" ', 1)
        return svg.replace("\n", "").replace("  ", "")
    data_json = json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    # </script> inside JSON payload would terminate the data block early
    data_json = data_json.replace("</", "<\\/")

    out = template
    for token, value in (
        ("__TOKENS_CSS__", tokens_css),
        ("__PATTERNS_CSS__", patterns_css),
        ("__DATA_JSON__", data_json),
        ("__BUILD_META__", build_id),
        ("__LOGO_IMG__", logo_datauri),
        ("__ICON_SEARCH__", brand_icon("Search")),
        ("__ICON_EDIT__", brand_icon("Edit")),
        ("__ICON_DOWNLOAD__", brand_icon("Download")),
        ("__ICON_QUESTION__", brand_icon("Question")),
        ("__ICON_CHECK__", brand_icon("Check")),
        ("__ICON_FLAG__", brand_icon("Error")),
        ("__ICON_GRAPH__", brand_icon("Hierarchy")),
        ("__ICON_LEARN__", brand_icon("Education")),
    ):
        if token not in out:
            rep.error("build/template.html", "placeholder %s missing from template" % token)
        out = out.replace(token, value)
    leftovers = sorted(set(re.findall(r"__[A-Z][A-Z_]+__", out)))
    for tok in leftovers:
        rep.error("build/template.html", "unsubstituted placeholder %s" % tok)

    os.makedirs(DIST, exist_ok=True)
    out_bytes = len(out.encode("utf-8"))
    if out_bytes > SIZE_WARN_BYTES:
        rep.warn("dist/enablement-master.html", "app is %.1f MB (>6 MB) — consider client-side render escape hatch" % (out_bytes / 1048576.0))

    write_report(rep, compiled, out_bytes)
    if rep.errors:
        print("BUILD FAILED — %d error(s), %d warning(s). See dist/validation-report.md" % (len(rep.errors), len(rep.warnings)))
        for where, msg in rep.errors[:25]:
            print("  ERROR %s — %s" % (where, msg))
        return 1

    write(os.path.join(DIST, "enablement-master.html"), out)
    write(os.path.join(DIST, "chunks.jsonl"), build_chunks(compiled))
    print("Build OK — %d units, %.2f MB, %d warning(s). build id %s" % (
        len(compiled), out_bytes / 1048576.0, len(rep.warnings), build_id))
    return 0


if __name__ == "__main__":
    sys.exit(main())
