import pathlib
import sys

# deckkit is imported from its source of truth (the deck-build skill)
SCRIPTS = pathlib.Path(__file__).resolve().parents[1] / "skills" / "deck-build" / "scripts"
if str(SCRIPTS) not in sys.path:
    sys.path.insert(0, str(SCRIPTS))
