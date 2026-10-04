"""Decks written by other tools: the python-pptx stock template and LibreOffice."""

import subprocess
from pathlib import Path

import pytest
import review_builders
from deckreview.checks import run_checks
from deckreview.inspect import inspect_pptx


def _lo_roundtrip(src: Path, soffice: str, out: Path) -> Path:
    """pptx -> odp -> pptx, so the final file is written by LibreOffice's exporter."""
    profile = Path(out) / "profile"
    for fmt, path in (("odp", src), ("pptx", out / "odp" / (src.stem + ".odp"))):
        dest = out / fmt
        subprocess.run([soffice, "--headless", "--norestore",
                        f"-env:UserInstallation={profile.as_uri()}", "--convert-to", fmt,
                        "--outdir", str(dest), str(path)],
                       capture_output=True, timeout=180, check=False)
    result = out / "pptx" / src.name
    if not result.exists():
        pytest.skip("LibreOffice conversion failed")
    return result


@pytest.fixture(scope="module")
def lo_decks(decks, soffice, tmp_path_factory):
    out = tmp_path_factory.mktemp("lo")
    return {k: _lo_roundtrip(decks[k], soffice, out) for k in ("flawed1", "flawed2", "clean")}


def test_stock_template_deck_is_read_and_judged(decks):
    deck = inspect_pptx(decks["plain"])
    assert [s["title"] for s in deck["slides"]][:2] == ["Team offsite", "Agenda"]
    labels = {i["slide"] for i in run_checks(deck) if i["check"] == "title_not_claim"}
    assert labels == {3, 5}  # "Customer feedback", "Ticket volume"; Agenda is exempt


def test_libreoffice_written_decks_are_read(lo_decks):
    for path in lo_decks.values():
        deck = inspect_pptx(path)
        assert len(deck["slides"]) >= 5 and not deck["warnings"]
        assert all(s["title"] for s in deck["slides"])


def test_seeded_defects_survive_a_libreoffice_round_trip(lo_decks):
    issues = {k: run_checks(inspect_pptx(lo_decks[k])) for k in ("flawed1", "flawed2")}

    def found(deck, slide, check):
        return any(i["check"] == check and (i.get("slide") == slide or any(
            loc["slide"] == slide for loc in i.get("locations", []))) for i in issues[deck])

    hits = [d for d in review_builders.SEEDED_DEFECTS if found(d[0], d[1], d[2])]
    # LibreOffice grows the overflowing box to fit and flattens the four fills to
    # one theme color, so those two defects no longer exist in its output.
    assert len(hits) >= 7, [d[2] for d in hits]


def test_clean_deck_stays_clean_after_libreoffice(lo_decks):
    serious = [(i["slide"], i["check"], i["message"])
               for i in run_checks(inspect_pptx(lo_decks["clean"]))
               if i["severity"] in ("high", "medium")]
    assert serious == []
