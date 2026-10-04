import pytest

from deckkit import text_fit


def test_width_of_latin_text_uses_font_metrics():
    # Arial advance widths: H722 e556 l222 l222 o556 space278 w722 o556 r333 l222 d556 = 4945/1000 em
    assert text_fit.text_width("Hello world", "Arial", 10) == pytest.approx(49.45, abs=0.01)


def test_bold_is_wider_than_regular():
    assert text_fit.text_width("Revenue", "Arial", 12, bold=True) > text_fit.text_width("Revenue", "Arial", 12)


def test_unknown_font_falls_back_to_a_known_table():
    assert text_fit.text_width("abc", "Some Brand Sans", 10) == text_fit.text_width("abc", "Arial", 10)


def test_cjk_characters_are_one_em_wide():
    assert text_fit.text_width("한국어", "Arial", 20) == pytest.approx(60)
    assert text_fit.text_width("日本語", "Arial", 20) == pytest.approx(60)


def test_wrap_breaks_at_spaces_and_keeps_words_whole():
    lines = text_fit.wrap("alpha beta gamma delta", "Arial", 10, width_pt=60)
    assert len(lines) > 1
    assert " ".join(lines) == "alpha beta gamma delta"


def test_wrap_breaks_a_word_longer_than_the_line():
    lines = text_fit.wrap("x" * 200, "Arial", 10, width_pt=50)
    assert all(text_fit.text_width(line, "Arial", 10) <= 50 for line in lines)
    assert "".join(lines) == "x" * 200


def test_japanese_wraps_between_characters():
    lines = text_fit.wrap("日本語の文章は空白がなくても折り返します", "Arial", 20, width_pt=100)
    assert len(lines) >= 4


def test_fit_keeps_largest_size_that_fits():
    fit = text_fit.fit([text_fit.Para("Short title")], width_pt=500, height_pt=80, max_size=28, min_size=24)
    assert fit.size == 28
    assert fit.lines == 1
    assert not fit.overflow


def test_fit_shrinks_long_text_before_overflowing():
    text = "Region B grew fastest and now drives most of the gap to plan for the year ahead of us all"
    roomy = text_fit.fit([text_fit.Para(text)], width_pt=900, height_pt=200, max_size=28, min_size=24, max_lines=2)
    tight = text_fit.fit([text_fit.Para(text)], width_pt=560, height_pt=200, max_size=28, min_size=20, max_lines=2)
    assert roomy.size == 28
    assert 20 <= tight.size < 28
    assert tight.lines <= 2
    assert not tight.overflow


def test_fit_reports_overflow_at_the_floor():
    fit = text_fit.fit([text_fit.Para("word " * 200)], width_pt=200, height_pt=50, max_size=16, min_size=12)
    assert fit.overflow
    assert fit.size == 12


def test_fit_scales_paragraphs_together():
    paras = [text_fit.Para("Headline", bold=True, scale=1.0), text_fit.Para("Detail text", scale=0.75)]
    fit = text_fit.fit(paras, width_pt=400, height_pt=100, max_size=20, min_size=12)
    assert fit.sizes == [20, 15]
