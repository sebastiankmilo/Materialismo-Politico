#!/usr/bin/env python3
"""Genera data.js (capítulos indexados, vocabulario y fuentes) para los sitios html-2 / html-3."""

import json
import os
import re
import glob

BASE = os.path.dirname(os.path.abspath(__file__))
DOC_DIR = os.path.join(BASE, "escolastica", "relacion entre la escolastica católica y el materialismo politico.md")
VOCAB_PATH = os.path.join(BASE, "escolastica", "vocabulario", "vocabulario.md")
OUT_DIRS = [os.path.join(BASE, "html-3")]

SUPS = "¹²³⁴⁵⁶⁷⁸⁹⁰"
SUP_MAP = {"¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5",
           "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁰": "0"}
VERSE_RE = re.compile("([" + SUPS + "]+)")


def esc(s):
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def md_inline(s):
    """Conversión mínima de markdown en línea sobre texto ya escapado."""
    s = re.sub(r"\\([()\[\]*|_#>])", r"\1", s)
    out = []
    pos = 0
    # enlaces
    for m in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)", s):
        out.append(_inline_no_links(s[pos:m.start()]))
        label, url = m.group(1), m.group(2)
        cite = parse_cite(label, url)
        if cite:
            out.append(cite_html(label, cite))
        elif url.startswith("http"):
            out.append(f'<a href="{esc(url)}" target="_blank" rel="noopener">{esc(label)}</a>')
        else:
            out.append(f'<a href="{esc(url)}">{esc(label)}</a>')
        pos = m.end()
    out.append(_inline_no_links(s[pos:]))
    return "".join(out)


def _inline_no_links(s):
    s = esc(s)
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", s)
    s = re.sub(r"(?<!\w)_([^_\n]+?)_(?!\w)", r"<em>\1</em>", s)
    s = re.sub(r"`([^`]+?)`", r"<code>\1</code>", s)
    return s


def parse_cite(label, url):
    m = re.search(r"(\d+)\s*:\s*([\d\s,\-]+)\s*$", label)
    if not m:
        return None
    cap = int(m.group(1))
    verses = m.group(2).strip()
    return {"cap": cap, "verses": verses}


def cite_html(label, cite):
    target = first_verse(cite["verses"])
    ref = f"{cite['cap']}:{target}"
    return (f'<a href="#texto?v={ref}" class="cite" data-ref="{ref}" '
            f'data-cap="{cite["cap"]}" data-verses="{cite["verses"]}">{esc(label)}</a>')


def first_verse(verses):
    part = re.split(r"[,\s]", verses.strip())[0]
    if "-" in part:
        part = part.split("-")[0]
    try:
        return int(part)
    except ValueError:
        return 1


def parse_verses_string(verses):
    nums = []
    for chunk in verses.split(","):
        chunk = chunk.strip()
        if not chunk:
            continue
        if "-" in chunk:
            a, b = chunk.split("-", 1)
            try:
                a, b = int(a), int(b)
            except ValueError:
                continue
            if b - a < 50:
                nums.extend(range(a, b + 1))
            else:
                nums.append(a)
        else:
            try:
                nums.append(int(chunk))
            except ValueError:
                pass
    return nums


def verses_to_html(text, cap):
    """Divide por marcadores superíndice y envuelve cada versículo."""
    parts = VERSE_RE.split(text)
    html = []
    pending = ""
    cur = None
    for part in parts:
        if not part:
            continue
        if VERSE_RE.fullmatch(part):
            if cur is None:
                if pending.strip():
                    html.append(md_inline(pending))
            else:
                html.append(_close_v(cap, cur, pending))
            num = int("".join(SUP_MAP[c] for c in part))
            cur = num
            pending = ""
        else:
            pending += part
    if cur is None:
        if pending.strip():
            html.append(md_inline(pending))
    else:
        html.append(_close_v(cap, cur, pending))
    return "".join(html)


def _close_v(cap, num, content):
    ref = f"{cap}:{num}"
    inner = md_inline(content)
    return (f'<span class="v" id="v-{cap}-{num}" data-ref="{ref}">'
            f'<sup class="vn" data-ref="{ref}" title="{ref}">{num}</sup>{inner}</span>')


def classify_line(line):
    stripped = line.lstrip()
    if re.match(r"^(#{1,6})\s+", stripped):
        return "heading"
    if stripped.startswith(">"):
        return "quote"
    if stripped.startswith("* ") or stripped.startswith("- ") or re.match(r"^\d+\)\s*", stripped):
        return "li"
    return "p"


def clean_md_line(line):
    s = line.strip()
    s = re.sub(r"^(#{1,6})\s+", "", s)
    if s.startswith(">"):
        s = re.sub(r"^>\s?", "", s)
    s = re.sub(r"^([-*]|\d+\))\s*", "", s)
    return s.strip()


