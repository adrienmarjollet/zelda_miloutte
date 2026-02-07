"""Pixel art sprites for treasure chests."""

from .pixel_art import surface_from_grid

# Chest palette - wooden box with metallic clasp
_CHEST_PAL = {
    'w': (139, 90, 43),     # dark brown (wood)
    'W': (180, 130, 70),    # light brown (wood highlight)
    'b': (100, 60, 20),     # very dark brown (shadow/outline)
    'g': (255, 215, 0),     # gold (lock/clasp)
    'G': (200, 160, 0),     # dark gold (lock shadow)
    'y': (255, 240, 130),   # light yellow (gold highlight)
    'i': (255, 220, 180),   # light interior (when open)
    'I': (220, 180, 140),   # darker interior
    '.': None,
}

# Closed chest (12x12 grid, scaled 2x = 24x24)
_CHEST_CLOSED = [
    "............",
    "..bbbbbbbb..",
    ".bWWWWWWWWb.",
    ".bwwwwwwwwb.",
    ".bwwggggwwb.",
    ".bwwgGGgwwb.",
    ".bwwgGGgwwb.",
    ".bwwggggwwb.",
    ".bwwwwwwwwb.",
    ".bwwwwwwwwb.",
    ".bbbbbbbbbb.",
    "............",
]

# Open chest (12x12 grid, scaled 2x = 24x24)
_CHEST_OPEN = [
    ".bbbbbbbbb..",
    ".biiiiiiiib.",
    ".bIIIIIIIIb.",
    ".bbbbbbbbbb.",
    "..bWWWWWWWb.",
    "..bwwwwwwwb.",
    "..bwwggggwb.",
    "..bwwgGGgwb.",
    "..bwwgGGgwb.",
    "..bwwggggwb.",
    "..bbbbbbbb..",
    "............",
]

# Cache
_chest_closed_cache = None
_chest_open_cache = None


def get_chest_closed():
    """Return closed chest sprite (24x24)."""
    global _chest_closed_cache
    if _chest_closed_cache is not None:
        return _chest_closed_cache
    _chest_closed_cache = surface_from_grid(_CHEST_CLOSED, _CHEST_PAL, 2)
    return _chest_closed_cache


def get_chest_open():
    """Return open chest sprite (24x24)."""
    global _chest_open_cache
    if _chest_open_cache is not None:
        return _chest_open_cache
    _chest_open_cache = surface_from_grid(_CHEST_OPEN, _CHEST_PAL, 2)
    return _chest_open_cache
