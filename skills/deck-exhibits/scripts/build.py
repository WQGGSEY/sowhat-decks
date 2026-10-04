#!/usr/bin/env python3
"""Build an editable .pptx (and a PDF/PNG preview) from a deck spec JSON.

    python3 build.py deck.json -o out/            # deck.pptx, deck.pdf, preview/*.png
    python3 build.py deck.json --template brand.potx
    python3 build.py --help
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from deckkit.cli import build_main  # noqa: E402

if __name__ == "__main__":
    sys.exit(build_main())
