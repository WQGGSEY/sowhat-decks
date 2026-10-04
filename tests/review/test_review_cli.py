"""End to end through the command line, the way an agent runs the skill."""

import json
import subprocess
import sys
from pathlib import Path

CLI = Path(__file__).resolve().parents[2] / "skills" / "deck-review" / "scripts" / "review.py"


def _run(*args):
    return subprocess.run([sys.executable, str(CLI), *map(str, args)], capture_output=True,
                          text=True, timeout=300)


def test_review_without_rendering_writes_report_json_and_fixed_deck(decks, tmp_path):
    out = tmp_path / "rev"
    proc = _run("run", decks["flawed1"], "--out", out, "--no-render")
    assert proc.returncode == 0, proc.stderr
    md = (out / "review.md").read_text()
    for heading in ("## Top 5 fixes", "## Title read-through", "## Rewritten titles",
                    "## Slide by slide", "## Automatic fixes"):
        assert heading in md
    assert "Market Overview" in md
    data = json.loads((out / "review.json").read_text())
    assert {i["check"] for i in data["issues"]} >= {"title_not_claim", "missing_source"}
    assert (out / "flawed1.fixed.pptx").exists()


def test_full_review_draws_annotated_pngs(decks, soffice, tmp_path):
    out = tmp_path / "rev"
    proc = _run("run", decks["flawed2"], "--out", out, "--soffice", soffice, "--width", 800)
    assert proc.returncode == 0, proc.stderr
    annotated = sorted(p.name for p in (out / "annotated").glob("*.png"))
    assert "slide-02.png" in annotated and "slide-03.png" in annotated
    assert "annotated/slide-03.png" in (out / "review.md").read_text()


def test_check_subcommand_prints_issues_as_json(decks):
    proc = _run("check", decks["clean"])
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["issues"] == []


def test_inspect_subcommand_prints_titles(decks):
    proc = _run("inspect", decks["clean"])
    assert proc.returncode == 0, proc.stderr
    assert json.loads(proc.stdout)["slides"][1]["title"].startswith("Revenue grew 18%")


def test_unreadable_file_fails_with_a_clear_message(tmp_path):
    bad = tmp_path / "not-a-deck.pptx"
    bad.write_text("hello")
    proc = _run("check", bad)
    assert proc.returncode == 2
    assert "could not open" in proc.stderr.lower()


def test_rerun_does_not_leave_stale_annotations(decks, soffice, tmp_path):
    out = tmp_path / "rev"
    stale = out / "annotated" / "slide-09.png"
    stale.parent.mkdir(parents=True)
    stale.write_bytes(b"old")
    proc = _run("run", decks["flawed1"], "--out", out, "--soffice", soffice, "--width", 600)
    assert proc.returncode == 0, proc.stderr
    assert not stale.exists()
