#!/usr/bin/env python3
"""Render any .pptx to PDF and PNG previews with LibreOffice (if installed).

    python3 render.py deck.pptx -o out/preview
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))

from deckkit.cli import render_main  # noqa: E402

if __name__ == "__main__":
    sys.exit(render_main())
