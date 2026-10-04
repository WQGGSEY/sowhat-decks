"""Safe automatic fixes: layout and size only; text and numbers never change."""

import hashlib

from pptx import Presentation

from deckreview.checks import run_checks
from deckreview.fix import fix_pptx
from deckreview.inspect import inspect_pptx


def _texts(path):
    """Every text string and chart value in the deck, per slide."""
    out = []
    for i, slide in enumerate(Presentation(str(path)).slides, 1):
        items = []
        for shp in slide.shapes:
            if shp.has_text_frame and shp.text_frame.text.strip():
                items.append(shp.text_frame.text)
            if getattr(shp, "has_table", False) and shp.has_table:
                items += [c.text for r in shp.table.rows for c in r.cells]
            if getattr(shp, "has_chart", False) and shp.has_chart:
                for plot in shp.chart.plots:
                    for ser in plot.series:
                        items.append(tuple(ser.values))
        out.append(items)
    return out


def _sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def test_fixable_issues_are_gone_after_fixing(decks, tmp_path):
    for key in ("flawed1", "flawed2"):
        dst = tmp_path / f"{key}.fixed.pptx"
        applied = fix_pptx(decks[key], dst)
        assert applied, key
        left = {(i["slide"], i["check"]) for i in run_checks(inspect_pptx(dst))
                if i["check"] in ("font_below_floor", "off_slide", "missing_source",
                                  "misaligned")}
        assert left == set(), (key, left)


def test_fixing_keeps_every_text_and_number(decks, tmp_path):
    for key in ("flawed1", "flawed2", "clean"):
        dst = tmp_path / f"{key}.fixed.pptx"
        before_hash = _sha(decks[key])
        fix_pptx(decks[key], dst)
        assert _sha(decks[key]) == before_hash, "input file must not change"
        before, after = _texts(decks[key]), _texts(dst)
        for b, a in zip(before, after):
            added = [t for t in a if t not in b]
            assert all(t in a for t in b)
            assert all(isinstance(t, str) and "[SOURCE NEEDED]" in t for t in added)


def test_missing_source_gets_a_visible_placeholder_not_an_invented_source(decks, tmp_path):
    dst = tmp_path / "f1.pptx"
    fix_pptx(decks["flawed1"], dst)
    slide6 = Presentation(str(dst)).slides[5]
    texts = [s.text_frame.text for s in slide6.shapes if s.has_text_frame]
    assert "Source: [SOURCE NEEDED]" in texts
    issues = run_checks(inspect_pptx(dst))
    assert any(i["check"] == "data_needed" and i["slide"] == 6 for i in issues)


def test_small_footer_is_raised_to_the_10pt_floor_not_the_body_floor(make_deck, tmp_path):
    import review_builders as B

    def build(prs):
        s = B.add_titled_slide(prs, "Revenue grew 39% to $1.04B in 2025")
        B.add_text(s, "Body text.", 0.6, 1.7, 12.1, 0.8, size=16)
        B.add_text(s, "Confidential", 0.6, 7.05, 3.0, 0.3, size=8, name="Tiny footer")

    dst = tmp_path / "fixed.pptx"
    fix_pptx(make_deck(build), dst)
    footer = next(s for s in Presentation(str(dst)).slides[0].shapes if s.name == "Tiny footer")
    assert footer.text_frame.paragraphs[0].runs[0].font.size.pt == 10
