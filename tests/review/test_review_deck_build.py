"""Review decks produced by the deck-build skill (skipped if it is not present).

The review must hold its own against our builder: no high or medium issues on
the builder's all-layout test specs, in English and Korean.
"""

import subprocess
import sys
from pathlib import Path

import pytest
from deckreview.checks import run_checks
from deckreview.inspect import inspect_pptx

REPO = Path(__file__).resolve().parents[2]
BUILD = REPO / "skills" / "deck-build" / "scripts" / "build.py"
SPECS = sorted((REPO / "tests" / "fixtures").glob("*-all-layouts.json"))


@pytest.mark.skipif(not BUILD.exists() or not SPECS, reason="deck-build not available")
@pytest.mark.parametrize("spec", SPECS, ids=[p.stem for p in SPECS])
def test_deck_build_output_has_no_serious_issues(spec, tmp_path):
    proc = subprocess.run([sys.executable, str(BUILD), str(spec), "-o", str(tmp_path),
                           "--no-render"], capture_output=True, text=True, timeout=300)
    deck = tmp_path / "deck.pptx"
    if proc.returncode != 0 or not deck.exists():
        pytest.skip(f"deck-build failed: {proc.stderr[-300:]}")
    serious = [(i["slide"], i["check"], i["message"]) for i in run_checks(inspect_pptx(deck))
               if i["severity"] in ("high", "medium")]
    assert serious == []
