"""Automatic checks over the dict returned by inspect.inspect_pptx().

Pure functions: no file access. Each issue is a dict:

    check      id, e.g. "text_overflow" (see references/checks.md)
    severity   "high" | "medium" | "low"
    slide      1-based slide number, or None for deck-level issues
    shape_id   id of the shape inside the slide (None if not tied to one shape)
    shape      shape name, for humans
    bbox       [x, y, w, h] in EMU to draw on the rendered slide (or None)
    message    what is wrong, with numbers
    fix        what to do about it
    auto_fix   True if fix.py can repair it safely
    locations  for deck-level issues: [{slide, shape_id, shape, bbox}, ...]
"""

from __future__ import annotations

import colorsys
import re
from collections import Counter, defaultdict

from . import titles as T

EMU_IN = 914400

DEFAULTS = {
    "body_min_pt": 12.0,
    "source_min_pt": 10.0,
    "table_min_pt": 10.0,
    "chart_min_pt": 10.0,
    "title_min_pt": 24.0,
    "title_max_lines": 2,
    "title_max_words": 20,
    "title_max_chars": 120,
    "title_max_chars_cjk": 60,
    "overflow_ratio": 1.10,
    "overflow_high_ratio": 1.30,
    "autogrow_ratio": 1.50,
    "edge_tolerance_in": 0.02,
    "overlap_text_frac": 0.02,
    "overlap_label_frac": 0.25,
    "overlap_object_frac": 0.05,
    "align_min_in": 0.03,
    "align_max_in": 0.15,
    "max_fonts": 2,
    "max_accents": 1,
    "dense_words": 150,
    "picture_min_frac": 0.08,
}

SEVERITY_WEIGHT = {"high": 3.0, "medium": 1.5, "low": 0.5}
SEVERITY_ORDER = {"high": 0, "medium": 1, "low": 2}

SOURCE_LINE = re.compile(
    r"^\s*(\(?\d\)?\s*)?(sources?|note|notes|footnote|data)\s*[:：]|"
    r"^\s*(출처|자료|주|참고)\s*[:：]|^\s*(出典|出所|注|データ)\s*[:：]", re.IGNORECASE)
SOURCE_ANY = re.compile(r"\bsources?\s*[:：]|출처\s*[:：]|자료\s*[:：]|出典\s*[:：]|出所\s*[:：]|"
                        r"\b(sample|illustrative|hypothetical|dummy) data\b|샘플 데이터|"
                        r"예시 데이터|サンプルデータ", re.IGNORECASE)
PLACEHOLDER_TEXT = re.compile(
    r"\[\s*(data needed|source needed|tbd|tk|todo|placeholder)[^\]]*\]|\bTBD\b|"
    r"\bXX(\.X+)?\s?%|\$X+\b|\bX{3,}\b|lorem ipsum|\?\?\?|click to (add|edit) text|"
    r"\[데이터 ?필요[^\]]*\]|\[データ必要[^\]]*\]", re.IGNORECASE)
SYMBOL_FONTS = {"symbol", "wingdings", "wingdings 2", "wingdings 3", "webdings",
                "marlett", "zapf dingbats", "segoe ui symbol", "segoe ui emoji",
                "apple color emoji"}


# ---------------------------------------------------------------- helpers


def _in(emu):
    return emu / EMU_IN


def _fmt_in(emu):
    return f"{_in(emu):.2f} in"


def _issue(check, severity, message, fix, slide=None, shape=None, bbox=None,
           auto_fix=False, locations=None, **extra):
    d = {
        "check": check,
        "severity": severity,
        "slide": slide,
        "shape_id": shape.get("id") if shape else None,
        "shape": shape.get("name") if shape else None,
        "bbox": list(bbox) if bbox else None,
        "message": message,
        "fix": fix,
        "auto_fix": auto_fix,
    }
    if locations is not None:
        d["locations"] = locations
    d.update(extra)
    return d


def _loc(slide, shape, bbox=None):
    return {"slide": slide["index"], "shape_id": shape.get("id"), "shape": shape.get("name"),
            "bbox": bbox or shape.get("extent") or shape.get("bbox")}


def _area(b):
    return max(0, b[2]) * max(0, b[3]) if b else 0


def _inter(a, b):
    x1, y1 = max(a[0], b[0]), max(a[1], b[1])
    x2, y2 = min(a[0] + a[2], b[0] + b[2]), min(a[1] + a[3], b[1] + b[3])
    if x2 <= x1 or y2 <= y1:
        return None
    return [x1, y1, x2 - x1, y2 - y1]


