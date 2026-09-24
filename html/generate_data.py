#!/usr/bin/env python3
"""Genera data.js (HTML5 vanilla) a partir de los markdown del documento."""

from __future__ import annotations

import json
import re
import sys
from html import escape as html_escape
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DOC_DIR = ROOT / "escolastica" / "relacion entre la escolastica católica y el materialismo politico.md"
VOCAB_PATH = ROOT / "escolastica" / "vocabulario" / "vocabulario.md"
INDEX_PATH = DOC_DIR / "0-index.md"
OUT_PATH = HERE / "data.js"

SUP_CHARS = "⁰¹²³⁴⁵⁶⁷⁸⁹"
SUP_MAP = {c: i for i, c in enumerate(SUP_CHARS)}
SUP_CHUNK = re.compile(f"[{SUP_CHARS}]+")
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
CITE_TAIL_RE = re.compile(r"(\d+):(\d+(?:[-,]\d+)*)\s*$")
CITE_SIMPLE_RE = re.compile(r"^\s*(\d+):(\d+(?:[-,]\d+)*)\s*$")
SIN_ACUERDO_RE = re.compile(r"^\*\*\*sin acuerdo\*\*\*\s*", re.IGNORECASE)
SEP_CELL_RE = re.compile(r"^:?-{3,}:?$")

VOWEL_CLASSES = {
    "a": "aáàâä",
    "e": "eéèêë",
    "i": "iíìîï",
    "o": "oóòôö",
    "u": "uúùûü",
}


def escape_html(s: str) -> str:
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def inline_md(s: str) -> str:
    """Convierte énfasis markdown en HTML (sobre texto ya escapado)."""
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"<strong><em>\1</em></strong>", s, flags=re.DOTALL)
    s = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", s, flags=re.DOTALL)
    s = re.sub(r"(?<!\*)\*([^*\n]+?)\*(?!\*)", r"<em>\1</em>", s, flags=re.DOTALL)
    s = s.replace("\\[", "[").replace("\\]", "]").replace("\\(", "(").replace("\\)", ")")
    s = s.replace("\\-", "-")
    return s


def strip_md(s: str) -> str:
    s = re.sub(r"\*\*\*(.+?)\*\*\*", r"\1", s)
    s = re.sub(r"\*\*(.+?)\*\*", r"\1", s)
    s = re.sub(r"\*([^*\n]+?)\*", r"\1", s)
    s = s.replace("\\[", "[").replace("\\]", "]").replace("\\(", "(").replace("\\)", ")")
    s = s.replace("\\-", "-")
    return s.strip()


def sup_to_int(chunk: str) -> int:
    return int("".join(str(SUP_MAP[c]) for c in chunk))


def split_verses(raw: str) -> list[tuple[int | None, str]]:
    matches = list(SUP_CHUNK.finditer(raw))
    if not matches:
        return [(None, raw)]
    segs: list[tuple[int | None, str]] = []
    if matches[0].start() > 0:
        segs.append((None, raw[: matches[0].start()]))
    for i, m in enumerate(matches):
        start = m.end()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(raw)
        segs.append((sup_to_int(m.group()), raw[start:end]))
    return segs


def term_to_pattern(term: str) -> str:
    parts = []
    for ch in term.lower():
        if ch in VOWEL_CLASSES:
            chars = VOWEL_CLASSES[ch]
            chars = chars + chars.upper()
            uniq = "".join(dict.fromkeys(chars))
            parts.append(f"[{uniq}]")
        elif ch.isalnum():
            parts.append(re.escape(ch))
        else:
            parts.append(re.escape(ch))
    return "".join(parts)


