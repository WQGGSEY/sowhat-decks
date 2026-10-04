"""Write review.md from the inspection, issues, fixes and render results.

The script fills everything it can measure. Sections marked "(agent)" are left
for the agent to complete with references/rubric.md: story score per slide,
rewritten titles, so-what notes, duplication and gaps, evidence.
"""

from __future__ import annotations

from collections import OrderedDict

from . import titles as T
from .checks import SEVERITY_ORDER, is_content_slide, is_cover

HEADLINES = {
    "data_needed": ("Unfinished figures or sources",
                    "Fill in the real number and its source, or cut the claim that needs it."),
    "text_overflow": ("Text spills out of its box",
                      "Cut words, move detail to notes, or split the slide. Do not shrink "
                      "below the font floor."),
    "overlap": ("Text or exhibits collide", "Move or resize so nothing sits on top of text."),
    "off_slide": ("Shapes run off the slide", "Move them inside the margins."),
    "title_missing": ("Content slides without a title",
                      "Add a one-sentence action title to each."),
    "title_not_claim": ("Titles that may be topic labels (heuristic; confirm by reading)",
                        "Rewrite each as one sentence that states what the slide proves "
                        "(see Rewritten titles)."),
    "title_too_long": ("Titles longer than two lines",
                       "Cut the clause the exhibit already shows."),
    "duplicate_title": ("Slides repeat the same point", "Merge them or sharpen one title."),
    "missing_source": ("Exhibits without a source line",
                       "Add 'Source: ...' under each chart or table (10 pt or more)."),
    "chart_as_image": ("Charts pasted as pictures",
                       "Rebuild them as native charts so the data stays editable."),
    "font_below_floor": ("Text below the size floor",
                         "Body 12 pt, sources and tables 10 pt at least."),
    "font_count": ("Too many fonts", "Use the two theme fonts only."),
    "accent_colors": ("Too many accent colors",
                      "One accent for the thing to notice; everything else gray."),
    "title_font_small": ("Small titles", "Use the template title size."),
    "misaligned": ("Edges that almost line up", "Snap them to a shared edge."),
    "title_position": ("Titles jump between slides",
                       "Put every title in the layout's title position."),
    "dense_slide": ("Dense slides", "Keep only the words that prove the title."),
    "empty_placeholder": ("Empty placeholders", "Delete or fill them."),
}


def _cell(text, limit=90):
    t = " ".join(str(text or "").split()).replace("|", "\\|")
    return t if len(t) <= limit else t[: limit - 1] + "…"


def _slides_of(issue):
    if issue.get("slide") is not None:
        return [issue["slide"]]
    return sorted({loc["slide"] for loc in issue.get("locations", [])})


def top_fixes(issues, fixed_keys=frozenset(), limit=5):
    """Group issues by check; rank by worst severity, then how often it occurs."""
    groups = OrderedDict()
    for i in issues:
        g = groups.setdefault(i["check"], {"check": i["check"], "issues": [],
                                            "severity": i["severity"]})
        g["issues"].append(i)
        if SEVERITY_ORDER[i["severity"]] < SEVERITY_ORDER[g["severity"]]:
            g["severity"] = i["severity"]
    ranked = sorted(groups.values(),
                    key=lambda g: (SEVERITY_ORDER[g["severity"]], -len(g["issues"])))
    out = []
    for g in ranked[:limit]:
        head, action = HEADLINES.get(g["check"], (g["check"], g["issues"][0]["fix"]))
        slides = sorted({s for i in g["issues"] for s in _slides_of(i)})
        nums = [f"#{i['n']}" for i in g["issues"]]
        auto = all((i["check"], i.get("slide"), i.get("shape_id")) in fixed_keys
                   for i in g["issues"])
        out.append({"check": g["check"], "severity": g["severity"], "headline": head,
                    "action": action, "slides": slides, "refs": nums, "auto_fixed": auto})
    return out


