"""Repository rules: plugin manifests, skill format, no symlinks, no trademarks, no network code."""
import json
import os
import pathlib
import re

import pytest
from pptx import Presentation

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKIP_DIRS = {".git", ".venv", "out", "__pycache__", ".pytest_cache"}
MY_SKILLS = ["deck-build", "deck-exhibits"]
TEXT_SUFFIXES = {".md", ".py", ".json", ".yml", ".yaml", ".txt", ".toml", ".cfg"}


def repo_files():
    """Every file and every symlinked folder in the repo (outside .git, .venv, out)."""
    for dirpath, dirnames, filenames in os.walk(ROOT):
        yield from (pathlib.Path(dirpath) / d for d in dirnames if (pathlib.Path(dirpath) / d).is_symlink())
        dirnames[:] = [d for d in dirnames if d not in SKIP_DIRS]
        for name in filenames:
            yield pathlib.Path(dirpath) / name


def frontmatter(path):
    text = path.read_text(encoding="utf-8")
    match = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    assert match, f"{path} has no frontmatter"
    fields = dict(line.split(": ", 1) for line in match.group(1).splitlines() if ": " in line)
    return fields, text


def test_repo_is_its_own_marketplace():
    market = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
    assert market["plugins"][0]["source"] == "./"
    assert market["plugins"][0]["name"] == plugin["name"] == market["name"]
    assert plugin["skills"] == "./skills"
    assert (ROOT / "LICENSE").read_text().startswith("MIT License")


def test_no_symlinks_anywhere():
    assert [p for p in repo_files() if p.is_symlink()] == []


@pytest.mark.parametrize("skill", MY_SKILLS)
def test_skill_md_format(skill):
    path = ROOT / "skills" / skill / "SKILL.md"
    fields, text = frontmatter(path)
    assert fields["name"] == skill
    assert len(fields["description"]) <= 1024
    assert "Use when" in fields["description"]
    for word in ("deck", "slides", "presentation", "board update", "pitch", "PowerPoint"):
        assert word.lower() in fields["description"].lower(), word
    assert len(text.splitlines()) <= 500
    for link in re.findall(r"\]\((references/[^)#]+)", text):  # every linked reference exists
        assert (path.parent / link).is_file(), link


def test_no_trademarks_in_the_repo():
    # spelled in pieces so this file does not match itself
    names = ["Mc" + "Kinsey", "Boston " + "Consulting", r"\bB" + r"CG\b", r"\bBa" + r"in &", "think" + "-cell", "Think" + "Cell"]
    pattern = re.compile("|".join(names), re.I)
    hits = [str(p.relative_to(ROOT)) for p in repo_files()
            if p.is_file() and p.suffix in TEXT_SUFFIXES and pattern.search(p.read_text(encoding="utf-8", errors="ignore"))]
    assert hits == []


def test_scripts_make_no_network_calls():
    pattern = re.compile(r"^\s*(import|from)\s+(urllib|requests|httpx|aiohttp|socket|http\.client|ftplib|smtplib)\b", re.M)
    hits = [str(p.relative_to(ROOT)) for skill in MY_SKILLS for p in (ROOT / "skills" / skill).rglob("*.py")
            if pattern.search(p.read_text(encoding="utf-8"))]
    assert hits == []


def test_scripts_do_not_eval_or_use_a_shell():
    pattern = re.compile(r"\beval\(|\bexec\(|shell\s*=\s*True|os\.system\(")
    hits = [str(p.relative_to(ROOT)) for skill in MY_SKILLS for p in (ROOT / "skills" / skill).rglob("*.py")
            if pattern.search(p.read_text(encoding="utf-8"))]
    assert hits == []


def test_default_template_asset_opens():
    prs = Presentation(ROOT / "skills" / "deck-build" / "assets" / "default-template.pptx")
    assert (prs.slide_width, prs.slide_height) == (12192000, 6858000)
    assert "Title Only" in [layout.name for layout in prs.slide_layouts]


def test_brand_name_is_always_sowhat_decks():
    """The product name is written as a unit: "SoWhat Decks" (#16)."""
    pattern = re.compile("SoWhat" + r"(?! Decks)")  # split so this file does not match itself
    hits = [f"{p.relative_to(ROOT)}:{n}" for p in repo_files()
            if p.is_file() and p.suffix in TEXT_SUFFIXES and "tests" not in p.relative_to(ROOT).parts
            for n, line in enumerate(p.read_text(encoding="utf-8", errors="ignore").splitlines(), 1)
            if pattern.search(line)]
    assert hits == []


def test_built_and_shipped_themes_are_named_sowhat_decks():
    import zipfile
    from deckkit.template_map import open_template
    from deckkit.theme import _theme_xml
    from pptx.oxml.ns import qn
    root = _theme_xml(open_template(None).prs)
    names = {root.get("name"), root.find(".//" + qn("a:clrScheme")).get("name"), root.find(".//" + qn("a:fontScheme")).get("name")}
    assert names == {"SoWhat Decks"}
    with zipfile.ZipFile(ROOT / "skills" / "deck-build" / "assets" / "default-template.pptx") as z:
        theme = z.read("ppt/theme/theme1.xml").decode()
    assert theme.count('name="SoWhat Decks"') == 3