def _contains(a, b, tol=0):
    return (a[0] - tol <= b[0] and a[1] - tol <= b[1] and
            a[0] + a[2] + tol >= b[0] + b[2] and a[1] + a[3] + tol >= b[1] + b[3])


def _runs(shape):
    if shape["kind"] == "text":
        for p in shape.get("paragraphs", []):
            for r in p["runs"]:
                yield p, r
    elif shape["kind"] == "table":
        for c in shape["table"]["cells"]:
            for r in c.get("runs", []):
                yield None, r


def _is_exhibit_picture(shape, deck, cfg):
    if shape["kind"] != "picture" or not shape.get("bbox"):
        return False
    slide_area = deck["slide_width"] * deck["slide_height"]
    if _area(shape["bbox"]) < cfg["picture_min_frac"] * slide_area:
        return False
    return chart_likeness(shape) is not None


def chart_likeness(shape):
    """Return a reason string if a picture looks like a chart, else None."""
    hint = f"{shape.get('name', '')} {shape.get('alt_text', '')}".lower()
    if re.search(r"\b(chart|graph|plot)\b", hint):
        return "its name or alt text says chart"
    img = shape.get("image") or {}
    if img.get("ext") in ("emf", "wmf"):
        return "it is a vector metafile, the usual format of a chart pasted from Excel"
    f = img.get("features")
    if f and f["colors"] <= 160 and f["light_frac"] >= 0.30 and (f["axis_rows"] or
                                                                 f["axis_cols"]):
        return (f"few flat colors ({f['colors']}), a light background "
                f"({int(f['light_frac'] * 100)}%) and straight axis lines")
    return None


EXHIBIT_KINDS = ("chart", "table", "picture", "diagram", "object")


def is_divider(slide, slide_h=None):
    """Section divider: a 'Section' layout, or a lone big title with little text."""
    if re.search(r"section|divider|섹션|구역|セクション", slide.get("layout") or "", re.I):
        return not any(s["kind"] in ("chart", "table") for s in slide["shapes"])
    if any(s["kind"] in EXHIBIT_KINDS for s in slide["shapes"]):
        return False
    words = sum(len(s["text"].split()) for s in slide["shapes"]
                if s["kind"] == "text" and s.get("role") == "body")
    title = _title_shape(slide)
    low_title = bool(title and title.get("bbox") and slide_h and
                     title["bbox"][1] > 0.25 * slide_h)
    return low_title and words <= 12


def is_content_slide(slide, slide_h=None):
    """True if the slide carries body content or an exhibit (not a cover/divider)."""
    if is_divider(slide, slide_h):
        return False
    for s in slide["shapes"]:
        if s["kind"] in ("chart", "table", "picture", "diagram", "object"):
            return True
        if s["kind"] == "text" and s.get("role") in ("body", "source"):
            return True
    return False


def is_cover(slide):
    """Cover: centered-title placeholder, a 'Title Slide'/'Cover' layout, or a
    first slide with no exhibit and little text besides the title."""
    if any(s.get("placeholder") == "ctrTitle" for s in slide["shapes"]):
        return True
    if re.search(r"title slide|cover|표지|タイトル スライド", slide.get("layout") or "", re.I):
        return True
    if slide["index"] != 1:
        return False
    if any(s["kind"] in ("chart", "table") for s in slide["shapes"]):
        return False
    other = sum(len(s["text"].split()) for s in slide["shapes"]
                if s["kind"] == "text" and s.get("role") != "title")
    return other <= 15


def _title_shape(slide):
    for s in slide["shapes"]:
        if s["id"] == slide.get("title_id") and s.get("role") == "title":
            return s
    return None


# ---------------------------------------------------------------- slide checks


