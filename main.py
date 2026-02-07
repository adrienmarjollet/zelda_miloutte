# /// script
# dependencies = [
#  "pygame-ce",
# ]
# ///
"""Entry point for pygbag web build."""
import asyncio
import importlib
import sys
import types
from pathlib import Path

# Add the package to Python path for pygbag
_base = Path(__file__).parent
sys.path.insert(0, str(_base))

# Pre-register only the top-level package in sys.modules so that
# pygbag's WASM import handler won't try to fetch it from PyPI.
# Sub-packages are NOT registered here — they must be loaded normally
# from the filesystem so their __init__.py content is preserved
# (e.g. zelda_miloutte/sprites/__init__.py defines AnimatedSprite).
_pkg = types.ModuleType("zelda_miloutte")
_pkg.__path__ = [str(_base / "zelda_miloutte")]
_pkg.__package__ = "zelda_miloutte"
_pkg.__file__ = str(_base / "zelda_miloutte" / "__init__.py")
sys.modules["zelda_miloutte"] = _pkg


async def main():
    # Use importlib to avoid pygbag's AST import scanner
    Game = importlib.import_module("zelda_miloutte.game").Game
    CinematicState = importlib.import_module(
        "zelda_miloutte.states.cinematic_state"
    ).CinematicState

    game = Game()
    game.push_state(CinematicState(game))
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
