"""Command line entry points used by scripts/build.py and scripts/render.py."""
from __future__ import annotations

import argparse
import json
import pathlib
import sys

from pptx import Presentation

from . import checks, render as renderer, spec as deckspec
from .build import build_deck
from .template_map import TemplateError, open_template


def build_main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="build.py", description="Build an editable .pptx from a deck spec JSON.")
    ap.add_argument("spec", nargs="?", help="deck spec JSON (see references/deck-spec.schema.json)")
    ap.add_argument("-o", "--out", help="output folder (default: out/<spec name>/ next to the spec)")
    ap.add_argument("--template", help="your .pptx or .potx template (overrides spec.template.path)")
    ap.add_argument("--name", default="deck", help="file name for deck.pptx/deck.pdf (default: deck)")
    ap.add_argument("--no-render", action="store_true", help="skip the LibreOffice PDF/PNG preview")
    ap.add_argument("--strict", action="store_true", help="exit 3 if any text overflows or a check fails")
    ap.add_argument("--check-only", action="store_true", help="validate the spec and stop")
    ap.add_argument("--export-template", metavar="PATH", help="write the built-in default template and stop")
    args = ap.parse_args(argv)

    if args.export_template:
        tpl = open_template(None)
        tpl.prs.save(args.export_template)
        print(f"wrote default template to {args.export_template}")
        return 0
    if not args.spec:
        ap.error("a spec file is required")

    spec_path = pathlib.Path(args.spec)
    try:
        spec = deckspec.load(spec_path)
    except FileNotFoundError:
        print(f"error: spec not found: {spec_path}", file=sys.stderr)
        return 2
    except deckspec.SpecError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    if args.check_only:
        print(f"spec OK: {len(spec['slides'])} slides")
        return 0

    spec_dir = spec_path.resolve().parent
    out = pathlib.Path(args.out) if args.out else spec_dir / "out" / spec_path.stem
    out.mkdir(parents=True, exist_ok=True)
    try:
        prs, report = build_deck(spec, template=args.template, base_dir=spec_dir)
    except TemplateError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    pptx = out / f"{args.name}.pptx"
    prs.save(pptx)
    issues = checks.inspect(Presentation(pptx))  # check the saved file, as the user will open it
    data = report.as_dict()
    data["checks"] = [str(i) for i in issues]
    (out / "build-report.json").write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

    print(f"built {pptx} ({len(spec['slides'])} slides)")
    for o in report.overflows:
        print(f"  overflow: slide {o['slide']} {o['role']} at {o['size']}pt: {o['text']!r}")
    for i in issues:
        print(f"  check: {i}")
    if not report.overflows and not issues:
        print("  checks passed: no overflow, nothing off-slide, type sizes at or above the floors")

    if not args.no_render:
        try:
            result = renderer.render(pptx, out)
        except Exception as exc:  # a broken LibreOffice install must not lose the built deck
            print(f"  render failed: {exc}", file=sys.stderr)
        else:
            if result.pdf:
                print(f"  pdf: {result.pdf}")
            if result.pngs:
                print(f"  previews: {result.pngs[0].parent}/ ({len(result.pngs)} png)")
            print(f"  {result.message}")
    if args.strict and (report.overflows or issues):
        return 3
    return 0


def render_main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="render.py", description="Render a .pptx to PDF and PNG previews.")
    ap.add_argument("pptx")
    ap.add_argument("-o", "--out", help="output folder (default: next to the pptx)")
    ap.add_argument("--width", type=int, default=1600, help="PNG width in pixels")
    args = ap.parse_args(argv)
    pptx = pathlib.Path(args.pptx)
    if not pptx.is_file():
        print(f"error: not found: {pptx}", file=sys.stderr)
        return 2
    out = pathlib.Path(args.out) if args.out else pptx.parent
    result = renderer.render(pptx, out, width=args.width)
    if result.pdf:
        print(f"pdf: {result.pdf}")
    for p in result.pngs:
        print(p)
    print(result.message)
    return 0 if result.pdf else 1