class TermLinker:
    def __init__(self, items: list[dict]):
        # items: [{term, entry, title}] ya filtrados
        self.items = sorted(items, key=lambda it: len(it["term"]), reverse=True)
        if not self.items:
            self.rx = None
            return
        alts = [f"({term_to_pattern(it['term'])})" for it in self.items]
        self.rx = re.compile("|".join(alts), re.IGNORECASE)

    def apply(self, text: str) -> str:
        if not self.rx:
            return text

        def repl(m: re.Match) -> str:
            for i, it in enumerate(self.items, start=1):
                if m.group(i) is not None:
                    title = html_escape(it["title"], quote=True)
                    return (
                        f'<a class="term-link" href="#{it["entry"]}" '
                        f'title="{title}">{m.group(0)}</a>'
                    )
            return m.group(0)

        return self.rx.sub(repl, text)


def render_inline_full(raw: str, linker: TermLinker | None) -> str:
    """escape → term links → énfasis → <br> por saltos de línea."""
    s = escape_html(raw)
    if linker:
        s = linker.apply(s)
    s = inline_md(s)
    s = s.replace("\n", "<br>\n")
    return s


# ----------------------------------------------------------------------------- capítulos


class ChapterRenderer:
    def __init__(self, chap: int, linker: TermLinker):
        self.chap = chap
        self.linker = linker
        self.cur_verse: int | None = None
        self.seen: set[int] = set()
        self.out: list[str] = []

    def take_id(self, v: int) -> str:
        if v in self.seen:
            return ""
        self.seen.add(v)
        return f' id="v{self.chap}-{v}"'

    def render_content(self, raw: str) -> str:
        parts: list[str] = []
        for v, txt in split_verses(raw):
            inner = render_inline_full(txt, self.linker)
            if v is None:
                if self.cur_verse is not None:
                    parts.append(
                        f'<span class="verse cont" data-verse="{self.chap}:{self.cur_verse}">'
                        f"{inner}</span>"
                    )
                else:
                    parts.append(inner)
            else:
                self.cur_verse = v
                vid = self.take_id(v)
                sup = (
                    f'<sup class="vn"><a href="#v{self.chap}-{v}" '
                    f'title="Capítulo {self.chap}, versículo {v}">{v}</a></sup>'
                )
                parts.append(
                    f'<span class="verse"{vid} data-verse="{self.chap}:{v}">'
                    f"{sup}{inner}</span>"
                )
        return "".join(parts)

    def render_blocks(self, text: str) -> str:
        lines = text.splitlines()
        i = 0
        html: list[str] = []
        title = ""
        while i < len(lines):
            line = lines[i]
            if not line.strip():
                i += 1
                continue
            if line.startswith("#"):
                level = len(line) - len(line.lstrip("#"))
                content = line.lstrip("#").strip()
                if level == 1:
                    if not title:
                        title = content
                else:
                    tag = f"h{min(level, 4)}"
                    html.append(f'<{tag}>{inline_md(escape_html(content))}</{tag}>')
                i += 1
                continue
            if line.startswith(">"):
                buf = []
                while i < len(lines) and lines[i].startswith(">"):
                    buf.append(lines[i].lstrip(">").strip())
                    i += 1
                inner = self.render_content("\n".join(buf))
                html.append(f"<blockquote>{inner}</blockquote>")
                continue
            if line.startswith("* ") or line.startswith("- "):
                items = []
                while i < len(lines) and (
                    lines[i].startswith("* ") or lines[i].startswith("- ")
                ):
                    items.append(lines[i][2:].strip())
                    i += 1
                lis = "".join(f"<li>{self.render_content(it)}</li>" for it in items)
                html.append(f"<ul>{lis}</ul>")
                continue
            buf = []
            while i < len(lines) and lines[i].strip():
                ln = lines[i]
                if (
                    ln.startswith("#")
                    or ln.startswith(">")
                    or ln.startswith("* ")
                    or ln.startswith("- ")
                ):
                    break
                buf.append(ln.rstrip())
                i += 1
            if buf:
                html.append(f"<p>{self.render_content(chr(10).join(buf))}</p>")
        return title, "".join(html)


