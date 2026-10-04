"""PDF and PNG previews through LibreOffice. Skipped when LibreOffice is not installed."""
import json
import pathlib

import pytest

from deckkit import render
from deckkit.build import build_deck

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT = ROOT / "out" / "tests" / "render"

needs_soffice = pytest.mark.skipif(render.find_soffice() is None, reason="LibreOffice not installed")


@needs_soffice
@pytest.mark.parametrize("name", ["01-en-all-layouts", "02-ko-all-layouts"])
def test_all_layouts_render_to_pdf_and_png(name):
    spec = json.loads((ROOT / "tests" / "fixtures" / f"{name}.json").read_text(encoding="utf-8"))
    prs, _ = build_deck(spec)
    out = OUT / name
    out.mkdir(parents=True, exist_ok=True)
    pptx = out / "deck.pptx"
    prs.save(pptx)
    result = render.render(pptx, out, width=800)
    assert result.pdf and result.pdf.stat().st_size > 10_000
    assert len(result.pngs) == len(spec["slides"]) == 12
    from PIL import Image
    for png in result.pngs:  # every page has visible content, not a blank render
        lo, hi = Image.open(png).convert("L").getextrema()
        assert lo < 100 < hi, png.name


def test_missing_libreoffice_is_reported_not_raised(tmp_path, monkeypatch):
    monkeypatch.setattr(render, "find_soffice", lambda: None)
    result = render.render(tmp_path / "deck.pptx", tmp_path)
    assert result.pdf is None and "LibreOffice not found" in result.message
