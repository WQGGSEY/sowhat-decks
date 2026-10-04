"""Must-not-regress set for the claim-vs-label title check.

The corpus (tests/fixtures/review/title_corpus.py) holds the Team Lead's 85
review titles (42 verbatim, 43 of the same kinds), every action title in the
deck-build specs, the second review's adversarial titles, our own probes, and
further claim and label shapes. Every title must be
judged correctly; the seeded "Market Overview" defect is covered by
test_review_seeded_defects.py.
"""

import time

import pytest
import title_corpus as C
from deckreview.titles import classify

CLAIMS = (C.LEAD_CLAIMS + C.DECK_BUILD_TITLES + C.EXTRA_CLAIMS + C.ADVERSARIAL_CLAIMS
          + C.PROBE_CLAIMS)
LABELS = C.LEAD_LABELS + C.EXTRA_LABELS + C.ADVERSARIAL_LABELS + C.PROBE_LABELS


@pytest.mark.parametrize("title", CLAIMS)
def test_claim_titles_pass(title):
    assert classify(title)["claim"], classify(title)


@pytest.mark.parametrize("title", LABELS)
def test_topic_labels_are_flagged(title):
    assert not classify(title)["claim"], classify(title)


@pytest.mark.parametrize("title", C.KNOWN_WRONG)
def test_known_limits_stay_documented(title):
    # Claims the rules still miss (main misses them too). If one starts passing,
    # move it to PROBE_CLAIMS.
    assert not classify(title)["claim"]


def test_corpus_has_the_review_set():
    assert (len(C.LEAD_CLAIMS), len(C.LEAD_LABELS)) == (41, 44)


def test_very_long_title_is_judged_in_linear_time():
    started = time.perf_counter()
    classify("Revenue grew, " * 20000)
    assert time.perf_counter() - started < 2.0