def parse_chapter(path, cap):
    raw = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    lines = raw.split("\n")
    blocks = []
    buf = []
    buf_type = None

    def flush():
        nonlocal buf, buf_type
        if not buf or buf_type is None:
            buf, buf_type = [], None
            return
        if buf_type == "heading":
            level = buf[0][1]
            text = buf[0][0]
            h = min(2 + level - 1, 6)
            blocks.append({"type": f"h{h}", "id": f"cap{cap}-h{len(blocks)}",
                           "html": md_inline(text), "text": re.sub(r"[*_`]", "", text)})
        elif buf_type == "quote":
            text = " ".join(x[0] for x in buf)
            blocks.append({"type": "quote", "html": verses_to_html(text, cap)})
        elif buf_type == "li":
            for item in buf:
                blocks.append({"type": "li", "html": verses_to_html(item[0], cap)})
        else:
            text = " ".join(x[0].rstrip() for x in buf)
            if text.strip():
                blocks.append({"type": "p", "html": verses_to_html(text, cap)})
        buf, buf_type = [], None

    for line in lines:
        if not line.strip():
            flush()
            continue
        kind = classify_line(line)
        if kind == "heading":
            flush()
            m = re.match(r"^(#{1,6})\s+(.*)$", line.strip())
            buf = [(m.group(2).strip(), len(m.group(1)))]
            buf_type = "heading"
            flush()
            continue
        if buf_type is None:
            buf_type = kind if kind != "heading" else "p"
            buf = [(clean_md_line(line), None)]
        elif kind == buf_type or (buf_type in ("p", "quote") and kind == buf_type):
            if kind == "li":
                flush()
                buf_type = "li"
                buf = [(clean_md_line(line), None)]
            else:
                buf.append((clean_md_line(line), None))
        elif kind == "li" and buf_type == "p":
            # una lista interrumpe el párrafo
            flush()
            buf_type = "li"
            buf = [(clean_md_line(line), None)]
        elif kind == "heading":
            flush()
        else:
            # cambio de tipo (p -> quote, li -> p, etc.)
            if buf_type in ("p", "quote") and kind == "quote":
                flush()
                buf_type = "quote"
                buf = [(clean_md_line(line), None)]
            else:
                flush()
                buf_type = kind
                buf = [(clean_md_line(line), None)]
    flush()

    # título del capítulo
    title = ""
    for b in blocks:
        if b["type"] == "h2":
            title = b["text"]
            break
    max_verse = 0
    for b in blocks:
        for m in re.finditer(r'id="v-(\d+)-(\d+)"', b.get("html", "")):
            max_verse = max(max_verse, int(m.group(2)))
    headings = [{"id": b["id"], "text": b["text"], "level": int(b["type"][1])}
                for b in blocks if b["type"].startswith("h") and b["type"] != "h2"]
    return {"cap": cap, "title": title, "blocks": blocks, "maxVerse": max_verse, "headings": headings}


def split_row(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def is_sep_row(cells):
    return all(re.fullmatch(r":?-{2,}:?", c or "-") for c in cells)


def parse_vocab(path):
    entries = []
    table = None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        if line.startswith("## Tabla 1"):
            table = 1
            continue
        if line.startswith("## Tabla 2"):
            table = 2
            continue
        if not line.startswith("|") or table is None:
            continue
        cells = split_row(line)
        if not cells or cells[0] in ("Índice", "Tabla") or is_sep_row(cells):
            continue
        if table == 1 and len(cells) < 8:
            continue
        if table == 2 and len(cells) < 7:
            continue
        try:
            idx = int(cells[0]) if cells[0] else None
        except ValueError:
            continue
        try:
            sub = int(cells[1]) if cells[1] else 1
        except ValueError:
            sub = 1
        term_raw = cells[2]
        term = re.sub(r"[*_`]+", "", term_raw).strip()
        if not term:
            continue
        if table == 1:
            definicion, ejemplo, fuente, fecha, tema = cells[3], cells[4], cells[5], cells[6], cells[7]
        else:
            definicion = ""
            ejemplo, fuente, fecha, tema = cells[3], cells[4], cells[5], cells[6]
        cites = extract_cites(ejemplo) + extract_cites(fuente)
        # dedupe por ref
        seen = set()
        uniq = []
        for c in cites:
            if c["ref"] not in seen:
                seen.add(c["ref"])
                uniq.append(c)

        def def_html(txt):
            t = txt.strip()
            warn = ""
            m = re.match(r"^\*{0,3}(sin acuerdo)\*{0,3}\s*", t, flags=re.I)
            if m:
                warn = '<span class="chip chip-warn">sin acuerdo</span>'
                t = t[m.end():]
            return warn + md_inline(t)

        entries.append({
            "table": table,
            "index": idx if idx is not None else len([e for e in entries if e["table"] == table]) + 1,
            "sub": sub,
            "term": term,
            "termRaw": term_raw,
            "def": definicion.strip(),
            "defHtml": def_html(definicion) if definicion.strip() else "",
            "example": ejemplo.strip(),
            "exampleHtml": md_inline(ejemplo.strip()) if ejemplo.strip() else "",
            "source": fuente.strip(),
            "sourceHtml": md_inline(fuente.strip()) if fuente.strip() else "",
            "date": fecha.strip(),
            "topics": [t.strip() for t in tema.split(",") if t.strip()],
            "cites": uniq,
            "id": f"e{table}-{idx if idx is not None else 0}-{sub}",
        })
    # índice para términos sin número
    for t in (1, 2):
        n = 0
        last = None
        for e in entries:
            if e["table"] != t:
                continue
            if e["index"] is None or (last is not None and e["index"] == last):
                pass
        # renumerar solo si hace falta: mantener original
    return entries


def extract_cites(cell):
    cites = []
    for m in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)\)", cell):
        c = parse_cite(m.group(1), m.group(2))
        if c:
            nums = parse_verses_string(c["verses"])
            cites.append({
                "label": m.group(1),
                "cap": c["cap"],
                "verses": c["verses"],
                "nums": nums,
                "ref": f"{c['cap']}:{first_verse(c['verses'])}",
            })
    return cites


