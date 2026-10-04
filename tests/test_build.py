import copy

from pptx import Presentation
from pptx.oxml.ns import qn
from pptx.util import Emu

from deckkit.build import build_deck

SPEC = {
    "spec_version": "1.0",
    "meta": {"title": "Quarterly review", "language": "en", "sample_data": True, "draft": True},
    "slides": [
        {"layout": "cover", "subtitle": "Board meeting", "date": "October 2026"},
        {"layout": "exhibit", "title": "Region B grew fastest and now drives most of the gap to plan",
         "exhibit": {"type": "bar", "title": "Revenue growth by region, Q3 vs Q2", "unit": "%",
                     "categories": ["Region A", "Region B", "Region C"], "values": [4, 12, 2],
                     "highlight": ["Region B"]},
         "source": "Sample data", "notes": "Say the number first."},
    ],
}


def test_build_returns_a_deck_that_reopens(tmp_path):
    prs, report = build_deck(copy.deepcopy(SPEC))
    path = tmp_path / "deck.pptx"
    prs.save(path)
    again = Presentation(path)
    assert len(again.slides) == 2
    assert again.slides[1].shapes.title.text_frame.text == SPEC["slides"][1]["title"]
    assert report.overflows == []


def test_default_deck_is_16_by_9():
    prs, _ = build_deck(copy.deepcopy(SPEC))
    assert (prs.slide_width, prs.slide_height) == (Emu(12192000), Emu(6858000))


def test_speaker_notes_are_written():
    prs, _ = build_deck(copy.deepcopy(SPEC))
    assert prs.slides[1].notes_slide.notes_text_frame.text == "Say the number first."


def _texts(slide):
    return [sh.text_frame.text for sh in slide.shapes if sh.has_text_frame]


def test_ghost_box_separates_evidence_in_hand_from_gaps():
    spec = {"spec_version": "1.0", "meta": {"title": "Ghost"}, "slides": [
        {"layout": "ghost", "title": "Region B drives growth, so fund it first",
         "ghost": {"exhibit": "Bar: growth by region, %",
                   "evidence": ["E1 Revenue by region [SRC 1]", "E2 Growth rates [CALC]", "[DATA NEEDED] Region B pipeline"]}}]}
    prs, _ = build_deck(spec)
    box_text = next(t for t in _texts(prs.slides[0]) if "Region B pipeline" in t)
    lines = box_text.split("\n")
    assert lines.index("Evidence") < lines.index("E1 Revenue by region [SRC 1]") < lines.index("Still needed")
    assert lines.index("Still needed") < lines.index("[DATA NEEDED] Region B pipeline")


def test_ghost_box_without_gaps_has_no_still_needed_heading():
    spec = {"spec_version": "1.0", "meta": {"title": "Ghost"}, "slides": [
        {"layout": "ghost", "title": "A title", "ghost": {"evidence": ["E1 Revenue [SRC 1]"]}}]}
    prs, _ = build_deck(spec)
    assert not any("Still needed" in t for t in _texts(prs.slides[0]))


def test_negative_bars_are_marked_not_to_invert():
    # LibreOffice draws negative bars as positive unless invertIfNegative is written explicitly
    spec = copy.deepcopy(SPEC)
    spec["slides"][1]["exhibit"]["values"] = [4, -3, 2]
    prs, _ = build_deck(spec)
    chart = next(sh.chart for sh in prs.slides[1].shapes if sh.has_chart)
    series = chart.plots[0].series[0]
    assert series.invert_if_negative is False
    assert list(series.values) == [4, -3, 2]
    # the highlighted bar (Region B, negative) has its own data-point element; it must not invert either
    dpts = series._element.findall(qn("c:dPt"))
    assert dpts and all(d.find(qn("c:invertIfNegative")).get("val") == "0" for d in dpts)


def _named(slide, name):
    return [sh for sh in slide.shapes if sh.name == name]


def test_source_line_always_says_source():
    prs, _ = build_deck(copy.deepcopy(SPEC))
    assert _named(prs.slides[1], "sw:source")[0].text_frame.text == "Source: Sample data"


def test_sample_flag_is_added_to_a_real_source():
    spec = copy.deepcopy(SPEC)
    spec["slides"][1]["source"] = "Finance system export"
    prs, _ = build_deck(spec)
    assert _named(prs.slides[1], "sw:source")[0].text_frame.text == "Source: Sample data; Finance system export"


def test_korean_source_prefix():
    spec = copy.deepcopy(SPEC)
    spec["meta"]["language"] = "ko"
    spec["slides"][1]["source"] = "샘플 데이터"
    prs, _ = build_deck(spec)
    assert _named(prs.slides[1], "sw:source")[0].text_frame.text == "출처: 샘플 데이터"


def test_takeaways_heading_top_aligns_with_the_exhibit_title():
    spec = copy.deepcopy(SPEC)
    spec["slides"][1].update(layout="exhibit_takeaways", takeaways=["Region B adds most new revenue"])
    prs, _ = build_deck(spec)
    slide = prs.slides[1]
    heading = next(sh for sh in _named(slide, "sw:label") if sh.text_frame.text == "So what")
    assert heading.top == _named(slide, "sw:exhibit-title")[0].top


def test_checker_flags_text_that_does_not_fit(tmp_path):
    from deckkit import checks
    pillar = {"heading": "Heading", "body": "word " * 44, "bullets": ["word " * 20] * 4}
    spec = {"spec_version": "1.0", "meta": {"title": "Dense"},
            "slides": [{"layout": "pillars", "title": "Four pillars with too much text", "pillars": [pillar] * 4}]}
    prs, report = build_deck(spec)
    prs.save(tmp_path / "dense.pptx")
    issues = checks.inspect(Presentation(tmp_path / "dense.pptx"))
    assert report.overflows and any(i.kind == "overflow" for i in issues)
