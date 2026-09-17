"""mdlite — the markdown-subset renderer for DQ Enablement Studio knowledge units.

Supported (see CLAUDE.md "Body markdown subset"):
  ##/### headings, paragraphs, bold/italic/inline-code, fenced code blocks (```sql
  gets minimal keyword highlighting), pipe tables, ordered/unordered lists (one
  nesting level), blockquotes incl. Obsidian callouts (> [!note] / [!warning] /
  [!tip]), wikilinks [[unit-id]] / [[unit-id|label]], external [text](url), and
  --- horizontal rules.

Anything outside the subset is reported as an issue (kind "warning"); raw HTML
outside code fences is reported as kind "error". Nothing degrades silently.

render(md, resolve) -> {"html", "text", "sections", "issues", "wikilinks"}
  resolve(unit_id) -> title string, or None if the id is unknown (unknown ids
  are rendered as broken-link spans and reported via "wikilinks" so the build
  can fail on them).
  sections: [{"heading": str|None, "text": plain_text}] split at ## boundaries
  (pre-first-heading prose gets heading None) — the chunking basis.
"""

import html as _html
import re

_SQL_KEYWORDS = (
    "SELECT FROM WHERE JOIN INNER LEFT RIGHT OUTER ON AND OR NOT NULL IS IN AS CASE WHEN THEN "
    "ELSE END GROUP BY ORDER HAVING UNION ALL DISTINCT WITH CAST LIKE BETWEEN EXISTS COUNT SUM "
    "MIN MAX AVG COALESCE CONCAT CREATE VIEW INSERT UPDATE DELETE INTO VALUES SET"
).split()
_SQL_KW_RE = re.compile(r"\b(" + "|".join(_SQL_KEYWORDS) + r")\b", re.IGNORECASE)

_CALLOUT_KINDS = {"note": "Note", "warning": "Warning", "tip": "Tip", "important": "Important",
                  "info": "Info", "example": "Example", "success": "Success"}


def _highlight_sql(escaped_code):
    return _SQL_KW_RE.sub(lambda m: '<span class="sql-k">' + m.group(1) + "</span>", escaped_code)


def _inline(text, resolve, issues, wikilinks, lineno):
    """Render inline markdown for one already-raw text run. Escapes HTML first."""
    # Raw HTML check happens before escaping (block level passes prose lines here).
    out = []
    # Tokenize code spans first so nothing inside them is styled.
    parts = re.split(r"(`[^`]+`)", text)
    for part in parts:
        if part.startswith("`") and part.endswith("`") and len(part) > 2:
            out.append("<code>" + _html.escape(part[1:-1]) + "</code>")
            continue
        seg = _html.escape(part, quote=False)
        # Wikilinks [[id]] / [[id|label]]
        def _wl(m):
            uid = m.group(1).strip()
            label = (m.group(2) or "").strip()
            title = resolve(uid) if resolve else None
            wikilinks.append({"id": uid, "line": lineno, "resolved": title is not None})
            shown = label or title or uid
            if title is None:
                return '<span class="wl-broken" title="unknown unit id">' + _html.escape(shown) + "</span>"
            return '<a class="wl" href="#/unit/' + _html.escape(uid) + '">' + _html.escape(shown) + "</a>"
        seg = re.sub(r"\[\[([^\]|]+)(?:\|([^\]]+))?\]\]", _wl, seg)
        # External links [text](url) — after wikilinks so [[..]] is untouched.
        seg = re.sub(
            r"\[([^\]]+)\]\((https?://[^)\s]+)\)",
            r'<a class="ext" href="\2" target="_blank" rel="noopener">\1</a>',
            seg,
        )
        # Bold then italic (** before *)
        seg = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", seg)
        seg = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"<em>\1</em>", seg)
        out.append(seg)
    return "".join(out)