def parse_sources(path):
    text = open(path, encoding="utf-8").read().replace("\r\n", "\n")
    sources = []
    for line in text.split("\n"):
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if "—" in line:
            ref_part, rest = line.split("—", 1)
        else:
            ref_part, rest = line, ""
        ref_part = ref_part.strip().rstrip("—").strip()
        cited = "no citada" not in rest
        usages = []
        seen = set()
        for m in re.finditer(r"\[([^\]]+)\]\(([^)\s]+)\)", rest):
            c = parse_cite(m.group(1), m.group(2))
            if c:
                nums = parse_verses_string(c["verses"])
                ref = f"{c['cap']}:{first_verse(c['verses'])}"
                if ref in seen:
                    continue
                seen.add(ref)
                usages.append({"cap": c["cap"], "verses": c["verses"], "nums": nums, "ref": ref,
                               "label": m.group(1)})
        # texto de la referencia: quitar enlaces, conservar http sueltos
        ref_html = md_inline(re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", ref_part))
        url_m = re.search(r"https?://[^\s\]]+", rest)
        ext = url_m.group(0) if url_m else None
        plain = re.sub(r"[*_`]", "", ref_part)
        year = 0
        ym = re.search(r"\((\d{4})", plain) or re.search(r"\b(\d{4})\b", plain)
        if ym:
            try:
                year = int(ym.group(1))
            except ValueError:
                year = 0
        author_m = re.match(r"^(.{1,60}?)[.(]", plain)
        sources.append({
            "ref": ref_html,
            "plain": plain,
            "cited": cited,
            "usages": usages,
            "url": ext,
            "sort": plain.lower(),
            "year": year,
        })
    return sources


def collect_topics(entries):
    topics = {}
    desc = {
        "ontologia": "Términos sobre el ser, la existencia, la esencia y las categorías del ser.",
        "escolastica": "Escolástica católica y tradición salmantina.",
        "materialismo-filosofico": "Categorías del materialismo filosófico.",
        "fundamentos-materialismo-politico": "Fundamentos del materialismo político.",
        "materialismo-historico": "Materialismo histórico de Marx.",
    }
    for e in entries:
        for t in e["topics"]:
            topics.setdefault(t, desc.get(t, ""))
    return topics


def main():
    chapters = []
    files = sorted(glob.glob(os.path.join(DOC_DIR, "cap-*.md")))
    for f in files:
        name = os.path.basename(f)
        m = re.match(r"cap-(\d+)", name)
        if not m:
            continue
        cap = int(m.group(1))
        ch = parse_chapter(f, cap)
        chapters.append(ch)
    chapters.sort(key=lambda c: c["cap"])

    entries = parse_vocab(VOCAB_PATH)
    sources = parse_sources(os.path.join(DOC_DIR, "fuentes-y-referencias.md"))
    topics = collect_topics(entries)

    data = {
        "meta": {
            "title": "La relación entre la escolástica católica y el materialismo político",
            "author": "Román Hernández Suárez",
            "built": "2026-09-24",
        },
        "chapters": chapters,
        "vocab": entries,
        "sources": sources,
        "topics": topics,
    }

    payload = "window.SITE_DATA = " + json.dumps(data, ensure_ascii=False, separators=(",", ":")) + ";\n"
    for d in OUT_DIRS:
        os.makedirs(d, exist_ok=True)
        out = os.path.join(d, "data.js")
        with open(out, "w", encoding="utf-8") as fh:
            fh.write(payload)
        print(f"escrito {out} ({len(payload):,} bytes)")

    print(f"capítulos: {len(chapters)} | entradas vocab: {len(entries)} | fuentes: {len(sources)}")
    for c in chapters:
        print(f"  cap {c['cap']}: {len(c['blocks'])} bloques, {c['maxVerse']} versículos — {c['title'][:60]}")


if __name__ == "__main__":
    main()
