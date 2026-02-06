"""Sign sprites using pixel art grid system."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid
from zelda_miloutte.settings import BROWN, DARK_GRAY

_sign_sprite_cache = None


def get_sign_sprite():
    """Returns a 24x24 wooden sign post sprite (12x12 grid at scale 2)."""
    global _sign_sprite_cache
    if _sign_sprite_cache is None:
        # 12x12 grid at scale 2 = 24x24 pixels
        # Wooden sign: brown board on darker post
        grid = [
            "            ",
            "            ",
            "   BBBBBB   ",
            "  BBBBBBBB  ",
            "  BBBBBBBB  ",
            "  BBBBBBBB  ",
            "   BBBBBB   ",
            "     PP     ",
            "     PP     ",
            "     PP     ",
            "     PP     ",
            "            ",
        ]
        palette = {
            "B": (139, 90, 43),  # Brown (board)
            "P": (80, 60, 40),   # Dark brown (post/stick)
        }
        _sign_sprite_cache = surface_from_grid(grid, palette, scale=2)
    return _sign_sprite_cache
