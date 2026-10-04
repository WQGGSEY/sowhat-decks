"""Rendering through LibreOffice. Skipped when soffice is not installed."""

from deckreview.render import install_hint, render_pptx


def test_render_writes_a_pdf_and_one_png_per_slide(decks, soffice, tmp_path):
    result = render_pptx(decks["clean"], tmp_path / "render", soffice=soffice, width_px=800)
    assert result["pdf"] and result["pdf"].exists()
    assert len(result["pngs"]) == 5
    from PIL import Image

    with Image.open(result["pngs"][0]) as im:
        assert im.size[0] == 800


def test_missing_libreoffice_gives_install_advice_instead_of_installing(decks, tmp_path):
    result = render_pptx(decks["clean"], tmp_path / "render",
                         soffice=str(tmp_path / "no-such-soffice"))
    assert result["pdf"] is None and result["pngs"] == []
    assert "libreoffice" in result["error"].lower()
    assert "brew install" in install_hint()
