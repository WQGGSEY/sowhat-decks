# AGENTS.md

Guide for coding agents that use or change this repository. The skills are tested in Claude Code.

## Using the skills

Each folder in `skills/` is a self-contained agent skill with a `SKILL.md`. Read the `SKILL.md` first; it says when the skill applies and what to do.

| Skill | Use it to |
|---|---|
| `deck-storyline` | turn a goal, an audience and raw material into an answer-first storyline and a title-only ghost deck |
| `deck-build` | turn a deck spec (JSON) into an editable `.pptx`, optionally on the user's own template, with a PDF/PNG preview |
| `deck-exhibits` | pick and build the right exhibit (native chart, table, 2x2, process) for each message |
| `deck-review` | render any `.pptx`, check it against the rules and a rubric, and fix what is safe to fix |

Script mode (when you can run Python):

```bash
python3 -m pip install --user python-pptx pypdfium2   # python-pptx is required; pypdfium2 only for PNG previews
python3 skills/deck-build/scripts/build.py deck.json -o out/   # deck.pptx, build-report.json, deck.pdf, preview/*.png
```

LibreOffice is optional and only used for the PDF/PNG preview. The scripts never install anything and never use the network.

No-code mode (plain chat; designed for Claude for PowerPoint too, not yet tested there): follow the same rules in each `SKILL.md` and its `references/` without running scripts.

## Rules for changing this repository

- Runtime dependency is `python-pptx` only (`pypdfium2` is optional, for PNG previews). No network calls, no shell eval, no obfuscated code, no secrets.
- The shared library lives in `skills/deck-build/scripts/deckkit/`. Never edit a copy in another skill. After changing it run `python tools/sync_lib.py`; CI runs `python tools/sync_lib.py --check`.
- The deck spec contract is `skills/deck-build/references/deck-spec.schema.json` (explained in `layouts.md`). Keep changes backward compatible.
- No symlinks anywhere: plugin installs and `npx skills add` copy folders and drop links.
- Never invent numbers in examples or tests. Use public sources with citations, or mark the data "Sample data".
- Do not use consulting-firm or third-party product trademarks in names, docs or examples.
- `SKILL.md` files stay under 500 lines; long material goes in `references/`.
- Build outputs go to `out/` (gitignored).

## Tests

```bash
python -m pytest -q
```

Render tests run only when LibreOffice is installed (`SOFFICE=/path/to/soffice` to point at it).