def check_titles(deck, slide, cfg):
    out = []
    idx = slide["index"]
    title = slide.get("title")
    shape = _title_shape(slide)
    content = is_content_slide(slide, deck["slide_height"])
    if is_cover(slide) or slide.get("hidden"):
        return out
    if not title:
        if content:
            out.append(_issue("title_missing", "medium",
                              "Content slide has no title.",
                              "Add an action title: one sentence stating what the slide proves.",
                              slide=idx))
        return out
    bbox = shape.get("bbox") if shape else None
    if content and not T.is_exempt(title):
        verdict = T.classify(title)
        if not verdict["claim"]:
            appendix = idx in cfg.get("_appendix", ())
            out.append(_issue(
                "title_not_claim", "low" if appendix else "medium",
                f"Title \"{title}\" reads like a topic label ({verdict['reason']})"
                + ("; a label is acceptable in the appendix, a claim is better." if appendix
                   else "."),
                "Rewrite as a claim: subject + verb + so-what, e.g. what changed, by how much, "
                "and why it matters.", slide=idx, shape=shape, bbox=bbox,
                title=title))
    words = T.word_count(title)
    cjk = bool(re.search(r"[぀-ヿ一-鿿가-힣]", title))
    lines = shape.get("fit", {}).get("lines") if shape else None
    too_long = []
    if lines and lines > cfg["title_max_lines"]:
        too_long.append(f"wraps to about {lines} lines")
    if not cjk and words > cfg["title_max_words"]:
        too_long.append(f"{words} words")
    limit = cfg["title_max_chars_cjk"] if cjk else cfg["title_max_chars"]
    if len(title) > limit:
        too_long.append(f"{len(title)} characters")
    if too_long:
        out.append(_issue(
            "title_too_long", "medium",
            f"Title is too long: {', '.join(too_long)} (limit: 2 lines, "
            f"{cfg['title_max_words']} words).",
            "Cut the clause the exhibit already shows; keep subject, direction, size.",
            slide=idx, shape=shape, bbox=bbox))
    if shape and content:
        sizes = [r["size_pt"] for _, r in _runs(shape)]
        if sizes and max(sizes) < cfg["title_min_pt"]:
            out.append(_issue(
                "title_font_small", "low",
                f"Title is {max(sizes):g} pt (deck standard: {cfg['title_min_pt']:g} pt or more).",
                "Use the template title size; shorten the title instead of shrinking it.",
                slide=idx, shape=shape, bbox=bbox))
    return out


def check_font_floor(deck, slide, cfg):
    out = []
    idx = slide["index"]
    for s in slide["shapes"]:
        role = s.get("role")
        if s["kind"] == "text" and role in ("body", "source", "subtitle"):
            worst = None
            for p in s.get("paragraphs", []):
                is_src = role == "source" or bool(SOURCE_LINE.match(p["text"]))
                floor = cfg["source_min_pt"] if is_src else cfg["body_min_pt"]
                for r in p["runs"]:
                    if not r["text"].strip():
                        continue
                    if r["size_pt"] < floor - 0.05:
                        if worst is None or r["size_pt"] - floor < worst[0] - worst[1]:
                            worst = (r["size_pt"], floor, "source" if is_src else "body")
            if worst:
                out.append(_issue(
                    "font_below_floor", "medium",
                    f"{worst[2].capitalize()} text at {worst[0]:g} pt in \"{s['name']}\" "
                    f"(floor {worst[1]:g} pt).",
                    f"Raise to {worst[1]:g} pt; if it no longer fits, cut words or split the "
                    "slide.", slide=idx, shape=s, bbox=s.get("bbox"), auto_fix=True,
                    min_pt=worst[0], floor_pt=worst[1]))
        elif s["kind"] == "text" and role in ("footer", "label"):
            sizes = [r["size_pt"] for _, r in _runs(s) if r["text"].strip()]
            if sizes and min(sizes) < cfg["source_min_pt"] - 0.05:
                out.append(_issue(
                    "font_below_floor", "low",
                    f"Footer or label text at {min(sizes):g} pt in \"{s['name']}\" "
                    f"(floor {cfg['source_min_pt']:g} pt).",
                    f"Raise to {cfg['source_min_pt']:g} pt.", slide=idx, shape=s,
                    bbox=s.get("bbox"), auto_fix=True, min_pt=min(sizes),
                    floor_pt=cfg["source_min_pt"]))
        elif s["kind"] == "table":
            sizes = [r["size_pt"] for _, r in _runs(s) if r["text"].strip()]
            if sizes and min(sizes) < cfg["table_min_pt"] - 0.05:
                out.append(_issue(
                    "font_below_floor", "medium",
                    f"Table text at {min(sizes):g} pt (floor {cfg['table_min_pt']:g} pt).",
                    "Raise the table text size; drop columns or rows that do not support the "
                    "title.", slide=idx, shape=s, bbox=s.get("extent"), auto_fix=True,
                    min_pt=min(sizes), floor_pt=cfg["table_min_pt"]))
        elif s["kind"] == "chart":
            mn = (s.get("chart") or {}).get("min_font_pt")
            if mn is not None and mn < cfg["chart_min_pt"] - 0.05:
                out.append(_issue(
                    "font_below_floor", "low",
                    f"Chart text at {mn:g} pt (floor {cfg['chart_min_pt']:g} pt).",
                    "Raise chart labels to 10 pt or more; remove gridlines or labels you "
                    "do not need.", slide=idx, shape=s, bbox=s.get("bbox"),
                    min_pt=mn, floor_pt=cfg["chart_min_pt"]))
    return out


