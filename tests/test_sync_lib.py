"""Every skill that ships deckkit carries an identical copy (no symlinks, no ../ imports)."""
import filecmp
import pathlib
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import sync_lib  # noqa: E402
SOURCE = ROOT / "skills" / "deck-build" / "scripts" / "deckkit"


def files(lib):
    return sorted(str(p.relative_to(lib)) for p in lib.rglob("*")
                  if p.is_file() and "__pycache__" not in p.parts and p.name != ".DS_Store")


def test_sync_tool_finds_no_differences():
    assert sync_lib.differences() == []


def test_copies_are_byte_identical_to_the_source():
    copies = [p for p in ROOT.glob("skills/*/scripts/deckkit") if p != SOURCE]
    assert ROOT / "skills" / "deck-exhibits" / "scripts" / "deckkit" in copies
    for lib in copies:
        assert files(lib) == files(SOURCE), lib
        for name in files(SOURCE):
            assert filecmp.cmp(SOURCE / name, lib / name, shallow=False), lib / name


def test_bundled_schema_matches_the_reference_copy():
    ref = ROOT / "skills" / "deck-build" / "references" / "deck-spec.schema.json"
    assert filecmp.cmp(ref, SOURCE / "deck-spec.schema.json", shallow=False)
