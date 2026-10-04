"""Acceptance: two deliberately flawed decks carry 10 seeded defects.

The bar from the build plan is 8 of 10; the per-defect tests show which ones
are found.
"""

import pytest
import review_builders
from deckreview.checks import run_checks
from deckreview.inspect import inspect_pptx

SEEDED = review_builders.SEEDED_DEFECTS


def _issues(decks, key, cache={}):
    if key not in cache:
        cache[key] = run_checks(inspect_pptx(decks[key]))
    return cache[key]


def _found(issues, slide, check):
    for i in issues:
        if i["check"] != check:
            continue
        if i.get("slide") == slide:
            return True
        if any(loc.get("slide") == slide for loc in i.get("locations", [])):
            return True
    return False


@pytest.mark.parametrize("deck,slide,check,why", SEEDED,
                         ids=[f"{d}-s{s}-{c}" for d, s, c, _ in SEEDED])
def test_each_seeded_defect_is_reported(decks, deck, slide, check, why):
    assert _found(_issues(decks, deck), slide, check), why


def test_at_least_8_of_10_seeded_defects_are_reported(decks):
    hits = sum(_found(_issues(decks, d), s, c) for d, s, c, _ in SEEDED)
    assert len(SEEDED) == 10
    assert hits >= 8