def check_overflow(deck, slide, cfg):
    out = []
    idx = slide["index"]
    for s in slide["shapes"]:
        if s["kind"] != "text" or not s.get("fit") or not s.get("bbox"):
            continue
        if s.get("role") == "footer":
            continue
        fit = s["fit"]
        ratio = fit.get("overflow_ratio") or 0
        box_h = s["bbox"][3]
        need = fit["needed_height"]
        auto = s.get("autofit")
        if auto == "shape":
            if ratio >= cfg["autogrow_ratio"]:
                bottom = s["bbox"][1] + need
                sev = "high" if bottom > deck["slide_height"] else "medium"
                out.append(_issue(
                    "text_overflow", sev,
                    f"Text in \"{s['name']}\" needs about {_fmt_in(need)} but the box was laid "
                    f"out at {_fmt_in(box_h)}; it grows {ratio:.1f}x when shown.",
                    "Cut the text to the planned space, move detail to notes or a backup "
                    "slide, or split the slide.", slide=idx, shape=s,
                    bbox=s["bbox"][:3] + [need], ratio=ratio))
        elif ratio > cfg["overflow_ratio"]:
            sev = "high" if ratio > cfg["overflow_high_ratio"] else "medium"
            if auto == "normal":
                sizes = [r["size_pt"] for _, r in _runs(s)]
                shrunk = (min(sizes) / ratio ** 0.5) if sizes else 0
                floor = cfg["body_min_pt"] if s.get("role") == "body" else 0
                msg = (f"Text in \"{s['name']}\" needs about {ratio:.0%} of the box height; "
                       f"shrink-on-overflow will cut it to roughly {shrunk:.0f} pt.")
                if s.get("role") != "title" and shrunk >= floor:
                    sev = "medium" if sev == "high" else "low"
            else:
                msg = (f"Text in \"{s['name']}\" needs about {_fmt_in(need)} but the box is "
                       f"{_fmt_in(box_h)} ({ratio:.0%}); it will spill out of the box.")
            out.append(_issue(
                "text_overflow", sev, msg,
                "Cut words, widen the box, or split the slide. Do not shrink below the "
                "font floor.", slide=idx, shape=s, bbox=s.get("text_bbox") or s["bbox"],
                ratio=ratio))
        if not fit.get("wrap") and fit["used_width"] > s["bbox"][2] * 1.05:
            out.append(_issue(
                "text_overflow", "medium",
                f"Unwrapped text in \"{s['name']}\" is wider than its box "
                f"({_fmt_in(fit['used_width'])} vs {_fmt_in(s['bbox'][2])}).",
                "Turn on word wrap or widen the box.", slide=idx, shape=s,
                bbox=s.get("text_bbox") or s["bbox"]))
    return out


def check_off_slide(deck, slide, cfg):
    out = []
    idx = slide["index"]
    W, H = deck["slide_width"], deck["slide_height"]
    tol = cfg["edge_tolerance_in"] * EMU_IN
    for s in slide["shapes"]:
        b = s.get("extent") or s.get("bbox")
        if not b or s["kind"] == "placeholder":
            continue
        x, y, w, h = b
        if x >= -tol and y >= -tol and x + w <= W + tol and y + h <= H + tol:
            continue
        fully_out = x >= W or y >= H or x + w <= 0 or y + h <= 0
        if fully_out:
            out.append(_issue(
                "off_slide", "low",
                f"\"{s['name']}\" sits entirely outside the slide; it will not show.",
                "Delete it, or move its content into the speaker notes.",
                slide=idx, shape=s, bbox=None, fully_off=True))
            continue
        sides = []
        if x < -tol:
            sides.append(f"left by {_fmt_in(-x)}")
        if y < -tol:
            sides.append(f"top by {_fmt_in(-y)}")
        if x + w > W + tol:
            sides.append(f"right by {_fmt_in(x + w - W)}")
        if y + h > H + tol:
            sides.append(f"bottom by {_fmt_in(y + h - H)}")
        sev = "high"
        tb = s.get("text_bbox")
        if s["kind"] == "text" and tb and tb[0] >= -tol and tb[1] >= -tol and \
                tb[0] + tb[2] <= W + tol and tb[1] + tb[3] <= H + tol:
            sev = "low"  # the frame sticks out but the text itself is on the slide
        out.append(_issue(
            "off_slide", sev,
            f"\"{s['name']}\" runs off the slide ({', '.join(sides)}).",
            "Move it inside the slide margins.", slide=idx, shape=s,
            bbox=[max(0, x), max(0, y), min(W, x + w) - max(0, x), min(H, y + h) - max(0, y)],
            auto_fix=True))
    return out