def build_markdown(deck, issues, scores, *, fixes=None, after=None, render=None,
                   annotated=None, fixed_name=None, generated=None):
    fixes = fixes or []
    annotated = annotated or {}
    sev_count = {s: sum(1 for i in issues if i["severity"] == s) for s in
                 ("high", "medium", "low")}
    mean = sum(scores.values()) / len(scores) if scores else 0
    fixed_keys = {(f["check"], f["slide"], f.get("shape_id")) for f in fixes if f.get("ok")}
    L = []
    L.append(f"# Deck review: {deck['file']}")
    L.append("")
    L.append(f"Automatic checks by deck-review{(' on ' + generated) if generated else ''}. "
             "Sections marked *(agent)* are completed by the agent with "
             "`references/rubric.md`.")
    L.append("")
    L.append(f"- **Slides:** {len(deck['slides'])}")
    L.append(f"- **Issues:** {sev_count['high']} high, {sev_count['medium']} medium, "
             f"{sev_count['low']} low")
    L.append(f"- **Mechanical score:** {mean:.1f}/10 (mean of slides; story score is the "
             "agent's)")
    if render is not None:
        if render.get("pdf"):
            L.append(f"- **Rendered:** `render/{render['pdf'].name}`, "
                     f"{len(render.get('pngs', []))} PNGs; problems boxed in `annotated/`")
        if render.get("error"):
            L.append(f"- **Rendering:** {render['error'].splitlines()[0]} "
                     "(see the console for install steps)")
    if fixed_name:
        ok = [f for f in fixes if f.get("ok")]
        L.append(f"- **Fixed copy:** `{fixed_name}` with {len(ok)} safe fixes; "
                 f"{len(after or [])} issues remain in it")
    if deck.get("warnings"):
        L.append(f"- **Read warnings:** {'; '.join(deck['warnings'][:3])}")
    L.append("")

    # Top fixes
    L.append("## Top 5 fixes")
    L.append("")
    tops = top_fixes(issues, fixed_keys)
    if not tops:
        L.append("No automatic findings. Do the rubric review below.")
    for k, t in enumerate(tops, 1):
        where = ", ".join(str(s) for s in t["slides"]) or "deck"
        auto = " *(fixed automatically in the fixed copy)*" if t["auto_fixed"] else ""
        L.append(f"{k}. **[{t['severity']}] {t['headline']}** — slide{'s' if len(t['slides']) != 1 else ''} "
                 f"{where} ({', '.join(t['refs'][:6])}{', …' if len(t['refs']) > 6 else ''}). "
                 f"{t['action']}{auto}")
    L.append("")
    L.append("*(agent)* Re-rank after the rubric review: a weak storyline or unsupported "
             "claim outranks any formatting problem.")
    L.append("")

    # Title read-through
    L.append("## Title read-through")
    L.append("")
    L.append("Read only the titles, top to bottom. Do they tell the whole story? The "
             "claim/label verdicts are rule-based guesses; *(agent)* your reading decides.")
    L.append("")
    L.append("| Slide | Title | Verdict |")
    L.append("|---|---|---|")
    rewrite = []
    for s in deck["slides"]:
        t = s.get("title")
        if s.get("hidden"):
            verdict = "hidden slide"
        elif is_cover(s):
            verdict = "cover"
        elif not t:
            verdict = "**no title**"
        elif T.is_exempt(t):
            verdict = "agenda/appendix/closing"
        elif not is_content_slide(s, deck["slide_height"]):
            verdict = "section divider" + ("" if T.classify(t)["claim"] else " (label)")
        else:
            c = T.classify(t)
            verdict = "claim" if c["claim"] else f"**label?** ({c['reason']})"
            long_ = any(i["check"] == "title_too_long" and i["slide"] == s["index"]
                        for i in issues)
            if long_:
                verdict += ", **too long**"
            if not c["claim"] or long_:
                rewrite.append(s)
        L.append(f"| {s['index']} | {_cell(t or '—', 110)} | {verdict} |")
    L.append("")
    paragraph = " ".join((s.get("title") or "").strip().rstrip(".") + "." for s in deck["slides"]
                         if s.get("title") and not s.get("hidden"))
    L.append(f"As one paragraph: {_cell(paragraph, 2000)}")
    L.append("")

    # Rewritten titles
    L.append("## Rewritten titles")
    L.append("")
    if rewrite:
        L.append("*(agent)* Write a claim the slide's own content proves. Never invent a "
                 "number: use `[DATA NEEDED: ...]` when it is missing.")
        L.append("")
        L.append("| Slide | Current | Proposed |")
        L.append("|---|---|---|")
        for s in rewrite:
            L.append(f"| {s['index']} | {_cell(s.get('title') or '—')} | *(agent)* |")
    else:
        L.append("No title failed the automatic claim and length checks. *(agent)* Still "
                 "check that each claim is specific and supported.")
    L.append("")

    # Slide by slide
    L.append("## Slide by slide")
    L.append("")
    L.append("| Slide | Title | Mechanical (0-10) | Story (0-10) *(agent)* | Issues |")
    L.append("|---|---|---|---|---|")
    for s in deck["slides"]:
        refs = [f"#{i['n']}" for i in issues if s["index"] in _slides_of(i)]
        L.append(f"| {s['index']} | {_cell(s.get('title') or '—', 60)} | "
                 f"{scores.get(s['index'], 10):.1f} |  | {', '.join(refs) or '—'} |")
    L.append("")
    for s in deck["slides"]:
        own = [i for i in issues if i.get("slide") == s["index"]]
        L.append(f"### Slide {s['index']}: {_cell(s.get('title') or '(no title)', 100)}")
        L.append("")
        if s["index"] in annotated:
            L.append(f"![slide {s['index']}]({annotated[s['index']]})")
            L.append("")
        for i in own:
            L.append(f"- **#{i['n']} [{i['severity']}] {i['check']}**: {i['message']} "
                     f"Fix: {i['fix']}")
        if not own:
            L.append("- No automatic findings.")
        L.append("- *(agent)* So what? One line: what must the reader take from this slide, "
                 "and does the body prove it?")
        L.append("")

    deck_issues = [i for i in issues if i.get("slide") is None]
    if deck_issues:
        L.append("## Deck-level findings")
        L.append("")
        for i in deck_issues:
            where = ", ".join(str(x) for x in _slides_of(i))
            L.append(f"- **#{i['n']} [{i['severity']}] {i['check']}**: {i['message']} "
                     f"Slides: {where or '—'}. Fix: {i['fix']}")
        L.append("")

    # Fixes
    if fixed_name is not None:
        L.append("## Automatic fixes")
        L.append("")
        L.append(f"`{fixed_name}` changes layout and size only. Words, numbers, chart data "
                 "and slide order are unchanged. Any `[SOURCE NEEDED]` line it adds must be "
                 "replaced with the real source.")
        L.append("")
        if fixes:
            L.append("| Slide | Shape | Check | Change |")
            L.append("|---|---|---|---|")
            for f in fixes:
                L.append(f"| {f['slide']} | {_cell(f.get('shape'), 40)} | {f['check']} | "
                         f"{_cell(f['action'], 100)} |")
        else:
            L.append("Nothing needed a safe automatic fix.")
        L.append("")
        if after is not None:
            left = OrderedDict()
            for i in after:
                left.setdefault(i["check"], []).append(i)
            summary = ", ".join(f"{k} ×{len(v)}" for k, v in left.items()) or "none"
            L.append(f"Left in the fixed copy (need a person): {summary}.")
            L.append("")

    # Rubric placeholders
    markers = sorted({m for i in issues if i["check"] == "data_needed"
                      for m in i.get("markers", [])})
    L.append("## Rubric review *(agent)*")
    L.append("")
    L.append("- **Governing message** (from the titles alone): ")
    L.append("- **Storyline:** does each title follow from the one before? Where does it jump?")
    L.append("- **Duplication and gaps:** which slides repeat a point; which key argument has "
             "no slide?")
    L.append("- **Evidence:** which claims lack a number, a comparison or a source?")
    L.append(f"- **[DATA NEEDED] and placeholders found:** "
             f"{', '.join(markers) if markers else 'none found automatically'}")
    L.append("- **Verdict:** ready / ready after the top fixes / needs a storyline rework")
    L.append("")
    return "\n".join(L)