def parse_chapters(linker: TermLinker) -> tuple[list[dict], set[tuple[int, int]]]:
    chapters = []
    seen: set[tuple[int, int]] = set()
    files = sorted(DOC_DIR.glob("cap-*.md"))
    for f in files:
        m = re.match(r"cap-(\d+)", f.name)
        if not m:
            continue
        num = int(m.group(1))
        text = f.read_text(encoding="utf-8")
        r = ChapterRenderer(num, linker)
        title, html = r.render_blocks(text)
        # título por defecto desde el enlace del índice si falló
        if not title:
            first = next((ln for ln in text.splitlines() if ln.startswith("# ")), "")
            title = first[2:].strip()
        for v in r.seen:
            seen.add((num, v))
        chapters.append(
            {
                "num": num,
                "slug": re.sub(r"^cap-\d+-", "", f.stem),
                "title": re.sub(r"^\d+\.\s*", "", title),
                "html": html,
            }
        )
    chapters.sort(key=lambda c: c["num"])
    return chapters, seen


# ----------------------------------------------------------------------------- vocabulario


def parse_md_tables(text: str) -> list[tuple[list[str], list[list[str]]]]:
    rows: list[list[list[str]]] = []
    cur: list[list[str]] | None = None
    for line in text.splitlines():
        s = line.strip()
        if s.startswith("|") and s.endswith("|") and len(s) > 1:
            cells = [c.strip() for c in s[1:-1].split("|")]
            if cur is None:
                cur = []
            cur.append(cells)
        else:
            if cur:
                rows.append(cur)
                cur = None
    if cur:
        rows.append(cur)

    tables = []
    for block in rows:
        if not block:
            continue
        header = block[0]
        data = [
            r
            for r in block[1:]
            if not all(SEP_CELL_RE.match(c) for c in r if c)
            and any(c for c in r)
        ]
        tables.append((header, data))
    return tables


def col_idx(header: list[str], *needles: str) -> int:
    for i, h in enumerate(header):
        hl = h.lower()
        for n in needles:
            if n in hl:
                return i
    return -1


def cell_get(cells: list[str], idx: int) -> str:
    if 0 <= idx < len(cells):
        return cells[idx].strip()
    return ""


def render_cell(text: str) -> tuple[str, list[dict]]:
    """Renderiza una celda; devuelve (html, citas)."""
    if not text:
        return "", []
    cites: list[dict] = []
    parts: list[str] = []
    last = 0
    for m in LINK_RE.finditer(text):
        outside = text[last : m.start()]
        if outside:
            parts.append(inline_md(escape_html(outside)))
        label = m.group(1)
        cm = CITE_TAIL_RE.search(label)
        if cm:
            ch = int(cm.group(1))
            rest = cm.group(2)
            for part in rest.split(","):
                part = part.strip()
                if not part:
                    continue
                if "-" in part:
                    a, b = part.split("-", 1)
                    v = int(a)
                    lab = f"{ch}:{a}–{b}"
                else:
                    v = int(part)
                    lab = f"{ch}:{part}"
                cites.append({"ch": ch, "v": v, "label": lab})
                if parts and parts[-1].endswith("</a>"):
                    parts.append(" ")
                parts.append(
                    f'<a class="cite-chip" href="#v{ch}-{v}" '
                    f'title="Ir al texto · capítulo {ch}, versículo {v}">{lab}</a>'
                )
        else:
            parts.append(
                f'<a class="cite-chip soft" href="{escape_html(m.group(2))}" '
                f'target="_blank" rel="noopener">{escape_html(label)}</a>'
            )
        last = m.end()
    tail = text[last:]
    if tail:
        parts.append(inline_md(escape_html(tail)))
    return "".join(parts), cites


