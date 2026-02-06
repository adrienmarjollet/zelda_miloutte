"""Pixel art sprites for items (hearts and keys)."""

from zelda_miloutte.sprites.pixel_art import surface_from_grid

# ── Heart palette ─────────────────────────────────────────────────
_HEART_PAL = {
    'o': (100, 15, 15),     # dark red outline
    'r': (220, 40, 40),     # red
    'R': (170, 25, 25),     # dark red
    'l': (255, 90, 90),     # light red
    'p': (255, 160, 160),   # pink highlight
    '.': None,
}

# ── Key palette ───────────────────────────────────────────────────
_KEY_PAL = {
    'o': (120, 90, 10),     # dark gold outline
    'y': (255, 210, 60),    # gold
    'Y': (200, 160, 25),    # darker gold
    'l': (255, 240, 140),   # highlight
    'h': (170, 120, 15),    # handle/center dark
    '.': None,
}

# ── Heart frames (16x16, 2 frames for subtle bob) ────────────────
_HEART_0 = [
    "................",
    "..oooo..oooo....",
    ".opplr..rlppo...",
    ".olrrroorrrrro..",
    "orrrrrrrrrrrro..",
    "orrrrrrrrrrrrro.",
    ".orrrrrrrrrrrro.",
    "..orrrrrrrrrrr..",
    "..orrrrrrrrrro..",
    "...orrrrrrrro...",
    "....orrrrrrr....",
    ".....orrrRRo....",
    "......oRRRo.....",
    ".......oRo......",
    "........o.......",
    "................",
]

_HEART_1 = [
    "................",
    "................",
    "..oooo..oooo....",
    ".opplr..rlppo...",
    ".olrrroorrrrro..",
    "orrrrrrrrrrrro..",
    "orrrrrrrrrrrrro.",
    ".orrrrrrrrrrrro.",
    "..orrrrrrrrrrr..",
    "..orrrrrrrrrro..",
    "...orrrrrrrro...",
    "....orrrrrrr....",
    ".....orrrRRo....",
    "......oRRRo.....",
    ".......oRo......",
    "................",
]

# ── Key frames (16x16, 2 frames for subtle bob) ──────────────────
_KEY_0 = [
    "................",
    "....oooooo......",
    "...oyyllyo......",
    "...oylhhly......",
    "...oylhhly......",
    "...oyyllyo......",
    "....oooooo......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYYo......",
    ".....oyYo.......",
    ".....oYYYo......",
    ".....oyYo.......",
    "................",
]

_KEY_1 = [
    "................",
    "................",
    "....oooooo......",
    "...oyyllyo......",
    "...oylhhly......",
    "...oylhhly......",
    "...oyyllyo......",
    "....oooooo......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYo.......",
    ".....oYYYo......",
    ".....oyYo.......",
    ".....oYYYo......",
    "................",
]

# ── Build surfaces ────────────────────────────────────────────────
_heart_cache = None
_key_cache = None


def get_heart_frames():
    """Return [frame0, frame1] for heart item."""
    global _heart_cache
    if _heart_cache is not None:
        return _heart_cache
    _heart_cache = [surface_from_grid(g, _HEART_PAL, 1) for g in (_HEART_0, _HEART_1)]
    return _heart_cache


def get_key_frames():
    """Return [frame0, frame1] for key item."""
    global _key_cache
    if _key_cache is not None:
        return _key_cache
    _key_cache = [surface_from_grid(g, _KEY_PAL, 1) for g in (_KEY_0, _KEY_1)]
    return _key_cache
