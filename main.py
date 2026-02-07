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

# Pre-register zelda_miloutte and its sub-packages in sys.modules.
# This prevents pygbag's WASM import handler from trying to fetch them from PyPI.
for _name in [
    "zelda_miloutte",
    "zelda_miloutte.data",
    "zelda_miloutte.entities",
    "zelda_miloutte.sprites",
    "zelda_miloutte.states",
    "zelda_miloutte.ui",
    "zelda_miloutte.world",
]:
    _mod = types.ModuleType(_name)
    _parts = _name.split(".")
    _mod.__path__ = [str(_base / "/".join(_parts))]
    _mod.__package__ = _name
    _mod.__file__ = str(_base / "/".join(_parts) / "__init__.py")
    sys.modules[_name] = _mod


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
