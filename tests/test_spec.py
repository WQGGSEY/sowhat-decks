import copy
import json

import pytest

from deckkit import spec as deckspec

MINIMAL = {
    "spec_version": "1.0",
    "meta": {"title": "Test deck", "sample_data": True},
    "slides": [
        {"layout": "cover"},
        {
            "layout": "exhibit",
            "title": "Region B grew fastest",
            "exhibit": {"type": "bar", "title": "Growth by region", "unit": "%",
                        "categories": ["A", "B", "C"], "values": [1, 2, 3], "highlight": ["B"]},
            "source": "Sample data",
        },
    ],
}


def errors_for(mutate):
    s = copy.deepcopy(MINIMAL)
    mutate(s)
    return deckspec.validate(s)


def test_minimal_spec_is_valid():
    assert deckspec.validate(MINIMAL) == []


def test_missing_action_title_is_reported_with_its_path():
    errs = errors_for(lambda s: s["slides"][1].pop("title"))
    assert any("slides[1]" in e and "title" in e for e in errs)


def test_unknown_layout_lists_the_allowed_layouts():
    errs = errors_for(lambda s: s["slides"][1].update(layout="mosaic"))
    assert any("mosaic" in e and "exhibit_takeaways" in e for e in errs)


def test_unknown_exhibit_type_is_reported():
    errs = errors_for(lambda s: s["slides"][1]["exhibit"].update(type="pie"))
    assert any("pie" in e for e in errs)


def test_unexpected_field_is_rejected():
    errs = errors_for(lambda s: s["slides"][1].update(colour="red"))
    assert any("colour" in e for e in errs)


def test_title_longer_than_cap_is_rejected():
    errs = errors_for(lambda s: s["slides"][1].update(title="x" * 121))
    assert any("slides[1].title" in e for e in errs)


def test_values_must_match_categories():
    errs = errors_for(lambda s: s["slides"][1]["exhibit"].update(values=[1, 2]))
    assert any("values" in e and "categories" in e for e in errs)


def test_highlight_must_name_a_category():
    errs = errors_for(lambda s: s["slides"][1]["exhibit"].update(highlight=["Z"]))
    assert any("Z" in e for e in errs)


def test_exhibit_slide_needs_a_source():
    errs = errors_for(lambda s: s["slides"][1].pop("source"))
    assert any("source" in e for e in errs)


def test_ghost_slide_needs_only_a_title():
    errs = errors_for(lambda s: s["slides"].append({"layout": "ghost", "title": "Storyline only"}))
    assert errs == []


def test_load_raises_with_all_errors(tmp_path):
    bad = copy.deepcopy(MINIMAL)
    bad["slides"][1].pop("title")
    bad["slides"][1].pop("source")
    path = tmp_path / "deck.json"
    path.write_text(json.dumps(bad))
    with pytest.raises(deckspec.SpecError) as exc:
        deckspec.load(path)
    assert len(exc.value.errors) >= 2
