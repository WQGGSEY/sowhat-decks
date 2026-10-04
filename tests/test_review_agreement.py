"""The build must never say "pass" on a deck that deck-review flags for overlap, overflow or off-slide.

Runs deck-review's own inspector and checks (skills/deck-review) on decks built at and near the
text limits, in English, Korean and Japanese. Skipped if deck-review is not in the repo.
"""
import itertools
import json
import pathlib
import sys

import pytest
from pptx import Presentation

from deckkit import checks
from deckkit.build import build_deck

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "skills" / "deck-review" / "scripts"))
deckreview = pytest.importorskip("deckreview.checks")
from deckreview.inspect import inspect_pptx  # noqa: E402

SERIOUS = {"overlap", "overflow", "off_slide"}
FILL = {"en": "Revenue grew in the region ", "ko": "매출 성장은 지역에서 ", "ja": "売上は地域で伸びた"}


def text(lang, n):
    return (FILL[lang] * (n // len(FILL[lang]) + 1))[:n].strip()


def cases():
    for lang, n, head, detail in itertools.product(["en", "ko", "ja"], [3, 4, 5], [60, 120], [0, 160, 240]):
        yield f"summary-{lang}-{n}-{head}-{detail}", lang, {
            "layout": "executive_summary", "title": text(lang, 30), "source": "Sample data",
            "points": [{"headline": text(lang, head), **({"detail": text(lang, detail)} if detail else {})}] * n}
    for lang, n, action, detail in itertools.product(["en", "ko"], [4, 6], [60, 100], [0, 160]):
        yield f"recs-{lang}-{n}-{action}-{detail}", lang, {
            "layout": "recommendations", "title": text(lang, 30), "source": "Sample data",
            "items": [{"action": text(lang, action), **({"detail": text(lang, detail)} if detail else {}),
                       "owner": text(lang, 12), "due": text(lang, 10)}] * n}


def verdicts(spec, path):
    prs, report = build_deck(spec)
    prs.save(path)
    mine = bool(report.overflows) or any(i.kind in ("overflow", "overlap", "out-of-bounds") for i in checks.inspect(Presentation(path)))
    theirs = [i for i in deckreview.run_checks(inspect_pptx(str(path))) if i["severity"] == "high" and i["check"] in SERIOUS]
    return mine, theirs


@pytest.mark.parametrize("name,lang,slide", list(cases()), ids=[c[0] for c in cases()])
def test_build_flags_what_deck_review_flags(name, lang, slide, tmp_path):
    spec = {"spec_version": "1.0", "meta": {"title": "Agreement", "language": lang}, "slides": [slide]}
    mine, theirs = verdicts(spec, tmp_path / f"{name}.pptx")
    assert mine or not theirs, theirs[0]["message"]


@pytest.mark.parametrize("path", sorted((ROOT / "tests" / "fixtures").glob("*.json")), ids=lambda p: p.stem)
def test_committed_specs_are_clean_for_deck_review(path, tmp_path):
    mine, theirs = verdicts(json.loads(path.read_text(encoding="utf-8")), tmp_path / "deck.pptx")
    assert not mine and not theirs, [t["message"] for t in theirs]
