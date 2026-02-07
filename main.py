"""Entry point for pygbag web build."""
import asyncio
import sys
from pathlib import Path

# Add the package to Python path for pygbag
sys.path.insert(0, str(Path(__file__).parent))

from zelda_miloutte.game import Game
from zelda_miloutte.states.cinematic_state import CinematicState


async def main():
    game = Game()
    game.push_state(CinematicState(game))
    await game.run()


if __name__ == "__main__":
    asyncio.run(main())
