import asyncio
from .game import Game
from .states.cinematic_state import CinematicState


async def main():
    game = Game()
    game.push_state(CinematicState(game))
    await game.run()


def _sync_entry():
    """Synchronous entry point for console_scripts."""
    asyncio.run(main())


if __name__ == "__main__":
    asyncio.run(main())
