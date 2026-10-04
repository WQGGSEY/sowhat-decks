import shutil
import sys
from pathlib import Path

import pytest

REPO = Path(__file__).resolve().parents[2]
SCRIPTS = REPO / "skills" / "deck-review" / "scripts"
FIXTURES = REPO / "tests" / "fixtures" / "review"

for p in (SCRIPTS, FIXTURES):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))

import review_builders  # noqa: E402


def find_soffice():
    from deckreview.render import find_soffice as _find

    return _find()


@pytest.fixture(scope="session")
def decks(tmp_path_factory):
    """Build every fixture deck once per test session: {key: path}."""
    out = tmp_path_factory.mktemp("decks")
    return {key: fn(out / f"{key}.pptx") for key, fn in review_builders.BUILDERS.items()}


@pytest.fixture(scope="session")
def soffice():
    path = find_soffice()
    if not path:
        pytest.skip("LibreOffice (soffice) not installed")
    return path


@pytest.fixture
def make_deck(tmp_path):
    """Build a one-off deck: make_deck(fn) where fn(prs) adds slides."""
    counter = {"n": 0}

    def _make(fn, wide=True):
        counter["n"] += 1
        prs = review_builders.new_deck(wide=wide)
        fn(prs)
        path = tmp_path / f"deck{counter['n']}.pptx"
        prs.save(str(path))
        return path

    return _make


def pytest_report_header(config):
    return f"deck-review scripts: {SCRIPTS}; soffice: {shutil.which('soffice') or 'search paths'}"
