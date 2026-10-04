"""Build the release ZIPs: one per skill, plus one with all four.

    python3 tools/build_skill_zips.py --out dist

Each skill ZIP holds one folder, `<skill>/`, with SKILL.md at its top, the
skill's scripts, references and assets, and a copy of the MIT license. Tests,
caches and compiled files are left out, so the folder is exactly what a user
uploads to Claude or copies into a skills directory. The release workflow
(.github/workflows/release.yml) attaches these files to the GitHub Release.

Standard library only. The ZIPs are reproducible: entries are sorted and
carry a fixed timestamp.
"""
from __future__ import annotations

import argparse
import pathlib
import re
import sys
import zipfile

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
ALL_NAME = "sowhat-decks-all-skills.zip"
EXCLUDE_DIRS = {"tests", "__pycache__", ".pytest_cache"}
EXCLUDE_FILES = {".DS_Store"}
EXCLUDE_SUFFIXES = {".pyc", ".pyo"}
FIXED_TIME = (2026, 1, 1, 0, 0, 0)


def skill_names() -> list[str]:
    return sorted(p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file())


def skill_files(skill: str) -> list[pathlib.Path]:
    base = SKILLS / skill
    files = []
    for path in sorted(base.rglob("*")):
        rel = path.relative_to(base)
        if any(part in EXCLUDE_DIRS for part in rel.parts):
            continue
        if path.is_symlink():
            raise SystemExit(f"symlink in {skill}: {rel} (skills must not contain symlinks)")
        if path.is_file() and path.name not in EXCLUDE_FILES and path.suffix not in EXCLUDE_SUFFIXES:
            files.append(path)
    return files


def _add(zf: zipfile.ZipFile, arcname: str, data: bytes) -> None:
    info = zipfile.ZipInfo(arcname, date_time=FIXED_TIME)
    info.compress_type = zipfile.ZIP_DEFLATED
    info.external_attr = 0o644 << 16
    zf.writestr(info, data)


def entries(skill: str) -> list[tuple[str, bytes]]:
    base = SKILLS / skill
    out = [(f"{skill}/{p.relative_to(base).as_posix()}", p.read_bytes()) for p in skill_files(skill)]
    out.append((f"{skill}/LICENSE.txt", (ROOT / "LICENSE").read_bytes()))
    return sorted(out)


def write_zip(path: pathlib.Path, items: list[tuple[str, bytes]]) -> None:
    with zipfile.ZipFile(path, "w") as zf:
        for arcname, data in items:
            _add(zf, arcname, data)


def check_zip(path: pathlib.Path, skills: list[str]) -> list[str]:
    """Problems with a built ZIP; an empty list means it is fine."""
    problems = []
    with zipfile.ZipFile(path) as zf:
        names = zf.namelist()
        for skill in skills:
            if f"{skill}/SKILL.md" not in names:
                problems.append(f"{path.name}: {skill}/SKILL.md missing")
                continue
            text = zf.read(f"{skill}/SKILL.md").decode("utf-8")
            match = re.search(r"^name:\s*(\S+)\s*$", text, re.M)
            if not match or match.group(1) != skill:
                problems.append(f"{path.name}: {skill}/SKILL.md name is not {skill}")
        tops = {n.split("/", 1)[0] for n in names}
        if tops != set(skills):
            problems.append(f"{path.name}: top-level folders {sorted(tops)}, expected {sorted(skills)}")
        for n in names:
            parts = n.split("/")
            if any(p in EXCLUDE_DIRS for p in parts) or n.endswith((".pyc", ".pyo")) or parts[-1] in EXCLUDE_FILES:
                problems.append(f"{path.name}: should not contain {n}")
    return problems


def build(out: pathlib.Path) -> list[pathlib.Path]:
    out.mkdir(parents=True, exist_ok=True)
    names = skill_names()
    built = []
    for skill in names:
        path = out / f"{skill}.zip"
        write_zip(path, entries(skill))
        built.append(path)
    path = out / ALL_NAME
    write_zip(path, [item for skill in names for item in entries(skill)])
    built.append(path)
    return built


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--out", default="dist", help="output folder (default: dist)")
    args = ap.parse_args(argv)
    built = build(pathlib.Path(args.out))
    names = skill_names()
    problems = []
    for path in built:
        expected = names if path.name == ALL_NAME else [path.stem]
        problems += check_zip(path, expected)
        print(f"{path}  {path.stat().st_size // 1024} KB")
    for p in problems:
        print(f"error: {p}", file=sys.stderr)
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
