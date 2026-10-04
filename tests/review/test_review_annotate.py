"""Annotated PNGs: a numbered box around each located problem."""

import pytest

PIL = pytest.importorskip("PIL")
from PIL import Image  # noqa: E402

from deckreview.annotate import SEVERITY_COLORS, annotate  # noqa: E402

EMU_IN = 914400


def test_problem_area_is_boxed_in_its_severity_color(tmp_path):
    png = tmp_path / "slide-01.png"
    Image.new("RGB", (1000, 750), "white").save(png)
    deck = {"slide_width": 10 * EMU_IN, "slide_height": int(7.5 * EMU_IN),
            "slides": [{"index": 1, "hidden": False}]}
    issue = {"check": "overlap", "severity": "high", "slide": 1,
             "bbox": [2 * EMU_IN, 2 * EMU_IN, 4 * EMU_IN, 1 * EMU_IN], "message": "m"}
    out = annotate({1: png}, [issue], deck, tmp_path / "annotated")
    assert [p.name for p in out] == ["slide-01.png"]
    with Image.open(out[0]) as im:
        im = im.convert("RGB")
        # left edge of the box sits at x = 200 px, between y = 200 and 300 px
        assert im.getpixel((200, 250)) == SEVERITY_COLORS["high"]
        assert im.getpixel((400, 250)) == (255, 255, 255)
