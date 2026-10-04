"""Spec -> python-pptx Presentation."""
from __future__ import annotations

import pathlib

from . import layouts, spec as deckspec
from .draw import Ctx, chrome, finish, keep_placeholders, notes
from .template_map import TITLE_TYPES, open_template
from .text import Report


def build_deck(spec: dict, template: str | pathlib.Path | None = None,
               base_dir: str | pathlib.Path | None = None, on_template=None):
    """Build the deck. Returns (presentation, report). Raises SpecError on an invalid spec.

    template overrides spec["template"]["path"]; relative paths resolve against base_dir.
    on_template(template), if given, runs once after the template is opened and before any slide
    is drawn; add-on skills use it to adjust template.frame (for example to keep clear of a logo).
    """
    errors = deckspec.validate(spec)
    if errors:
        raise deckspec.SpecError(errors)
    meta = spec["meta"]
    tmpl = spec.get("template") or {}
    path = template  # as given (relative to the caller's working directory)
    if not path and tmpl.get("path"):  # the spec's own path is relative to the spec file
        path = pathlib.Path(base_dir or ".") / tmpl["path"]
    tpl = open_template(path, accent=(spec.get("theme") or {}).get("accent"),
                        language=meta.get("language", "en"), layout_map=tmpl.get("layout_map"))
    if on_template is not None:
        on_template(tpl)
    ghost_mode = spec.get("mode") == "ghost"
    if ghost_mode:
        meta = {**meta, "draft": meta.get("draft", True)}  # a ghost deck is a draft unless told otherwise
    report = Report()
    ctx = Ctx(tpl=tpl, meta=meta, report=report)
    prs = tpl.prs
    for i, s in enumerate(spec["slides"], 1):
        ctx.slide_no = i
        kind = s["layout"]
        if ghost_mode and kind not in layouts.FULL:
            kind = "ghost"
        role = kind if kind in layouts.FULL else "content"
        layout = tpl.layouts[role]
        slide = prs.slides.add_slide(layout)
        if kind in layouts.FULL:
            layouts.FULL[kind](ctx, slide, s)
            chrome(ctx, slide, s, kind=kind, layout=layout)
        else:
            keep_placeholders(slide, TITLE_TYPES)
            body = chrome(ctx, slide, s, kind=kind, layout=layout)
            layouts.CONTENT[kind](ctx, slide, s, body)
        finish(slide)
        notes(slide, s.get("notes"))
    return prs, report