def _overlap_items(slide):
    items = []
    for s in slide["shapes"]:
        role = s.get("role")
        if s["kind"] == "text" and role != "footer":
            area = s.get("bbox") if s.get("fill") else (s.get("text_bbox") or s.get("bbox"))
            if area:
                items.append(("text", s, area))
        elif s["kind"] in ("picture", "chart", "table", "diagram", "object"):
            b = s.get("extent") or s.get("bbox")
            if b:
                items.append(("object", s, b))
    return items


def check_overlap(deck, slide, cfg):
    out = []
    idx = slide["index"]
    items = _overlap_items(slide)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            ka, a, ba = items[i]
            kb, b, bb = items[j]
            if a.get("in_group") and b.get("in_group"):
                continue  # grouped shapes are usually composed on purpose
            inter = _inter(ba, bb)
            if not inter:
                continue
            small = min(_area(ba), _area(bb)) or 1
            frac = _area(inter) / small
            if ka == "text" and kb == "text":
                if frac >= cfg["overlap_text_frac"] and inter[2] > 0.03 * EMU_IN and \
                        inter[3] > 0.03 * EMU_IN:
                    out.append(_issue(
                        "overlap", "high",
                        f"Text of \"{a['name']}\" and \"{b['name']}\" overlap "
                        f"({frac:.0%} of the smaller one).",
                        "Move or resize one of them so the text does not collide.",
                        slide=idx, shape=b, bbox=inter, other=a.get("id")))
            elif ka == "object" and kb == "object":
                if frac >= cfg["overlap_object_frac"]:
                    out.append(_issue(
                        "overlap", "medium",
                        f"\"{a['name']}\" and \"{b['name']}\" overlap ({frac:.0%}).",
                        "Give each exhibit its own space.", slide=idx, shape=b, bbox=inter,
                        other=a.get("id")))
            else:
                text, tb = (a, ba) if ka == "text" else (b, bb)
                obj = b if ka == "text" else a
                tfrac = _area(inter) / (_area(tb) or 1)
                if tfrac >= cfg["overlap_label_frac"]:
                    out.append(_issue(
                        "overlap", "low",
                        f"Text \"{text['name']}\" sits on top of {obj['kind']} "
                        f"\"{obj['name']}\".",
                        "Fine if it is a deliberate label; otherwise move it clear.",
                        slide=idx, shape=text, bbox=inter, other=obj.get("id")))
    return out


def check_source(deck, slide, cfg):
    idx = slide["index"]
    exhibits = []
    for s in slide["shapes"]:
        if s["kind"] == "chart":
            exhibits.append(s)
        elif s["kind"] == "table" and s["table"].get("has_numbers"):
            exhibits.append(s)
        elif _is_exhibit_picture(s, deck, cfg):
            exhibits.append(s)
    if not exhibits:
        return []
    for s in slide["shapes"]:
        if s["kind"] == "text" and (SOURCE_ANY.search(s["text"]) or
                                    any(SOURCE_LINE.match(line)
                                        for line in s["text"].splitlines())):
            return []
        if s["kind"] == "table" and SOURCE_ANY.search(s["text"]):
            return []
    kinds = ", ".join(sorted({e["kind"] for e in exhibits}))
    return [_issue(
        "missing_source", "medium",
        f"Exhibit slide ({kinds}) has no source line.",
        "Add 'Source: ...' under the exhibit (10 pt or more). If the numbers are not real, "
        "say 'Sample data'.", slide=idx, shape=exhibits[0],
        bbox=exhibits[0].get("extent") or exhibits[0].get("bbox"), auto_fix=True)]


