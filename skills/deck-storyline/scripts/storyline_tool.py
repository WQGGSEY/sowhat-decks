#!/usr/bin/env python3
"""deck-storyline helper: read a storyline.md, lint it, print the title-only
read-out, and write a title-only "ghost deck" spec for deck-build.

Standard library only. No network access. Never invents content: every string in
the ghost spec comes from storyline.md.

Usage:
  python3 storyline_tool.py titles storyline.md      # title-only read-out + title lint
  python3 storyline_tool.py check  storyline.md      # full structure check (exit 1 on errors)
  python3 storyline_tool.py ghost  storyline.md -o ghost.json [--pure]
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass, field
from pathlib import Path

SPEC_VERSION = "1.0"
LAYOUTS = {
    "cover", "executive_summary", "section", "exhibit", "exhibit_takeaways",
    "two_column", "pillars", "table", "timeline", "quote", "recommendations",
    "appendix", "ghost",
}
LAYOUT_ALIASES = {
    "title": "cover", "executive-summary": "executive_summary", "summary": "executive_summary",
    "exhibit-takeaways": "exhibit_takeaways", "two-column": "two_column",
    "recommendation": "recommendations", "next-steps": "recommendations",
}
ROLES = {"cover", "summary", "section", "evidence", "recommendation", "next-steps", "appendix"}
NO_CLAIM_ROLES = {"cover", "section", "appendix"}
DATA_NEEDED_RE = re.compile(r"\[DATA NEEDED(?::[^\]]*)?\]")
PLACEHOLDER_RE = re.compile(r"<[^<>\n]{2,}>")

# --------------------------------------------------------------------------- parsing


@dataclass
class Slide:
    num: int
    title: str
    fields: dict = field(default_factory=dict)
    line: int = 0

    def get(self, key: str, default: str = "") -> str:
        return self.fields.get(key.lower(), default).strip()

    @property
    def role(self) -> str:
        return self.get("role", "evidence").lower()


@dataclass
class Storyline:
    deck_name: str = ""
    brief: dict = field(default_factory=dict)
    governing: str = ""
    scqa: dict = field(default_factory=dict)
    split: str = ""
    order: str = ""
    arguments: list = field(default_factory=list)
    slides: list = field(default_factory=list)
    title_test: str = ""
    ledger: dict = field(default_factory=dict)
    sources: dict = field(default_factory=dict)
    open_requests: list = field(default_factory=list)


FIELD_RE = re.compile(r"^\s*[-*]\s+([A-Za-z][A-Za-z /-]{0,30}):\s*(.*)$")


def _strip_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def _sections(text: str) -> dict:
    """Split on '## ' headings. Keys are lower-cased heading text without numbering."""
    out, cur, buf = {}, None, []
    for line in text.splitlines():
        if line.startswith("## "):
            if cur is not None:
                out[cur] = "\n".join(buf)
            cur = re.sub(r"^\d+[.)]?\s*", "", line[3:].strip()).lower()
            buf = []
        elif cur is not None:
            buf.append(line)
    if cur is not None:
        out[cur] = "\n".join(buf)
    return out


def _find(sections: dict, *keys: str) -> str:
    for name, body in sections.items():
        if any(k in name for k in keys):
            return body
    return ""


def _fields(body: str) -> dict:
    out = {}
    for line in body.splitlines():
        m = FIELD_RE.match(line)
        if m:
            out[m.group(1).strip().lower()] = m.group(2).strip()
    return out


def _table_rows(body: str) -> list:
    rows = []
    for line in body.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(re.fullmatch(r":?-{2,}:?", c) for c in cells if c):
            continue
        rows.append(cells)
    return rows[1:] if rows else []  # drop header


def parse(path: Path) -> Storyline:
    raw = path.read_text(encoding="utf-8")
    text = _strip_comments(raw)
    st = Storyline()
    m = re.search(r"^#\s+(?:Storyline:\s*)?(.+)$", text, flags=re.M)
    st.deck_name = m.group(1).strip() if m else path.stem
    secs = _sections(text)

    st.brief = _fields(_find(secs, "brief"))
    gm = _find(secs, "governing message")
    quote = [ln.lstrip("> ").strip() for ln in gm.splitlines() if ln.strip().startswith(">")]
    st.governing = " ".join(q for q in quote if q) or gm.strip()
    st.scqa = _fields(_find(secs, "scqa"))

    ka = _find(secs, "key argument")
    kaf = _fields(ka)
    st.split, st.order = kaf.get("split", ""), kaf.get("order", "")
    for line in ka.splitlines():
        m = re.match(r"^\s*(\d+)[.)]\s+(.*)$", line)
        if m:
            claim = re.split(r"\s+[—–-]{1,2}\s+answers?:", m.group(2), maxsplit=1)[0].strip()
            st.arguments.append(claim)

    plan = _find(secs, "slide plan")
    cur = None
    plan_offset = raw.count("\n", 0, raw.find("Slide plan")) if "Slide plan" in raw else 0
    for i, line in enumerate(plan.splitlines()):
        m = re.match(r"^###\s+(\d+)[.)]?\s+(.*)$", line)
        if m:
            cur = Slide(num=int(m.group(1)), title=m.group(2).strip(), line=plan_offset + i + 2)
            st.slides.append(cur)
            continue
        fm = FIELD_RE.match(line)
        if cur is not None and fm:
            cur.fields[fm.group(1).strip().lower()] = fm.group(2).strip()

    st.title_test = _find(secs, "title-only", "title only")
    for row in _table_rows(_find(secs, "evidence ledger", "ledger")):
        if len(row) >= 4 and re.fullmatch(r"[A-Za-z]{0,3}\d+[a-z]?", row[0]):
            st.ledger[row[0]] = {"fact": row[1], "tag": row[2], "source": row[3],
                                 "slides": row[4] if len(row) > 4 else ""}
    for line in _find(secs, "sources").splitlines():
        m = re.match(r"^\s*(\d+)[.)]\s+(.*)$", line)
        if m:
            st.sources[m.group(1)] = m.group(2).strip()
    st.open_requests = DATA_NEEDED_RE.findall(_find(secs, "open data", "data requests"))
    return st


# --------------------------------------------------------------------------- linting

LABEL_TITLES = {
    "overview", "summary", "executive summary", "agenda", "background", "introduction",
    "context", "next steps", "recommendations", "recommendation", "conclusion", "conclusions",
    "results", "financials", "financial summary", "market overview", "market", "competition",
    "competitive landscape", "team", "roadmap", "risks", "appendix", "key findings", "findings",
    "analysis", "update", "status", "kpis", "metrics", "q&a", "questions", "thank you",
}
VERB_BASES = set("""
be do have will would can could should must shall may might grow fall rise double triple
halve beat miss drive reach exceed outpace lag keep make take give get put suggest mean pay
save cut add bring win lose remain stay turn become come go require depend explain outgrow
overtake own cover improve decline increase decrease expand shrink slow accelerate peak
recover invest enter ask approve choose recommend move shift hire spend build ship stop
start let combine dominate absorb offset finish convert cancel renew deliver generate
produce widen narrow deepen lift lower raise boost hurt confirm prove protect threaten
solve reduce gain adopt prefer leave join replace serve enable allow create
continue outperform underperform shrink halt hit set match trail
""".split())
# Verbs that are also common nouns ("costs", "accounts"): only the -ed form counts,
# through the generic -ed rule. Kept as a list so they are not added to VERB_BASES.
NOUNISH_VERBS = set("""
account answer block buy carry churn close cost cross fix fund help hold land launch lead
limit matter need offer open pass rank return risk score sell show sign signal sit
stand support top trade use
""".split())
IRREGULAR_VERBS = set("""
is are was were been being am has had does did grew fell rose drove led held kept made took
gave got shown meant paid won lost became came went sold bought built spent brought left
stood sat ran
""".split())


# A word right after these is used as an adjective or noun ("of churned accounts").
NOT_AFTER = set("a an the of for by with in on per to from at our their its this that's".split())


def _is_verb(w: str, prev: str = "") -> bool:
    """Rough English verb test. Gerunds (-ing) never count: "hiring plan" is a noun phrase."""
    if w in IRREGULAR_VERBS:
        return True
    if prev in NOT_AFTER:
        return False
    if w in VERB_BASES:
        return True
    if len(w) > 4 and w.endswith("ed"):
        return True
    for suf, rep in (("ies", "y"), ("es", ""), ("s", "")):
        if w.endswith(suf) and w[: -len(suf)] + rep in VERB_BASES:
            return True
    return False


HEDGES = {"might", "possibly", "potentially", "perhaps", "somewhat", "arguably", "seems",
          "appears", "could"}
YEARISH = re.compile(r"^(?:(?:19|20)\d{2}|FY\d{2,4}|CY\d{2,4}|Q[1-4]|H[12]|[1-4]Q\d{0,4})$", re.I)


def _cjk_ratio(s: str) -> float:
    letters = [c for c in s if not c.isspace()]
    if not letters:
        return 0.0
    cjk = sum(1 for c in letters if "ᄀ" <= c <= "ᇿ" or "぀" <= c <= "ヿ"
              or "㐀" <= c <= "鿿" or "가" <= c <= "힯")
    return cjk / len(letters)


def _lang(s: str) -> str:
    if _cjk_ratio(s) < 0.3:
        return "en"
    if re.search(r"[가-힯]", s):
        return "ko"
    return "ja"


def _has_number_claim(title: str) -> bool:
    t = DATA_NEEDED_RE.sub("", title)
    for tok in re.findall(r"[A-Za-z$€£¥₩]*\d[\d,.]*[A-Za-z%$]*", t):
        if not YEARISH.match(tok.strip(".,")):
            return True
    return False


def lint_title(s: Slide, n_slides: int) -> list:
    """Return a list of (level, message). level is 'error' or 'warn'."""
    out = []
    t = s.title.strip()
    role = s.role
    if not t or PLACEHOLDER_RE.search(t):
        return [("error", "title is empty or still a template placeholder")]
    if role not in ROLES:
        out.append(("warn", f"unknown role '{role}' (use one of: {', '.join(sorted(ROLES))})"))
    lang = _lang(t)
    plain = DATA_NEEDED_RE.sub("X", t)
    if lang == "en":
        words = re.findall(r"[A-Za-z0-9$%][\w$%'’.,-]*", plain)
        nw, nc = len(words), len(t)
        if nw > 20 or nc > 120:
            out.append(("error", f"too long ({nw} words, {nc} chars); cap is 20 words / 120 chars"))
        elif nw > 18 or nc > 100:
            out.append(("warn", f"long ({nw} words, {nc} chars); aim for 10-16 words, <= 100 chars"))
    else:
        nc = len(re.sub(r"\s", "", plain))
        if nc > 60:
            out.append(("error", f"too long ({nc} chars); cap is 60 for {lang}"))
        elif nc > 50:
            out.append(("warn", f"long ({nc} chars); aim for 25-50 for {lang}"))
    if role in NO_CLAIM_ROLES:
        return out
    low = re.sub(r"[^\w\s&]", "", t.lower()).strip()
    if t.endswith("?") or t.endswith("？"):
        out.append(("error", "question title; state the answer instead"))
    if low in LABEL_TITLES:
        out.append(("error", "topic label, not a claim"))
    elif lang == "en":
        toks = re.findall(r"[a-z’']+", plain.lower())
        if len(toks) <= 3:
            out.append(("error", "too short to be a claim (<= 3 words)"))
        elif not any(_is_verb(w, toks[i - 1] if i else "") for i, w in enumerate(toks)):
            out.append(("warn", "no verb found; may be a topic label"))
        hedges = sorted({w for w in toks if w in HEDGES})
        if hedges:
            out.append(("warn", f"hedging words: {', '.join(hedges)}"))
    elif lang == "ko":
        if not re.search(r"(다|요|음|함|임|됨|짐)[.。]?$", t):
            out.append(("warn", "Korean title does not end in a predicate (~다); may be a topic label"))
    else:
        if not re.search(r"(る|た|い|だ|す|ない|ある|いる|できる)[。.]?$", t):
            out.append(("warn", "Japanese title does not end in a predicate; may be a topic label"))
    if DATA_NEEDED_RE.search(t):
        out.append(("warn", "title contains [DATA NEEDED]; fine for a storyline, fails final review"))
    elif _has_number_claim(t):
        ev = s.get("evidence").lower()
        if not ev or ev in {"none", "-", "n/a"}:
            out.append(("error", "title states a number but the slide lists no evidence"))
    return out


def _norm_tokens(t: str) -> set:
    return {w for w in re.findall(r"\w+", t.lower()) if len(w) > 2}


def duplicate_pairs(slides: list) -> list:
    pairs = []
    for i, a in enumerate(slides):
        for b in slides[i + 1:]:
            ta, tb = _norm_tokens(a.title), _norm_tokens(b.title)
            if ta and tb and len(ta & tb) / len(ta | tb) >= 0.7:
                pairs.append((a.num, b.num))
    return pairs


def title_paragraph(st: Storyline) -> str:
    parts = []
    for s in st.slides:
        t = s.title.strip()
        parts.append(t if re.search(r"[.!?。！？]$", t) else t + ".")
    return " ".join(parts)


# --------------------------------------------------------------------------- commands


def _ev_ids(s: Slide) -> list:
    return re.findall(r"\b([A-Z]{1,3}\d+[a-z]?)\b", DATA_NEEDED_RE.sub("", s.get("evidence")))


def _gaps(s: Slide) -> list:
    gaps = DATA_NEEDED_RE.findall(s.get("gaps")) + DATA_NEEDED_RE.findall(s.get("evidence"))
    gaps += [g for g in DATA_NEEDED_RE.findall(s.title) if g not in gaps]
    return gaps


def run_titles(st: Storyline) -> int:
    print("TITLE-ONLY READ-OUT\n")
    print(title_paragraph(st))
    print("\nPER-TITLE LINT")
    errors = 0
    for s in st.slides:
        issues = lint_title(s, len(st.slides))
        mark = "ok " if not issues else ("ERR" if any(l == "error" for l, _ in issues) else "wrn")
        print(f"  [{mark}] {s.num:>2}. ({s.role}) {s.title}")
        for level, msg in issues:
            errors += level == "error"
            print(f"         {level}: {msg}")
    for a, b in duplicate_pairs(st.slides):
        print(f"  [wrn] slides {a} and {b} have very similar titles; check for a repeated claim")
    print("\nNow answer the 7 title-only questions (references/action-titles.md, section 9)")
    print("and record PASS/FAIL with reasoning in section 5 of storyline.md.")
    return 1 if errors else 0


def run_check(st: Storyline) -> int:
    errs, warns = [], []
    for key in ("purpose", "audience", "decision"):
        if not st.brief.get(key) or PLACEHOLDER_RE.search(st.brief.get(key, "")):
            errs.append(f"brief: '{key}' is missing")
    gm = st.governing.strip()
    if not gm or PLACEHOLDER_RE.search(gm):
        errs.append("governing message is missing")
    else:
        sentences = [x for x in re.split(r"(?<=[.!?。])\s+", gm) if x.strip()]
        if len(sentences) > 1:
            warns.append(f"governing message has {len(sentences)} sentences; use one")
        nw = len(gm.split()) if _lang(gm) == "en" else len(gm) // 2
        if nw > 35:
            warns.append(f"governing message is long (~{nw} words); aim for <= 30")
    for key in ("situation", "complication", "question", "answer"):
        if not st.scqa.get(key) or PLACEHOLDER_RE.search(st.scqa.get(key, "")):
            errs.append(f"SCQA: '{key}' is missing")
    n = len(st.arguments)
    if not 3 <= n <= 5:
        (errs if n < 2 or n > 6 else warns).append(f"{n} key arguments; use 3-5")
    if not st.split:
        warns.append("key arguments: no 'Split:' recorded for the overlap-and-gap (MECE) check")
    if not st.slides:
        errs.append("slide plan has no '### n. title' blocks")
    used_args = set()
    for s in st.slides:
        for level, msg in lint_title(s, len(st.slides)):
            (errs if level == "error" else warns).append(f"slide {s.num}: {msg}")
        layout = s.get("layout").lower()
        if layout and LAYOUT_ALIASES.get(layout, layout) not in LAYOUTS:
            warns.append(f"slide {s.num}: layout '{layout}' is not a deck-build layout")
        for a in re.findall(r"\d+", s.get("argument")):
            used_args.add(int(a))
        if s.role in NO_CLAIM_ROLES:
            continue
        ids, gaps = _ev_ids(s), _gaps(s)
        if not ids and not gaps and s.role not in {"summary"}:
            warns.append(f"slide {s.num}: no evidence IDs and no [DATA NEEDED]; what proves the title?")
        for i in ids:
            if st.ledger and i not in st.ledger:
                errs.append(f"slide {s.num}: evidence {i} is not in the evidence ledger")
    for i in range(1, n + 1):
        if i not in used_args:
            warns.append(f"key argument {i} has no slide (Argument: {i})")
    content = [s for s in st.slides if s.role not in {"appendix"}]
    if content and content[-1].role not in {"recommendation", "next-steps"}:
        warns.append("the last main slide is not a recommendation / next-steps slide")
    for eid, row in st.ledger.items():
        for src in re.findall(r"SRC\s*(\d+)", row["tag"] + " " + row["source"]):
            if src not in st.sources:
                errs.append(f"ledger {eid}: SRC {src} has no entry in Sources")
        if "CALC" in row["tag"].upper() and not re.search(r"[=×x*/+−-]", row["source"]):
            warns.append(f"ledger {eid}: CALC without a formula")
    for a, b in duplicate_pairs(st.slides):
        warns.append(f"slides {a} and {b} have very similar titles")
    if not re.search(r"Overall:\s*(PASS|FAIL)", st.title_test, flags=re.I):
        warns.append("title-only test not recorded (section 5, 'Overall: PASS|FAIL')")
    gaps = sorted({g for s in st.slides for g in _gaps(s)})
    sample = "sample" in st.brief.get("data status", "").lower()

    print(f"Storyline: {st.deck_name}")
    print(f"  slides: {len(st.slides)}  key arguments: {n}  ledger rows: {len(st.ledger)}"
          f"  sources: {len(st.sources)}  [DATA NEEDED]: {len(gaps)}"
          f"  sample data: {'yes' if sample else 'no'}")
    for e in errs:
        print(f"  ERROR: {e}")
    for w in warns:
        print(f"  warn:  {w}")
    if gaps:
        print("  open data requests:")
        for g in gaps:
            print(f"    - {g}")
    print("RESULT:", "FAIL" if errs else "PASS", f"({len(errs)} errors, {len(warns)} warnings)")
    return 1 if errs else 0


def _clip(s: str, n: int) -> str:
    """Shorten to n chars at a separator or word boundary, never inside a number."""
    s = re.sub(r"\s+", " ", s).strip()
    if len(s) <= n:
        return s
    cut = s[: n - 1]
    for sep in ("; ", ", ", " "):
        i = cut.rfind(sep)
        if i > n * 0.5:
            cut = cut[:i]
            break
    return cut.rstrip(" ,;:—-") + "…"


def _evidence_lines(st: Storyline, s: Slide) -> list:
    lines = []
    for i in _ev_ids(s):
        row = st.ledger.get(i)
        if row:
            tag = f" [{row['tag'].strip()}]" if row["tag"].strip() else ""
            lines.append(_clip(f"{i} {row['fact']}", 160 - len(tag)) + tag)
        else:
            lines.append(i)
    for g in _gaps(s):
        body = g[len("[DATA NEEDED"):].lstrip(":").rstrip("]").strip()
        lines.append("[DATA NEEDED] " + body if body else "[DATA NEEDED]")
    if len(lines) > 5:
        extra = len(lines) - 4
        lines = lines[:4] + [f"+{extra} more items in storyline.md"]
    return [_clip(x, 160) for x in lines]


def build_ghost(st: Storyline, pure: bool = False) -> tuple:
    warnings = []
    lang = st.brief.get("language", "en").split()[0].lower()
    if lang not in {"en", "ko", "ja"}:
        warnings.append(f"language '{lang}' not supported by deck-build; using en")
        lang = "en"
    meta = {"title": _clip(st.deck_name, 120), "language": lang, "draft": True}
    deck_type = st.brief.get("deck type", "").split("|")[0].strip()
    meta["subtitle"] = _clip("Ghost deck (storyline draft)" + (f" · {deck_type}" if deck_type else ""), 160)
    if st.brief.get("date"):
        meta["date"] = _clip(st.brief["date"], 40)
    if st.brief.get("presenter"):
        meta["author"] = _clip(st.brief["presenter"], 80)
    if "sample" in st.brief.get("data status", "").lower():
        meta["sample_data"] = True
    slides = []
    section_no = 0
    for s in st.slides:
        notes = s.get("notes")
        layout = LAYOUT_ALIASES.get(s.get("layout").lower(), s.get("layout").lower()) or "ghost"
        if s.role == "cover":
            d = {"layout": "cover", "title": _clip(s.title, 100)}
            sub = s.get("subtitle") or st.governing
            if sub:
                d["subtitle"] = _clip(sub, 160)
            if st.brief.get("date"):
                d["date"] = _clip(st.brief["date"], 40)
        elif s.role == "section":
            section_no += 1
            d = {"layout": "section", "title": _clip(s.title, 80), "number": section_no}
        elif (s.role == "summary" and not pure and 2 <= len(st.arguments) <= 5
              and all(len(a) <= 120 for a in st.arguments)):
            d = {"layout": "executive_summary", "title": _clip(s.title, 120),
                 "points": [a for a in st.arguments]}
            if meta.get("sample_data"):
                d["source"] = "Sample data"
        else:
            g = {}
            if layout and layout != "ghost":
                g["layout"] = layout
            ex = re.sub(r"^none\s*[—–-]+\s*", "", s.get("exhibit"), flags=re.I)
            if ex and ex.lower() not in {"none", "-"}:
                g["exhibit"] = _clip(ex, 160)
            ev = _evidence_lines(st, s)
            if ev:
                g["evidence"] = ev
            d = {"layout": "ghost", "title": _clip(s.title, 120)}
            if s.get("tracker"):
                d["tracker"] = _clip(s.get("tracker"), 40)
            elif s.role == "appendix":
                d["tracker"] = "Appendix"
            if g:
                d["ghost"] = g
        if len(s.title) > (100 if s.role == "cover" else 80 if s.role == "section" else 120):
            warnings.append(f"slide {s.num}: title clipped to the schema limit")
        if notes:
            d["notes"] = _clip(notes, 4000)
        d["id"] = f"s{s.num:02d}"
        slides.append(d)
    spec = {"spec_version": SPEC_VERSION, "meta": meta, "slides": slides}
    if pure:
        # every slide (except cover/section) rendered title-only by deck-build
        spec = {"spec_version": SPEC_VERSION, "mode": "ghost", "meta": meta, "slides": slides}
    return spec, warnings


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("titles", "check", "ghost"):
        p = sub.add_parser(name)
        p.add_argument("storyline", type=Path)
        if name == "ghost":
            p.add_argument("-o", "--out", type=Path, required=True, help="ghost deck spec JSON to write")
            p.add_argument("--pure", action="store_true",
                           help="title-only everywhere (no key-argument bullets on the summary slide)")
    a = ap.parse_args(argv)
    if not a.storyline.exists():
        print(f"not found: {a.storyline}", file=sys.stderr)
        return 2
    st = parse(a.storyline)
    if a.cmd == "titles":
        return run_titles(st)
    if a.cmd == "check":
        return run_check(st)
    spec, warnings = build_ghost(st, pure=a.pure)
    a.out.parent.mkdir(parents=True, exist_ok=True)
    a.out.write_text(json.dumps(spec, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    for w in warnings:
        print("warn:", w)
    print(f"wrote {a.out} ({len(spec['slides'])} slides, ghost deck)")
    print("next: render it with deck-build, e.g.")
    print(f"  python3 <deck-build>/scripts/build.py {a.out} -o out/ --name ghost")
    return 0


if __name__ == "__main__":
    sys.exit(main())