def parse_vocab() -> tuple[list[dict], list[str], list[dict]]:
    text = VOCAB_PATH.read_text(encoding="utf-8")
    tables = parse_md_tables(text)
    entries: list[dict] = []
    themes_all: list[str] = []

    for header, data in tables:
        if col_idx(header, "índice", "indice") < 0:
            continue
        table_no = len({e["table"] for e in entries}) + 1
        i_idx = col_idx(header, "índice", "indice")
        i_sub = col_idx(header, "subíndice", "subindice")
        i_term = col_idx(header, "término", "termino")
        i_def = col_idx(header, "definición", "definicion")
        i_ex = col_idx(header, "ejemplo")
        i_src = col_idx(header, "fuente")
        i_date = col_idx(header, "fecha")
        i_theme = col_idx(header, "tema")
        i_ai = col_idx(header, "término-con-ia", "termino-con-ia")

        for row in data:
            term_raw = cell_get(row, i_term)
            term = strip_md(term_raw)
            if not term:
                continue
            def_raw = cell_get(row, i_def) if i_def >= 0 else ""
            sin_acuerdo = False
            if def_raw:
                m = SIN_ACUERDO_RE.match(def_raw)
                if m:
                    sin_acuerdo = True
                    def_raw = def_raw[m.end() :]
            def_html = inline_md(escape_html(def_raw.strip())) if def_raw.strip() else ""
            def_plain = strip_md(def_raw)

            ex_html, ex_cites = render_cell(cell_get(row, i_ex) if i_ex >= 0 else "")
            src_html, src_cites = render_cell(cell_get(row, i_src) if i_src >= 0 else "")

            src_plain_raw = cell_get(row, i_src) if i_src >= 0 else ""
            src_is_cite = bool(CITE_TAIL_RE.search(strip_md(src_plain_raw)))

            themes_raw = cell_get(row, i_theme) if i_theme >= 0 else ""
            themes = [t.strip() for t in themes_raw.split(",") if t.strip()]
            for t in themes:
                if t not in themes_all:
                    themes_all.append(t)

            idx = cell_get(row, i_idx) if i_idx >= 0 else ""
            sub = cell_get(row, i_sub) if i_sub >= 0 else ""
            date = cell_get(row, i_date) if i_date >= 0 else ""
            ai = cell_get(row, i_ai) if i_ai >= 0 else ""

            all_cites = ex_cites + [c for c in src_cites if c not in ex_cites]
            # Cita principal = primera aparición en el documento (cap:verso menor)
            primary = (
                min(all_cites, key=lambda c: (c["ch"], c["v"])) if all_cites else None
            )

            entries.append(
                {
                    "id": f"t-{len(entries)}",
                    "table": table_no,
                    "index": idx,
                    "subindex": sub,
                    "term": term,
                    "definition": def_html,
                    "definitionPlain": def_plain,
                    "sinAcuerdo": sin_acuerdo,
                    "example": ex_html,
                    "examplePlain": strip_md(cell_get(row, i_ex) if i_ex >= 0 else ""),
                    "source": src_html,
                    "sourcePlain": strip_md(src_plain_raw),
                    "sourceIsCite": src_is_cite,
                    "date": date,
                    "themes": themes,
                    "ai": strip_md(ai),
                    "primaryCite": primary,
                    "citesText": " ".join(
                        dict.fromkeys(c["label"].replace("–", "-") for c in all_cites)
                    ),
                }
            )

    # mapa de términos para enlazar en el texto
    term_map: list[dict] = []
    seen_terms: set[str] = set()
    for e in entries:
        t = e["term"]
        if len(t) < 5:
            continue
        key = t.casefold()
        if key in seen_terms:
            continue
        seen_terms.add(key)
        preview = e["definitionPlain"] or e["examplePlain"] or e["term"]
        preview = re.sub(r"\s+", " ", preview).strip()
        if len(preview) > 150:
            preview = preview[:147] + "…"
        title = f'{e["term"]} — {preview}' if preview and preview != e["term"] else e["term"]
        term_map.append({"term": t, "entry": e["id"], "title": title})

    return entries, themes_all, term_map


# ----------------------------------------------------------------------------- fuentes


def parse_cite_list(fragment: str) -> list[dict]:
    cites = []
    for m in LINK_RE.finditer(fragment):
        label = m.group(1).strip()
        cm = CITE_SIMPLE_RE.match(label) or CITE_TAIL_RE.search(label)
        if not cm:
            continue
        ch = int(cm.group(1))
        rest = cm.group(2)
        for part in rest.split(","):
            part = part.strip()
            if not part:
                continue
            if "-" in part:
                a, b = part.split("-", 1)
                v = int(a)
                lab = f"{ch}:{a}–{b}"
            else:
                v = int(part)
                lab = f"{ch}:{part}"
            cites.append({"ch": ch, "v": v, "label": lab})
    return cites