def check_chart_images(deck, slide, cfg):
    out = []
    slide_area = deck["slide_width"] * deck["slide_height"]
    for s in slide["shapes"]:
        if s["kind"] != "picture" or not s.get("bbox"):
            continue
        if _area(s["bbox"]) < cfg["picture_min_frac"] * slide_area:
            continue
        why = chart_likeness(s)
        if why:
            out.append(_issue(
                "chart_as_image", "medium",
                f"\"{s['name']}\" looks like a chart pasted as a picture ({why}).",
                "Rebuild it as a native chart so the numbers stay editable and text stays "
                "sharp.", slide=slide["index"], shape=s, bbox=s["bbox"]))
    return out


def check_placeholder_text(deck, slide, cfg):
    out = []
    for s in slide["shapes"]:
        if s["kind"] not in ("text", "table"):
            continue
        hits = sorted({m.group(0).strip() for m in PLACEHOLDER_TEXT.finditer(s["text"])})
        if hits:
            out.append(_issue(
                "data_needed", "high",
                f"Unfinished content in \"{s['name']}\": {', '.join(hits[:3])}.",
                "Fill in the real figure and its source, or cut the claim that needs it.",
                slide=slide["index"], shape=s,
                bbox=s.get("text_bbox") if s["kind"] == "text" else s.get("extent"),
                markers=hits))
    return out


def check_empty_placeholders(deck, slide, cfg):
    empty = [s for s in slide["shapes"] if s.get("empty_placeholder")]
    if not empty:
        return []
    names = ", ".join(f"\"{s['name']}\"" for s in empty[:4])
    n = len(empty)
    return [_issue(
        "empty_placeholder", "low",
        f"{n} empty placeholder{'s' if n > 1 else ''} ({names}) show 'Click to add text' "
        "while editing.", "Delete or fill them.", slide=slide["index"], shape=empty[0],
        bbox=empty[0].get("bbox"),
        locations=[_loc(slide, s, s.get("bbox")) for s in empty[1:]])]


def check_density(deck, slide, cfg):
    if slide["words"] > cfg["dense_words"]:
        return [_issue(
            "dense_slide", "low",
            f"{slide['words']} words on one slide (guide: {cfg['dense_words']} or fewer).",
            "Keep the words that prove the title; move the rest to notes or backup.",
            slide=slide["index"])]
    return []


def _edge(b, name):
    return {"left": b[0], "right": b[0] + b[2], "top": b[1]}[name]


def check_alignment(deck, slide, cfg):
    """Near-miss edges: two shapes that almost, but not quite, line up.

    For each pair, the shape whose edge position is rarer on the slide is the
    outlier; it gets one issue per edge, pointing at the shape to snap to.
    """
    lo, hi = cfg["align_min_in"] * EMU_IN, cfg["align_max_in"] * EMU_IN
    items = [s for s in slide["shapes"]
             if s.get("bbox") and not s.get("in_group") and
             (s["kind"] in ("picture", "chart", "table") or
              (s["kind"] == "text" and s.get("role") in ("title", "body", "source",
                                                         "subtitle")))]
    wide = 0.25 * deck["slide_width"]
    counts = {e: Counter(round(_edge(s["bbox"], e) / 9144) for s in items)
              for e in ("left", "right", "top")}
    found = {}  # (outlier id, edge) -> (outlier, anchor, delta)
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            ba, bb = a["bbox"], b["bbox"]
            if _contains(ba, bb) or _contains(bb, ba):
                continue  # padding inside a container is deliberate
            v_overlap = min(ba[1] + ba[3], bb[1] + bb[3]) - max(ba[1], bb[1])
            for edge in ("left", "right", "top"):
                if edge == "right" and (ba[2] < wide or bb[2] < wide):
                    continue
                if edge == "top" and v_overlap <= 0:
                    continue
                d = abs(_edge(ba, edge) - _edge(bb, edge))
                if not lo < d <= hi:
                    continue
                ca = counts[edge][round(_edge(ba, edge) / 9144)]
                cb = counts[edge][round(_edge(bb, edge) / 9144)]
                outlier, anchor = (a, b) if ca < cb else (b, a)
                if a.get("role") == "title" and ca == cb:
                    outlier, anchor = b, a
                found.setdefault((outlier["id"], edge), (outlier, anchor, d))
    out = []
    for (_, edge), (o, a, d) in found.items():
        bo, ba = o["bbox"], a["bbox"]
        x1, y1 = min(bo[0], ba[0]), min(bo[1], ba[1])
        x2 = max(bo[0] + bo[2], ba[0] + ba[2])
        y2 = max(bo[1] + bo[3], ba[1] + ba[3])
        out.append(_issue(
            "misaligned", "low",
            f"\"{o['name']}\" is {_fmt_in(d)} off the {edge} edge of \"{a['name']}\".",
            "Snap it to the same edge.", slide=slide["index"], shape=o,
            bbox=[x1, y1, x2 - x1, y2 - y1], auto_fix=True, anchor_id=a["id"], edge=edge))
    return out


