#!/usr/bin/env python3
"""deck-review command line. Works on any .pptx.

  python review.py run DECK.pptx [--out DIR] [--no-render] [--no-fix]
                                 [--soffice PATH] [--width PX]
      Everything: inspect, check, render, annotate, safe-fix, write review.md.
      Default DIR: <deck folder>/<deck name>-review/

  python review.py inspect DECK.pptx   structured JSON of the deck (stdout)
  python review.py check DECK.pptx     automatic issues as JSON (stdout)
  python review.py render DECK.pptx [--out DIR] [--soffice PATH] [--width PX]
  python review.py fix DECK.pptx [--out FILE]    safe fixes -> DECK.fixed.pptx

Needs python-pptx. Rendering also needs LibreOffice, pypdfium2 and Pillow; the
review runs without them and says how to install them. No network access.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from deckreview import checks as C  # noqa: E402
from deckreview.inspect import inspect_pptx  # noqa: E402


def _json_default(o):
    if isinstance(o, Path):
        return str(o)
    raise TypeError(type(o).__name__)


def _load(deck_path: Path):
    if not deck_path.is_file():
        raise SystemExit(_fail(f"No such file: {deck_path}"))
    try:
        return inspect_pptx(deck_path)
    except Exception as exc:  # corrupt zip, .ppt binary, macro deck, ...
        raise SystemExit(_fail(f"Could not open {deck_path.name} as a .pptx ({exc}). "
                               "Old .ppt files must be saved as .pptx first."))


def _fail(msg: str) -> int:
    print(f"deck-review: {msg}", file=sys.stderr)
    return 2


def _number(issues):
    for n, i in enumerate(issues, start=1):
        i["n"] = n
    return issues


def _visible_map(deck, pngs):
    """Map rendered page PNGs to slide numbers (LibreOffice skips hidden slides)."""
    slides = [s["index"] for s in deck["slides"]]
    visible = [s["index"] for s in deck["slides"] if not s.get("hidden")]
    order = visible if len(pngs) == len(visible) else slides
    return dict(zip(order, pngs))


def cmd_inspect(args):
    deck = _load(Path(args.deck))
    json.dump(deck, sys.stdout, ensure_ascii=False, indent=None if args.compact else 1)
    print()
    return 0


def cmd_check(args):
    deck = _load(Path(args.deck))
    issues = _number(C.run_checks(deck))
    json.dump({"file": deck["file"], "issues": issues,
               "scores": C.slide_scores(deck, issues)}, sys.stdout, ensure_ascii=False,
              indent=1)
    print()
    return 0


def cmd_render(args):
    from deckreview.render import render_pptx

    deck_path = Path(args.deck)
    out = Path(args.out) if args.out else deck_path.with_name(deck_path.stem + "-render")
    res = render_pptx(deck_path, out, soffice=args.soffice, width_px=args.width)
    if res["error"]:
        print(res["error"], file=sys.stderr)
    if res["pdf"]:
        print(f"PDF: {res['pdf']}\nPNGs: {len(res['pngs'])} in {out}")
    return 0 if res["pdf"] else 1


def cmd_fix(args):
    from deckreview.fix import fix_pptx

    deck_path = Path(args.deck)
    _load(deck_path)
    dst = Path(args.out) if args.out else deck_path.with_name(deck_path.stem + ".fixed.pptx")
    fixes = fix_pptx(deck_path, dst)
    for f in fixes:
        print(f"slide {f['slide']}: {f['check']}: {f['shape']}: {f['action']}")
    print(f"Wrote {dst} ({sum(1 for f in fixes if f['ok'])} fixes)")
    return 0


def cmd_run(args):
    from deckreview.report import build_markdown

    deck_path = Path(args.deck)
    deck = _load(deck_path)
    out = Path(args.out) if args.out else deck_path.with_name(deck_path.stem + "-review")
    out.mkdir(parents=True, exist_ok=True)
    issues = _number(C.run_checks(deck))
    scores = C.slide_scores(deck, issues)

    for sub in ("render", "annotated"):  # drop pages left from an earlier run
        for old in (out / sub).glob("slide-[0-9]*.png"):
            old.unlink()
    render = None
    annotated = {}
    if not args.no_render:
        from deckreview.render import render_pptx

        render = render_pptx(deck_path, out / "render", soffice=args.soffice,
                             width_px=args.width)
        if render["pngs"]:
            try:
                from deckreview.annotate import annotate

                pngs = _visible_map(deck, render["pngs"])
                for p in annotate(pngs, issues, deck, out / "annotated"):
                    idx = next(k for k, v in pngs.items() if v.name == p.name)
                    annotated[idx] = f"annotated/{p.name}"
            except ImportError:
                render["error"] = "Annotation needs Pillow: pip install pillow"

    fixes, after, fixed_name = None, None, None
    if not args.no_fix:
        from deckreview.fix import fix_pptx

        fixed = out / (deck_path.stem + ".fixed.pptx")
        fixes = fix_pptx(deck_path, fixed, issues=issues)
        after = C.run_checks(inspect_pptx(fixed))
        fixed_name = fixed.name

    md = build_markdown(deck, issues, scores, fixes=fixes, after=after, render=render,
                        annotated=annotated, fixed_name=fixed_name,
                        generated=_dt.date.today().isoformat())
    (out / "review.md").write_text(md, encoding="utf-8")
    summary = {
        "file": deck["file"],
        "slides": [{"index": s["index"], "title": s.get("title"), "hidden": s.get("hidden"),
                    "score": scores.get(s["index"])} for s in deck["slides"]],
        "issues": issues,
        "fixes": fixes,
        "issues_after_fix": after,
        "render_error": (render or {}).get("error"),
        "annotated": annotated,
    }
    (out / "review.json").write_text(json.dumps(summary, ensure_ascii=False, indent=1,
                                                default=_json_default), encoding="utf-8")
    (out / "inspect.json").write_text(json.dumps(deck, ensure_ascii=False),
                                      encoding="utf-8")

    sev = {s: sum(1 for i in issues if i["severity"] == s) for s in ("high", "medium", "low")}
    print(f"Reviewed {deck['file']}: {len(deck['slides'])} slides, {sev['high']} high, "
          f"{sev['medium']} medium, {sev['low']} low issues.")
    print(f"Report:    {out / 'review.md'}")
    if annotated:
        print(f"Annotated: {out / 'annotated'} ({len(annotated)} slides)")
    if fixed_name:
        print(f"Fixed:     {out / fixed_name} ({sum(1 for f in fixes if f['ok'])} safe fixes, "
              f"{len(after)} issues left)")
    if render and render.get("error"):
        print(render["error"], file=sys.stderr)
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(prog="review.py", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("run", help="full review: report, annotated PNGs, fixed deck")
    p.add_argument("deck")
    p.add_argument("--out", help="output folder (default: <deck>-review next to the deck)")
    p.add_argument("--no-render", action="store_true", help="skip LibreOffice rendering")
    p.add_argument("--no-fix", action="store_true", help="do not write a fixed copy")
    p.add_argument("--soffice", help="path to the LibreOffice soffice binary")
    p.add_argument("--width", type=int, default=1600, help="PNG width in pixels")
    p.set_defaults(func=cmd_run)

    p = sub.add_parser("inspect", help="print the deck structure as JSON")
    p.add_argument("deck")
    p.add_argument("--compact", action="store_true")
    p.set_defaults(func=cmd_inspect)

    p = sub.add_parser("check", help="print automatic issues as JSON")
    p.add_argument("deck")
    p.set_defaults(func=cmd_check)

    p = sub.add_parser("render", help="render to PDF and PNGs")
    p.add_argument("deck")
    p.add_argument("--out")
    p.add_argument("--soffice")
    p.add_argument("--width", type=int, default=1600)
    p.set_defaults(func=cmd_render)

    p = sub.add_parser("fix", help="write a copy with safe fixes")
    p.add_argument("deck")
    p.add_argument("--out", help="output .pptx (default: <deck>.fixed.pptx)")
    p.set_defaults(func=cmd_fix)

    args = ap.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
