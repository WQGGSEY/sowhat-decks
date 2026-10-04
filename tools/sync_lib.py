"""Copy the shared deckkit library into every skill that needs it.

`npx skills add` can install a single skill, so each skill must carry its own
copy of the library (no symlinks, no ../ imports). The source of truth is
skills/deck-build/scripts/deckkit/ plus skills/deck-build/references/deck-spec.schema.json.

    python tools/sync_lib.py            # copy into every target
    python tools/sync_lib.py --check    # exit 1 if any copy differs (CI)
    python tools/sync_lib.py --add deck-review   # opt a skill in, then copy

Targets: deck-exhibits always, plus any skill that already has scripts/deckkit/.
"""
from __future__ import annotations

import argparse
import filecmp
import fnmatch
import os
import pathlib
import shutil
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
SKILLS = ROOT / "skills"
SOURCE_SKILL = SKILLS / "deck-build"
SOURCE_LIB = SOURCE_SKILL / "scripts" / "deckkit"
SCHEMA = SOURCE_SKILL / "references" / "deck-spec.schema.json"
SCRIPTS = ("build.py", "render.py")  # thin CLI wrappers copied next to deckkit/
ALWAYS = ("deck-exhibits",)
IGNORE = ("__pycache__", "*.pyc", ".DS_Store")  # never copied, never compared


def targets() -> list[pathlib.Path]:
    found = {SKILLS / name for name in ALWAYS}
    found |= {p.parents[1] for p in SKILLS.glob("*/scripts/deckkit") if p.is_dir()}
    found.discard(SOURCE_SKILL)
    return sorted(found)


def lib_files(lib: pathlib.Path) -> set[str]:
    return {str(p.relative_to(lib)) for p in lib.rglob("*")
            if p.is_file() and not any(fnmatch.fnmatch(part, pat) for part in p.relative_to(lib).parts for pat in IGNORE)}


def differences() -> list[str]:
    problems = []
    if not filecmp.cmp(SCHEMA, SOURCE_LIB / SCHEMA.name, shallow=False):
        problems.append(f"{SOURCE_LIB / SCHEMA.name} differs from {SCHEMA}")
    want = lib_files(SOURCE_LIB)
    for skill in targets():
        lib = skill / "scripts" / "deckkit"
        have = lib_files(lib) if lib.is_dir() else set()
        for name in sorted(want ^ have):
            problems.append(f"{lib / name}: {'missing' if name in want else 'extra'}")
        for name in sorted(want & have):
            if not filecmp.cmp(SOURCE_LIB / name, lib / name, shallow=False):
                problems.append(f"{lib / name}: differs")
        for script in SCRIPTS:
            src, dst = SOURCE_SKILL / "scripts" / script, skill / "scripts" / script
            if not dst.is_file() or not filecmp.cmp(src, dst, shallow=False):
                problems.append(f"{dst}: missing or differs")
    return [p.replace(f"{ROOT}{os.sep}", "") for p in problems]


def sync() -> list[pathlib.Path]:
    shutil.copyfile(SCHEMA, SOURCE_LIB / SCHEMA.name)
    done = []
    for skill in targets():
        dst = skill / "scripts" / "deckkit"
        if dst.exists():
            shutil.rmtree(dst)
        shutil.copytree(SOURCE_LIB, dst, ignore=shutil.ignore_patterns(*IGNORE))
        for script in SCRIPTS:
            shutil.copyfile(SOURCE_SKILL / "scripts" / script, skill / "scripts" / script)
        done.append(skill)
    return done


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--check", action="store_true", help="report differences, change nothing")
    ap.add_argument("--add", metavar="SKILL", help="opt a skill folder in (creates scripts/deckkit/)")
    args = ap.parse_args(argv)
    if args.check:
        problems = differences()
        for p in problems:
            print(p)
        print("deckkit copies are in sync" if not problems else f"{len(problems)} problem(s); run python tools/sync_lib.py")
        return 1 if problems else 0
    if args.add:
        skill = SKILLS / args.add
        if not (skill / "SKILL.md").is_file():
            print(f"{skill} has no SKILL.md", file=sys.stderr)
            return 2
        (skill / "scripts" / "deckkit").mkdir(parents=True, exist_ok=True)
    for skill in sync():
        print(f"synced deckkit -> {skill.relative_to(ROOT)}/scripts/")
    return 0


if __name__ == "__main__":
    sys.exit(main())
