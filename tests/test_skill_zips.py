"""The release ZIPs (tools/build_skill_zips.py) are complete, clean and self-contained."""
import importlib.util
import pathlib
import subprocess
import sys
import zipfile

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("build_skill_zips", ROOT / "tools" / "build_skill_zips.py")
bsz = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bsz)

SKILLS = ["deck-build", "deck-exhibits", "deck-review", "deck-storyline"]


@pytest.fixture(scope="module")
def dist(tmp_path_factory):
    out = tmp_path_factory.mktemp("dist")
    bsz.build(out)
    return out


def test_one_zip_per_skill_plus_one_with_all(dist):
    assert bsz.skill_names() == SKILLS
    assert sorted(p.name for p in dist.glob("*.zip")) == sorted([f"{s}.zip" for s in SKILLS] + [bsz.ALL_NAME])


@pytest.mark.parametrize("skill", SKILLS)
def test_skill_zip_has_one_clean_folder(dist, skill):
    path = dist / f"{skill}.zip"
    assert bsz.check_zip(path, [skill]) == []
    names = zipfile.ZipFile(path).namelist()
    assert f"{skill}/LICENSE.txt" in names
    source = {f"{skill}/{p.relative_to(ROOT / 'skills' / skill).as_posix()}" for p in bsz.skill_files(skill)}
    assert source <= set(names)  # nothing the skill needs is left out


def test_all_skills_zip(dist):
    assert bsz.check_zip(dist / bsz.ALL_NAME, SKILLS) == []


def test_zips_are_reproducible(tmp_path):
    a, b = tmp_path / "a", tmp_path / "b"
    bsz.build(a)
    bsz.build(b)
    for path in a.glob("*.zip"):
        assert path.read_bytes() == (b / path.name).read_bytes(), path.name


def test_unzipped_skills_run_on_their_own(dist, tmp_path):
    """deck-build and deck-review work from the unzipped folders alone (no repository around them)."""
    for skill in ("deck-build", "deck-review"):
        zipfile.ZipFile(dist / f"{skill}.zip").extractall(tmp_path)
    spec_json = ROOT / "tests" / "fixtures" / "05-exhibits-bar.json"
    out = tmp_path / "out"
    build = subprocess.run([sys.executable, str(tmp_path / "deck-build" / "scripts" / "build.py"), str(spec_json),
                            "-o", str(out), "--no-render"], capture_output=True, text=True, check=False, cwd=tmp_path)
    assert build.returncode == 0, build.stdout + build.stderr
    review = subprocess.run([sys.executable, str(tmp_path / "deck-review" / "scripts" / "review.py"), "check",
                             str(out / "deck.pptx")], capture_output=True, text=True, check=False, cwd=tmp_path)
    assert review.returncode == 0, review.stdout + review.stderr
    assert '"issues"' in review.stdout