SLIDE_CHECKS = [check_titles, check_font_floor, check_overflow, check_off_slide,
                check_overlap, check_source, check_chart_images, check_placeholder_text,
                check_empty_placeholders, check_density, check_alignment]


# ---------------------------------------------------------------- deck checks


def check_fonts(deck, cfg):
    usage = Counter()
    where = defaultdict(list)
    for slide in deck["slides"]:
        for s in slide["shapes"]:
            used = set()
            for _, r in _runs(s):
                f = (r.get("font") or "").strip()
                if not f or not r["text"].strip() or f.lower() in SYMBOL_FONTS:
                    continue
                usage[f] += len(r["text"])
                used.add(f)
            for f in used:
                where[f].append(_loc(slide, s))
    if len(usage) <= cfg["max_fonts"]:
        return []
    keep = [f for f, _ in usage.most_common(cfg["max_fonts"])]
    extra = [f for f in usage if f not in keep]
    locs = [loc for f in extra for loc in where[f]]
    return [_issue(
        "font_count", "medium",
        f"Deck uses {len(usage)} fonts: {', '.join(f for f, _ in usage.most_common())} "
        f"(limit {cfg['max_fonts']}).",
        f"Use the theme fonts only; change {', '.join(extra)} to {keep[0]}.",
        locations=locs, fonts=dict(usage))]


def _hue_family(rgb):
    try:
        r, g, b = (int(rgb[i:i + 2], 16) / 255 for i in (0, 2, 4))
    except (ValueError, TypeError):
        return None
    h, s, v = colorsys.rgb_to_hsv(r, g, b)
    if s < 0.25 or v < 0.25:
        return None  # black, white, gray: not an accent
    return h * 360


