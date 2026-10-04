"""A deck that follows the rules must come back (almost) clean."""

from deckreview.checks import run_checks
from deckreview.inspect import inspect_pptx


def test_clean_deck_has_no_high_or_medium_issues(decks):
    issues = run_checks(inspect_pptx(decks["clean"]))
    serious = [(i["slide"], i["check"], i["message"]) for i in issues
               if i["severity"] in ("high", "medium")]
    assert serious == []


def test_photo_is_not_mistaken_for_a_chart(decks):
    issues = run_checks(inspect_pptx(decks["plain"]))
    assert not [i for i in issues if i["check"] == "chart_as_image"]
