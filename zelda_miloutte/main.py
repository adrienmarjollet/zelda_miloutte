from zelda_miloutte.game import Game
from zelda_miloutte.states.cinematic_state import CinematicState


def main():
    game = Game()
    game.push_state(CinematicState(game))
    game.run()


if __name__ == "__main__":
    main()