def parse_sources() -> list[dict]:
    fuentes_path = DOC_DIR / "fuentes-y-referencias.md"
    text = fuentes_path.read_text(encoding="utf-8")
    out = []
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    for para in paras:
        if para.startswith("#"):
            continue
        cited = True
        cites: list[dict] = []
        body = para
        if "— no citada en el cuerpo" in para:
            body = para.split("— no citada en el cuerpo")[0].strip()
            cited = False
        elif "— usada en" in para:
            body, rest = para.split("— usada en", 1)
            body = body.strip()
            cites = parse_cite_list(rest)
        body = body.rstrip()
        body_html = inline_md(escape_html(body))
        chips = " ".join(
            f'<a class="cite-chip" href="#v{c["ch"]}-{c["v"]}" '
            f'title="Ir al texto · capítulo {c["ch"]}, versículo {c["v"]}">'
            f'{c["label"]}</a>'
            for c in cites
        )
        out.append(
            {
                "id": f"s-{len(out)}",
                "html": body_html,
                "plain": strip_md(body),
                "cited": cited,
                "chips": chips,
                "citesText": " ".join(c["label"].replace("–", "-") for c in cites),
                "uses": len(cites),
                "primaryCite": cites[0] if cites else None,
            }
        )
    return out


def parse_meta() -> dict:
    text = INDEX_PATH.read_text(encoding="utf-8")
    title = ""
    author = ""
    for line in text.splitlines():
        if line.startswith("# "):
            title = line[2:].strip()
        m = re.match(r"\*\*(.+?)\*\*\s*$", line.strip())
        if m and m.group(1).rstrip(":").strip().lower() != "por":
            if not author:
                author = m.group(1).strip()
    return {"title": title, "author": author}


def main() -> int:
    entries, themes, term_map_raw = parse_vocab()
    linker = TermLinker(term_map_raw)
    chapters, verse_ids = parse_chapters(linker)
    sources = parse_sources()
    meta = parse_meta()

    warnings = []
    for e in entries:
        # comprobar citas en example/source ya renderizadas
        for label in (e["citesText"] or "").split():
            m = re.match(r"(\d+):(\d+)", label)
            if not m:
                continue
            ch, v = int(m.group(1)), int(m.group(2))
            if (ch, v) not in verse_ids:
                warnings.append(f'vocab "{e["term"]}": cita {ch}:{v} no existe')
    for s in sources:
        for label in (s["citesText"] or "").split():
            m = re.match(r"(\d+):(\d+)", label)
            if not m:
                continue
            ch, v = int(m.group(1)), int(m.group(2))
            if (ch, v) not in verse_ids:
                warnings.append(f'fuente {s["id"]}: cita {ch}:{v} no existe')

    data = {
        "meta": meta,
        "chapters": chapters,
        "vocabulary": entries,
        "themes": themes,
        "termMap": term_map_raw,
        "sources": sources,
        "stats": {
            "chapters": len(chapters),
            "verses": len(verse_ids),
            "terms": len(entries),
            "sources": len(sources),
        },
    }

    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":"))
    OUT_PATH.write_text(
        "// Generado por generate_data.py — no editar a mano.\n"
        f"window.SITE_DATA = {payload};\n",
        encoding="utf-8",
    )

    print(f"OK → {OUT_PATH}")
    print(
        f"  capítulos: {len(chapters)} | versículos: {len(verse_ids)} | "
        f"términos: {len(entries)} | fuentes: {len(sources)} | "
        f"términos enlazables: {len(term_map_raw)}"
    )
    print(f"  tamaño: {OUT_PATH.stat().st_size / 1024:.1f} KB")
    if warnings:
        print(f"  ⚠ {len(warnings)} avisos:", file=sys.stderr)
        for w in warnings[:30]:
            print(f"    - {w}", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