def _plain(text):
    """Inline markdown → plain text (for search blobs and chunks)."""
    t = re.sub(r"`([^`]+)`", r"\1", text)
    t = re.sub(r"\[\[([^\]|]+)\|([^\]]+)\]\]", r"\2", t)
    t = re.sub(r"\[\[([^\]|]+)\]\]", r"\1", t)
    t = re.sub(r"\[([^\]]+)\]\((https?://[^)\s]+)\)", r"\1", t)
    t = re.sub(r"\*\*([^*]+)\*\*", r"\1", t)
    t = re.sub(r"(?<!\*)\*([^*\n]+)\*(?!\*)", r"\1", t)
    return t


_RAW_HTML_RE = re.compile(r"<[a-zA-Z/!]")


def render(md, resolve=None):
    lines = md.split("\n")
    html_out = []
    issues = []       # {"kind": "error"|"warning", "line": n, "msg": str}
    wikilinks = []    # {"id", "line", "resolved"}
    sections = []     # [{"heading", "text"}]
    cur_section = {"heading": None, "text": []}

    def close_section():
        nonlocal cur_section
        if cur_section["text"] or cur_section["heading"] is not None:
            sections.append({"heading": cur_section["heading"], "text": "\n".join(cur_section["text"]).strip()})
        cur_section = {"heading": None, "text": []}

    i = 0
    n = len(lines)
    para = []

    def flush_para():
        if para:
            joined = " ".join(p.strip() for p in para)
            html_out.append("<p>" + _inline(joined, resolve, issues, wikilinks, i) + "</p>")
            cur_section["text"].append(_plain(joined))
            para.clear()

    while i < n:
        line = lines[i]
        stripped = line.strip()

        # Fenced code block
        if stripped.startswith("```"):
            flush_para()
            lang = stripped[3:].strip().lower()
            code_lines = []
            i += 1
            closed = False
            while i < n:
                if lines[i].strip().startswith("```"):
                    closed = True
                    break
                code_lines.append(lines[i])
                i += 1
            if not closed:
                issues.append({"kind": "warning", "line": i, "msg": "unclosed code fence"})
            code = "\n".join(code_lines)
            escaped = _html.escape(code)
            if lang == "sql":
                escaped = _highlight_sql(escaped)
            cls = ' class="lang-' + _html.escape(lang) + '"' if lang else ""
            html_out.append("<pre" + cls + "><code>" + escaped + "</code></pre>")
            cur_section["text"].append(code)
            i += 1
            continue

        # Blank line
        if not stripped:
            flush_para()
            i += 1
            continue

        # Raw HTML (outside code fences and inline code spans) is an error
        if _RAW_HTML_RE.search(re.sub(r"`[^`]*`", "", line)):
            issues.append({"kind": "error", "line": i + 1, "msg": "raw HTML outside a code fence: " + stripped[:60]})
            i += 1
            continue

        # Headings (## and ###; # reserved for the unit title -> warning)
        m = re.match(r"^(#{1,4})\s+(.*)$", stripped)
        if m:
            flush_para()
            depth = len(m.group(1))
            text = m.group(2).strip()
            if depth == 1:
                issues.append({"kind": "warning", "line": i + 1, "msg": "# heading in body (title comes from frontmatter); rendered as ##"})
                depth = 2
            if depth == 4:
                issues.append({"kind": "warning", "line": i + 1, "msg": "#### heading demoted to ###"})
                depth = 3
            if depth == 2:
                close_section()
                cur_section["heading"] = _plain(text)
            slug = re.sub(r"[^a-z0-9]+", "-", _plain(text).lower()).strip("-")
            html_out.append(
                "<h{d} id=\"s-{slug}\">{t}</h{d}>".format(d=depth, slug=_html.escape(slug), t=_inline(text, resolve, issues, wikilinks, i))
            )
            cur_section["text"].append(_plain(text))
            i += 1
            continue

        # Horizontal rule
        if re.match(r"^-{3,}$", stripped):
            flush_para()
            html_out.append("<hr>")
            i += 1
            continue

        # Blockquote / callout
        if stripped.startswith(">"):
            flush_para()
            quote_lines = []
            while i < n and lines[i].strip().startswith(">"):
                quote_lines.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            kind, title = None, None
            m = re.match(r"^\[!(\w+)\]\s*(.*)$", quote_lines[0].strip()) if quote_lines else None
            if m:
                kw = m.group(1).lower()
                if kw in _CALLOUT_KINDS:
                    kind = kw
                    title = m.group(2).strip() or _CALLOUT_KINDS[kw]
                    quote_lines = quote_lines[1:]
                else:
                    issues.append({"kind": "warning", "line": i, "msg": "unknown callout kind [!" + kw + "], rendered as blockquote"})
            body_txt = " ".join(q.strip() for q in quote_lines if q.strip())
            inner = _inline(body_txt, resolve, issues, wikilinks, i)
            if kind:
                html_out.append(
                    '<aside class="callout co-' + kind + '"><div class="co-title">' + _html.escape(title) + "</div><p>" + inner + "</p></aside>"
                )
            else:
                html_out.append("<blockquote><p>" + inner + "</p></blockquote>")
            cur_section["text"].append(((title + ": ") if kind and title else "") + _plain(body_txt))
            continue

        # Table (pipe)
        if stripped.startswith("|") and i + 1 < n and re.match(r"^\|[\s:|-]+\|?$", lines[i + 1].strip()):
            flush_para()
            header = [c.strip() for c in stripped.strip("|").split("|")]
            i += 2
            rows = []
            while i < n and lines[i].strip().startswith("|"):
                rows.append([c.strip() for c in lines[i].strip().strip("|").split("|")])
                i += 1
            th = "".join("<th>" + _inline(c, resolve, issues, wikilinks, i) + "</th>" for c in header)
            trs = []
            for r in rows:
                trs.append("<tr>" + "".join("<td>" + _inline(c, resolve, issues, wikilinks, i) + "</td>" for c in r) + "</tr>")
            html_out.append('<div class="tbl-wrap"><table><thead><tr>' + th + "</tr></thead><tbody>" + "".join(trs) + "</tbody></table></div>")
            cur_section["text"].append(" | ".join(header) + "\n" + "\n".join(" | ".join(r) for r in rows))
            continue

        # Lists (ul/ol, one nesting level)
        m = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", line)
        if m:
            flush_para()
            items_html, items_text = [], []
            ordered = m.group(2)[0].isdigit()
            tag = "ol" if ordered else "ul"
            while i < n:
                lm = re.match(r"^(\s*)([-*]|\d+\.)\s+(.*)$", lines[i])
                if not lm:
                    break
                indent = len(lm.group(1))
                text = lm.group(3)
                if indent >= 2 and items_html:
                    # one nesting level: attach as a sub-list on the previous item
                    sub_tag = "ol" if lm.group(2)[0].isdigit() else "ul"
                    subs_html, subs_text = [], []
                    while i < n:
                        sm = re.match(r"^(\s{2,})([-*]|\d+\.)\s+(.*)$", lines[i])
                        if not sm:
                            break
                        if len(sm.group(1)) >= 4:
                            issues.append({"kind": "warning", "line": i + 1, "msg": "list nesting deeper than one level flattened"})
                        subs_html.append("<li>" + _inline(sm.group(3), resolve, issues, wikilinks, i) + "</li>")
                        subs_text.append(_plain(sm.group(3)))
                        i += 1
                    items_html[-1] = items_html[-1][:-5] + "<" + sub_tag + ">" + "".join(subs_html) + "</" + sub_tag + "></li>"
                    items_text.extend(subs_text)
                    continue
                items_html.append("<li>" + _inline(text, resolve, issues, wikilinks, i) + "</li>")
                items_text.append(_plain(text))
                i += 1
            html_out.append("<" + tag + ">" + "".join(items_html) + "</" + tag + ">")
            cur_section["text"].append("\n".join(items_text))
            continue

        # Paragraph accumulation
        para.append(line)
        i += 1

    flush_para()
    close_section()

    text = "\n\n".join(s["text"] for s in sections if s["text"])
    return {"html": "\n".join(html_out), "text": text, "sections": sections, "issues": issues, "wikilinks": wikilinks}