def check_colors(deck, cfg):
    samples = []  # (hue, rgb, location)
    theme_colors = (deck.get("theme") or {}).get("colors", {})
    for slide in deck["slides"]:
        for s in slide["shapes"]:
            colors = set()
            for _, r in _runs(s):
                if r.get("color") and r["text"].strip():
                    colors.add(r["color"])
            if s.get("fill") and s["kind"] in ("text", "shape"):
                colors.add(s["fill"])
            if s["kind"] == "table":
                colors.update(s["table"].get("fills", []))
            if s["kind"] == "chart":
                ch = s.get("chart") or {}
                series = ch.get("series", [])
                for k, ser in enumerate(series):
                    if ser.get("color"):
                        colors.add(ser["color"])
                    elif len(series) > 1:
                        auto = theme_colors.get(f"accent{k % 6 + 1}")
                        if auto:
                            colors.add(auto)
                    colors.update(ser.get("point_colors", []))
            for c in colors:
                hue = _hue_family(c)
                if hue is not None:
                    samples.append((hue, c, _loc(slide, s)))
    if not samples:
        return []
    weights = Counter()
    for hue, _, _ in samples:
        weights[int(hue // 10)] += 1
    families = []  # [center_hue, [samples]]
    for hue, c, loc in sorted(samples, key=lambda t: -weights[int(t[0] // 10)]):
        for fam in families:
            d = abs(fam[0] - hue)
            if min(d, 360 - d) <= 25:
                fam[1].append((c, loc))
                break
        else:
            families.append([hue, [(c, loc)]])
    if len(families) <= cfg["max_accents"]:
        return []
    families.sort(key=lambda f: -len(f[1]))
    main = families[0]
    others = families[1:]
    locs = [loc for fam in others for _, loc in fam[1]]
    names = [f"#{fam[1][0][0]}" for fam in families]
    sev = "medium" if len(families) > 2 else "low"
    return [_issue(
        "accent_colors", sev,
        f"{len(families)} accent hues in use ({', '.join(names)}); the rule is one accent "
        f"plus grays.",
        f"Keep #{main[1][0][0]} for the one thing to notice; turn the rest gray.",
        locations=locs, families=names)]


def check_duplicate_titles(deck, cfg):
    out = []
    seen = []
    for slide in deck["slides"]:
        t = slide.get("title")
        if not t or is_cover(slide) or T.is_exempt(t):
            continue
        norm = re.sub(r"\(cont(inued|'d|\.)?\)", "", t.lower())
        toks = set(re.findall(r"\w+", norm))
        for prev_idx, prev_toks, prev_title in seen:
            if not toks or not prev_toks:
                continue
            jac = len(toks & prev_toks) / len(toks | prev_toks)
            if toks == prev_toks or (len(toks) >= 4 and jac >= 0.8):
                out.append(_issue(
                    "duplicate_title", "medium",
                    f"Title repeats slide {prev_idx}: \"{prev_title}\".",
                    "Each slide should make its own point; merge the slides or sharpen "
                    "one title.", slide=slide["index"],
                    shape=_title_shape(slide),
                    bbox=(_title_shape(slide) or {}).get("bbox"), other_slide=prev_idx))
                break
        seen.append((slide["index"], toks, t))
    return out


def check_title_position(deck, cfg):
    pos = {}
    for slide in deck["slides"]:
        s = _title_shape(slide)
        if (is_cover(slide) or not s or not s.get("bbox")
                or not is_content_slide(slide, deck["slide_height"])):
            continue
        pos[slide["index"]] = (s, (round(s["bbox"][0] / 9144), round(s["bbox"][1] / 9144)))
    if len(pos) < 3:
        return []
    mode, n = Counter(p for _, p in pos.values()).most_common(1)[0]
    if n < 2:
        return []
    out = []
    for idx, (s, p) in pos.items():
        dx, dy = abs(p[0] - mode[0]) / 100, abs(p[1] - mode[1]) / 100
        if (cfg["align_min_in"] < dx < 1.0 or cfg["align_min_in"] < dy < 1.0):
            out.append(_issue(
                "title_position", "low",
                f"Title sits {dx:.2f} in / {dy:.2f} in away from where most slides put it; "
                "it jumps when you flip slides.",
                "Use the layout's title placeholder position.", slide=idx, shape=s,
                bbox=s["bbox"]))
    return out


DECK_CHECKS = [check_fonts, check_colors, check_duplicate_titles, check_title_position]


# ---------------------------------------------------------------- entry points


APPENDIX = re.compile(r"^\s*(appendix|appendices|backup|부록|付録)\b", re.IGNORECASE)


def appendix_slides(deck) -> set[int]:
    """Slides after an 'Appendix' divider, or whose tracker/label says Appendix."""
    out, inside = set(), False
    for slide in deck["slides"]:
        if APPENDIX.match(slide.get("title") or ""):
            inside = True
            out.add(slide["index"])
            continue
        tagged = any(s["kind"] == "text" and s.get("role") in ("label", "footer") and
                     APPENDIX.match(s["text"]) for s in slide["shapes"])
        if inside or tagged:
            out.add(slide["index"])
    return out


def run_checks(deck: dict, config: dict | None = None) -> list[dict]:
    """Run every check. Returns issues sorted by slide, then severity."""
    cfg = dict(DEFAULTS)
    if config:
        cfg.update(config)
    cfg["_appendix"] = appendix_slides(deck)
    issues = []
    for slide in deck["slides"]:
        for fn in SLIDE_CHECKS:
            issues.extend(fn(deck, slide, cfg))
    for fn in DECK_CHECKS:
        issues.extend(fn(deck, cfg))
    issues.sort(key=lambda i: (i["slide"] if i["slide"] is not None else 10 ** 6,
                               SEVERITY_ORDER[i["severity"]]))
    return issues


def slide_scores(deck: dict, issues: list[dict]) -> dict[int, float]:
    """Mechanical score per slide, 0-10: 10 minus weighted issues on that slide.

    Deck-level issues count on each slide they point to.
    """
    penalty = defaultdict(float)
    for i in issues:
        w = SEVERITY_WEIGHT[i["severity"]]
        if i["slide"] is not None:
            penalty[i["slide"]] += w
        else:
            for s in {loc["slide"] for loc in i.get("locations", [])}:
                penalty[s] += w / 2
    return {s["index"]: max(0.0, round(10 - penalty[s["index"]], 1)) for s in deck["slides"]}
