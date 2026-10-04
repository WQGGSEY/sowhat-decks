import json

from deckreview.inspect import inspect_pptx


def test_inspection_lists_every_slide_with_its_title(decks):
    info = inspect_pptx(decks["clean"])
    titles = [s["title"] for s in info["slides"]]
    assert titles == [
        "Q3 board update",
        "Revenue grew 18% in Q3, driven by mid-market expansion",
        "Revenue grew every quarter and reached $4.6M in Q4",
        "Vietnam leads the shortlist on four of five criteria",
        "We recommend moving two sales hires to onboarding",
    ]


def test_inspection_is_json_serialisable(decks):
    for path in decks.values():
        json.dumps(inspect_pptx(path))
